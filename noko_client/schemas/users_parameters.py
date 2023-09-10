"""Noko Users Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `users` endpoint of the Noko API.
"""
from pydantic import BaseModel, field_validator
from pydantic_core import ValidationError

VALID_ROLE: tuple = ("supervisor", "leader", "coworker", "contractor")
VALID_STATE: tuple = ("disabled", "pending", "active", "suspended")


def validate_role(value: str | None) -> str | None:
    """Validate that role is a valid string."""
    if isinstance(value, str) and value not in VALID_ROLE:
        raise ValidationError(f"Role must be one of: {', '.join(VALID_ROLE)}.")
    return value


def validate_state(value: str | None) -> str | None:
    """Validate that state is a valid string."""
    if isinstance(value, str) and value not in VALID_STATE:
        raise ValidationError(f"State must be one of: {', '.join(VALID_STATE)}.")
    return value


class BaseUser(BaseModel):
    """Base user for Noko user actions."""

    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None

    _validate_role = field_validator("role")(validate_role)


class CreateNokoUserParameters(BaseUser):
    """Process and validate parameters to make POST requests to the `users` endpoint."""

    email: str
    role: str | None = "leader"


class EditNokoUserParameters(BaseUser):
    """Process and validate parameters to make PUT requests to the `users` endpoint."""


class GetNokoUsersParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `users` endpoint."""

    name: str | None = None
    email: str | None = None
    role: str | None = None
    state: str | None = None

    _validate_role = field_validator("role")(validate_role)

    _validate_state = field_validator("state")(validate_state)

    def model_dump(self, **kwargs) -> dict:
        """Override the custom `dict` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}
