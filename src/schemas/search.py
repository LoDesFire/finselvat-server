import datetime

from schemas.base_schema import BaseSchema


class SearchRequest(BaseSchema):
    start_date: datetime.datetime
    end_date: datetime.datetime
    limit: int
    offset: int