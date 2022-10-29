import lzma

from sc_compression.signatures import Signatures, get_signature
from sc_compression.utils.reader import Reader

try:
    import lzham
except ImportError:
    from platform import system as get_system_name

    lzham = None
    if get_system_name() == 'Windows':
        from sc_compression.support.lzham import LZHAM

        lzham = LZHAM

try:
    import zstandard
except ImportError:
    zstandard = None


class Decompressor(Reader):
    def __init__(self):
        super().__init__(b'')

        self.signature = Signatures.NONE
        self.file_version = -1
        self.hash = None

    def decompress(self, buffer: bytes) -> bytes:
        super().__init__(buffer, 'little')

        decompressed = buffer
        self.signature = get_signature(self.buffer, self.file_version)
        if self.signature == Signatures.NONE:
            return decompressed

        if self.signature == Signatures.SC:
            super().__init__(buffer, 'big')
            self.read(2)
            self.file_version = self.readInt32()
            if self.file_version >= 4:
                self.file_version = self.readInt32()
            self.hash = self.read(self.readInt32())
            decompressed = self.decompress(buffer[self.i:])
        elif self.signature == Signatures.SIG:
            buffer = buffer[68:]
            decompressed = self.decompress(buffer)
        elif self.signature == Signatures.SCLZ:
            self.read(4)
            dict_size_log2 = self.readUByte()
            uncompressed_size = self.readInt32()

            if lzham:
                filters = {
                    'dict_size_log2': dict_size_log2
                }
                decompressed = lzham.decompress(self.buffer[self.tell():], uncompressed_size, filters)
        elif self.signature == Signatures.LZMA:
            decompressor = lzma.LZMADecompressor()
            compressed = self.buffer[:5] + b'\xff' * 8 + self.buffer[9:]

            decompressed = decompressor.decompress(compressed)
        elif self.signature == Signatures.ZSTD:
            if zstandard:
                decompressor = zstandard.ZstdDecompressor()
                decompressed = decompressor.decompress(self.buffer)
        else:
            raise TypeError(self.signature)

        return decompressed
