"""Noko Entries Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `entries` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
from datetime import datetime

from dateutil.parser import parse
from pydantic import BaseModel, Field, field_validator, model_validator

from noko_client.schemas.utilities import (
    boolean_as_lower_string,
    date_to_string,
    list_to_string,
    timestamp_to_string,
)


class CreateNokoEntryParameters(BaseModel):
    """Process and validate parameters to make POST requests to the `entries` endpoint."""

    date: str | datetime
    user_id: str | int
    minutes: int
    description: str | None = None
    project_id: str | int | None = None
    project_name: str | None = None
    source_url: str | None = None

    @field_validator("date")
    def format_date(cls, value: str | datetime | None) -> str | None:
        """If date provided as datetime, convert to string. If provided as string, validate for ISO 8601."""
        if isinstance(value, str):
            assert datetime.strptime(value, "%Y-%m-%d")
        return date_to_string(value) if isinstance(value, datetime) else value

    @field_validator("user_id", "project_id")
    def format_ids(cls, value: str | int | None) -> int | None:
        """Turn IDs provided as strings into integers."""
        return int(value) if isinstance(value, str) else value

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class EditNokoEntryParameters(BaseModel):
    """Process and validate parameters to make PUT requests to the `entries/:id` endpoint."""

    date: str | datetime | None = None
    user_id: str | int | None = None
    minutes: int | None = None
    description: str | None = None
    project_id: str | int | None = None
    project_name: str | None = None
    source_url: str | None = None

    @field_validator("date")
    def format_date(cls, value: str | datetime | None) -> str | None:
        """If date provided as datetime, convert to string. If provided as string, validate for ISO 8601."""
        if isinstance(value, str):
            assert datetime.strptime(value, "%Y-%m-%d")
        return date_to_string(value) if isinstance(value, datetime) else value

    @field_validator("user_id", "project_id")
    def format_ids(cls, value: str | int | None) -> int | None:
        """Turn IDs provided as strings into integers."""
        return int(value) if isinstance(value, str) else value

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class GetNokoEntriesParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `entries` endpoint."""

    user_ids: str | list | None = None
    description: str | None = None
    project_ids: str | list | None = None
    tag_ids: str | list | None = None
    tag_filter_type: str | None = None
    from_: str | datetime | None = Field(alias="from", default=None)
    to: str | datetime | None = Field(default=None)
    invoiced: bool | str | None = None
    updated_from: str | datetime | None = None
    updated_to: str | datetime | None = None
    billable: bool | str | None = None
    approved_at_from: str | datetime | None = None
    approved_at_to: str | datetime | None = None

    @model_validator(mode="before")
    def set_from(cls, values: dict) -> dict:
        """If `from_` provided, use it to set the `from` field."""
        if "from_" in values.keys():
            values["from"] = values.pop("from_")
        return values

    @field_validator("user_ids", "project_ids", "tag_ids")
    def format_id_lists(cls, value: str | list | None) -> str | None:
        """If IDs provided as lists, convert to a comma separated string."""
        return list_to_string(value) if isinstance(value, list) else value

    @field_validator("from_", "to", "approved_at_from", "approved_at_to")
    def format_dates(cls, value: str | datetime | None) -> str | None:
        """If dates provided as datetime objects, convert to string. If provided as string, validate for ISO 8601."""
        if isinstance(value, str):
            assert datetime.strptime(value, "%Y-%m-%d")
        return date_to_string(value) if isinstance(value, datetime) else value

    @field_validator("updated_from", "updated_to")
    def format_timestamps(cls, value: str | datetime | None) -> str | None:
        """Format a timestamp into ISO 8601 format."""
        if isinstance(value, str):
            value = parse(value.split("Z")[0])
        return timestamp_to_string(value) if isinstance(value, datetime) else value

    @field_validator("invoiced", "billable")
    def format_booleans(cls, value: bool | str | None) -> str | None:
        """Format boolean parameters into the respective lower case string expected by Noko."""
        return boolean_as_lower_string(value)

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Convert `from_` property to expected `from` key and remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        data["from"] = data.pop("from_")
        return {key: value for key, value in data.items() if value is not None}
