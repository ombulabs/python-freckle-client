"""Reusable validators for multiple Pydantic schemas."""

from utilities import list_to_string


def format_id_lists(value: str | list | None) -> str | None:
    """If IDs provided as lists, convert to a comma separated string."""
    return list_to_string(value) if isinstance(value, list) else value
