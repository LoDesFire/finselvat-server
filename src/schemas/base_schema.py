import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Annotated

from pydantic import BaseModel, ConfigDict, AfterValidator, field_serializer, PlainSerializer
from pydantic.alias_generators import to_pascal

from utils import datetime_utils


class BaseSchema(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_pascal,
        validate_by_name=True,
        serialize_by_alias=True,
        from_attributes=True,
    )

Decimal2 = Annotated[
    Decimal,
    PlainSerializer(
        lambda v: round(float(v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)), 2),
        return_type=float
    )
]

UTCDateTime = Annotated[datetime.datetime, AfterValidator(datetime_utils.to_utc)]
