import time
import logging
import logging.handlers

import binascii
import struct

from digimat.n2 import N2BaseDevice, N2Message

# 9x commands
N29x_CMD_READ_ITEM=0x0
N29x_CMD_WRITE_ITEM=0x80


class N29xDevice(N2BaseDevice):
    def __init__(self, n2, address, name=None):
        super(N29xDevice, self).__init__(n2, address, name)

    # http://davidejones.com/blog/1413-python-precision-floating-point/
    def f32tof16(self, float32):
        F16_EXPONENT_BITS = 0x1F
        F16_EXPONENT_SHIFT = 10
        F16_EXPONENT_BIAS = 15
        F16_MANTISSA_BITS = 0x3ff
        F16_MANTISSA_SHIFT = (23 - F16_EXPONENT_SHIFT)
        F16_MAX_EXPONENT = (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

        a = struct.pack('>f', float32)
        b = binascii.hexlify(a)

        f32 = int(b, 16)
        f16 = 0
        sign = (f32 >> 16) & 0x8000
        exponent = ((f32 >> 23) & 0xff) - 127
        mantissa = f32 & 0x007fffff

        if exponent == 128:
            f16 = sign | F16_MAX_EXPONENT
            if mantissa:
                f16 |= (mantissa & F16_MANTISSA_BITS)
        elif exponent > 15:
            f16 = sign | F16_MAX_EXPONENT
        elif exponent > -15:
            exponent += F16_EXPONENT_BIAS
            mantissa >>= F16_MANTISSA_SHIFT
            f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
        else:
            f16 = sign
        return f16

    def f16tof32(self, float16):
        s = int((float16 >> 15) & 0x00000001)    # sign
        e = int((float16 >> 10) & 0x0000001f)    # exponent
        f = int(float16 & 0x000003ff)            # fraction

        if e == 0:
            if f == 0:
                return int(s << 31)
            else:
                while not (f & 0x00000400):
                    f = f << 1
                    e -= 1
                e += 1
                f &= ~0x00000400
                # print(s,e,f)
        elif e == 31:
            if f == 0:
                return int((s << 31) | 0x7f800000)
            else:
                return int((s << 31) | 0x7f800000 | (f << 13))

        e = e + (127 -15)
        f = f << 13
        return int((s << 31) | (e << 23) | f)

        # -----------------------------------------------------------------
        # h = struct.unpack(">H",file.read(struct.calcsize(">H")))[0]
        # fcomp = Float16Compressor()
        # temp = fcomp.decompress(h)
        # str = struct.pack('I',temp)
        # f = struct.unpack('f',str)[0]
        # print(f)

        # #write half float to file from float
        # fcomp = Float16Compressor()
        # f16 = fcomp.compress(float32)
        # file.write(struct.pack(">H",f16))
        # -----------------------------------------------------------------

    def bcc(self, sdata):
        s1=0
        s2=0
        for b in sdata:
            s1+=ord(b)

            if s1>0xff:
                s1-=0xff

            s2+=s1
            if s2>0xff:
                s2-=0xff

            bcc=s1+s2
            if bcc>0xff:
                bcc-=0xff

        bcc=(~bcc) & 0xff | s2 << 8
        return bcc

    def read(self, itemid, page=0):
        message=N2Message(self.address)
        message.command=N29x_CMD_READ_ITEM
        message.write('%01X' % int(region))
        message.write('%02X' % int(objectid))
        message.write('%02X' % int(attributeid))
        return self.sendMessageAndGetResponse(message)

    #def readFloat32(self, region, objectid, attributeid):
    #     r=self.read(region, objectid, attributeid)
    #     if r:
    #         r.readByte() # don't know whats inside yet
    #         return r.readFloat32()

    # def readByte(self, region, objectid, attributeid):
    #     r=self.read(region, objectid, attributeid)
    #     if r:
    #         r.readByte() # don't know whats inside yet
    #         return r.readByte()

    # def readBit(self, region, objectid, attributeid):
    #     r=self.read(region, objectid, attributeid)
    #     if r:
    #         return r.readBit()

    # def write(self, region, objectid, attributeid, sdata):
    #     if sdata:
    #         message=N2Message(self.address)
    #         message.command='2'
    #         # region is only 1 byte long here ...
    #         message.write('%01X' % int(region))
    #         message.write('%02X' % int(objectid))
    #         if attributeid is not None:
    #             message.write('%02X' % int(attributeid))
    #         message.write('%s' % sdata)
    #         return self.sendMessageAndCheckResult(message)

    # def override(self, region, objectid, sdata):
    #     if sdata:
    #         message=N2Message(self.address)
    #         message.command='7'
    #         message.write('%01X' % 2) # subcommand
    #         # ... but 2 bytes here ...
    #         message.write('%02X' % int(region))
    #         message.write('%02X' % int(objectid))
    #         message.write('%s' % sdata)
    #         return self.sendMessageAndCheckResult(message)

    # def releaseOverride(self, region, objectid):
    #     message=N2Message(self.address)
    #     message.command='7'
    #     message.write('%01X' % 3) # subcommand
    #     # ... and here.
    #     message.write('%02X' % int(region))
    #     message.write('%02X' % int(objectid))
    #     return self.sendMessageAndCheckResult(message)


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
