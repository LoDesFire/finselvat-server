import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, AfterValidator
from pydantic.alias_generators import to_pascal

from utils import datetime_utils


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_pascal,
        validate_by_name=True,
        serialize_by_alias=True,
        from_attributes=True,
    )


UTCDateTime = Annotated[datetime.datetime, AfterValidator(datetime_utils.to_utc)]
