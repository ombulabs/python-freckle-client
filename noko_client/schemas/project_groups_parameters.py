"""Noko Project Groups Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `project_groups` endpoint
of the Noko API.
"""
# pylint: disable=no-self-argument
from pydantic import BaseModel, field_validator

from noko_client.schemas.utilities import list_to_string


class CreateNokoProjectGroupsParameters(BaseModel):
    """Process and validate parameters to make POST requests to the `project_groups` endpoint."""

    name: str
    project_ids: str | list

    @field_validator("project_ids")
    def format_id_lists(cls, value: str | list) -> str:
        """If IDs provided as lists, convert to a comma separated string."""
        return list_to_string(value) if isinstance(value, list) else value

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class GetNokoProjectGroupsParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `project_groups` endpoint."""

    name: str | None = None
    project_ids: str | list | None = None

    @field_validator("project_ids")
    def format_id_lists(cls, value: str | list | None) -> str | None:
        """If IDs provided as lists, convert to a comma separated string."""
        return list_to_string(value) if isinstance(value, list) else value

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}
