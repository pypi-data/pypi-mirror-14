# -*- coding: utf-8 -*-
import time

import logging
import logging.handlers

import socket

# from threading import RLock
from threading import Thread
from threading import Event
from threading import Lock

from digimat.lp import PacketManager, LP
from digimat.simpletimer import SimpleTimer

BLOCKSERVERPORT=5000
BLOCKMODELNAMEMAXLEN=10
BLOCKMAXNBINPUTS=16
BLOCKMAXNBOUTPUTS=16

kLP_BS=0xA0
kBS_PING=1
kBS_PONG=2
kBS_SYNC=3
kBS_DECLAREBLOCK=4
kBS_BLOCKINPUTS=5
kBS_BLOCKOUTPUTS=6
kBS_BLOCKDEFAULTOUTPUTS=7


class BlockIO(object):
    def __init__(self, block, index):
        self._block=block
        self._index=index
        self._value=None
        self._minValue=None
        self._maxValue=None
        self._defaultValue=None
        self._unit=None
        self._stamp=0
        self._timerWatchdog=SimpleTimer(60)
        self.resetWatchdog()

    @property
    def block(self):
        return self._block

    @property
    def index(self):
        return self._index

    @property
    def logger(self):
        return self.block.logger

    def updated(self):
        self._stamp=time.time()
        try:
            self.onUpdate()
        except:
            pass

    def resetWatchdog(self):
        self._timerWatchdog.restart()

    @property
    def value(self):
        self.checkWatchdog()
        return self._value

    @value.setter
    def value(self, value):
        if value is not None:
            if self._minValue is not None:
                if value<self._minValue:
                    value=self._minValue
            if self._maxValue is not None:
                if value>self._maxValue:
                    value=self._maxValue

        if value!=self._value:
            self._value=value
            self.updated()
        self.resetWatchdog()
        if self.isInput():
            self.block.resetWatchdog()

    def getValue(self, default=0.0):
        if self.isValid():
            return self._value
        return default

    @property
    def unit(self):
        self.checkWatchdog()
        return self._unit

    @unit.setter
    def unit(self, unit):
        if unit!=self._unit:
            self._unit=unit
            self.updated()
        self.resetWatchdog()

    def set(self, value, unit):
        self.value=value
        self.unit=unit

    def setValueAgain(self):
        # used to force recalc (for example after changing min/max)
        self.value=self.value

    def setNull(self):
        self.set(None, 0xFF)

    def setMaximum(self, value):
        self._maxValue=value
        self.setValueAgain()

    def setMinimum(self, value):
        self._minValue=value
        self.setValueAgain()

    def setMinMax(self, vmin, vmax):
        self.setMinimum(vmin)
        self.setMaximum(vmax)

    def setFromIO(self, io):
        try:
            self.set(io.value, io.unit)
        except:
            pass

    def age(self):
        return time.time()-self._stamp

    def checkWatchdog(self):
        if self._timerWatchdog.isPendingTimeout():
            if self.isInput():
                self.logger.error('%s.input(%d) watchdog !' % (self.block.name, self.index))
            else:
                self.logger.error('%s.output(%d) watchdog !' % (self.block.name, self.index))

            self.onError()
        return True

    def isInput(self):
        return True

    def isOutput(self):
        return not self.isInput()

    def isValid(self):
        if self._value is not None and not self._timerWatchdog.isTimeout():
            return True

    def getDefaultValue(self):
        return self._defaultValue

    def setDefaultValue(self, value):
        if value!=self._defaultValue:
            self._defaultValue=value
            self.onUpdateDefaultValue()

    def resetDefaultValue(self):
        self.setDefaultValue(None)

    def onUpdate(self):
        pass

    def onUpdateDefaultValue(self):
        pass

    def onError(self):
        if self._defaultValue is not None:
            self._value=self._defaultValue


class BlockInput(BlockIO):
    def isInput(self):
        return True

    def onUpdate(self):
        self.block.signalInputUpdate()

    def onError(self):
        self.logger.error('%s.input(%d) error!' % (self.block.name, self.index))
        super(BlockInput, self).onError()

    def next(self):
        return self.block.input(self.index+1)


class BlockOutput(BlockIO):
    def isInput(self):
        return False

    def onUpdate(self):
        self.block.signalOutputUpdate()

    def onUpdateDefaultValue(self):
        self.block.signalDefaultOutputValueUpdate()

    def onError(self):
        self.logger.error('%s.output(%d) error!' % (self.block.name, self.index))
        super(BlockOutput, self).onError()

    def next(self):
        return self.block.output(self.index+1)

    def makeBlockDefaultOutput(self):
        self.block.setIndexOfDefaultOutput(self.index)


