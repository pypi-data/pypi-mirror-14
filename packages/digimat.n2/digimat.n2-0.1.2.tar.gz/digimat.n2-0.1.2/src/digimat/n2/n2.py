import time
import logging
import logging.handlers

from threading import Event
import struct

N2_CHAR_SOM='>'
N2_CHAR_EOM='\x0d'


class N2Message(object):
    def __init__(self, address=None, command=None):
        self.reset()
        if address is not None:
            self._address=address
        if command is not None:
            self._command=command

    def reset(self):
        self._valid=True
        self._address=None
        self._command=None
        self._data=bytearray()

    def isValid(self):
        return self._valid

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address=int(address)

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        if isinstance(command, basestring):
            self._command=command[0]
        else:
            self._command=chr(command & 0xFF)

    @property
    def data(self):
        return self._data

    def write(self, data):
        if data:
            for b in data:
                self._data.extend(b)

    def checksum(self, sdata):
        csum=0
        if sdata:
            for b in sdata:
                csum+=ord(b)
        return csum & 0xff

    def decode(self, sdata):
        try:
            self.reset()
            self._valid=False
            if sdata and len(sdata)>=5:
                csum=int(sdata[-2:], 16)
                if self.checksum(sdata[:-2])==csum:
                    self._address=int(sdata[:2], 16)
                    self._command=sdata[2]
                    data=sdata[3:-2]
                    if data:
                        for b in data:
                            self._data.extend(b)
                    self._valid=True
                return True
        except:
            pass

    def encode(self):
        try:
            if self._valid:
                data=[]
                data.append('%02X' % self._address)
                data.append(self._command)
                if self._data:
                    for b in self._data:
                        data.append(chr(b))
                sdata=''.join(data)
                return '%s%s' % (sdata, '%02X' % self.checksum(sdata))
        except:
            pass

    def __str__(self):
        return self.encode()


class N2Response(object):
    def __init__(self, sdata=None):
        self.reset()
        self.decode(sdata)

    def reset(self):
        self._valid=True
        self._ecode=0xff
        self._data=bytearray()
        self._readpos=0

    def isValid(self):
        return self._valid

    def isSuccess(self):
        if self._valid and self._ecode==0xFF:
            return True

    def isNAK(self):
        if not self.isSuccess() and self._ecode<0xff:
            return True

    def errorCode(self):
        return self._ecode

    def checksum(self, sdata):
        csum=0
        if sdata:
            for b in sdata:
                csum+=ord(b)
        return csum & 0xff

    def decode(self, sdata):
        try:
            self.reset()
            self._valid=False
            if sdata:
                size=len(sdata)
                if size==1:
                    if sdata[0]=='A':
                        self._valid=True
                elif size>=2:
                    if sdata[0]=='A':
                        self._ecode=0xFF
                        csum=int(sdata[-2:], 16)
                        if self.checksum(sdata[1:-2])==csum:
                            self._valid=True
                            data=sdata[1:-2]
                            for b in data:
                                self._data.extend(b)
                    elif sdata[0]=='N':
                        self._valid=True
                        self._ecode=int(sdata[-2:], 10)
            return self.isValid()
        except:
            pass

    def readChars(self, size):
        try:
            if size>0 and self._data:
                if self._readpos+size<=len(self._data):
                    data=self._data[self._readpos:self._readpos+size]
                    self._readpos+=size
                    # return corresponding bytearray
                    return data
        except:
            pass

    def readString(self, size):
        try:
            return str(self.readChars(size))
        except:
            pass

    def readHexBytes(self, size):
        try:
            # reminder : 2 chars per byte !
            data=self.readString(size*2)
            # print "HEXBYTES=", data
            return data.decode('hex')
        except:
            pass

    def readHexValue(self, size):
        try:
            # reminder : 2 chars per byte !
            data=self.readString(size*2)
            value=0
            for b in data:
                if b>='0' and b<='9':
                    bvalue=ord(b)-ord('0')
                elif b>='A' and b<='F':
                    bvalue=10+ord(b)-ord('A')
                else:
                    return None
                value<<=4
                value|=bvalue
            return value
        except:
            pass

    def readByte(self):
        return self.readHexValue(1)

    def readSourceAddress(self):
        return self.readByte()

    def readFloat32(self):
        try:
            value=self.readHexBytes(4)
            return struct.unpack('>f', value)[0]
        except:
            pass

    def readBit(self):
        try:
            value=self.readHexValue(1)
            print value
            return bool(value)
        except:
            pass


