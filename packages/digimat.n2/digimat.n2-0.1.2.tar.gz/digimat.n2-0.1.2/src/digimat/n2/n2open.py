import time
# import logging
# import logging.handlers
import struct

from digimat.n2 import N2BaseDevice, N2Message

# N2Open regions
N2_REGION_ANALOG_INPUT=1
N2_REGION_BINARY_INPUT=2
N2_REGION_ANALOG_OUTPUT=3
N2_REGION_BINARY_OUTPUT=4
N2_REGION_INTERNAL_FLOAT=5
N2_REGION_INTERNAL_INTEGER=6
N2_REGION_INTERNAL_BYTE=7

# N2Open analog input attributes
N2_ATTRIBUTE_AI_OBJECT_CONFIG=1
N2_ATTRIBUTE_AI_OBJECT_STATUS=2
N2_ATTRIBUTE_AI_CURRENTVALUE=3
N2_ATTRIBUTE_AI_LALARM_LIMIT=4
N2_ATTRIBUTE_AI_HALARM_LIMIT=5
N2_ATTRIBUTE_AI_LWARNING_LIMIT=6
N2_ATTRIBUTE_AI_HWARNING_LIMIT=7
N2_ATTRIBUTE_AI_DIFFERENTIAL=8

# N2Open binary input attributes
N2_ATTRIBUTE_BI_OBJECT_CONFIG=1
N2_ATTRIBUTE_BI_OBJECT_STATUS=2

# N2Open analog output attributes
N2_ATTRIBUTE_AO_OBJECT_CONFIG=1
N2_ATTRIBUTE_AO_OBJECT_STATUS=2
N2_ATTRIBUTE_AO_CURRENTVALUE=3

# N2Open binary output attributes
N2_ATTRIBUTE_BO_OBJECT_CONFIG=1
N2_ATTRIBUTE_BO_OBJECT_STATUS=2
N2_ATTRIBUTE_BO_MIN_ONTIME=3
N2_ATTRIBUTE_BO_MIN_OFFTIME=4
N2_ATTRIBUTE_BO_MAX_CYCLESHOUR=5

# N2Open internal float attributes
N2_ATTRIBUTE_IF_OBJECT_STATUS=1
N2_ATTRIBUTE_IF_CURRENTVALUE=2

# N2Open internal integer attributes
# todo: not implemented yet
N2_ATTRIBUTE_ADI_OBJECT_STATUS=1
N2_ATTRIBUTE_ADI_CURRENTVALUE=2

# N2Open internal byte attributes
N2_ATTRIBUTE_IB_OBJECT_STATUS=1
N2_ATTRIBUTE_IB_CURRENTVALUE=2


class N2OpenDevice(N2BaseDevice):
    def __init__(self, n2, address, name=None):
        self._AI={}
        self._AO={}
        self._IF={}
        self._BI={}
        self._BO={}
        self._IB={}
        super(N2OpenDevice, self).__init__(n2, address, name)

    def read(self, region, objectid, attributeid):
        message=N2Message(self.address)
        message.command='1'
        message.write('%01X' % int(region))
        message.write('%02X' % int(objectid))
        message.write('%02X' % int(attributeid))
        return self.sendMessageAndGetResponse(message)

    def readFloat32(self, region, objectid, attributeid):
        r=self.read(region, objectid, attributeid)
        if r:
            r.readByte()  # don't know whats inside yet
            return r.readFloat32()

    def readByte(self, region, objectid, attributeid):
        r=self.read(region, objectid, attributeid)
        if r:
            r.readByte()  # don't know whats inside yet
            return r.readByte()

    def readBit(self, region, objectid, attributeid):
        r=self.read(region, objectid, attributeid)
        if r:
            return r.readBit()

    def write(self, region, objectid, attributeid, sdata):
        if sdata:
            message=N2Message(self.address)
            message.command='2'
            # region is only 1 byte long here ...
            message.write('%01X' % int(region))
            message.write('%02X' % int(objectid))
            if attributeid is not None:
                message.write('%02X' % int(attributeid))
            message.write('%s' % sdata)
            return self.sendMessageAndCheckResult(message)

    def override(self, region, objectid, sdata):
        if sdata:
            message=N2Message(self.address)
            message.command='7'
            message.write('%01X' % 2)  # subcommand
            # ... but 2 bytes here ...
            message.write('%02X' % int(region))
            message.write('%02X' % int(objectid))
            message.write('%s' % sdata)
            return self.sendMessageAndCheckResult(message)

    def releaseOverride(self, region, objectid):
        message=N2Message(self.address)
        message.command='7'
        message.write('%01X' % 3)  # subcommand
        # ... and here.
        message.write('%02X' % int(region))
        message.write('%02X' % int(objectid))
        return self.sendMessageAndCheckResult(message)

    # --------------------

    def AI(self, index, name=None, label=None):
        try:
            item=self._AI[index]
        except:
            item=N2OpenAnalogInput(self, index, name, label)
            self._AI[index]=item
            self._items[item.name]=item
        return item

    def AnalogInput(self, index, name=None, label=None):
        return self.AI(index, name, label)

    # --------------------

    def AO(self, index, name=None, label=None):
        try:
            item=self._AO[index]
        except:
            item=N2OpenAnalogOutput(self, index, name, label)
            self._AO[index]=item
            self._items[item.name]=item
        return item

    def AnalogOutput(self, index, name=None, label=None):
        return self.AO(index, name, label)

    # --------------------

    def IF(self, index, name=None, label=None):
        try:
            item=self._IF[index]
        except:
            item=N2OpenInternalFloat(self, index, name, label)
            self._IF[index]=item
            self._items[item.name]=item
        return item

    def InternalFloat(self, index, name=None, label=None):
        return self.IF(index, name, label)

    # --------------------

    def BI(self, index, name=None, label=None):
        try:
            item=self._IF[index]
        except:
            item=N2OpenBinaryInput(self, index, name, label)
            self._BI[index]=item
            self._items[item.name]=item
        return item

    def BinaryInput(self, index, name=None, label=None):
        return self.BI(index, name, label)

    # --------------------

    def BO(self, index, name=None, label=None):
        try:
            item=self._IF[index]
        except:
            item=N2OpenBinaryOutput(self, index, name, label)
            self._BO[index]=item
            self._items[item.name]=item
        return item

    def BinaryOutput(self, index, name=None, label=None):
        return self.BO(index, name, label)

    # --------------------

    def IB(self, index, name=None, label=None):
        try:
            item=self._IB[index]
        except:
            item=N2OpenInternalByte(self, index, name, label)
            self._IB[index]=item
            self._items[item.name]=item
        return item

    def InternalByte(self, index, name=None, label=None):
        return self.IB(index, name, label)

    # --------------------