class Block(object):
    def __init__(self, blockManager, lid):
        self._blockManager=blockManager
        self._lid=lid
        self._rinstance=0xFFFF
        self._model=self.getModel()
        if len(self._model)>BLOCKMODELNAMEMAXLEN:
            self.logger.error('%s model name too long and may be unreachable!' % self.model)

        self._name='%s:%s%d' % (blockManager.channel.name, self._model, lid)

        self._inputs=[]
        self._eventInputUpdate=Event()

        self._outputs=[]
        self._indexOfDefaultOutput=0
        self._eventOutputUpdate=Event()

        self._eventOutputDefaultValueUpdate=Event()

        self._periodEval=5
        self._timerEval=SimpleTimer()
        self._stampEval=0

        self._timerDispatchOutputs=SimpleTimer(20)
        self._timerInhibitDispatchOutputs=SimpleTimer()
        self._eventInternalError=Event()

        self._timerWatchdog=SimpleTimer(180)

        try:
            self.logger.debug('%s.onInit()' % self.name)
            self.onInit()
        except:
            self.logger.exception('%s.onInit()' % self.name)

    def dispose(self):
        self.logger.debug('%s.onDispose()' % self.name)
        try:
            self.onDispose()
        except:
            self.logger.exception('%s.onDispose()' % self.name)

    @classmethod
    def getModelFromClass(cls):
        # "BlockTest" will return "Test"
        model=cls.__name__[5:]
        if not model:
            return 'rblock'
        return model

    def getModel(self):
        # may be overriden
        return self.getModelFromClass()

    def onInit(self):
        pass

    def onEvaluate(self):
        # return True for immediate reexecution triggering,
        # False for standard reexecution time (periodic+eventTrigger),
        # or fDelay in seconds (i.e. 0.5) for custom reexecution time trigger
        return False

    def onDispose(self):
        pass

    @property
    def blockManager(self):
        return self._blockManager

    @property
    def logger(self):
        return self.blockManager.logger

    @property
    def model(self):
        return self._model

    def isModel(self, model):
        if model and self._model.lower()==model.lower():
            return True

    @property
    def name(self):
        return self._name

    @property
    def lid(self):
        return self._lid

    @property
    def rinstance(self):
        return self._rinstance

    def setDefaultOutputValue(self, index, value):
        try:
            self.input(index).setDefaultValue(value)
        except:
            pass

    def setIndexOfDefaultOutput(self, index):
        if index!= self._indexOfDefaultOutput:
            self.logger.error('%s.output(%d) defined as DEFAULT output' % (self.name, index))
            self._indexOfDefaultOutput=index
            self.signalOutputUpdate()

    def getIndexOfDefaultOutput(self):
        index=self._indexOfDefaultOutput
        if index<self.getNbOutputs():
            return index
        return 0xFF

    def resetWatchdog(self):
        self._timerWatchdog.restart()

    def signalError(self):
        self._eventInternalError.set()

    def isError(self):
        return self._eventInternalError.isSet()

    def getNbInputs(self):
        return len(self._inputs)

    def getNbOutputs(self):
        return len(self._outputs)

    def getNbIo(self):
        return self.getNbInputs()+self.getNbOutputs()

    def hasNoIo(self):
        if self.getNbIo()<=0:
            return True

    def setRemoteInstance(self, rinstance):
        if rinstance != self._rinstance:
            self._rinstance=rinstance
            self.logger.debug('%s.setRemoteInstance(%d)' % (self.name, rinstance))

    def setNbInputs(self, icount, value=None, unit=None):
        if icount>0 and self.getNbInputs()!=icount:
            # reduce if needed
            self._inputs=self._inputs[:icount]
            # expand if needed
            while self.getNbInputs()<icount:
                if not self.addInput(value, unit):
                    break
            self.logger.info('block %s has now %d inputs' % (self.name, icount))

    def setNbOutputs(self, ocount, value=None, unit=None, defaultValue=None):
        if ocount>0 and self.getNbOutputs()!=ocount:
            # reduce if needed
            self._outputs=self._outputs[:ocount]
            # expand if needed
            while self.getNbOutputs()<ocount:
                if not self.addOutput(value, unit, defaultValue):
                    break
            self.logger.info('block %s has now %d outputs' % (self.name, ocount))

    def setEvalPeriod(self, period):
        self.logger.info('%s.setEvalPeriod(%ds)' % (self.name, period))
        self._periodEval=period
        self._timerEval.startWithImmediateTimeout()

    def __del__(self):
        try:
            self.blockManager.removeBlock(self)
        except:
            pass

    def isDead(self):
        return self._timerWatchdog.isTimeout()

    def areInputsValid(self):
        for io in self.inputs():
            if not io.isValid():
                return False
        return True

    def signalInputUpdate(self):
        self._eventInputUpdate.set()

    def signalOutputUpdate(self):
        self._eventOutputUpdate.set()

    def signalDefaultOutputValueUpdate(self):
        self._eventOutputDefaultValueUpdate.set()

    def inputs(self):
        return self._inputs

    def outputs(self):
        return self._outputs

    def input(self, index):
        try:
            return self._inputs[index]
        except:
            # self.logger.error('access to non-existant %s.input(%d)' % (self.name, index))
            pass

    def i(self, index):
        return self.input(index)

    def output(self, index=0):
        try:
            return self._outputs[index]
        except:
            # self.logger.error('access to non-existant %s.output(%d)' % (self.name, index))
            pass

    def o(self, index=0):
        return self.output(index)

    def getInputValue(self, index, defaultValue=None):
        try:
            return self.input(index).value
        except:
            return defaultValue

    def getOutputValue(self, index, defaultValue=None):
        try:
            return self.output(index).value
        except:
            return defaultValue

    def addInput(self, value=None, unit=None):
        if self.getNbInputs()<BLOCKMAXNBINPUTS:
            index=len(self._inputs)
            self.logger.debug('adding %s.input(%d)' % (self.name, index))
            io=BlockInput(self, index)
            io.set(value, unit)
            self._inputs.append(io)
            return io

    def addOutput(self, value=None, unit=None, defaultValue=None):
        if self.getNbOutputs()<BLOCKMAXNBOUTPUTS:
            index=len(self._outputs)
            self.logger.debug('adding %s.output(%d)' % (self.name, index))
            io=BlockOutput(self, index)
            io.set(value, unit)
            io.setDefaultValue(defaultValue)
            self._outputs.append(io)
            return io

    def dispatchOutputs(self):
        if self._timerInhibitDispatchOutputs.isTimeout():
            # self.logger.debug('%s.dispatchOutputs()' % self.name)
            if self.blockManager.packetManager.sendBlockOutputs(self):
                self._timerDispatchOutputs.start(20)
                self._timerInhibitDispatchOutputs.start(0.5)
                return True
            self.logger.warning('%s.dispatchOutputs() error!' % self.name)

    def dispatchDefaultOutputValues(self):
        # self.logger.debug('%s.dispatchDefaultOutputValues()' % self.name)
        if self.blockManager.packetManager.sendBlockDefaultOutputValues(self):
            return True

    def applyDefaultOutputValues(self):
        for io in self.outputs():
            defaultValue=io.getDefaultValue()
            if defaultValue is not None:
                io.value=defaultValue

    def manager(self):
        if self._timerWatchdog.isPendingTimeout():
            self.logger.error('%s watchdog !' % self.name)
            self._dead=True

        if self._eventInputUpdate.isSet() or self._timerEval.isTimeout():
            self._eventInputUpdate.clear()
            # self.logger.debug('%s.onEval()' % self.name)
            try:
                self._eventInternalError.clear()

                # onEvaluate() returns True for immediate rescheduling
                # or fDelay (in seconds) for custom delay

                delay=self.onEvaluate()
                if delay is None or delay is False:
                    self._timerEval.start(self._periodEval)
                elif delay is True:
                    self._timerEval.start(0.1)
                else:
                    try:
                        self._timerEval.start(float(delay))
                    except:
                        self._timerEval.start(self._periodEval)

            except:
                self.logger.exception('%s.onEvaluate()' % self.name)
                self.signalError()

            if self.isError():
                self.applyDefaultOutputValues()
                self._timerEval.start(2.0)

        if self._eventOutputDefaultValueUpdate.isSet():
            if self.dispatchDefaultOutputValues():
                self._eventOutputDefaultValueUpdate.clear()

        if self._eventOutputUpdate.isSet() or self._timerDispatchOutputs.isTimeout():
            if self.dispatchOutputs():
                self._eventOutputUpdate.clear()

    def dump(self):
        print '+-> %s()' % self.name


