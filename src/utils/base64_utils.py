import base64
import binascii

def decode_bytes_base64(v: bytes) -> bytes:
    """Decode Base64 string to bytes."""
    return base64.b64decode(v)

def encode_bytes_base64(v: bytes) -> bytes:
    """Encode bytes to Base64 string."""
    return base64.b64encode(v)


def decode_str_base64(v: str) -> str:
    """Decode Base64 string to UTF-8 string.

    Validates Base64 encoding correctness.
    """
    try:
        return base64.b64decode(v, validate=True).decode("utf-8")
    except binascii.Error as e:
        raise ValueError("Invalid base64") from e

def encode_str_base64(v: str) -> str:
    """Encode UTF-8 string to Base64 string."""
    return base64.b64encode(v.encode("utf-8")).decode("utf-8")
