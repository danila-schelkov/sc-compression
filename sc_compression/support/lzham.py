from sc_compression.utils.writer import Writer
from tempfile import mktemp
from os import remove, system, path


class LZHAM:
    @staticmethod
    def decompress(data, uncompressed_size, filters):
        writer = Writer('little')
        writer.write(b'LZH\x30')
        writer.writeByte(filters['dict_size_log2'])
        writer.writeUInt32(uncompressed_size)
        writer.writeUInt32(0)
        writer.write(data)

        temp_file_path = mktemp('.lzham')
        with open(temp_file_path, 'wb') as f:
            f.write(writer.buffer)
            f.close()

        if system(f'{path.dirname(__file__)}/lzham.exe '
                  f'-c -d{filters["dict_size_log2"]} '
                  f'd {temp_file_path} {temp_file_path} > nul 2>&1'):
            return None
        with open(temp_file_path, 'rb') as f:
            decompressed = f.read()
            f.close()

        remove(temp_file_path)

        return decompressed

    @staticmethod
    def compress(data, filters):
        temp_file_path = mktemp('.data')
        with open(temp_file_path, 'wb') as f:
            f.write(data)
            f.close()

        compressed_path = mktemp('.lzham')
        if system(f'{path.dirname(__file__)}/lzham.exe '
                  f'-c -d{filters["dict_size_log2"]} '
                  f'c {temp_file_path} {compressed_path} > nul 2>&1'):
            return None
        with open(compressed_path, 'rb') as f:
            compressed = f.read()[13:]
            f.close()

        remove(temp_file_path)
        remove(compressed_path)

        return compressed
