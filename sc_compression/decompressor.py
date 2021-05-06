import lzma

from sc_compression.signatures import Signatures
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
        self.signatures = Signatures()
        self.file_version = -1
        self.hash = None

    def decompress(self, buffer: bytes) -> bytes:
        super().__init__(buffer, 'little')

        decompressed = buffer
        signature = self.signatures.get_signature(self.buffer, self.file_version)
        if signature == Signatures.SC:
            super().__init__(buffer, 'big')
            self.read(2)
            self.file_version = self.readInt32()
            self.hash = self.read(self.readInt32())
            decompressed = self.decompress(buffer[26:])
        elif signature == Signatures.SIG:
            buffer = buffer[68:]
            decompressed = self.decompress(buffer)
        elif signature == Signatures.SCLZ:
            self.read(4)
            dict_size_log2 = self.readUByte()
            uncompressed_size = self.readInt32()

            if lzham:
                filters = {
                    'dict_size_log2': dict_size_log2
                }
                decompressed = lzham.decompress(self.buffer[self.tell():], uncompressed_size, filters)
        elif signature == Signatures.LZMA:
            decompressor = lzma.LZMADecompressor()
            compressed = self.buffer[:5] + b'\xff' * 8 + self.buffer[9:]

            decompressed = decompressor.decompress(compressed)
        elif signature == Signatures.ZSTD:
            if zstandard:
                decompressor = zstandard.ZstdDecompressor()
                decompressed = decompressor.decompress(self.buffer)
        else:
            raise TypeError(signature)

        return decompressed
