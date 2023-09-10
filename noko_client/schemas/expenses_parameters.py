"""Noko Expenses Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `expenses` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from noko_client.schemas.validators import format_booleans, format_date, format_id_lists


class ExpenseBase(BaseModel):
    """Base model for expense create and edit schema."""

    date: str | datetime | None = None
    project_id: str | int | None = None
    price: int | float | None = None
    user_id: str | int | None = None
    taxable: bool | str | None = None
    description: str | None = None

    _format_date = field_validator("date")(format_date)

    _format_booleans = field_validator("taxable")(format_booleans)

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

    _format_id_lists = field_validator("user_ids", "project_ids", "invoice_ids")(
        format_id_lists
    )

    _format_date = field_validator("from_", "to")(format_date)

    _format_booleans = field_validator("taxable", "invoiced")(format_booleans)

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Convert `from_` property to expected `from` key and remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        data["from"] = data.pop("from_")
        return {key: value for key, value in data.items() if value is not None}
