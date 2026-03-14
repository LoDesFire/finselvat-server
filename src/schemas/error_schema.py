from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_pascal


class ErrorSchema(BaseModel):
    status_code: int
    error: str
    details: Optional[Any] = Field(None, exclude_if=lambda details: not details)

    model_config = ConfigDict(alias_generator=to_pascal, validate_by_name=True, serialize_by_alias=True)