class UnknownFileMagicException(Exception):
    def __init__(self, magic: bytes, expected_magic: bytes, *args):
        super().__init__(f"Unknown file magic: {magic.hex()}, while expected was {expected_magic.hex()}", *args)
