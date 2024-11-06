import struct
from typing import Literal


ENDIAN_SIGN = {"big": ">", "little": "<"}


class Writer:
    def __init__(self, endian: Literal["little", "big"] = "big"):
        super(Writer, self).__init__()

        self.endian: Literal["little", "big"] = endian
        self.buffer = b""

    def write(self, data: bytes):
        self.buffer += data

    def write_u_integer(self, integer: int, length: int = 1):
        self.buffer += integer.to_bytes(length, self.endian, signed=False)

    def write_integer(self, integer: int, length: int = 1):
        self.buffer += integer.to_bytes(length, self.endian, signed=True)

    def write_u_int64(self, integer: int) -> None:
        self.write_u_integer(integer, 8)

    def write_int64(self, integer: int) -> None:
        self.write_integer(integer, 8)

    def write_float(self, floating: float) -> None:
        self.write(struct.pack(ENDIAN_SIGN[self.endian] + "f", floating))

    def write_u_int32(self, integer: int) -> None:
        self.write_u_integer(integer, 4)

    def write_int32(self, integer: int) -> None:
        self.write_integer(integer, 4)

    def write_nu_int16(self, integer: int) -> None:
        self.write_u_int16(integer * 65535)

    def write_u_int16(self, integer: int) -> None:
        self.write_u_integer(integer, 2)

    def write_n_int16(self, integer: int) -> None:
        self.write_int16(integer * 32512)

    def write_int16(self, integer: int) -> None:
        self.write_integer(integer, 2)

    def write_u_int8(self, integer: int) -> None:
        self.write_u_integer(integer)

    def write_int8(self, integer: int) -> None:
        self.write_integer(integer)

    def write_bool(self, boolean: bool) -> None:
        if boolean:
            self.write_u_int8(1)
        else:
            self.write_u_int8(0)

    def write_char(self, string: str) -> None:
        self.buffer += string.encode("utf-8")

    def write_string(self, string: str) -> None:
        encoded = string.encode("utf-8")
        self.write_u_int16(len(encoded))
        self.buffer += encoded
