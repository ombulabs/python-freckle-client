"""Common utilities shared by the client's methods."""
import logging
from datetime import datetime


def boolean_as_lower_string(value: bool | str | None) -> str | None:
    """Return a boolean value as a lower case string."""
    if isinstance(value, bool):
        value = "true" if value else "false"
    return value.lower() if isinstance(value, str) else value


def date_to_string(date: datetime | str) -> str:
    """Convert datetime object to ISO 8601 string."""
    if isinstance(date, datetime):
        date = date.strftime("%Y-%m-%d")
    return date


def list_to_list_of_integers(value: list) -> list:
    """Turn a list into a list of integers.

    If an object in the list cannot be converted to an integer, it will be removed from the resulting list.
    """
    result = []
    for item in value:
        try:
            result.append(int(item))
        except (TypeError, ValueError) as error:
            logging.info("Value %s removed from list. Error: %s", item, error)
    return result


def list_to_string(value: list) -> str:
    """Turn a list into a comma separated string."""
    return ",".join([str(item) for item in value])


def timestamp_to_string(timestamp: datetime | str | None) -> str | None:
    """Convert a datetime object to an ISO 8601 timestamp string."""
    if isinstance(timestamp, datetime):
        timestamp = f"{timestamp.replace(microsecond=0).isoformat()}Z"
    return timestamp
