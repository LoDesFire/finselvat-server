import base64
import binascii

def decode_bytes_base64(v: bytes) -> bytes:
    return base64.b64decode(v)

def encode_bytes_base64(v: bytes) -> bytes:
    return base64.b64encode(v)


def decode_str_base64(v: str) -> str:
    try:
        return base64.b64decode(v, validate=True).decode("utf-8")
    except binascii.Error as e:
        raise ValueError("Invalid base64") from e

def encode_str_base64(v: str) -> str:
    return base64.b64encode(v.encode("utf-8")).decode("utf-8")
