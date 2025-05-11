from typing import Any
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BeforeValidator


def get_datetime(
    days_from_now: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0
) -> datetime:
    """
    Get a datetime object with the specified offset from now in India timezone.
    """
    dt = datetime.now(tz=ZoneInfo("Asia/Kolkata")) + timedelta(
        days=days_from_now, hours=hours, minutes=minutes, seconds=seconds
    )
    return _get_nearest_microsecond(dt)


def _get_nearest_microsecond(dt: datetime) -> datetime:
    """
    Get a datetime object with the nearest microsecond.
    """
    return dt.replace(microsecond=dt.microsecond - (dt.microsecond % 1000))


def convert_datetime_to_ist(value: Any) -> datetime | Any:
    """
    Converts a datetime object or a recognizable datetime string
    to a timezone-aware datetime in IST.
    Handles naive datetimes by assuming they are UTC.
    """
    ist_tz = ZoneInfo("Asia/Kolkata")

    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=ZoneInfo("UTC")).astimezone(ist_tz)
        else:
            return value.astimezone(ist_tz)
    return value

UTCDateTime = Annotated[datetime, BeforeValidator(convert_datetime_to_ist)]