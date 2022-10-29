import lzma
from hashlib import md5

from sc_compression.signatures import Signatures
from sc_compression.utils.writer import Writer

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


class Compressor(Writer):
    lzham_filters = {
        'dict_size_log2': 18
    }
    lzma_filters = [
        {
            "id": lzma.FILTER_LZMA1,
            "dict_size": 256 * 1024,
            "lc": 3,
            "lp": 0,
            "pb": 2,
            "mode": lzma.MODE_NORMAL
        },
    ]

    def __init__(self):
        super().__init__('little')

    def compress(self, data, signature: Signatures, file_version: int = None) -> bytes:
        uncompressed_size = len(data)

        if file_version is None:
            file_version = 3 if zstandard and signature != Signatures.SCLZ else 1

        if signature == Signatures.ZSTD and not zstandard or \
                signature == Signatures.SCLZ and not lzham:
            signature = Signatures.SC

        super().__init__('little')
        if signature is Signatures.NONE:
            return data
        elif signature in (Signatures.LZMA, Signatures.SIG) or (signature == Signatures.SC and file_version != 3):
            compressed = lzma.compress(data, format=lzma.FORMAT_ALONE, filters=self.lzma_filters)

            self.write(compressed[:5])

            self.writeInt32(uncompressed_size)

            self.write(compressed[13:])

            compressed = self.buffer
        elif signature == Signatures.SCLZ and lzham:
            compressed = lzham.compress(data, filters=self.lzham_filters)

            self.write(b'SCLZ')
            self.writeUByte(self.lzham_filters['dict_size_log2'])
            self.writeInt32(uncompressed_size)
            self.write(compressed)

            compressed = self.buffer
        elif signature in (Signatures.SC, Signatures.ZSTD) and file_version == 3:
            compressor = zstandard.ZstdCompressor()
            compressed = compressor.compress(data)
        else:
            raise TypeError('Unknown Signature!')

        super().__init__('big')
        if signature in (Signatures.SC, Signatures.SCLZ):
            data_hash = md5(data).digest()

            self.write(b'SC')
            self.writeInt32(file_version)
            if file_version == 4:
                self.writeInt32(1)
            self.writeInt32(len(data_hash))
            self.write(data_hash)
            compressed = self.buffer + compressed
        elif signature == Signatures.SIG:
            self.write(b'Sig:')
            self.write(b'\x00' * 64)  # sha64
            compressed = self.buffer + compressed

        return compressed
