"""Reusable validators for multiple Pydantic schemas."""
from datetime import datetime

from dateutil.parser import parse

from noko_client.schemas.utilities import (
    boolean_as_lower_string,
    date_to_string,
    list_to_list_of_integers,
    list_to_string,
    timestamp_to_string,
)


def format_booleans(value: bool | str | None) -> str | None:
    """Format boolean parameters into the respective lower case string expected by Noko."""
    return boolean_as_lower_string(value)


def format_date(value: str | datetime) -> str:
    """If date provided as datetime, convert to string. If provided as string, validate for ISO 8601."""
    if isinstance(value, str):
        parse(value)
    return date_to_string(value) if isinstance(value, datetime) else value


def format_id_lists(value: str | int | list | None) -> str | None:
    """If IDs provided as lists, convert to a comma separated string."""
    return list_to_string(value) if isinstance(value, list) else str(value)


def format_list_of_integers(value: list | None) -> list | None:
    """Format a list as a list of integers."""
    return list_to_list_of_integers(value) if isinstance(value, list) else value


def format_timestamps(value: str | datetime | None) -> str | None:
    """Format a timestamp into ISO 8601 format."""
    if isinstance(value, str):
        value = parse(value.split("Z")[0])
    return timestamp_to_string(value) if isinstance(value, datetime) else value
