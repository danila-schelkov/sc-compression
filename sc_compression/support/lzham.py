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
        with open(temp_file_path, 'wb') as file:
            file.write(writer.buffer)

        decompressed_path = mktemp('.lzham')
        if system(f'{path.dirname(__file__)}/lzham.exe '
                  f'-c -d{filters["dict_size_log2"]} '
                  f'd {temp_file_path} {decompressed_path} > nul 2>&1'):
            remove(temp_file_path)
            remove(decompressed_path)
            return None
        with open(decompressed_path, 'rb') as file:
            decompressed = file.read()

        remove(temp_file_path)
        remove(decompressed_path)

        return decompressed

    @staticmethod
    def compress(data, filters):
        temp_file_path = mktemp('.data')
        with open(temp_file_path, 'wb') as file:
            file.write(data)

        compressed_path = mktemp('.lzham')
        if system(f'{path.dirname(__file__)}/lzham.exe '
                  f'-c -d{filters["dict_size_log2"]} '
                  f'c {temp_file_path} {compressed_path} > nul 2>&1'):
            remove(temp_file_path)
            remove(compressed_path)
            return None
        with open(compressed_path, 'rb') as file:
            compressed = file.read()[13:]

        remove(temp_file_path)
        remove(compressed_path)

        return compressed
