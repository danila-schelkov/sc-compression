import re
from enum import Enum


class Signatures(Enum):
    NONE = 0
    LZMA = 1
    SC = 2
    SCLZ = 3
    SIG = 4
    ZSTD = 5


def get_signature(buffer: bytes) -> Signatures:
    signature = Signatures.NONE

    if re.match(b"\x00\x00?\x00", buffer[1:5]):
        signature = Signatures.LZMA
    elif buffer.startswith(b"\x28\xb5\x2f\xfd"):
        signature = Signatures.ZSTD

    if buffer.startswith(b"SCLZ"):
        signature = Signatures.SCLZ
    elif buffer.startswith(b"SC"):
        signature = Signatures.SC
    elif buffer.startswith(b"Sig:"):
        signature = Signatures.SIG

    return signature
