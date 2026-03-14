from datetime import datetime, timezone


def to_utc(v: datetime) -> datetime:
    if v.tzinfo is None:
        raise ValueError("Timezone required")

    return v.astimezone(timezone.utc)
