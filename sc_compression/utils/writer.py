class Writer:
    def __init__(self, endian: str = 'big'):
        super(Writer, self).__init__()
        self.endian = endian
        self.buffer = b''

    def write(self, data: bytes):
        self.buffer += data

    def writeUInteger(self, integer: int, length: int = 1):
        self.buffer += integer.to_bytes(length, self.endian, signed=False)

    def writeInteger(self, integer: int, length: int = 1):
        self.buffer += integer.to_bytes(length, self.endian, signed=True)

    def writeUInt64(self, integer: int):
        self.writeUInteger(integer, 8)

    def writeInt64(self, integer: int):
        self.writeInteger(integer, 8)

    def writeFloat(self, floating: float):
        exponent = 0
        sign = 1

        if floating < 0:
            sign = -1
            floating = -floating

        if floating >= 2 ** -1022:
            value = floating

            while value < 1:
                exponent -= 1
                value *= 2
            while value >= 2:
                exponent += 1
                value /= 2

        mantissa = floating / 2 ** exponent

        exponent += 127

        as_integer_bin = '0'
        if sign == -1:
            as_integer_bin = '1'

        as_integer_bin += bin(exponent)[2:].zfill(8)

        mantissa_bin = ''
        for x in range(24):
            bit = '0'
            if mantissa >= 1/2**x:
                mantissa -= 1/2**x
                bit = '1'
            mantissa_bin += bit

        mantissa_bin = mantissa_bin[1:]

        as_integer_bin += mantissa_bin
        as_integer = int(as_integer_bin, 2)

        self.writeUInt32(as_integer)

    def writeUInt32(self, integer: int):
        self.writeUInteger(integer, 4)

    def writeInt32(self, integer: int):
        self.writeInteger(integer, 4)

    def writeNUInt16(self, integer: int):
        self.writeUInt16(integer * 65535)

    def writeUInt16(self, integer: int):
        self.writeUInteger(integer, 2)

    def writeNInt16(self, integer: int):
        self.writeInt16(integer * 32512)

    def writeInt16(self, integer: int):
        self.writeInteger(integer, 2)

    def writeUInt8(self, integer: int):
        self.writeUInteger(integer)

    def writeInt8(self, integer: int):
        self.writeInteger(integer)

    def writeBool(self, boolean: bool):
        if boolean:
            self.writeUInt8(1)
        else:
            self.writeUInt8(0)

    writeUInt = writeUInteger
    writeInt = writeInteger

    writeULong = writeUInt64
    writeLong = writeInt64

    writeNUShort = writeNUInt16
    writeNShort = writeNInt16

    writeUShort = writeUInt16
    writeShort = writeInt16

    writeUByte = writeUInt8
    writeByte = writeInt8

    def writeChar(self, string: str):
        for char in list(string):
            self.buffer += char.encode('utf-8')

    def writeString(self, string: str):
        encoded = string.encode('utf-8')
        self.writeUShort(len(encoded))
        self.buffer += encoded
