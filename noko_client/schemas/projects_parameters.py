"""Noko Projects Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `projects` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
from pydantic import BaseModel, field_validator

from noko_client.schemas.utilities import boolean_as_lower_string, list_to_string


class CreateNokoProjectParameters(BaseModel):
    """Process and validate parameters to make POST requests to the `projects` endpoint."""

    name: str
    billable: str | bool | None = None
    project_group_id: str | int | None = None
    billing_increment: int | None
    color: str | None

    @field_validator("billable")
    def format_booleans(cls, value: bool | str | None) -> str | None:
        """Format boolean parameters into the respective lower case string expected by Noko."""
        return boolean_as_lower_string(value)

    @field_validator("project_group_id")
    def format_ids(cls, value: str | int | None) -> int | None:
        """Turn IDs provided as strings into integers."""
        return int(value) if isinstance(value, str) else value

    @field_validator("billing_increment")
    def validate_billing_increment(cls, value: int | None) -> int | None:
        """Validate billing increment, if provided, is an accepted value."""
        valid_billing_increment = (1, 5, 6, 10, 15, 20, 30, 60)
        if isinstance(value, int):
            assert value in valid_billing_increment
        return value

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class EditNokoProjectParameters(BaseModel):
    """Process and validate parameters to make PUT requests to the `projects` endpoint."""

    name: str | None = None
    project_group_id: str | int | None = None
    billing_increment: int | None
    color: str | None

    @field_validator("project_group_id")
    def format_ids(cls, value: str | int | None) -> int | None:
        """Turn IDs provided as strings into integers."""
        return int(value) if isinstance(value, str) else value

    @field_validator("billing_increment")
    def validate_billing_increment(cls, value: int | None) -> int | None:
        """Validate billing increment, if provided, is an accepted value."""
        valid_billing_increment = (1, 5, 6, 10, 15, 20, 30, 60)
        if isinstance(value, int):
            assert value in valid_billing_increment
        return value

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class GetNokoProjectsParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `projects` endpoint."""

    name: str | None = None
    project_group_ids: str | list | None = None
    billing_increment: int | None = None
    enabled: bool | str | None = None
    billable: bool | str | None = None

    @field_validator("project_group_ids")
    def format_id_lists(cls, value: str | list) -> str:
        """If IDs provided as lists, convert to a comma separated string."""
        return list_to_string(value) if isinstance(value, list) else value

    @field_validator("billing_increment")
    def validate_billing_increment(cls, value: int | None) -> int | None:
        """If dates provided as datetime objects, convert to string. If provided as string, validate for ISO 8601."""
        valid_billing_increment = (1, 5, 6, 10, 15, 20, 30, 60)
        if isinstance(value, int):
            assert value in valid_billing_increment
        return value

    @field_validator("enabled", "billable")
    def format_booleans(cls, value: bool | str | None) -> str | None:
        """Format boolean parameters into the respective lower case string expected by Noko."""
        return boolean_as_lower_string(value)

    def model_dump(self, **kwargs) -> dict:
        """Override the custom `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}