class BlockManager(object):
    def __init__(self, channel):
        self._channel=channel
        self._blocks={}
        self._lock=Lock()
        self.reset()

    def reset(self):
        with self._lock:
            for block in self.blocks():
                block.dispose()
            self._blocks={}

    def close(self):
        self.logger.debug('BlockManager[%s]::close()' % self.channel.name)
        self.reset()

    @property
    def channel(self):
        return self._channel

    @property
    def packetManager(self):
        return self.channel.packetManager

    @property
    def server(self):
        return self.channel.server

    @property
    def logger(self):
        return self.channel.logger

    def block(self, lid):
        try:
            return self._blocks[lid]
        except:
            pass

    def __get__(self, lid):
        return self.block(lid)

    def blocks(self):
        return self._blocks.values()

    def removeBlock(self, block):
        try:
            lid=block.lid
            self.logger.info('BlockManager[%s]::removing block %s' % (self.channel.name, block.name))
            with self._lock:
                block.dispose()
                del self._blocks[lid]
        except:
            pass

    def instanciateBlock(self, model, lid):
        try:
            block=self.block(lid)
            if block:
                if block.isModel(model):
                    block.resetWatchdog()
                    return block
                self.removeBlock(block)

            block=self.server.blockLibrary.instanciateBlock(self, model, lid)
            if block:
                with self._lock:
                    self._blocks[block.lid]=block
                return block
        except:
            self.logger.exception('BlockManager[%s]::instanciateBlock(%s, %d)' % (self.channel.name, model, lid))

    def manager(self):
        try:
            pendingDeadBlocks=[]

            with self._lock:
                for block in self.blocks():
                    block.manager()
                    if block.isDead():
                        pendingDeadBlocks.append(block)

            while pendingDeadBlocks:
                block=pendingDeadBlocks[0]
                self.removeBlock(block)
                pendingDeadBlocks=pendingDeadBlocks[1:]
        except:
            self.logger.exception('BlockManager[%s]::manager()' % self.channel.name)

    def dump(self):
        for block in self.blocks():
            block.dump()


