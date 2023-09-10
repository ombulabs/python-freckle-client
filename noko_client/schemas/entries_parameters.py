"""Noko Entries Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `entries` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
# mypy: disable-error-code=assignment
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from noko_client.schemas.validators import (
    format_booleans,
    format_date,
    format_id_lists,
    format_timestamps,
)


class BaseEntry(BaseModel):
    """Base model for actions related to entries."""

    date: str | datetime | None = None
    user_id: str | int | None = None
    minutes: int | None = None
    description: str | None = None
    project_id: str | int | None = None
    project_name: str | None = None
    source_url: str | None = None

    _format_date = field_validator("date")(format_date)

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


class CreateNokoEntryParameters(BaseEntry):
    """Process and validate parameters to make POST requests to the `entries` endpoint."""

    date: str | datetime
    user_id: str | int
    minutes: int


class EditNokoEntryParameters(BaseEntry):
    """Process and validate parameters to make PUT requests to the `entries/:id` endpoint."""


class GetNokoEntriesParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `entries` endpoint."""

    user_ids: str | list | None = None
    description: str | None = None
    project_ids: str | list | None = None
    tag_ids: str | list | None = None
    tag_filter_type: str | None = None
    from_: str | datetime | None = Field(alias="from", default=None)
    to: str | datetime | None = None
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

    _format_id_lists = field_validator("user_ids", "project_ids", "tag_ids")(
        format_id_lists
    )

    _format_dates = field_validator(
        "from_", "to", "approved_at_from", "approved_at_to"
    )(format_date)

    _format_timestamps = field_validator("updated_from", "updated_to")(
        format_timestamps
    )

    _format_booleans = field_validator("invoiced", "billable")(format_booleans)

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Convert `from_` property to expected `from` key and remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        data["from"] = data.pop("from_")
        return {key: value for key, value in data.items() if value is not None}
