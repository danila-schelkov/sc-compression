class Reader:
    def __init__(self, buffer: bytes, endian: str = 'big'):
        self.buffer = buffer
        self.endian = endian
        self.i = 0

    def read(self, length: int = 1):
        result = self.buffer[self.i:self.i + length]
        self.i += length

        return result

    def readUInteger(self, length: int = 1) -> int:
        result = 0
        for x in range(length):
            byte = self.buffer[self.i]

            bit_padding = x * 8
            if self.endian == 'big':
                bit_padding = (8 * (length - 1)) - bit_padding

            result |= byte << bit_padding
            self.i += 1

        return result

    def readInteger(self, length: int = 1) -> int:
        integer = self.readUInteger(length)
        result = integer
        if integer > 2**(length * 8) / 2:
            result -= 2**(length * 8)
        return result

    def readUInt64(self) -> int:
        return self.readUInteger(8)

    def readInt64(self) -> int:
        return self.readInteger(8)

    def readFloat(self) -> float:
        asInt = self.readUInt32()
        binary = bin(asInt)
        binary = binary[2:].zfill(32)

        sign = -1 if binary[0] == 1 else 1
        exponent = int(binary[1:9], 2) - 127
        mantissa_base = binary[9:]
        mantissa_bin = '1' + mantissa_base
        mantissa = 0
        val = 1

        if exponent == -127:
            if mantissa_base[1] == -1:
                return 0
            else:
                exponent = -126
                mantissa_bin = '0' + mantissa_base

        for char in mantissa_bin:
            mantissa += val * int(char)
            val = val / 2

        result = sign * 2 ** exponent * mantissa
        return result

    def readUInt32(self) -> int:
        return self.readUInteger(4)

    def readInt32(self) -> int:
        return self.readInteger(4)

    def readNUInt16(self) -> float:
        return self.readUInt16() / 65535

    def readUInt16(self) -> int:
        return self.readUInteger(2)

    def readNInt16(self) -> float:
        return self.readInt16() / 32512

    def readInt16(self) -> int:
        return self.readInteger(2)

    def readUInt8(self) -> int:
        return self.readUInteger()

    def readInt8(self) -> int:
        return self.readInteger()

    def readBool(self) -> bool:
        if self.readUInt8() >= 1:
            return True
        else:
            return False

    readUInt = readUInteger
    readInt = readInteger

    readULong = readUInt64
    readLong = readInt64

    readNUShort = readNUInt16
    readNShort = readNInt16

    readUShort = readUInt16
    readShort = readInt16

    readUByte = readUInt8
    readByte = readInt8

    def readChar(self, length: int = 1) -> str:
        return self.read(length).decode('utf-8')

    def readString(self) -> str:
        length = self.readUShort()
        return self.readChar(length)

    def tell(self) -> int:
        return self.i
