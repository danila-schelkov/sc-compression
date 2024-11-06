import struct
from typing import Literal


ENDIAN_SIGN = {"big": ">", "little": "<"}


class Reader:
    def __init__(self, buffer: bytes, endian: Literal["little", "big"] = "big"):
        self.buffer = buffer
        self.endian: Literal["little", "big"] = endian
        self._position = 0

    def read(self, length: int = 1):
        result = self.buffer[self._position : self._position + length]
        self._position += length

        return result

    def read_u_integer(self, length: int = 1) -> int:
        return int.from_bytes(self.read(length), self.endian, signed=False)

    def read_integer(self, length: int = 1) -> int:
        return int.from_bytes(self.read(length), self.endian, signed=True)

    def read_u_int64(self) -> int:
        return self.read_u_integer(8)

    def read_int64(self) -> int:
        return self.read_integer(8)

    def read_float(self) -> float:
        (floating,) = struct.unpack(ENDIAN_SIGN[self.endian] + "f", self.read(4))
        return floating

    def read_u_int32(self) -> int:
        return self.read_u_integer(4)

    def read_int32(self) -> int:
        return self.read_integer(4)

    def read_nu_int16(self) -> float:
        return self.read_u_int16() / 65535

    def read_u_int16(self) -> int:
        return self.read_u_integer(2)

    def read_n_int16(self) -> float:
        return self.read_int16() / 32512

    def read_int16(self) -> int:
        return self.read_integer(2)

    def read_u_int8(self) -> int:
        return self.read_u_integer()

    def read_int8(self) -> int:
        return self.read_integer()

    def read_bool(self) -> bool:
        if self.read_u_int8() >= 1:
            return True
        else:
            return False

    readUInt = read_u_integer
    readInt = read_integer

    readULong = read_u_int64
    readLong = read_int64

    readNUShort = read_nu_int16
    readNShort = read_n_int16

    readUShort = read_u_int16
    readShort = read_int16

    readUByte = read_u_int8
    readByte = read_int8

    def read_char(self, length: int = 1) -> str:
        return self.read(length).decode("utf-8")

    def read_string(self) -> str:
        length = self.readUShort()
        return self.read_char(length)

    def tell(self) -> int:
        return self._position
