import lzma
from hashlib import md5

import lzham

from sc_compression.utils.reader import Reader
from sc_compression.utils.writer import Writer


class Decompressor(Reader):
    def __init__(self, buffer: bytes):
        super().__init__(buffer, 'little')

    def get_signature(self):
        if self.buffer[:3] == b'\x5d\x00\x00':
            return 'lzma'
        elif self.buffer.startswith(b'SC'):
            if len(self.buffer) >= 30 and self.buffer[26:30] == b'SCLZ':
                return 'sclz'
            return 'sc'
        elif self.buffer[:4] == 'SIG:':
            return 'sig'
        return None

    def decompress(self) -> bytes:
        signature = self.get_signature()
        if signature is None:
            return self.buffer
        elif signature == 'sc':
            self.buffer = self.buffer[26:]
            signature = 'lzma'
        elif signature == 'sig':
            self.buffer = self.buffer[68:]
            signature = 'lzma'

        if signature == 'lzma':
            decompressor = lzma.LZMADecompressor()

            self.read(5)
            uncompressed_size = self.readInt32()

            lzma_byte = (b'\xff' if uncompressed_size == -1 else b'\x00')
            compressed = self.buffer[:9] + lzma_byte * 4 + self.buffer[9:]

            decompressed = decompressor.decompress(compressed)
        elif signature == 'sclz':
            self.read(30)
            dict_size_log2 = self.readUByte()
            uncompressed_size = self.readInt32()

            filters = {
                'dict_size_log2': dict_size_log2
            }
            decompressed = lzham.decompress(self.buffer[35:], uncompressed_size, filters)
        else:
            raise TypeError(signature)

        return decompressed


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

    def compress(self, data, signature: str) -> bytes:
        uncompressed_size = len(data)

        if signature is None:
            return data
        elif signature in ['lzma', 'sc', 'sig']:
            compressor = lzma.LZMACompressor(format=lzma.FORMAT_ALONE, filters=self.lzma_filters)

            compressed = compressor.compress(data)

            self.write(compressed[:9])  # [:5]

            # self.writeUInt32(uncompressed_size)

            self.write(compressed[13:])

            compressed = self.buffer
        elif signature == 'sclz':
            compressed = lzham.compress(data, filters=self.lzham_filters)

            self.write(b'SCLZ')
            self.writeUByte(18)
            self.writeInt32(uncompressed_size)
            self.write(compressed)

            compressed = self.buffer
        else:
            raise TypeError('Unknown Signature: ' + signature)

        super().__init__('big')
        if signature in ['sc', 'sclz']:
            data_hash = md5(data)

            self.write(b'SC')
            self.writeInt32(1)
            self.writeInt32(16)
            compressed = self.buffer + data_hash.digest() + compressed
        elif signature == 'sig':
            self.write(b'Sig:')
            self.write(b'\x00'*64)  # sha64
            compressed = self.buffer + compressed

        return compressed