class N2OpenItem(object):
    def __init__(self, device, region, index, name, label):
        self._device=device
        self._region=int(region)
        self._index=int(index)
        self._name=name
        self._label=label
        self._value=None
        self._stampValue=0

    @property
    def device(self):
        return self._device

    @property
    def n2(self):
        return self.device.n2

    @property
    def region(self):
        return self._region

    @property
    def index(self):
        return self._index

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def value(self):
        return self._value

    def age(self):
        return time.time()-self._stampValue

    def readCurrentValue(self):
        value=self.onReadCurrentValue()
        if value is not None:
            self._value=value
            self._stampValue=time.time()
        return self.value

    def onReadCurrentValue(self):
        pass

    def encodeFloat32Value(self, value):
        return struct.pack('>f', float(value)).encode('hex')

    def encodeByteValue(self, value):
        return struct.pack('B', float(value)).encode('hex')

    def encodeValue(self, value):
        pass

    def write(self, attributeid, value):
        try:
            data=self.encodeValue(value)
            if data is not None:
                return self.device.write(self.region, self.index, attributeid, data)
        except:
            pass

    def override(self, value):
        try:
            data=self.encodeValue(value)
            if data is not None:
                return self.device.override(self.region, self.index, data)
        except:
            pass

    def releaseOverride(self):
        return self.device.releaseOverride(self.region, self.index)


class N2OpenFloat32Item(N2OpenItem):
    def encodeValue(self, value):
        return self.encodeFloat32Value(value)

    def write(self, value):
        return super(N2OpenFloat32Item, self).write(None, value)


class N2OpenAnalogInput(N2OpenFloat32Item):
    def __init__(self, device, index, name=None, label=None):
        name=name or 'ai%d' % index
        super(N2OpenAnalogInput, self).__init__(device, N2_REGION_ANALOG_INPUT, index, name, label)

    def onReadCurrentValue(self):
        return self.device.readFloat32(self.region, self.index, N2_ATTRIBUTE_AI_CURRENTVALUE)


class N2OpenAnalogOutput(N2OpenFloat32Item):
    def __init__(self, device, index, name=None, label=None):
        name=name or 'ao%d' % index
        super(N2OpenAnalogOutput, self).__init__(device, N2_REGION_ANALOG_OUTPUT, index, name, label)

    def onReadCurrentValue(self):
        return self.device.readFloat32(self.region, self.index, N2_ATTRIBUTE_AO_CURRENTVALUE)


class N2OpenInternalFloat(N2OpenFloat32Item):
    def __init__(self, device, index, name=None, label=None):
        name=name or 'if%d' % index
        super(N2OpenInternalFloat, self).__init__(device, N2_REGION_INTERNAL_FLOAT, index, name, label)

    def onReadCurrentValue(self):
        return self.device.readFloat32(self.region, self.index, N2_ATTRIBUTE_IF_CURRENTVALUE)


class N2OpenBinaryItem(N2OpenItem):
    def encodeValue(self, value):
        if value:
            return '01'
        return '00'

    def write(self, value):
        return super(N2OpenBinaryItem, self).write(None, value)


class N2OpenBinaryInput(N2OpenBinaryItem):
    def __init__(self, device, index, name=None, label=None):
        name=name or 'bi%d' % index
        super(N2OpenBinaryInput, self).__init__(device, N2_REGION_BINARY_INPUT, index, name, label)

    def onReadCurrentValue(self):
        return self.device.readBit(self.region, self.index, N2_ATTRIBUTE_BI_OBJECT_STATUS)


class N2OpenBinaryOutput(N2OpenBinaryItem):
    def __init__(self, device, index, name=None, label=None):
        name=name or 'bo%d' % index
        super(N2OpenBinaryOutput, self).__init__(device, N2_REGION_BINARY_OUTPUT, index, name, label)

    def onReadCurrentValue(self):
        return self.device.readBit(self.region, self.index, N2_ATTRIBUTE_BO_OBJECT_STATUS)


class N2OpenByteItem(N2OpenItem):
    def encodeValue(self, value):
        return self.encodeByteValue(value)

    def write(self, value):
        return super(N2OpenByteItem, self).write(None, value)


class N2OpenInternalByte(N2OpenByteItem):
    def __init__(self, device, index, name=None, label=None):
        name=name or 'ib%d' % index
        super(N2OpenInternalByte, self).__init__(device, N2_REGION_INTERNAL_BYTE, index, name, label)

    def onReadCurrentValue(self):
        return self.device.readByte(self.region, self.index, N2_ATTRIBUTE_IB_CURRENTVALUE)
