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
        if value!=self._value:
            self._value=value
            self.updated()
        self.resetWatchdog()
        if self.isInput():
            self.block.resetWatchdog()

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

    def setNull(self):
        self.set(None, 0xFF)

    def setFromIO(self, io):
        try:
            self.set(io.value, io.unit)
        except:
            pass

    def age(self):
        return time.time()-self._stamp

    def checkWatchdog(self):
        if self._timerWatchdog.isPendingTimeout():
            self.logger.error('%s.io(%d) watchdog !' (self.block.name, self.index))
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
        if self._applyDefault:
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
    def __init__(self, blockmanager, lid):
        self._blockmanager=blockmanager
        self._lid=lid
        self._rinstance=0xFFFF
        self._model=self.getModel()
        if len(self._model)>BLOCKMODELNAMEMAXLEN:
            self.logger.error('%s model name too long and may be unreachable!' % self.model)
        self._name='%s%d' % (self._model, lid)

        self._inputs=[]
        self._eventInputUpdate=Event()

        self._outputs=[]
        self._indexOfDefaultOutput=0
        self._eventOutputUpdate=Event()

        self._eventOutputDefaultValueUpdate=Event()

        self._periodEval=5
        self._timerEval=SimpleTimer()
        self._stampEval=0

        self._timerDispatchOutputs=SimpleTimer()
        self._timerInhibitDispatchOutputs=SimpleTimer()
        self._eventInternalError=Event()

        self._timerWatchdog=SimpleTimer(180)

        try:
            self.logger.debug('%s.onInit()' % self.name)
            self.onInit()
        except:
            self.logger.exception('%s.onInit()' % self.name)

    @classmethod
    def getModelFromClass(cls):
        # "BlockTest" will return "Test"
        # model=cls.__class__.__name__[5:]
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
        # return True for immediate reexecution triggering
        return False

    def onDispose(self):
        pass

    @property
    def blockmanager(self):
        return self._blockmanager

    @property
    def logger(self):
        return self.blockmanager.logger

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
            self.blockmanager.removeBlock(self)
        except:
            pass

    def dispose(self):
        self.logger.debug('%s.onDispose()' % self.name)
        try:
            self.onDispose()
        except:
            self.logger.exception('%s.onDispose()' % self.name)

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
            self.logger.debug('%s.dispatchOutputs()' % self.name)
            if self.blockmanager.server.sendBlockOutputs(self):
                self._timerDispatchOutputs.start(60)
                self._timerInhibitDispatchOutputs.start(0.5)
                return True
            self._timerInhibitDispatchOutputs.start(3.0)

    def dispatchDefaultOutputValues(self):
        self.logger.debug('%s.dispatchDefaultOutputValues()' % self.name)
        if self.blockmanager.server.sendBlockDefaultOutputValues(self):
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
            self.logger.debug('%s.onEval()' % self.name)
            try:
                self._eventInternalError.clear()
                if not self.onEvaluate():
                    self._timerEval.start(self._periodEval)
                else:
                    # onEvaluate() returns True for immediate rescheduling
                    self._timerEval.startWithImmediateTimeout()
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


class BlockServerManager(object):
    def __init__(self, server):
        self._server=server
        self._models={}
        self._blocks={}
        self._lock=Lock()
        self.reset()

    def reset(self):
        self.logger.info('reset()')
        with self._lock:
            for block in self.blocks():
                block.dispose()
            self._blocks={}

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
            self.logger.info('removing block %s' % block.name)
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

            try:
                bclass=self._models[model.lower()]
                block=bclass(self, lid)
                with self._lock:
                    self._blocks[block.lid]=block
                    self.logger.info('new block instance %s created' % block.name)
                    return block
            except:
                # self.logger.exception('debug')
                pass

        except:
            self.logger.exception('instanciateBlock(%s, %d)' % (model, lid))

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
            self.logger.exception('manager()')

    def dump(self):
        # TODO
        print "DUMP<%s>" % self.name


class BlockServerChannel(object):
    def __init__(self, port, logger):
        self._port=port
        self._socketServer=None
        self._socketClient=None
        self._conn=None
        self._connected=False
        self._logger=logger
        self._timerInhibit=SimpleTimer(3)
        self._eventConnect=Event()

    @property
    def logger(self):
        return self._logger

    def accept(self):
        try:
            socketClient, addr = self._socketServer.accept()
            return socketClient
        except:
            pass

    def acceptAndClose(self):
        socketClient=self.accept()
        if socketClient:
            try:
                self.logger.warning('refusing new incoming connection!')
                socketClient.close()
            except:
                pass

    def connect(self):
        try:
            if not self._connected:
                if self._timerInhibit.isTimeout():
                    if not self._socketServer:
                        self._socketServer=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self._socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        self._socketServer.setblocking(0)

                        self._socketServer.bind(('0.0.0.0', self._port))
                        self._socketServer.listen(0)
                        self.logger.info("BlockServerChannel::online, now listening on port %d." % self._port)

                self._socketClient=self.accept()
                if self._socketClient:
                    self._connected=True
                    self.logger.info("BlockServerChannel::connected!")
                    self._eventConnect.set()

        except:
            self.logger.exception("BlockServerChannel.connect()")
            try:
                self._socketServer.close()
            except:
                pass

            self._timerInhibit.start()
            self._socketServer=None
            self._socketClient=None

        # clear any pending connection while already connected
        if self._connected:
            self.acceptAndClose()

        return self._connected

    def isConnected(self):
        return self._connected

    def isConnectPendingEvent(self):
        if self.isConnected():
            pending=self._eventConnect.isSet()
            if pending:
                self._eventConnect.clear()
                return True

    def disconnect(self):
        try:
            self._socketClient.close()
        except:
            pass
        try:
            self._socketServer.close()
        except:
            pass

        self._socketServer=None
        self._socketClient=None

        self.logger.info("BlockServerChannel::offline!")
        self._connected=False

    def write(self, data):
        try:
            self.connect()
            self._socketClient.send(data)
            return True
        except:
            self.logger.error("BlockServerChannel::write error!")
            self.disconnect()

    def read(self):
        try:
            self.connect()
            data = self._socketClient.recv(4096)
            if not data:
                self.logger.error("BlockServerChannel::read error!")
                self.disconnect()
            return data
        except:
            pass

    def dump(self):
        for block in self.blocks():
            block.dump()


