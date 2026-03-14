import hashlib


def sha256_hash(value: bytes) -> bytes:
    return hashlib.sha256(value).digest()