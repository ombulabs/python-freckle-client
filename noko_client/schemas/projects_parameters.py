"""Noko Projects Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `projects` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
from pydantic import BaseModel, field_validator
from pydantic_core import ValidationError

from noko_client.schemas.validators import format_booleans, format_id_lists

VALID_BILLING_INCREMENT = (1, 5, 6, 10, 15, 20, 30, 60)


def validate_billing_increment(value: int | None) -> int | None:
    """Validate billing increment, if provided, is an accepted value."""
    if isinstance(value, int) and value not in VALID_BILLING_INCREMENT:
        options_string = ", ".join(
            [str(increment) for increment in VALID_BILLING_INCREMENT]
        )
        raise ValidationError(
            f"Invalid billing increment provided. Must be one of {options_string}"
        )
    return value


class ProjectBase(BaseModel):
    """Base model for project create and edit schema."""

    name: str | None = None
    project_group_id: str | int | None = None
    billing_increment: int | None = None
    color: str | None = None

    @field_validator("project_group_id")
    def format_ids(cls, value: str | int | None) -> int | None:
        """Turn IDs provided as strings into integers."""
        return int(value) if isinstance(value, str) else value

    _validate_billing_increment = field_validator("billing_increment")(
        validate_billing_increment
    )

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class CreateNokoProjectParameters(ProjectBase):
    """Process and validate parameters to make POST requests to the `projects` endpoint."""

    name: str
    billable: str | bool | None = None

    _format_booleans = field_validator("billable")(format_booleans)


class EditNokoProjectParameters(ProjectBase):
    """Process and validate parameters to make PUT requests to the `projects` endpoint."""


class GetNokoProjectsParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `projects` endpoint."""

    name: str | None = None
    project_group_ids: str | list | None = None
    billing_increment: int | None = None
    enabled: bool | str | None = None
    billable: bool | str | None = None

    _format_id_lists = field_validator("project_group_ids")(format_id_lists)

    _validate_billing_increment = field_validator("billing_increment")(
        validate_billing_increment
    )

    _format_booleans = field_validator("enabled", "billable")(format_booleans)

    def model_dump(self, **kwargs) -> dict:
        """Override the custom `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}
