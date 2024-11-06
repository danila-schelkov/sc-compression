import lzma
from hashlib import md5

from sc_compression.signatures import Signatures
from sc_compression.utils.writer import Writer

try:
    import lzham
except ImportError:
    from platform import system as get_system_name

    lzham = None
    if get_system_name() == "Windows":
        from sc_compression.support.lzham import LZHAM

        lzham = LZHAM

try:
    import zstandard
except ImportError:
    zstandard = None


class Compressor:
    lzham_filters = {"dict_size_log2": 18}
    lzma_filters = [
        {
            "id": lzma.FILTER_LZMA1,
            "dict_size": 256 * 1024,
            "lc": 3,
            "lp": 0,
            "pb": 2,
            "mode": lzma.MODE_NORMAL,
        },
    ]

    def compress(
        self, data: bytes, signature: Signatures, file_version: int = None
    ) -> bytes:
        uncompressed_size = len(data)

        if file_version is None:
            file_version = 3 if zstandard and signature != Signatures.SCLZ else 1

        if (
            signature == Signatures.ZSTD
            and not zstandard
            or signature == Signatures.SCLZ
            and not lzham
        ):
            signature = Signatures.SC

        writer = Writer("little")
        if signature is Signatures.NONE:
            return data
        elif signature in (Signatures.LZMA, Signatures.SIG) or (
            signature == Signatures.SC and file_version != 3
        ):
            compressed = lzma.compress(
                data, format=lzma.FORMAT_ALONE, filters=self.lzma_filters
            )

            writer.write(compressed[:5])

            writer.write_int32(uncompressed_size)

            writer.write(compressed[13:])

            compressed = writer.buffer
        elif signature == Signatures.SCLZ and lzham:
            compressed = lzham.compress(data, filters=self.lzham_filters)

            writer.write(b"SCLZ")
            writer.write_u_int8(self.lzham_filters["dict_size_log2"])
            writer.write_int32(uncompressed_size)
            writer.write(compressed)

            compressed = writer.buffer
        elif signature in (Signatures.SC, Signatures.ZSTD) and zstandard is not None:
            compressor = zstandard.ZstdCompressor()
            compressed = compressor.compress(data)
        else:
            raise TypeError("Unknown Signature!")

        compressed = self._write_header(compressed, data, file_version, signature)

        return compressed

    @staticmethod
    def _write_header(
        compressed: bytes, data: bytes, file_version: int, signature: Signatures
    ) -> bytes:
        if signature in (Signatures.SC, Signatures.SCLZ):
            data_hash = md5(data).digest()

            writer = Writer("big")
            writer.write(b"SC")
            writer.write_int32(file_version)
            if file_version == 4:
                writer.write_int32(1)
            writer.write_int32(len(data_hash))
            writer.write(data_hash)
            return writer.buffer + compressed
        elif signature == Signatures.SIG:
            writer = Writer("big")
            writer.write(b"Sig:")
            writer.write(b"\x00" * 64)  # sha64
            return writer.buffer + compressed

        return compressed
