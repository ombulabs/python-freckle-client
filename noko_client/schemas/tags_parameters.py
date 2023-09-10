"""Noko Tags Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `tags` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
from pydantic import BaseModel, field_validator

from noko_client.schemas.validators import format_booleans


class GetNokoTagsParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `entries` endpoint."""

    name: str | None
    billable: str | bool | None

    _format_booleans = field_validator("billable")(format_booleans)

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}
