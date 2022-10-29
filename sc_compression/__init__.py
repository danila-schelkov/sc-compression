from .compressor import Compressor
from .decompressor import Decompressor
from .signatures import Signatures


__all__ = [
    'Decompressor',
    'Compressor',
    'Signatures',

    'decompress',
    'compress'
]


def compress(buffer: bytes, signature: Signatures, file_version: int = None) -> bytes:
    return Compressor().compress(buffer, signature, file_version)


def decompress(buffer: bytes) -> (bytes, int):
    _decompressor = Decompressor()
    decompressed = _decompressor.decompress(buffer)

    return decompressed, _decompressor.signature