class BlockServerChannelPacketManager(PacketManager):
    def __init__(self, channel):
        super(BlockServerChannelPacketManager, self).__init__()
        self._channel=channel
        self._timerWatchdog=SimpleTimer(60)
        self.registerHandlers()
        self.sendSync()

    @property
    def channel(self):
        return self._channel

    @property
    def logger(self):
        return self.channel.logger

    def close(self):
        self.dispose()

    def write(self, data):
        return self.channel.write(data)

    def manager(self):
        data=self.channel.read()
        if data:
            self.receive(data)
        if self._timerWatchdog.isTimeout():
            self.logger.error('BlockServerPacketManager[%s]::watchdog!' % self.channel.name)
            self.channel.close()

    def resetWatchdog(self):
        self._timerWatchdog.restart()

    def lp(self, lptype=kLP_BS):
        return LP(lptype, self)

    def registerHandlers(self):
        self.addHandler(kLP_BS, kBS_PONG, self.onReceivePong)
        self.addHandler(kLP_BS, kBS_DECLAREBLOCK, self.onReceiveDeclareBlock)
        self.addHandler(kLP_BS, kBS_BLOCKINPUTS, self.onReceiveBlockInputs)

    def sendPing(self):
        # print "->PING"
        lp=self.lp()
        up=lp.up(kBS_PING)
        up.store()
        lp.send()

    def onReceivePong(self, up):
        pass

    def sendSync(self):
        # print "->SYNC"
        self.logger.info('BlockServerPacketManager[%s]::send SYNC request' % self.channel.name)
        lp=self.lp()
        up=lp.up(kBS_SYNC)
        up.store()
        lp.send()

    def onReceiveDeclareBlock(self, up):
        self.resetWatchdog()
        lid=up.readWord()
        rinstance=up.readWord()
        model=up.readStrField(BLOCKMODELNAMEMAXLEN)
        icount=up.readByte()
        ocount=up.readByte()

        # print self.channel.name, "<-BLOCKDECLARE", model, lid, rinstance, icount, ocount
        block=self.channel.blockManager.instanciateBlock(model, lid)
        if block:
            block.setRemoteInstance(rinstance)
            block.setNbInputs(icount)
            block.setNbOutputs(ocount)
            if block.hasNoIo():
                self.logger.warning('%s has no io!' % block.name)

            # force refresh
            block.signalDefaultOutputValueUpdate()
            block.signalOutputUpdate()
        else:
            self.logger.error('BlockServerPacketManager[%s]::unable to declare block %s/%d' % (self.channel.name, model, lid))

    def onReceiveBlockInputs(self, up):
        self.resetWatchdog()
        lid=up.readWord()
        rinstance=up.readWord()
        block=self.channel.blockManager.block(lid)
        if block:
            print "%s<-BLOCKINPUTS" % block.name
            if block.rinstance==rinstance:
                io=block.input(0)
                while io and up.readable(6):
                    value=up.readFloat()
                    unit=up.readByte()
                    connected=up.readBool()
                    if connected:
                        io.set(value, unit)
                    else:
                        io.setNull()
                    io=io.next()
            else:
                self.logger.error('BlockServerPacketManager[%s]::block %s rinstance incoherence!' % (self.channel.name, block.name))
                self.channel.close()

    def sendBlockOutputs(self, block):
        print "%s->BLOCKOUTPUTS" % block.name
        lp=self.channel.packetManager.lp()
        up=lp.up(kBS_BLOCKOUTPUTS)
        up.writeWord(block.lid)
        up.writeWord(block.rinstance)
        up.writeBool(block.isError())
        up.writeByte(block.getIndexOfDefaultOutput())
        for io in block.outputs():
            data=io.value
            if data is None:
                data=0.0
            up.writeFloat(data)
            data=io.unit
            if data is None:
                data=0xFF
            up.writeByte(data)
        up.store()
        if lp.send():
            return True

    def sendBlockDefaultOutputValues(self, block):
        print "%s->BLOCKDEFAULTOUTPUTS" % block.name
        lp=self.channel.packetManager.lp()
        up=lp.up(kBS_BLOCKDEFAULTOUTPUTS)
        up.writeWord(block.lid)
        up.writeWord(block.rinstance)
        for io in block.outputs():
            defaultValue=io.getDefaultValue()
            if defaultValue is None:
                up.writeBool(False)
                up.writeFloat(0.0)
            else:
                up.writeBool(True)
                up.writeFloat(float(defaultValue))
        up.store()
        if lp.send():
            return True


