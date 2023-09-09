"""Noko API Client.

Provide an interface to easily interact with the Noko API. Supports parameter validation and formatting into what
is expected by Noko.

References
    Noko's full API documentation can be found at https://developer.nokotime.com/v2
"""
from datetime import datetime

from noko_client.base_client import BaseClient
from noko_client.schemas import (
    CreateNokoEntryParameters,
    EditNokoEntryParameters,
    GetNokoEntriesParameters,
)
from noko_client.schemas.utilities import (
    date_to_string,
    list_to_list_of_integers,
    timestamp_to_string,
)


class NokoClient(BaseClient):
    """Simple Client for the Noko API.

    Provide a friendlier interface to interact with the Noko API. Where Noko expects parameters to be passed in
    a specific way (for example, a list of strings for IDs, provide support for multiple types and handle formatting
    and validation.

    This client does not currently support oAuth.

    Attributes:
        access_token (str): The Noko access token to authenticate the requests.
    """

    # Entry related methods

    def list_entries(self, **kwargs: dict) -> list[dict] | None:
        """List all entries.

        By default, extracts all entries. The entries to extract can be filtered based on accepted Keyword Arguments.
        Noko List Entries Documentation: https://developer.nokotime.com/v2/entries/#list-entries

        Keyword Args:
            user_ids (str | list | None): IDs of users to filter. If provided as a string, must be comma separated.
                If provided as a list, can be provided as a list of integers or strings. Defaults to None.
            description (str | None): Only descriptions containing the provided text will be returned. Defaults to None.
            project_ids (str | list | None): IDs of projects to filter for. If provided as a string, must be comma
                separated. If provided as a list, can be provided as a list of integers or strings. Defaults to None.
            tag_ids (str | list | None): IDs of users to filter for. If provided as a string, must be comma separated.
                If provided as a list, can be provided as a list of integers or strings. Defaults to None.
            tag_filter_type (str | None): The type of filter to apply if filtering for tag_ids. Defaults to None.
            from_ (str | datetime | None): The date from which to search. Only entries logged on this day onwards
                will be returned. If provided as string, must be in ISO 8601 format (YYYY-MM-DD).
            to (str | datetime | None): The date up to which to search. Only entries logged up to this day will
                be returned. If provided as string, must be in ISO 8601 format (YYYY-MM-DD).
            invoiced (bool | str | None): Whether to filter for invoiced or uninvoiced entries. If provided as string,
                must be lower case. Defaults to None.
            updated_from (str | datetime | None): Only entries with updates from this timestamp onwards are returned.
                If provided as string, must be in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Defaults to None.
            updated_to (str | datetime | None): Only entries with updates up to this timestamp are returned.
                If provided as string, must be in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Defaults to None.
            billable (bool | str | None): Whether to filter for billable or unbillable entries. If provided as string,
                must be lower case. Defaults to None.
            approved_at_from (str | datetime | None): Only entries with approvals from this date on will be returned.
                If provided as string, must be in ISO 8601 format (YYYY-MM-DD). Defaults to None.
            approved_at_to (str | datetime | None): Only entries with approvals up to this date will be returned.
                If provided as string, must be in ISO 8601 format (YYYY-MM-DD). Defaults to None.

        Returns:
            (list[dict]): The complete response from Noko as a list of dictionaries.
        """
        params = GetNokoEntriesParameters(**kwargs).model_dump()
        return self.fetch_json("entries", http_method="GET", query_params=params)

    def get_single_entry(self, entry_id: str | int) -> list[dict] | None:
        """Retrieve a single entry based on the entry ID.

        Args:
            entry_id (str | int): the ID of the entry to retrieve.

        Returns:
            (list[dict]): The retrieved entry as a dictionary.
        """
        return self.fetch_json(f"entries/{entry_id}", http_method="GET")

    def create_entry(self, **kwargs: dict) -> list[dict] | None:
        """Create new entry in Noko.

        Keyword Args:
            date (str | datetime): Date the entry will be logged to. If provided as string,
                must be in ISO 8601 format (YYYY-MM-DD).
            user_id (str | int): The ID of the user who logged this time entry.
            minutes (int): The total number of minutes logged to the time entry. The number will automatically be
                rounded up to meet the project's `billing_increment` settings.
            description (str | None): The description to attach to the time entry. Defaults to None.
            project_id (str | int | None): The ID of the project to log the entry under. Defaults to None.
            project_name (str | None): The name of the project to log the entry under. If both `project_id` and
                `project_name`  are provided, `project_id` will be used. If no `project_id` or `project_name` are
                provided, the entry won't be logged under any project. If a name is provided and a project with this
                name does not exist yet, one will be created. Defaults to None.
            source_url (str | None): A URL representing the work completed in this time entry. For example, the URL
                to a GitHub PR or a Jira ticket ID. Defaults to None.

        Returns:
            (dict): The entry created with the provided information as a dictionary.
        """
        data = CreateNokoEntryParameters(**kwargs).model_dump()
        return self.fetch_json("entries", post_args=data, http_method="POST")

    def edit_entry(self, entry_id: int | str, **kwargs: dict) -> list[dict] | None:
        """Edit an existing entry.

        Args:
            entry_id (int | str): The ID of the time entry to edit.

        Keyword Args:
            date (str | datetime | None): Date the entry will be logged to. If provided as string,
                must be in ISO 8601 format (YYYY-MM-DD). If not provided, date will not be changed.
            user_id (str | int | None): The ID of the user who logged this time entry. If not provided, user will not
                be changed.
            minutes (int | None): The total number of minutes logged to the time entry. The number will automatically
                be rounded up to meet the project's `billing_increment` settings. If not provided, minutes will not be
                changed.
            description (str | None): The description to attach to the time entry. Any tags or hashtags will be
                automatically parsed. If not provided, description will not be changed.
            project_id (str | int | None): The ID of the project the entry is logged under. If not provided,
                the project will not be changed.
            project_name (str | None): The name of the project to log the entry under. If both `project_id` and
                `project_name`  are provided, `project_id` will be used. If no `project_id` or `project_name` are
                provided, the entry won't be logged under any project. If a name is provided and a project with this
                name does not exist yet, one will be created. If not provided, the project will not be changed.
            source_url (str | None): A URL representing the work completed in this time entry. For example, the URL
                to a GitHub PR or a Jira ticket ID. If not provided, the source URL will not be changed.

        Returns:
            (dict): The edited entry with the provided information as a dictionary.
        """
        data = EditNokoEntryParameters(**kwargs).model_dump()
        return self.fetch_json(f"entries/{entry_id}", post_args=data, http_method="PUT")

    def mark_as_invoiced(
        self, entry_ids: int | str | list[int] | list[str], date: str | datetime
    ) -> None:
        """Mark an entry or a list of entries as invoiced outside of Noko.

        If an entry has already been marked as invoiced outside of noko, the action will modify the `invoiced_at`
        date for that entry.

        Args:
            entry_ids (int | str | list[int] | list[str]): The ID of the entry (or entries) to mark as invoiced.
            date (str | datetime): The date to mark the entry as invoiced at. If provided as string, must be
                in ISO 8601 format (YYYY-MM-DD).

        Returns:
            (None): If unsuccessful, will raise an exception.
        """
        date = date_to_string(date)
        post_args = {"date": date}
        uri = f"entries/{entry_ids}/mark_as_invoiced"
        if isinstance(entry_ids, list):
            uri = "entries/mark_as_invoiced"
            post_args["entry_ids"] = list_to_list_of_integers(entry_ids)  # type: ignore[assignment]
        self.fetch_json(uri, post_args=post_args, http_method="PUT")

    def mark_as_approved(
        self, entry_ids: int | str | list[int | str], approved_at: str | datetime | None = None
    ) -> None:
        """Mark an entry or a list of entries as approved.

        Approved entries cannot be edited or deleted.

        If a single entry is provided and is associated with an archived project or is already approved,
        the request will fail.

        Any entries in a bulk request that cannot be edited or approved will be ignored and will not cause
        an unsuccessful response.

        Args:
            entry_ids (int | str | list[int] | list[str]): The ID of the entry (or entries) to mark as invoiced.
            approved_at (str | datetime | None): The timestamp for when the entry was approved. If provided as string,
            must be in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). If not provided, current time will be used.

        Returns:
            (None): If unsuccessful, will raise an exception.
        """
        approved_at = timestamp_to_string(approved_at)
        uri = f"entries/{entry_ids}/approved"
        post_args = {"approved_at": approved_at}
        if isinstance(entry_ids, list):
            uri = "entries/approved"
            post_args["entry_ids"] = list_to_list_of_integers(entry_ids)  # type: ignore[assignment]
        self.fetch_json(uri, post_args=post_args, http_method="PUT")

    def mark_as_unapproved(self, entry_ids: int | str | list[int | str]) -> None:
        """Mark an entry or a list of entries as unapproved.

        Unapproved entries can be edited or deleted.

        If a single entry is provided and is associated with an archived project, the request will fail.

        Any entries in a bulk request that cannot be edited or unapproved will be ignored and will not cause
        an unsuccessful response.

        Args:
            entry_ids (int | str | list[int] | list[str]): The ID of the entry (or entries) to mark as invoiced.

        Returns:
            (None): If unsuccessful, will raise an exception.
        """
        uri = f"entries/{entry_ids}/unapproved"
        post_args = {}
        if isinstance(entry_ids, list):
            uri = "entries/unapproved"
            post_args["entry_ids"] = list_to_list_of_integers(entry_ids)
        self.fetch_json(uri, post_args=post_args, http_method="PUT")

    def delete_entry(self, entry_id: str | int) -> None:
        """Delete a time entry.

        Entries that have been invoiced, approved or belong to an archived project cannot be deleted. In these cases,
        the request will fail with a custom error indicative of the issue.

        Args:
            entry_id (str | int): The ID of the time entry to delete.

        Returns:
            (None): If unsuccessful, will raise an exception.
        """
        self.fetch_json(f"entries/{entry_id}", http_method="DELETE")
