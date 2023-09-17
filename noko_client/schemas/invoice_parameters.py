"""Noko Invoices Request Parameters Schema.

Pydantic schemas to process and validate parameters before making requests to the `invoices` endpoint of the Noko API.
"""
# pylint: disable=no-self-argument
# mypy: disable-error-code=assignment
from datetime import datetime

from pydantic import BaseModel, field_validator
from pydantic_core import ValidationError

from noko_client.schemas.validators import (
    format_booleans,
    format_date,
    format_id_lists,
    format_list_of_integers,
    format_timestamps,
)

VALID_RATE_CALCULATION = ("custom_hourly_rates", "standard_hourly_rate", "flat_rate")
VALID_STATE = ("unpaid", "awaiting_payment", "in_progress", "paid", "none")


class CreateNokoInvoiceParameters(BaseModel):
    """Process and validate parameters to make POST requests to the `invoices` endpoint."""

    invoice_date: str | datetime
    reference: str | None = None
    project_name: str | None = None
    company_name: str | None = None
    company_details: str | None = None
    recipient_details: str | None = None
    description: str | None = None
    footer: str | None = None
    show_hours_worked: bool | str = True
    show_full_report: bool | str = False
    show_user_summaries: bool | str = False
    show_project_summaries: bool | str = False
    show_project_name_for_expenses: bool | str = False
    rate_calculation: dict | None = None
    entry_ids: list | None = None
    expense_ids: list | None = None
    taxes: list[dict] | None = None
    customization: dict | None = None

    _format_date = field_validator("invoice_date")(format_date)

    _format_booleans = field_validator(
        "show_hours_worked",
        "show_full_report",
        "show_user_summaries",
        "show_project_summaries",
        "show_project_name_for_expenses",
    )(format_booleans)

    @field_validator("rate_calculation")
    def validate_rate_calculation(cls, value: dict | None) -> dict | None:
        """Validate that rate calculation is a valid string (it is one of the accepted values)."""
        if value is None:
            return None

        calc_method = value.get("calculation_method")
        if calc_method not in VALID_RATE_CALCULATION:
            raise ValidationError(
                "Rate calculation provided with invalid calculation_method."
            )

        match calc_method:
            case "flat_rate":
                if "flat_rate" not in value.keys():
                    raise ValidationError(
                        "Rate calculation set to flat_rate but flat_rate parameter not provided."
                    )
            case "standard_hourly_rate":
                if (
                    "standard_hourly_rate" not in value.keys()
                    and "custom_hourly_rate" not in value.keys()
                ):
                    raise ValidationError(
                        "Rate calculation set to standard_hourly_rate but none of standard_hourly_rate or custom_hourly_rate not provided."
                    )
            case "custom_hourly_rate":
                if "custom_hourly_rate" not in value.keys():
                    raise ValidationError(
                        "Rate calculation set to custom_hourly_rate but custom_hourly_rate parameter not provided."
                    )
        return value

    _format_list_of_integers = field_validator("entry_ids", "expense_ids")(
        format_list_of_integers
    )

    @field_validator("taxes")
    def validate_taxes(cls, value: list[dict] | None) -> list[dict] | None:
        """Validate taxes dictionaries."""
        if value is None:
            return value

        for item in value:
            if "percentage" not in item:
                raise ValidationError(
                    "A dictionary in the taxes list is missing the required percentage."
                )
        return value

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}


class EditNokoInvoiceParameters(CreateNokoInvoiceParameters):
    """Process and validate parameters to make PUT requests to the `invoices` endpoint."""

    invoice_date: str | datetime | None = None


class GetNokoInvoicesParameters(BaseModel):
    """Process and validate parameters to make GET requests to the `invoices` endpoint."""

    state: str | None = None
    reference: str | None = None
    invoice_date_from: str | datetime | None = None
    invoice_date_to: str | datetime | None = None
    project_name: str | None = None
    total_amount_from: int | float | None = None
    total_amount_to: int | float | None = None
    recipient_details: str | None = None
    project_ids: str | int | list | None = None
    company_name: str | None = None
    company_details: str | None = None
    description: str | None = None
    footer: str | None = None
    has_online_payment_details: bool | str | None = None
    has_custom_html: bool | str | None = None
    show_hours_worked: bool | str | None = None
    show_full_report: bool | str | None = None
    show_user_summaries: bool | str | None = None
    show_project_summaries: bool | str | None = None
    show_project_name_for_expenses: bool | str | None = None
    locale: str | None = None
    currency_code: str | None = None
    currency_symbol: str | None = None
    rate_calculation: str | None = None
    updated_from: str | datetime | None = None
    updated_to: str | datetime | None = None

    @field_validator("state")
    def validate_state(cls, value: str) -> str:
        """Validate state is a valid string (one of the accepted values)."""
        if value not in VALID_STATE:
            raise ValidationError(
                f"Invalid state. Must be one of {', '.join(VALID_STATE)}"
            )
        return value

    _format_date = field_validator("invoice_date_from", "invoice_date_to")(format_date)

    _format_id_list = field_validator("project_ids")(format_id_lists)

    _format_booleans = field_validator(
        "has_online_payment_details",
        "has_custom_html",
        "show_hours_worked",
        "show_full_report",
        "show_user_summaries",
        "show_project_summaries",
        "show_project_name_for_expenses",
    )(format_booleans)

    @field_validator("rate_calculation")
    def validate_rate_calculation(cls, value: str | None) -> str | None:
        """Validate that rate calculation is a valid string (it is one of the accepted values)."""
        if value not in VALID_RATE_CALCULATION:
            raise ValidationError(
                f"Invalid rate calculation. Must be one of {', '.join(VALID_RATE_CALCULATION)}"
            )
        return value

    _format_timestamps = field_validator("updated_from", "updated_to")(
        format_timestamps
    )

    def model_dump(self, **kwargs) -> dict:
        """Override the `model_dump` method.

        Remove None values from the dictionary.
        """
        data = super().model_dump(**kwargs)
        return {key: value for key, value in data.items() if value is not None}
