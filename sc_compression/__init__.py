__all__ = [
    'decompressor',
    'compressor',
    'signatures',
    'decompress',
    'compress'
]

from sc_compression.compressor import Compressor
from sc_compression.decompressor import Decompressor


def compress(buffer: bytes, signature: int, file_version: int = None) -> bytes:
    return Compressor().compress(buffer, signature, file_version)


def decompress(buffer: bytes) -> (bytes, int):
    decompressor = Decompressor()
    decompressed = decompressor.decompress(buffer)

    return decompressed, decompressor.signatures.last_signature
