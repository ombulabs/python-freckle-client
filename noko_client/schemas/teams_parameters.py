"""Noko Teams Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `teams` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
from pydantic import BaseModel, field_validator

from noko_client.schemas.validators import format_id_lists


class BaseTeam(BaseModel):
    """Base model for the actions related to the `team` endpoint."""

    name: str | None = None
    user_ids: str | int | list | None = None

    _format_user_ids = field_validator("user_ids")(format_id_lists)

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class CreateNokoTeamParameters(BaseTeam):
    """Process and validate parameters to make POST requests to the `teams` endpoint."""

    name: str
    user_ids: str | int | list


class GetNokoTeamsParameters(BaseTeam):
    """Process and validate parameters to make GET requests to the `teams` endpoint."""
