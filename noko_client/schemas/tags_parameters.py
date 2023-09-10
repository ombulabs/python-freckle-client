"""Noko Tags Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `tags` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
from pydantic import BaseModel, field_validator

from noko_client.schemas.utilities import boolean_as_lower_string


class GetNokoTagsParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `entries` endpoint."""

    name: str | None
    billable: str | bool | None

    @field_validator("billable")
    def format_booleans(cls, value: bool | str | None) -> str | None:
        """Format boolean parameters into the respective lower case string expected by Noko."""
        return boolean_as_lower_string(value)

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}
