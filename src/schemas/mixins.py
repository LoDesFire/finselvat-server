import json
from typing import Any

from pydantic import field_validator, field_serializer

from utils.base64_utils import decode_str_base64, encode_str_base64


class DataValidatorsMixin:
    @field_validator('data', mode='before', check_fields=False)
    @classmethod
    def validate_data(cls, value: Any) -> Any:
        if isinstance(value, str):
            return json.loads(decode_str_base64(value))
        return value

    @field_serializer('data', mode='plain', check_fields=False)
    def serialize_data(self, value: Any) -> Any:
        return encode_str_base64(value.model_dump_json())



class SignatureValidatorMixin:
    @field_validator('sign', mode='after', check_fields=False)
    @classmethod
    def validate_sign(cls, value: bytes) -> Any:
        if value == b'':
            raise ValueError(f'Signature is invalid')
        return value
