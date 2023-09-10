"""Noko Expenses Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `expenses` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from noko_client.schemas.utilities import (
    boolean_as_lower_string,
    date_to_string,
    list_to_string,
)


class ExpenseBase(BaseModel):
    """Base model for expense create and edit schema."""

    date: str | datetime | None = None
    project_id: str | int | None = None
    price: int | float | None = None
    user_id: str | int | None = None
    taxable: bool | str | None = None
    description: str | None = None

    @field_validator("date")
    def format_dates(cls, value: str | datetime | None) -> str | None:
        """If dates provided as datetime objects, convert to string. If provided as string, validate for ISO 8601."""
        if isinstance(value, str):
            assert datetime.strptime(value, "%Y-%m-%d")
        return date_to_string(value) if isinstance(value, datetime) else value

    @field_validator("taxable")
    def format_booleans(cls, value: bool | str | None) -> str | None:
        """Format boolean parameters into the respective lower case string expected by Noko."""
        return boolean_as_lower_string(value)

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class CreateNokoExpenseParameters(ExpenseBase):
    """Process and validate parameters to make POST requests to the `expenses` endpoint."""

    date: str | datetime
    project_id: str | int
    price: int | float


class EditNokoExpenseParameters(ExpenseBase):
    """Process and validate parameters to make PUT requests to the `expenses` endpoint."""


class GetNokoExpensesParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `expenses` endpoint."""

    user_ids: str | list | None = None
    description: str | None = None
    project_ids: str | list | None = None
    invoice_ids: str | list | None = None
    from_: str | datetime | None = Field(alias="from", default=None)
    to: str | datetime | None = None
    price_from: int | float | None = None
    price_to: int | float | None = None
    taxable: bool | str | None = None
    invoiced: bool | str | None = None

    @field_validator("user_ids", "project_ids", "invoice_ids")
    def format_id_lists(cls, value: str | list) -> str:
        """If IDs provided as lists, convert to a comma separated string."""
        return list_to_string(value) if isinstance(value, list) else value

    @field_validator("from_", "to")
    def format_dates(cls, value: str | datetime | None) -> str | None:
        """If dates provided as datetime objects, convert to string. If provided as string, validate for ISO 8601."""
        if isinstance(value, str):
            assert datetime.strptime(value, "%Y-%m-%d")
        return date_to_string(value) if isinstance(value, datetime) else value

    @field_validator("taxable", "invoiced")
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