class BlockSocketChannel(object):
    def __init__(self, socketServer, socket, name):
        self._socketServer=socketServer
        self._socket=socket
        self._name=name
        self._packetManager=BlockServerChannelPacketManager(self)
        self._blockManager=BlockManager(self)
        print "***************** connect", self.name

    @property
    def socketServer(self):
        return self._socketServer

    @property
    def logger(self):
        return self.socketServer.logger

    @property
    def server(self):
        return self.socketServer.server

    @property
    def name(self):
        return self._name

    @property
    def packetManager(self):
        return self._packetManager

    @property
    def blockManager(self):
        return self._blockManager

    def close(self):
        self.logger.info('BlockSocketChannel[%s]::close()' % self.name)
        self._blockManager.close()
        self._packetManager.close()
        try:
            self._socket.close()
        except:
            pass
        self._socket=None

    def isDead(self):
        if not self._socket:
            return True

    def write(self, data):
        try:
            self._socket.send(data)
            return True
        except:
            self.logger.error("BlockSocketChannel[%s]::write error!" % self.name)
            self.close()

    def read(self):
        try:
            data = self._socket.recv(4096)
            if not data:
                self.logger.error("BlockServerChannel[%s]::read error!" % self.name)
                self.close()
            return data
        except:
            pass

    def manager(self):
        self.packetManager.manager()
        self.blockManager.manager()


class BlockSocketServer(object):
    def __init__(self, server, port):
        self._port=port
        self._server=server
        self._socket=None
        self._channels={}

    @property
    def server(self):
        return self._server

    @property
    def logger(self):
        return self.server.logger

    def accept(self):
        try:
            socketClient, addr = self._socket.accept()
            if socketClient:
                name=addr[0]
                self.logger.info('BlockSocketServer::create new channel [%s]' % name)
                channel=BlockSocketChannel(self, socketClient, name)
                self._channels[channel]=channel.name
        except:
            pass

    def manager(self):
        try:
            if not self._socket:
                self._socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self._socket.setblocking(0)

                self._socket.bind(('0.0.0.0', self._port))
                self._socket.listen(5)
                self.logger.info("BlockSocketServer::online, now listening on port %d." % self._port)

            # serve new incoming connections
            self.accept()

            for channel in self._channels:
                channel.manager()
                if channel.isDead():
                    self.logger.info('BlockSocketServer::releasing channel %s' % channel.name)
                    channel.close()
                    del self._channels[channel]
                    break

        except:
            self.logger.exception("BlockSocketServer::manager()")
            self.close()

    def close(self):
        try:
            self._socket.close()
        except:
            pass
        self._socket=None

        self.logger.info('BlockSocketServer::close()')
        for channel in self._channels:
            channel.close()
        self._channels={}

        self.logger.info("BlockSocketServer::offline!")


