import hashlib


def sha256_hash(value: bytes) -> bytes:
    """Compute SHA-256 hash of bytes.
    """
    return hashlib.sha256(value).digest()