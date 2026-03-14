from typing import Self

from pydantic import Base64Bytes, model_validator

from schemas.base_schema import BaseSchema
from utils.hash_utils import sha256_hash


class SignedAPIData(BaseSchema):
    """Envelope for signed API requests and responses.
    """
    data: Base64Bytes
    sign: Base64Bytes
    signer_cert: Base64Bytes

    @model_validator(mode="after")
    def validate_signed_data(self) -> Self:
        """Validate that signature matches data hash."""
        if sha256_hash(self.data) != self.sign:
            raise ValueError("Signed API data does not match")
        return self