class BlockLibrary(object):
    def __init__(self, server):
        self._server=server
        self._models={}
        self._lock=Lock()

    @property
    def server(self):
        return self._server

    @property
    def logger(self):
        return self.server.logger

    def register(self, bclass):
        try:
            if bclass and issubclass(bclass, Block):
                with self._lock:
                    model=bclass.getModelFromClass().lower()
                    self._models[model]=bclass
                    self.logger.debug('block<%s> registered' % model)
                    return True
        except:
            self.logger.exception('register()')

    def instanciateBlock(self, blockManager, model, lid):
        try:
            bclass=self._models[model.lower()]
            block=bclass(blockManager, lid)
            return block
        except:
            pass


class BlockServer(object):
    def __init__(self, logServer='localhost', logLevel=logging.DEBUG):
        logger=logging.getLogger("BLOCKSERVER")
        logger.setLevel(logLevel)
        socketHandler = logging.handlers.SocketHandler(logServer, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(socketHandler)
        self._logger=logger

        self._eventStop=Event()
        self._thread=Thread(target=self._manager)
        self._thread.daemon=True

        self._eventWakeup=Event()
        self._blockLibrary=BlockLibrary(self)

        self._socketServer=BlockSocketServer(self, BLOCKSERVERPORT)
        self.registerAllBlocks()

    def dispose(self):
        pass

    def __del__(self):
        self.stop()
        self.disconnect()

    @property
    def logger(self):
        return self._logger

    @property
    def blockLibrary(self):
        return self._blockLibrary

    @property
    def socketServer(self):
        return self._socketServer

    def wakeup(self):
        self._eventWakeup.set()

    def sleep(self, timeout):
        if self._eventWakeup.wait(float(timeout)):
            self._eventWakeup.clear()
            return True

    def waitForExit(self):
        self.stop()
        self.logger.debug("wait for thread termination")
        self._thread.join()
        self.logger.info("done")

    def start(self):
        self.logger.debug("starting manager thread")
        self._thread.start()

    def _manager(self):
        self.logger.info("manager thread started")
        while not self._eventStop.isSet():
            try:
                self.socketServer.manager()
            # except SystemExit as e:
            except SystemExit:
                # todo: probably never coming in subprocess, only in main thread
                self.logger.warning("manager thread halted by sys.exit() exception")
                self.stop()
            except:
                self.logger.exception("manager thread exception occured within manager()")
            self.sleep(0.1)

        self.logger.info("manager stopped")
        if not self._eventStop.isSet():
            self.logger.error("unsollicited manager stop!")
            self.stop()

    def stop(self):
        self.wakeup()
        if not self._eventStop.isSet():
            self._eventStop.set()
            self.logger.debug("stop request!")
            self.socketServer.close()

    def isRunning(self):
        return not self._eventStop.isSet()

    def register(self, bclass):
        return self.blockLibrary.register(bclass)

    def registerAllBlocks(self):
        def get_all_subclasses(cls):
            """ Generator of all a class's subclasses. """
            try:
                for subclass in cls.__subclasses__():
                    yield subclass
                    for subclass in get_all_subclasses(subclass):
                        yield subclass
            except TypeError:
                return

        def all_subclasses3(classname):
            for cls in get_all_subclasses(object):
                if cls.__name__.split('.')[-1] == classname:
                    break
            else:
                raise ValueError('class %s not found' % classname)
            direct_subclasses = cls.__subclasses__()
            return direct_subclasses + [g for s in direct_subclasses
                for g in all_subclasses3(s.__name__)]

        try:
            self.logger.info('registering all found Block() subclasses')
            subcls=all_subclasses3('Block')
            for cls in subcls:
                self.register(cls)
        except:
            pass

    def serveForEver(self):
        self.start()
        try:
            while self.isRunning():
                self.sleep(2.0)
        except:
            self.stop()
        self.waitForExit()
        self.dispose()


if __name__ == "__main__":
    pass
