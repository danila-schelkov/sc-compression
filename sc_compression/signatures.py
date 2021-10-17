import re


class Signatures:
    LZMA = 2 ** 0
    SC = 2 ** 1
    SCLZ = 2 ** 2
    SIG = 2 ** 3
    ZSTD = 2 ** 4
    NONE = 2 ** 5

    def __init__(self):
        self.last_signature: int = -1

    def get_signature(self, buffer, file_version: int = -1) -> int:
        signature = Signatures.NONE

        if re.match(b'\x00\x00?\x00', buffer[1:5]):
            signature = Signatures.LZMA
        elif file_version >= 2 and buffer.startswith(b'\x28\xb5\x2f\xfd'):
            signature = Signatures.ZSTD

        if buffer.startswith(b'SCLZ'):
            signature = Signatures.SCLZ
        elif buffer.startswith(b'SC'):
            signature = Signatures.SC
        elif buffer[:4] == b'Sig:':
            signature = Signatures.SIG

        self.last_signature = signature

        return signature