class BlockServerChannelPacketManager(PacketManager):
    def __init__(self, channel, logger):
        super(BlockServerChannelPacketManager, self).__init__()
        self._logger=logger
        self._channel=channel

    @property
    def channel(self):
        return self._channel

    @property
    def logger(self):
        return self._logger

    def dispose(self):
        self.disconnect()
        super(BlockServerChannelPacketManager, self).dispose()

    def write(self, data):
        return self.channel.write(data)

    def manager(self):
        data=self.channel.read()
        if data:
            self.receive(data)

    def lp(self, lptype=kLP_BS):
        return LP(lptype, self)


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
        self._channel=BlockServerChannel(BLOCKSERVERPORT, self._logger)

        self._packetManager=BlockServerChannelPacketManager(self._channel, self._logger)
        self._blockManager=BlockServerManager(self)

        self.registerHandlers()
        self.registerAllBlocks()

        # todo: not functional but not yet found the good way to do it!
        # def _autostop():
        #     print("AUTOSTOP!")
        #     self.stop()
        #     atexit.unregister(_autostop)
        # atexit.register(_autostop)

        # no implicit startup, as for EBus
        # self.start()

    # def __enter__(self):
    #   pass

    # def __exit__(self):
    #   self.stop()

    def __del__(self):
        self.stop()
        self.disconnect()

    @property
    def logger(self):
        return self._logger

    @property
    def packetManager(self):
        return self._packetManager

    @property
    def blockManager(self):
        return self._blockManager

    @property
    def channel(self):
        return self._channel

    def wakeup(self):
        self._eventWakeup.set()

    def sleep(self, timeout):
        if self._eventWakeup.wait(float(timeout)):
            self._eventWakeup.clear()
            return True

    def addPacketHandler(self, lptype, uptype, handler):
        return self.addHandler(lptype, uptype, handler)

    def registerHandlers(self):
        self.packetManager.addHandler(kLP_BS, kBS_PONG, self.onReceivePong)
        self.packetManager.addHandler(kLP_BS, kBS_DECLAREBLOCK, self.onReceiveDeclareBlock)
        self.packetManager.addHandler(kLP_BS, kBS_BLOCKINPUTS, self.onReceiveBlockInputs)

    def sendPing(self):
        lp=self.packetManager.lp()
        up=lp.up(kBS_PING)
        up.store()
        lp.send()

    def onReceivePong(self, up):
        pass

    def sendSync(self):
        self.logger.info('send SYNC request')
        lp=self.packetManager.lp()
        up=lp.up(kBS_SYNC)
        up.store()
        lp.send()

    def onReceiveDeclareBlock(self, up):
        lid=up.readWord()
        rinstance=up.readWord()
        model=up.readStrField(BLOCKMODELNAMEMAXLEN)
        icount=up.readByte()
        ocount=up.readByte()

        print "<-BLOCKDECLARE", model, rinstance, icount, ocount
        block=self.blockManager.instanciateBlock(model, lid)
        if block:
            block.setRemoteInstance(rinstance)
            block.setNbInputs(icount)
            block.setNbOutputs(ocount)

            # force refresh
            block.signalDefaultOutputValueUpdate()
            block.signalOutputUpdate()
        else:
            self.logger.error('unable to declare block %s/%d' % (model, lid))

    def onReceiveBlockInputs(self, up):
        print "<-BLOCKINPUTS"
        lid=up.readWord()
        rinstance=up.readWord()
        block=self.blockManager.block(lid)
        if block:
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
                self.logger.error('block %s rinstance incoherence!' % block.name)
                self.disconnect()

    def sendBlockOutputs(self, block):
        print "->BLOCKOUTPUTS"
        lp=self.packetManager.lp()
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
        print "->BLOCKDEFAULTOUTPUTS"
        lp=self.packetManager.lp()
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

    def connect(self):
        if not self.channel.isConnected():
            self.channel.connect()
            self.ping()

    def disconnect(self):
        self.channel.disconnect()

    def inputs(self):
        return self.blockManager.inputs()

    def outputs(self):
        return self.blockManager.outputs()

    def dump(self):
        self.blockManager.dump()

    def waitForExit(self):
        self.stop()
        self.logger.debug("wait for thread termination")
        self._thread.join()
        self.logger.info("done")
        self.disconnect()

    def start(self):
        self.logger.debug("starting manager thread")
        self._thread.start()

    def _manager(self):
        self.logger.info("manager thread started")
        while not self._eventStop.isSet():
            try:
                if self.channel.isConnectPendingEvent():
                    self.sendSync()
                self.blockManager.manager()
                self.packetManager.manager()
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
        self._eventWakeup.set()
        if not self._eventStop.isSet():
            self._eventStop.set()
            self.logger.debug("stop request!")

    def isRunning(self):
        return not self._eventStop.isSet()

    def register(self, bclass):
        return self.blockManager.register(bclass)

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


if __name__ == "__main__":
    pass