class CommunicationChannel(object):
    def __init__(self, link, logger):
        self._logger=logger
        link.setLogger(logger)
        self._link=link
        self._dead=False
        self._eventDead=Event()
        self._inbuf=None
        self.reset()

    @property
    def logger(self):
        return self._logger

    @property
    def name(self):
        return self._link.name

    def setDead(self, state=True):
        if state and not self._eventDead.isSet():
            self._eventDead.set()
            self.close()
        self._dead=bool(state)

    def isDeadEvent(self, reset=True):
        e=self._eventDead.isSet()
        if e:
            if reset:
                self._eventDead.clear()
            return True

    def reset(self):
        self.logger.info('reset()')
        self._link.reset()
        self._inbuf=bytearray()

    def open(self):
        return self._link.open()

    def close(self):
        return self._link.close()

    def receive(self):
        data=self._link.read()
        if data:
            self._inbuf.extend(data)
        try:
            eom=self._inbuf.index(N2_CHAR_EOM)
            data=self._inbuf[:eom]
            self.logger.debug('RX[%s<CR>]' % data)
            self._inbuf=self._inbuf[eom+1:]
            r=N2Response()
            # if r.decode(''.join(map(chr, data))):
            if r.decode(str(data)):
                return r
        except:
            pass

    def send(self, message):
        try:
            if message and isinstance(message, N2Message):
                self.reset()
                data=bytearray()
                data.extend(N2_CHAR_SOM)
                for b in message.encode():
                    data.extend(b)
                self.logger.debug('TX[%s<CR>]' % data)
                data.extend(N2_CHAR_EOM)
                return self._link.write(data)
        except:
            self.logger.exception('sendMessage()')

    def sendMessageAndGetResponse(self, message, timeout=3.0):
        if self.send(message):
            t=time.time()+float(timeout)
            while time.time()<t:
                response=self.receive()
                if response:
                    return response
                time.sleep(0.1)


class N2(object):
    def __init__(self, link, logServer='localhost', logLevel=logging.DEBUG):
        logger=logging.getLogger("N2:%s" % link.name)
        logger.setLevel(logLevel)
        socketHandler = logging.handlers.SocketHandler(logServer,
                                            logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(socketHandler)
        self._logger=logger

        self._channel=CommunicationChannel(link, self._logger)
        self._devices={}

    @property
    def logger(self):
        return self._logger

    @property
    def channel(self):
        return self._channel

    def open(self):
        try:
            return self.channel.open()
        except:
            pass

    def close(self):
        try:
            return self.channel.close()
        except:
            pass

    def device(self, address):
        try:
            return self._devices[address]
        except:
            pass

    def devices(self):
        return self._devices.values()

    def __getitem__(self, key):
        return self.device(key)

    def registerDevice(self, device):
        try:
            self._devices[device.name]=device
            return device
        except:
            pass

    def sendMessageAndGetResponse(self, message, timeout=3.0, retry=3):
        while retry>0:
            response=self.channel.sendMessageAndGetResponse(message, timeout)
            if response and response.isSuccess():
                return response
            self.logger.warning('retry')
            retry-=1
        self.logger.error('unable to get response from device!')


class N2BaseDevice(object):
    def __init__(self, n2, address, name=None):
        self._n2=n2
        self._address=int(address)
        self._name=name or 'dev%d' % self._address
        self._items={}
        self._itemsAlias={}
        n2.registerDevice(self)
        self.onInit()

    def open(self):
        try:
            self.n2.channel.open()
        except:
            pass

    def close(self):
        try:
            self.n2.channel.close()
        except:
            pass

    def onInit(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def n2(self):
        return self._n2

    def sendMessageAndGetResponse(self, message):
        response=self.n2.sendMessageAndGetResponse(message)
        if response:
            return response

    def sendMessageAndCheckResult(self, message):
        response=self.sendMessageAndGetResponse(message)
        if response and response.isSuccess():
            return True

    def ping(self):
        return self.onPing()

    # should be overrided !
    def onPing(self):
        pass

    def item(self, name):
        try:
            return self._items[name]
        except:
            pass
        try:
            return self._itemsAlias[name]
        except:
            pass

    def items(self):
        return self._items.values()

    def alias(self, item, alias):
        if alias:
            self._itemsAlias[alias]=item

    def __getitem__(self, key):
        return self.item(key)

    def refresh(self):
        self.onRefresh()

    def onRefresh(self):
        pass


if __name__=='__main__':
    pass
