"""Noko API Client.

Provide an interface to easily interact with the Noko API. Supports parameter validation and formatting into what
is expected by Noko.

References
    Noko's full API documentation can be found at https://developer.nokotime.com/v2
"""
# mypy: disable-error-code="return-value, arg-type"
from datetime import datetime

from noko_client.base_client import BaseClient
from noko_client.schemas import (
    CreateNokoEntryParameters,
    CreateNokoExpenseParameters,
    CreateNokoInvoiceParameters,
    CreateNokoProjectGroupsParameters,
    CreateNokoProjectParameters,
    CreateNokoTeamParameters,
    CreateNokoUserParameters,
    EditNokoEntryParameters,
    EditNokoExpenseParameters,
    EditNokoInvoiceParameters,
    EditNokoProjectParameters,
    EditNokoUserParameters,
    GetNokoEntriesParameters,
    GetNokoExpensesParameters,
    GetNokoInvoicesParameters,
    GetNokoProjectGroupsParameters,
    GetNokoProjectsParameters,
    GetNokoTagsParameters,
    GetNokoTeamsParameters,
    GetNokoUsersParameters,
)
from noko_client.schemas.utilities import (
    date_to_string,
    list_to_list_of_integers,
    list_to_string,
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

    def list_entries(self, **kwargs) -> list[dict]:
        """List all entries.

        By default, retrieves all entries. The entries to retrieve can be filtered based on accepted Keyword Arguments.

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

    def get_single_entry(self, entry_id: str | int) -> list[dict]:
        """Retrieve a single entry based on the entry ID.

        Args:
            entry_id (str | int): the ID of the entry to retrieve.

        Returns:
            (list[dict]): The retrieved entry as a dictionary.
        """
        return self.fetch_json(f"entries/{entry_id}", http_method="GET")

    def create_entry(self, **kwargs) -> list[dict]:
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

    def edit_entry(self, entry_id: int | str, **kwargs) -> list[dict]:
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
        self,
        entry_ids: int | str | list[int | str],
        approved_at: str | datetime | None = None,
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

    # Tag related methods

    def list_tags(self, **kwargs) -> list[dict]:
        """List all tags.

        By default, retrieves all tags. The tags to retrieve can be filtered based on accepted Keyword Arguments.

        Keyword Args:
            name (str | None): Only tags containing the provided string in the name are returned. Defaults to None.
            billable (bool | None): Return only billable or unbillable tags. Defaults to both (set to None).

        Returns:
            (list[dict]): All retrieved tags as a list of dictionaries.
        """
        params = GetNokoTagsParameters(**kwargs).model_dump()
        return self.fetch_json("tags", query_params=params, http_method="GET")

    def create_tags(self, names: list[str]) -> list[dict]:
        """Create new Noko tags.

        If any one tag cannot be created for any reason, it will be ignored and will not affect the response.

        Args:
            names (list[str]): A list of the names of the tags to create. Adding a "*" at the end of a string
                indicates that the tag is unbillable.

        Returns:
            (list[dict]): A list of all created tags.
        """
        return self.fetch_json("tags", post_args={"names": names}, http_method="POST")

    def get_single_tag(self, tag_id: int | str) -> list[dict]:
        """Retrieve a single tag based on the tag ID.

        Args:
            tag_id (str | int): the ID of the tag to retrieve.

        Returns:
            (list[dict]): The retrieved tag as a dictionary.
        """
        return self.fetch_json(f"tags/{tag_id}", http_method="GET")

    def get_all_entries_for_tag(self, tag_id: str | int, **kwargs) -> list[dict]:
        """Retrieve all time entries associated with a tag.

        Results can be filtered using the same keyword arguments as the ones used for the list entries endpoint.
        All keyword arguments are optional.

        Args:
            tag_id (str | int): The ID of the tag to retrieve entries for.

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
            (list[dict]): A list of all retrieved entries meeting the specified criteria.
        """
        params = GetNokoEntriesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"tags/{tag_id}/entries", query_params=params, http_method="GET"
        )

    def edit_tag(self, tag_id: str | int, name: str) -> list[dict]:
        """Edit a single tag based on the tag ID.

        Args:
            tag_id (str | int): the ID of the tag to edit.
            name (str): The name for the tag. Adding a "*" at the end of the string indicates an unbillable tag.

        Returns:
            (list[dict]): The edited tag as a dictionary.
        """
        return self.fetch_json(
            f"tags/{tag_id}", post_args={"name": name}, http_method="PUT"
        )

    def merge_tag_into_this_tag(
        self, tag_id: str | int, tag_to_merge_id: str | int
    ) -> None:
        """Merge a tag into another one.

        When one tag is merged into another, the entries associated with the tag are associated with the new tag,
        and any instances of the old tags are replaced with the new tags in the Entry Description. This action is
        permanent, so you cannot undo after you merge tags.

        Args:
            tag_id (str | int): The ID of the tag to keep. This is the tag the other tag will be merged into.
            tag_to_merge_id (str | int): The ID of the tag to merge. This is the tag that will be merged into the
                other one.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(
            f"tags/{tag_id}/merge",
            post_args={"tag_id": tag_to_merge_id},
            http_method="PUT",
        )

    def delete_single_tag(self, tag_id: str | int) -> None:
        """Delete a single tag.

        When a tag is deleted, entries associated with it are not deleted. This action will, however, affect their
        descriptions. It will be updated so that the tag's text becomes part of the description.

        Args:
            tag_id (str | int): The ID of the tag to delete.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(f"tags/{tag_id}", http_method="DELETE")

    def delete_tags(self, tag_ids: list[str | int]) -> None:
        """Delete multiple tags at once.

        When a tag is deleted, entries associated with it are not deleted. This action will, however, affect their
        descriptions. It will be updated so that the tag's text becomes part of the description.

        If one of the tags in the provided list of IDs cannot be deleted, it will be ignored and it will not affect
        the response.

        Args:
            tag_ids (list [str | int]): The list of IDs of the tags to delete.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        tag_ids = list_to_list_of_integers(tag_ids)
        self.fetch_json(
            "tags/delete", post_args={"tag_ids": tag_ids}, http_method="DELETE"
        )

    # Project related methods

    def list_projects(self, **kwargs) -> list[dict]:
        """List all projects from Noko.

        By default, retrieves all projects. Projects to retrieve can be filtered based on accepted Keyword Arguments.

        Keyword Args:
            name (str | None): Only projects containing this string in the name are returned. Defaults to None.
            project_group_ids (str | list | None): Only projects belonging to the group IDs provided are returned.
                Accepts a comma separated string of IDs or a list of IDs. Defaults to None.
            billing_increment (int | None): Only projects with the specified billing increment are returned.
                Accepted values: 1, 5, 6, 10, 15, 20, 30, 60. Defaults to None.
            enabled (bool | None): Return only active or inactive projects. Defaults to None.
            billable (bool | None): Return only billable or unbillable projects. Defaults to None.

        Returns:
            (list[dict]): A list of retrieved projects.
        """
        params = GetNokoProjectsParameters(**kwargs).model_dump()
        return self.fetch_json("projects", query_params=params, http_method="GET")

    def get_single_project(self, project_id: str | int) -> list[dict]:
        """Retrieve a single project based on the project ID.

        Args:
            project_id (str | int): the ID of the entry to retrieve.

        Returns:
            (list[dict]): The retrieved project as a dictionary.
        """
        return self.fetch_json(f"projects/{project_id}", http_method="GET")

    def create_project(self, **kwargs) -> list[dict]:
        """Create new project in Noko.

        Keyword Args:
            name (str): The name of the project to create.
            billable (bool | None): Whether the project is billable or unabillable. Defaults to True.
            project_group_id (str | int | None): The ID of the project group the project will be associated with.
                Defaults to None.
            billing_increment (int | None): The billing increment to use for the project. The default amount will be
                the account's default billing increment (which is 15).
                Accepted values: 1, 5, 6, 10, 15, 20, 30, 60
            color (str | None): A hexadecimal color code to use as the project's color.

        Returns:
            (list[dict]): The project created with the provided information as a dictionary.
        """
        data = CreateNokoProjectParameters(**kwargs).model_dump()
        return self.fetch_json("projects", post_args=data, http_method="POST")

    def get_all_entries_for_project(
        self, project_id: str | int, **kwargs
    ) -> list[dict]:
        """Retrieve all time entries associated with a project.

        Results can be filtered using the same keyword arguments as the ones used for the list entries endpoint.
        All keyword arguments are optional.

        Args:
            project_id (str | int): The ID of the project to retrieve entries for.

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
            (list[dict]): A list of all retrieved entries meeting the specified criteria.
        """
        params = GetNokoEntriesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"projects/{project_id}/entries", query_params=params, http_method="GET"
        )

    def get_expenses_for_project(self, project_id: str | int, **kwargs) -> list[dict]:
        """Get all expenses associated with a project.

        Results can be filtered using the same keyword arguments as the ones used for the list expenses endpoint.
        All keyword arguments are optional.

        Args:
            project_id (str | int): The ID of the project to retrieve expenses for.

        Keyword Args:
            user_ids (str | list | None): The IDs of the users to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            description (str | None): Only expenses containing this text in their description are returned.
            project_ids (str | list | None): The IDs of the projects to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            invoice_ids (str | list | None): The IDs of the invoices to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            from_ (str | datetime | None): Only expenses from or after this date will be returned. If provided as
                string, must be in ISO 8601 format (YYY-MM-DD). Defaults to None.
            to (str | datetime | None): Only expenses on or before this date will be returned. If provided as
                string, must be in ISO 8601 format (YYY-MM-DD). Defaults to None.
            price_from (int | float | None): Only expenses with a price grater than or equal to this will be returned.
                Defaults to None.
            price_to (int | float | None): Only expenses with a price less than or equal to this will be returned.
                Defaults to None.
            taxable (bool | str | None): Return only expenses where taxes are applied or not applied. Defaults to both.
            invoiced (bool | str | None): Return only invoiced or uninvoiced expenses. Defaults to both.

        Returns:
            (list[dict]): A list of all retrieved expenses meeting the specified criteria.
        """
        params = GetNokoExpensesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"projects/{project_id}/expenses", query_params=params, http_method="GET"
        )

    def edit_project(self, project_id: str | int, **kwargs) -> list[dict]:
        """Edit an existing project.

        Args:
            project_id (int | str): The ID of the project to edit.

        Keyword Args:
            name (str | None): Name of the project. If not provided, date will not be changed.
            project_group_id (str | int | None): The ID of the project group the project will be associated with.
            billing_increment (int | None): Billing increment to be used by the project.
            color (str | None): The hexadecimal string representing a color to associate with the project.

        Returns:
            (list[dict]): The edited project with the provided information as a dictionary.
        """
        data = EditNokoProjectParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"projects/{project_id}", post_args=data, http_method="PUT"
        )

    def merge_project_into_this_project(
        self, project_id: str | int, project_to_merge_id: str | int
    ) -> None:
        """Merge a project into another one.

        When one project is merged into another, the entries, expenses and invoices associated with the project are
        associated with the new tag, and the merged project will be deleted once the merge has completed. This action
        is permanent, so you cannot undo after you merge projects. A merge cannot be performed if either project is
        archived.

        Args:
            project_id (str | int): The ID of the project to keep. This is the project the other project will
                be merged into.
            project_to_merge_id (str | int): The ID of the project to merge. This is the project that will be merged
            into the other one.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(
            f"projects/{project_id}/merge",
            post_args={"project_id": project_to_merge_id},
            http_method="PUT",
        )

    def delete_single_project(self, project_id: str | int) -> None:
        """Delete a single project.

        A project cannot be deleted if there are entries, invoices or expenses associated with it. Consider
        archiving the project instead.

        Args:
            project_id (str | int): The ID of the project to delete.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(f"projects/{project_id}", http_method="DELETE")

    def archive_single_project(self, project_id: str | int) -> None:
        """Archive a single project.

        A project cannot be deleted if there are no entries, invoices or expenses associated with it. Consider
        deleting the project instead.

        Args:
            project_id (str | int): The ID of the project to archive.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(f"projects/{project_id}/archive", http_method="PUT")

    def unarchive_single_project(self, project_id: str | int) -> None:
        """Unarchive a single project.

        Turn an archived project active.

        Args:
            project_id (str | int): The ID of the archived project to unarchive.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(f"projects/{project_id}/unarchive", http_method="PUT")

    def archive_projects(self, project_ids: list[int | str]) -> None:
        """Archive multiple projects.

        If any projects in the list cannot be archived, they will be ignored and will not affect the response.

        Args:
            project_ids (list[str | int]): The list of IDs of the projects to archive.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        post_args = {"project_ids": list_to_list_of_integers(project_ids)}
        self.fetch_json("projects/archive", post_args=post_args, http_method="PUT")

    def unarchive_projects(self, project_ids: list[int | str]) -> None:
        """Unarchive multiple projects.

        If any projects in the list cannot be unarchived, they will be ignored and will not affect the response.

        Args:
            project_ids (list[str | int]): The list of IDs of the projects to unarchive.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        post_args = {"project_ids": list_to_list_of_integers(project_ids)}
        self.fetch_json("projects/unarchive", post_args=post_args, http_method="PUT")

    def delete_projects(self, project_ids: list[int | str]) -> None:
        """Delete multiple projects.

        If any projects in the list cannot be deleted, they will be ignored and will not affect the response.

        Args:
            project_ids (list[str | int]): The list of IDs of the projects to delete.

        Returns:
            (None): Doesn't return anything, if unsuccessful, will raise an exception.
        """
        post_args = {"project_ids": list_to_list_of_integers(project_ids)}
        self.fetch_json("projects/delete", post_args=post_args, http_method="PUT")

    # Project group related methods

    def list_project_groups(self, **kwargs) -> list[dict]:
        """List all project groups from Noko.

        Keyword Args:
            name (str | None): Only project groups with this string in the name are returned. Defaults to None.
            project_ids (str | list | None): A list of project IDs to filter by. If provided as a string, must
                be a comma separated list. Defaults to None.

        Returns:
            (list[dict] | None): The retrieved Noko project groups as a list of dictionaries.
        """
        params = GetNokoProjectGroupsParameters(**kwargs).model_dump()
        return self.fetch_json("project_groups", query_params=params, http_method="GET")

    def create_project_group(self, **kwargs) -> list[dict]:
        """Create a new project group.

        Keyword Args:
            name (str): Name of the project group to be created.
            project_ids (str | list): A list of project IDs to associate with the new project group. A group cannot
                be created without at least one project associated with it.

        Returns:
            (list[dict]): The newly created project group as a dictionary.
        """
        params = CreateNokoProjectGroupsParameters(**kwargs).model_dump()
        return self.fetch_json(
            "project_groups", query_params=params, http_method="POST"
        )

    def get_single_project_group(self, project_group_id: str | int) -> list[dict]:
        """Retrieve a single project group.

        Args:
            project_group_id (str | int): The ID of the project group to retrieve.

        Returns:
            (list[dict]): The project group retrieved as a dictionary.
        """
        return self.fetch_json(f"project_groups/{project_group_id}", http_method="GET")

    def edit_project_group(self, project_group_id: str | int, name: str) -> list[dict]:
        """Edit a project group.

        Args:
            project_group_id (str | int): The ID of the project group to edit.
            name (str): The name to give the project group.

        Returns:
            (list[dict]): The updated project group as a dictionary.
        """
        post_args = {"name": name}
        return self.fetch_json(
            f"project_groups/{project_group_id}", post_args=post_args, http_method="PUT"
        )

    def get_all_entries_for_project_in_project_group(
        self, project_group_id: str | int, **kwargs
    ) -> list[dict]:
        """Retrieve all time entries associated with the projects in a project group.

        Results can be filtered using the same keyword arguments as the ones used for the list entries endpoint.
        All keyword arguments are optional.

        Args:
            project_group_id (str | int): The ID of the project group of the projects to retrieve entries for.

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
            (list[dict]): A list of all retrieved entries meeting the specified criteria.
        """
        params = GetNokoEntriesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"project_groups/{project_group_id}/entries",
            query_params=params,
            http_method="GET",
        )

    def get_all_projects_in_project_group(
        self, project_group_id: str | int, **kwargs
    ) -> list[dict]:
        """Retrieve all projects in a project group.

        Results can be filtered using the same keyword arguments as the ones used for the list projects endpoint.
        All keyword arguments are optional.

        Args:
            project_group_id (str | int): The ID of the project group of the projects to retrieve.

        Keyword Args:
            name (str | None): Only projects containing this string in the name are returned. Defaults to None.
            project_group_ids (str | list | None): Only projects belonging to the group IDs provided are returned.
                Accepts a comma separated string of IDs or a list of IDs. Defaults to None.
            billing_increment (int | None): Only projects with the specified billing increment are returned.
                Accepted values: 1, 5, 6, 10, 15, 20, 30, 60. Defaults to None.
            enabled (bool | None): Return only active or inactive projects. Defaults to None.
            billable (bool | None): Return only billable or unbillable projects. Defaults to None.

        Returns:
            (list[dict]): A list of all retrieved projects meeting the specified criteria.
        """
        params = GetNokoProjectsParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"project_groups/{project_group_id}/projects",
            query_params=params,
            http_method="GET",
        )

    def add_projects_to_group(
        self, project_group_id: str | int, project_ids: str | list[str | int]
    ) -> list[dict]:
        """Add projects to a project group.

        Args:
            project_group_id (str | int): The ID of the project group to add projects to.
            project_ids (str | list[str | int]): A list of IDs of projects to add to the project group. If provided
                as a list, must be a comma separated list.

        Returns:
            (list[dict]): A list of the projects added to the group.
        """
        if isinstance(project_ids, list):
            project_ids = list_to_list_of_integers(project_ids)
        post_args = {"project_ids": project_ids}
        return self.fetch_json(
            f"project_groups/{project_group_id}/add_projects",
            post_args=post_args,
            http_method="POST",
        )

    def remove_projects_from_group(
        self, project_group_id: str | int, project_ids: str | list[str | int]
    ) -> None:
        """Remove projects from a project group.

        Args:
            project_group_id (str | int): The ID of the project group to remove projects from.
            project_ids (str | list[str | int]): A list of IDs of projects to remove from the project group. If
                provided as a list, must be a comma separated list.

        Returns:
            (None): Does not return anything, if unsuccessful, raises an exception.
        """
        if isinstance(project_ids, list):
            project_ids = list_to_list_of_integers(project_ids)
        post_args = {"project_ids": project_ids}
        self.fetch_json(
            f"project_groups/{project_group_id}/remove_projects",
            post_args=post_args,
            http_method="PUT",
        )

    def remove_all_projects_from_group(self, project_group_id: str | int) -> None:
        """Remove all projects from a project group.

        Args:
            project_group_id (str | int): The ID of the project group to remove all projects from.

        Returns:
            (None): Does not return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(
            f"project_groups/{project_group_id}/remove_all_projects", http_method="PUT"
        )

    def delete_project_group(self, project_group_id: str | int) -> None:
        """Delete a project group.

        When a project group is deleted, the projects in it are not deleted, instead, they remain without a group.

        Args:
            project_group_id (str | int): The ID of the project group to delete.

        Returns:
            (None): Does not return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(f"project_groups/{project_group_id}", http_method="DELETE")

    # Invoice related methods

    def list_invoices(self, **kwargs) -> list[dict]:
        """List Noko invoices.

        Keyword Args:
            state (str | None): Only invoices in this state will be returned. Defaults to None.
                Accepted Values are: unpaid, awaiting_payment, in_progress, paid, none
            reference (str | None): Only invoices with this text in their invoice reference will be returned.
                Defaults to None.
            invoice_date_from (str | datetime | None): Only invoices dated from this day forward will be returned.
                If provided as string, must be in ISO 8061 format (YYYY-MM-DD). Defaults to None.
            invoice_date_to (str | datetime | None): Only invoices dated up to this day will be returned.
                If provided as string, must be in ISO 8061 format (YYYY-MM-DD). Defaults to None.
            project_name (str | None): Only invoices containing this text in their project_name field will be returned.
                Defaults to None.
            total_amount_from (int | float | None): Only invoices with a total amount due greater than or equal to
                this will be returned. Defaults to None.
            total_amount_to (int | float | None): Only invoices with a total amount due less than or equal to
                this will be returned. Defaults to None.
            recipient_details (str | None): Only invoices containing this text in their recipient_details field
                will be returned. Defaults to None.
            project_ids (str | list[int | str] | None): Only invoices containing these projects will be returned.
                If provided as a string, must be a comma separated string. Defaults to None.
            company_name (str | None): Only invoices containing this text in their company_name field are returned.
                Defaults to None.
            company_details (str | None): Only invoices containing this text in their company_details field
                are returned. Defaults to None.
            description (str | None): Only invoices containing this text in their description field are returned.
                Defaults to None.
            footer (str | None): Only invoices containing this text in their footer field are returned.
                Defaults to None.
            has_online_payment_details (str | bool | None): Whether to only return invoices that have or don't have
                online payment details. Defaults to None.
            has_custom_html (str | bool | None): Whether to only return invoices that include or don't include
                custom HTML. Defaults to None.
            show_hours_worked (str | bool | None): Whether to only return invoices that show or don't show hours worked.
                Defaults to None.
            show_full_report (str | bool | None): Whether to only return invoices that show or don't show the full
                report for the invoice. Defaults to None.
            show_user_summaries (str | bool | None): Whether to only return invoices that show or don't show the
                summary of hours worked for each team member. Defaults to None.
            show_project_summaries (str | bool | None): Whether to only return invoices that show or don't show the
                summary of hours worked for each project. Defaults to None.
            show_project_name_for_expenses (str | bool | None): Whether to only return invoices that show or don't
                show the expense's project name next to the expense description. Defaults to None.
            locale (str | None): Only invoices using the specified locally are returned. Accepted values are any of
                the locale codes supported by Noko. Defaults to None.
            currency_code (str | None): Only invoices using this currency are returned. Accepted values are any of
                the ISO currency codes support by Noko. Defaults to None.
            currency_symbol (str | None): Only invoices with this text as part of their currency_symbol are returned.
                Defaults to None.
            rate_calculation (str | None): Only invoices with the rate for the hours calculated in this manner are
                returned. Defaults to None.
                Accepted values: custom_hourly_rates, standard_hourly_rate, flat_rate
            updated_from (str | datetime | None): Only invoices updated from or after this timestamp will be returned.
                Defaults to None.
            updated_to (str | datetime | None): Only invoices updated on or before this timestamp will be returned.
                Defaults to None.

        Noko Invoice Locales: https://developer.nokotime.com/invoice_locales/#locales

        Returns:
            (list[dict]): All invoices matching the criteria as a list of dictionaries.
        """
        params = GetNokoInvoicesParameters(**kwargs).model_dump()
        return self.fetch_json("invoices", query_params=params, http_method="GET")

    def get_single_invoice(self, invoice_id: str | int) -> list[dict]:
        """Retrieve a single invoice from Noko.

        Args:
            invoice_id (str | int): The ID of the invoice to retrieve.

        Returns:
            (list[dict]): The invoice retrieved as a dictionary.
        """
        return self.fetch_json(f"invoices/{invoice_id}", http_method="GET")

    def create_invoice(self, **kwargs) -> list[dict]:
        """Create a new invoice in Noko.

        For additional information on options available for rate_calculation, taxes and customisation, refer to the
        Noko API documentation: https://developer.nokotime.com/v2/invoices/#create-an-invoice

        Keyword Args:
            invoice_date (str | datetime): The date the invoice was issued. If provided as a string, must be
                provided in ISO 8601 format (YYYY-MM-DD).
            reference (str | None): The invoice's reference identifier. If no value is provided, a value will be
                generated based on previous invoices as a default.
            project_name (str | None): The name of the project involved in this invoice. Defaults to None.
            company_name (str | None): The name of the company issuing the invoice. Defaults to None.
            company_details (str | None): The mailing address and any additional relevant information for the
                company issuing the invoice. Defaults to None.
            recipient_details (str | None): The mailing address and any additional relevant information for the
                recipient of the invoice. Defaults to None.
            description (str | None): A description of the invoice. Supports a limited version of Markdown.
                Noko documentation: https://help.nokotime.com/article/84-customizing-invoice-labels-and-formatting
            footer (str | None): The footer for each page of the invoice. Supports a limited version of Markdown.
                Noko documentation: https://help.nokotime.com/article/84-customizing-invoice-labels-and-formatting
            show_hours_worked (bool | str): Whether to show the hours worked when viewing the invoice.
                Defaults to True.
            show_full_report (bool | str): Whether to show the full report when viewing the invoice.
                Defaults to False.
            show_user_summaries (bool | str): Whether to show the total time in minutes worked by each team member.
                Defaults to False.
            show_project_summaries (bool | str): Whether to show the total time in minutes worked on each project.
                Defaults to False.
            show_project_name_for_expenses (bool | str): Whether to show the expense's project name next to its
                description on the invoice. Defaults to False.
            rate_calculation (dict | None): How to calculate the total amount of hours worked to generate the invoice.
                Dictionary keys are: calculation_method (required), flat_rate (required if calculation_method is
                flat_rate), standard_hourly_rate (required if calculation_method is standard_hourly_rate or
                custom_hourly_rate), custom_hourly_rates (required if calculation_method is custom_hourly_rate).
                Defaults to None.
            entry_ids (list | None): List of entries to include in the invoice. Can be a list of strings or integers.
                Defaults to None.
            expense_ids (list | None): List of expenses to include in the invoice. Can be a list of strings or integers.
                Defaults to None.
            taxes (list[dict] | None): The taxes to apply to this invoice, as a list of dictionaries.
                Dictionary fields: percentage (required), name (optional)
            customization (dict | None): Dictionary of customization options that define the labels and localization
                settings for the invoice. Reference: https://developer.nokotime.com/v2/invoices/#create-an-invoice

        Returns:
            (list[dict]): The created invoice as a dictionary.
        """
        data = CreateNokoInvoiceParameters(**kwargs).model_dump()
        return self.fetch_json("invoices", post_args=data, http_method="POST")

    def edit_invoice(self, invoice_id: str | int, **kwargs) -> list[dict]:
        """Edit a Noko invoice.

        Args:
            invoice_id (str | int): The ID of the invoice to edit.

        Keyword Args:
            invoice_date (str | datetime): The date the invoice was issued. If provided as a string, must be
                provided in ISO 8601 format (YYYY-MM-DD).
            reference (str | None): The invoice's reference identifier. If no value is provided, a value will be
                generated based on previous invoices as a default.
            project_name (str | None): The name of the project involved in this invoice. Defaults to None.
            company_name (str | None): The name of the company issuing the invoice. Defaults to None.
            company_details (str | None): The mailing address and any additional relevant information for the
                company issuing the invoice. Defaults to None.
            recipient_details (str | None): The mailing address and any additional relevant information for the
                recipient of the invoice. Defaults to None.
            description (str | None): A description of the invoice. Supports a limited version of Markdown.
                Noko documentation: https://help.nokotime.com/article/84-customizing-invoice-labels-and-formatting
            footer (str | None): The footer for each page of the invoice. Supports a limited version of Markdown.
                Noko documentation: https://help.nokotime.com/article/84-customizing-invoice-labels-and-formatting
            show_hours_worked (bool | str): Whether to show the hours worked when viewing the invoice.
                Defaults to True.
            show_full_report (bool | str): Whether to show the full report when viewing the invoice.
                Defaults to False.
            show_user_summaries (bool | str): Whether to show the total time in minutes worked by each team member.
                Defaults to False.
            show_project_summaries (bool | str): Whether to show the total time in minutes worked on each project.
                Defaults to False.
            show_project_name_for_expenses (bool | str): Whether to show the expense's project name next to its
                description on the invoice. Defaults to False.
            rate_calculation (dict | None): How to calculate the total amount of hours worked to generate the invoice.
                Dictionary keys are: calculation_method (required), flat_rate (required if calculation_method is
                flat_rate), standard_hourly_rate (required if calculation_method is standard_hourly_rate or
                custom_hourly_rate), custom_hourly_rates (required if calculation_method is custom_hourly_rate).
                Defaults to None.
            entry_ids (list | None): List of entries to include in the invoice. Can be a list of strings or integers.
                Defaults to None.
            expense_ids (list | None): List of expenses to include in the invoice. Can be a list of strings or integers.
                Defaults to None.
            taxes (list[dict] | None): The taxes to apply to this invoice, as a list of dictionaries.
                Dictionary fields: percentage (required), name (optional)
            customization (dict | None): Dictionary of customization options that define the labels and localization
                settings for the invoice. Reference: https://developer.nokotime.com/v2/invoices/#create-an-invoice

        Returns:
            (list[dict]): The edited invoice as a dictionary.
        """
        data = EditNokoInvoiceParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"invoices/{invoice_id}", post_args=data, http_method="PUT"
        )

    def mark_invoice_as_paid(self, invoice_id: str | int) -> None:
        """Mark an invoice as paid.

        Args:
            invoice_id (str | int): The ID of the invoice to mark as paid.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(f"invoices/{invoice_id}/paid", http_method="PUT")

    def mark_invoice_as_unpaid(self, invoice_id: str | int) -> None:
        """Mark an invoice as unpaid.

        Args:
            invoice_id (str | int): The ID of the invoice to mark as unpaid.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(f"invoices/{invoice_id}/unpaid", http_method="PUT")

    def get_invoice_entries(self, invoice_id: str | int, **kwargs) -> list[dict]:
        """Retrieve all time entries associated with an invoice.

        Results can be filtered using the same keyword arguments as the ones used for the list entries endpoint.
        All keyword arguments are optional.

        Args:
            invoice_id (str | int): The ID of the invoice to retrieve entries for.

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
            (list[dict]): A list of all retrieved entries meeting the specified criteria.
        """
        params = GetNokoEntriesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"invoices/{invoice_id}/entries", query_params=params, http_method="GET"
        )

    def get_invoice_expenses(self, invoice_id: str | int, **kwargs) -> list[dict]:
        """Retrieve all expenses associated with an invoice.

        Results can be filtered using the same keyword arguments as the ones used for the list expenses endpoint.
        All keyword arguments are optional.

        Args:
            invoice_id (str | int): The ID of the invoice to retrieve expenses for.

        Keyword Args:
            user_ids (str | list | None): The IDs of the users to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            description (str | None): Only expenses containing this text in their description are returned.
            project_ids (str | list | None): The IDs of the projects to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            invoice_ids (str | list | None): The IDs of the invoices to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            from_ (str | datetime | None): Only expenses from or after this date will be returned. If provided as
                string, must be in ISO 8601 format (YYY-MM-DD). Defaults to None.
            to (str | datetime | None): Only expenses on or before this date will be returned. If provided as
                string, must be in ISO 8601 format (YYY-MM-DD). Defaults to None.
            price_from (int | float | None): Only expenses with a price grater than or equal to this will be returned.
                Defaults to None.
            price_to (int | float | None): Only expenses with a price less than or equal to this will be returned.
                Defaults to None.
            taxable (bool | str | None): Return only expenses where taxes are applied or not applied. Defaults to both.
            invoiced (bool | str | None): Return only invoiced or uninvoiced expenses. Defaults to both.

        Returns:
            (list[dict]): A list of all retrieved expenses meeting the specified criteria.
        """
        params = GetNokoExpensesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"invoices/{invoice_id}/expenses", query_params=params, http_method="GET"
        )

    def add_entries_to_invoice(
        self, invoice_id: int | str, entry_ids: list[int | str]
    ) -> None:
        """Add time entries to an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to add entries to.
            entry_ids (list[int | str]): A list of the IDs of the entries to add to the invoice.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        post_args = {"entry_ids": list_to_list_of_integers(entry_ids)}
        self.fetch_json(
            f"invoices/{invoice_id}/add_entries", post_args=post_args, http_method="PUT"
        )

    def remove_entries_from_invoice(
        self, invoice_id: int | str, entry_ids: list[int | str]
    ) -> None:
        """Remove time entries from an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to remove entries from.
            entry_ids (list[int | str]): A list of the IDs of the entries to remove from the invoice. Any entries
                not associated with the invoice will be ignored and will not affect the response.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        post_args = {"entry_ids": list_to_list_of_integers(entry_ids)}
        self.fetch_json(
            f"invoices/{invoice_id}/remove_entries",
            post_args=post_args,
            http_method="PUT",
        )

    def remove_all_entries_from_invoice(self, invoice_id: int | str) -> None:
        """Remove all time entries from an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to remove all entries from.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(f"invoices/{invoice_id}/remove_all_entries", http_method="PUT")

    def add_expenses_to_invoice(
        self, invoice_id: int | str, expense_ids: list[int | str]
    ) -> None:
        """Add expenses to an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to add expenses to.
            expense_ids (list[int | str]): A list of the IDs of the expenses to add to the invoice.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        post_args = {"expense_ids": list_to_list_of_integers(expense_ids)}
        self.fetch_json(
            f"invoices/{invoice_id}/add_expenses",
            post_args=post_args,
            http_method="PUT",
        )

    def remove_expenses_from_invoice(
        self, invoice_id: int | str, expense_ids: list[int | str]
    ) -> None:
        """Remove expenses from an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to remove expenses from.
            expense_ids (list[int | str]): A list of the IDs of the expenses to remove from the invoice. Any expenses
                not associated with the invoice will be ignored and will not affect the response.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        post_args = {"expense_ids": list_to_list_of_integers(expense_ids)}
        self.fetch_json(
            f"invoices/{invoice_id}/remove_expenses",
            post_args=post_args,
            http_method="PUT",
        )

    def remove_all_expenses_from_invoice(self, invoice_id: int | str) -> None:
        """Remove all expenses from an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to remove all expenses from.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(f"invoices/{invoice_id}/remove_all_expenses", http_method="PUT")

    def add_taxes_to_invoice(self, invoice_id: int | str, taxes: list[dict]) -> None:
        """Add taxes to an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to add taxes to.
            taxes (list[dict]): A list of taxes to add to the invoice. Each tax should be represented as a dictionary
                with, at least, a `percentage` key and, optionally, a `name` key.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        post_args = {"taxes": taxes}
        self.fetch_json(
            f"invoices/{invoice_id}/add_taxes", post_args=post_args, http_method="PUT"
        )

    def remove_taxes_from_invoice(
        self, invoice_id: int | str, tax_ids: list[str | int]
    ) -> None:
        """Remove taxes from an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to remove taxes from.
            tax_ids (list[str | int]): The IDs of the taxes to remove from the invoice. Any taxes that are not
                associated with the invoice will be ignored and will not affect the response.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        post_args = {"tax_ids": list_to_list_of_integers(tax_ids)}
        self.fetch_json(
            f"invoices/{invoice_id}/remove_taxes",
            post_args=post_args,
            http_method="PUT",
        )

    def remove_all_taxes_from_invoice(self, invoice_id: int | str) -> None:
        """Remove all taxes from an invoice.

        Args:
            invoice_id (int | str): The ID of the invoice to remove all taxes from.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(f"invoices/{invoice_id}/remove_all_taxes", http_method="PUT")

    def delete_invoice(self, invoice_id: int | str) -> None:
        """Delete an invoice from Noko.

        When the invoice is deleted, the entries and expenses associated with it will be marked as uninvoiced.
        An invoice cannot be deleted if it has been paid or is locked for payment.

        Args:
            invoice_id (int | str): The ID of the invoice to delete.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(f"invoices/{invoice_id}", http_method="DELETE")

    # Expenses related methods

    def list_expenses(self, **kwargs) -> list[dict]:
        """List expenses from Noko.

        Keyword Args:
            user_ids (str | list | None): The IDs of the users to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            description (str | None): Only expenses containing this text in their description are returned.
            project_ids (str | list | None): The IDs of the projects to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            invoice_ids (str | list | None): The IDs of the invoices to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            from_ (str | datetime | None): Only expenses from or after this date will be returned. If provided as
                string, must be in ISO 8601 format (YYY-MM-DD). Defaults to None.
            to (str | datetime | None): Only expenses on or before this date will be returned. If provided as
                string, must be in ISO 8601 format (YYY-MM-DD). Defaults to None.
            price_from (int | float | None): Only expenses with a price grater than or equal to this will be returned.
                Defaults to None.
            price_to (int | float | None): Only expenses with a price less than or equal to this will be returned.
                Defaults to None.
            taxable (bool | str | None): Return only expenses where taxes are applied or not applied. Defaults to both.
            invoiced (bool | str | None): Return only invoiced or uninvoiced expenses. Defaults to both.

        Returns:
            (list[dict]): All retrieved expenses as a list of dictionaries.
        """
        params = GetNokoExpensesParameters(**kwargs).model_dump()
        return self.fetch_json("expenses", query_params=params, http_method="GET")

    def get_single_expense(self, expense_id: str | int) -> list[dict]:
        """Retrieve a single expense from Noko.

        Args:
            expense_id (str | int): The ID of the expense to retrieve.

        Returns:
            (list[dict]): The retrieve expense as a dictionary.
        """
        return self.fetch_json(f"expenses/{expense_id}", http_method="GET")

    def create_expense(self, **kwargs) -> list[dict]:
        """Create a new expense in Noko.

        Keyword Args:
            date (str | datetime): The date of the expense. If provided as string, must be in ISO 8601 format
                (YYYY-MM-DD).
            project_id (str | int): The ID of the project to log the expense to.
            price (int | float): The numeric price of the expense. Must be numeric only, and can be negative. Do not
                add the currency to this price.
            user_id (str | int | None): The ID of the user who created the expense. If no value is provided, the
                authenticated user will be used by default.
            taxable (bool | str | None): Whether the expense is taxable or not. Defaults to True.
            description (str | None): The description of the expense. Tags and hashtags will not be parsed.
                Defaults to None.

        Returns:
            (list[dict]): The newly created expense as a dictionary.
        """
        data = CreateNokoExpenseParameters(**kwargs).model_dump()
        return self.fetch_json("expenses", post_args=data, http_method="POST")

    def edit_expense(self, expense_id: str | int, **kwargs) -> list[dict]:
        """Edit an expense in Noko.

        Args:
            expense_id (str | int): The ID of the expense to edit.

        Keyword Args:
            date (str | datetime | None): The date of the expense. If provided as string, must be in ISO 8601 format
                (YYYY-MM-DD). Defaults to None.
            project_id (str | int): The ID of the project to log the expense to. Defaults to None.
            price (int | float): The numeric price of the expense. Must be numeric only, and can be negative. Do not
                add the currency to this price. Defaults to None.
            user_id (str | int | None): The ID of the user who created the expense. Defaults to None.
            taxable (bool | str | None): Whether the expense is taxable or not. Defaults to None.
            description (str | None): The description of the expense. Tags and hashtags will not be parsed.
                Defaults to None.

        Returns:
            (list[dict]): The edited expense as a dictionary.
        """
        data = EditNokoExpenseParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"expenses/{expense_id}", post_args=data, http_method="PUT"
        )

    def delete_expense(self, expense_id: str | int) -> None:
        """Delete an expense from Noko.

        Args:
            expense_id (str | int): The ID of the expense to delete.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        self.fetch_json(f"expenses/{expense_id}", http_method="DELETE")

    # Account related methods

    def get_account_details(self) -> list[dict]:
        """Get Noko account details.

        Returns:
            (list[dict]): The account's settings as a dictionary.
        """
        return self.fetch_json("account", http_method="GET")

    # User related methods

    def list_users(self, **kwargs) -> list[dict]:
        """List all Noko users in the account.

        Keyword Args:
            name (str | None): Only users with this string in their name are returned. Defaults to None.
            email (str | None): Only users with this string in their email address are returned. Defaults to None.
            role (str | None): Only users with this role will be returned. Defaults to all.
                Accepted values are: supervisor, leader, coworker, contractor
            state (str | None): Only users in this state will be returned. Defaults to all.
                Accepted values are: disabled, pending, active, suspended

        Returns:
            (list[dict]): A list of all users matching the specified criteria.
        """
        params = GetNokoUsersParameters(**kwargs).model_dump()
        return self.fetch_json("users", query_params=params, http_method="GET")

    def get_single_user(self, user_id: int | str) -> list[dict]:
        """Retrieve a single user from Noko.

        Args:
            user_id (str | int): The ID of the user to retrieve.

        Returns:
            (list[dict]): The retrieved user's information as a dictionary.
        """
        return self.fetch_json(f"users/{user_id}", http_method="GET")

    def get_user_entries(self, user_id: int | str, **kwargs) -> list[dict]:
        """Get all entries associated with a user.

        Results can be filtered using the same keyword arguments as the ones used for the list entries endpoint.
        All keyword arguments are optional.

        Args:
            user_id (str | int): The ID of the user to retrieve entries for.

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
            (list[dict]): A list of all retrieved entries meeting the specified criteria.
        """
        params = GetNokoEntriesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"users/{user_id}/entries", query_params=params, http_method="GET"
        )

    def get_user_expenses(self, user_id: str | int, **kwargs) -> list[dict]:
        """Retrieve all expenses associated with a user.

        Results can be filtered using the same keyword arguments as the ones used for the list expenses endpoint.
        All keyword arguments are optional.

        Args:
            user_id (str | int): The ID of the user to retrieve expenses for.

        Keyword Args:
            user_ids (str | list | None): The IDs of the users to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            description (str | None): Only expenses containing this text in their description are returned.
            project_ids (str | list | None): The IDs of the projects to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            invoice_ids (str | list | None): The IDs of the invoices to filter expenses by. If provided as string, must
                be a comma separated string. Defaults to None.
            from_ (str | datetime | None): Only expenses from or after this date will be returned. If provided as
                string, must be in ISO 8601 format (YYY-MM-DD). Defaults to None.
            to (str | datetime | None): Only expenses on or before this date will be returned. If provided as
                string, must be in ISO 8601 format (YYY-MM-DD). Defaults to None.
            price_from (int | float | None): Only expenses with a price grater than or equal to this will be returned.
                Defaults to None.
            price_to (int | float | None): Only expenses with a price less than or equal to this will be returned.
                Defaults to None.
            taxable (bool | str | None): Return only expenses where taxes are applied or not applied. Defaults to both.
            invoiced (bool | str | None): Return only invoiced or uninvoiced expenses. Defaults to both.

        Returns:
            (list[dict]): A list of all retrieved expenses meeting the specified criteria.
        """
        params = GetNokoExpensesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"users/{user_id}/expenses", query_params=params, http_method="GET"
        )

    def create_user(self, **kwargs) -> list[dict]:
        """Create a new Noko user.

        If your account has per-user billing, adding a new user will affect the total of your next invoice.

        Keyword Args:
            email (str): The email address of the user to create.
            first_name (str | None): The first name of the user to create. Defaults to None.
            last_name (str | None): The first name of the user to create. Defaults to None.
            role (str | None): The user's role in Noko. Defaulta to `leader`.
                Accepted values are: supervisor, leader, coworker, contractor

        Returns:
            (list[dict]): The created user's information as a dictionary.
        """
        data = CreateNokoUserParameters(**kwargs).model_dump()
        return self.fetch_json("users", post_args=data, http_method="POST")

    def edit_user(self, user_id: str | int, **kwargs) -> list[dict]:
        """Edit a Noko user's details.

        Args:
            user_id (str | int): The ID of the user to edit.

        Keyword Args:
            first_name (str | None): The first name of the user to create. Defaults to None.
            last_name (str | None): The first name of the user to create. Defaults to None.
            role (str | None): The user's role in Noko. Defaulta to None.
                Accepted values are: supervisor, leader, coworker, contractor

        Returns:
            (list[dict]): The edited user's information as a dictionary.
        """
        data = EditNokoUserParameters(**kwargs).model_dump()
        return self.fetch_json(f"users/{user_id}", post_args=data, http_method="PUT")

    def reactivate_user(self, user_id: str | int) -> None:
        """Reactivate a deactivated Noko user.

        If your account has per-user billing, this action will affect your next invoice's total.

        If the user is not deactivated, the action will fail. Similarly, if the maximum number of users in the
        account has been reached, the action will fail.

        Args:
            user_id (str | int): The ID of the deactivated user to reactivate.

        Returns:
            (None): Does not return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(f"users/{user_id}/activate", http_method="PUT")

    def give_user_access_to_projects(
        self, user_id: str | int, project_ids: list[str | int]
    ) -> None:
        """Give a Noko user access to a set of projects.

        If the user is deactivated, access cannot be granted and the action will fail. The authenticated user
        cannot change their own access rules.

        Args:
            user_id (str | int): The ID of the user to grant access to.
            project_ids (list[str | int]): The IDs of the projects to grant the user access to.

        Returns:
            (None): Does not return anything, if unsuccessful, will raise an exception.
        """
        post_args = {"project_ids": list_to_list_of_integers(project_ids)}
        self.fetch_json(
            f"users/{user_id}/give_access_to_projects",
            post_args=post_args,
            http_method="PUT",
        )

    def revoke_user_access_to_projects(
        self, user_id: str | int, project_ids: list[str | int]
    ) -> None:
        """Revoke a user's access to projects.

        Revoking a User’s access to a project prevents them from viewing the entries and expenses for the project.
        The user’s entries and expenses logged for the project are not deleted. Any projects that the user does
        not have access to are ignored.

        Cannot remove access from a deactivated user or a user that already has access to all projects. The
        authenticated user cannot change their own access rules.

        Any projects in the list the user does not have access to will be ignored and will not affect the response.

        Args:
            user_id (str | int): The ID of the user to revoke access from.
            project_ids (list[str | int]): The IDs of the projects to remove the user's access from.

        Returns:
            (None): Does not return anything, if unsuccessful, will raise an exception.
        """
        post_args = {"project_ids": list_to_list_of_integers(project_ids)}
        self.fetch_json(
            f"users/{user_id}/revoke_access_to_projects",
            post_args=post_args,
            http_method="PUT",
        )

    def revoke_user_access_to_all_projects(self, user_id: str | int) -> None:
        """Revoke a user's access to all projects.

        Cannot revoke access from deactivated users or users that can access all projects. The authenticated
        user cannot change their own access rules.

        Args:
            user_id (str | int): The ID of the user to revoke all access.

        Returns:
            (None): Does not return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(
            f"users/{user_id}/revoke_access_to_all_process", http_method="PUT"
        )

    def delete_user(self, user_id: str | int) -> None:
        """Delete a user from Noko.

        A user cannot be deleted if there are any entries associated with them. You can deactivate the user,
        which will remove this user from the list of active users and increment the number of users available
        until the account limit is reached.

        The account user also cannot be deleted, and the authenticate user cannot delete themselves.

        Args:
            user_id (str | int): The ID of the user to delete.

        Returns:
            (None): Does not return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(f"users/{user_id}", http_method="DELETE")

    def deactivate_user(self, user_id: str | int) -> None:
        """Deactivate a user from Noko.

        The account owner cannot be deactivated, and the authenticated user cannot deactivate themselves.
        If the user does not have entries associated with themselves, they can also not be deactivated and should
        be deleted instead.

        Args:
            user_id (str | int): The ID of the user to deactivate.

        Returns:
            (None): Does not return anything, if unsuccessful, will raise an exception.
        """
        self.fetch_json(f"users/{user_id}/deactivate", http_method="PUT")

    # Team related methods

    def list_teams(self, **kwargs) -> list[dict]:
        """List all teams in Noko.

        Keyword Args:
            name (str | None): Only teams with this string in the name will be returned. Defaults to None.
            user_ids (str | list[str | int] | None): List of user IDs to filter teams by. If provided as a string, must be a
                comma separated string. Defaults to None.

        Returns:
            (list[dict]): The list of teams in Noko as a list of dictionaries.
        """
        params = GetNokoTeamsParameters(**kwargs).model_dump()
        return self.fetch_json("teams", query_params=params, http_method="GET")

    def get_single_team(self, team_id: str | int) -> list[dict]:
        """Retrieve a single team from Noko.

        Args:
            team_id (str | int): The ID of the team to retrieve.

        Returns:
            (list[dict]): The retrieved team as a dictionary.
        """
        return self.fetch_json(f"teams/{team_id}", http_method="GET")

    def create_team(self, **kwargs) -> list[dict]:
        """Create a new team in Noko.

        Keyword Args:
            name (str): The name of the team to be created.
            user_ids (str | list[str | int]: List of users to associate with the team. If provided as a string,
            must be a comma separated string.

        Returns:
            (list[dict]): The created team as a dictionary.
        """
        data = CreateNokoTeamParameters(**kwargs).model_dump()
        return self.fetch_json("teams", post_args=data, http_method="POST")

    def edit_team(self, team_id: str | int, name: str) -> list[dict]:
        """Edit an existing team in Noko.

        Args:
            team_id (str | int): The ID of the team to edit in Noko.
            name (str): The name to give the team.

        Returns:
            (list[dict]): The created team as a dictionary.
        """
        post_args = {"name": name}
        return self.fetch_json(
            f"teams/{team_id}", post_args=post_args, http_method="PUT"
        )

    def get_entries_for_users_in_team(self, team_id: str | int, **kwargs) -> list[dict]:
        """Get all entries associated with a team.

        Results can be filtered using the same keyword arguments as the ones used for the list entries endpoint.
        All keyword arguments are optional.

        Args:
            team_id (str | int): The ID of the team to retrieve entries for.

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
            (list[dict]): A list of all retrieved entries meeting the specified criteria.
        """
        data = GetNokoEntriesParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"teams/{team_id}/entries", post_args=data, http_method="GET"
        )

    def get_users_in_team(self, team_id: str | int, **kwargs) -> list[dict]:
        """Get all users in a team.

        Results can be filtered using the same keyword arguments as the ones used for the users entries endpoint.
        All keyword arguments are optional.

        Args:
            team_id (str | int): The ID of the team to retrieve users for.

        Keyword Args:
            name (str | None): Only users with this string in their name are returned. Defaults to None.
            email (str | None): Only users with this string in their email address are returned. Defaults to None.
            role (str | None): Only users with this role will be returned. Defaults to all.
                Accepted values are: supervisor, leader, coworker, contractor
            state (str | None): Only users in this state will be returned. Defaults to all.
                Accepted values are: disabled, pending, active, suspended

        Returns:
            (list[dict]): A list of all retrieved users meeting the specified criteria.
        """
        data = GetNokoUsersParameters(**kwargs).model_dump()
        return self.fetch_json(
            f"teams/{team_id}/users", post_args=data, http_method="GET"
        )

    def add_users_to_team(
        self, team_id: str | int, user_ids: str | list[str | int]
    ) -> list[dict]:
        """Add users to a team.

        Args:
            team_id (str | int): The ID of the team to add users to.
            user_ids (str | list[str | int]): The IDs of the users to add to the team. If provided as string,
                must be a comma separated string.

        Returns:
            (list[dict]): A list of all users associated with the team.
        """
        post_args = {"user_ids": list_to_string(user_ids)}
        return self.fetch_json(
            f"teams/{team_id}/add_users", post_args=post_args, http_method="POST"
        )

    def remove_users_from_team(
        self, team_id: str | int, user_ids: str | list[str | int]
    ) -> None:
        """Remove users from a team.

        Args:
            team_id (str | int): The ID of the team to remove users from.
            user_ids (str | list[str | int]): The IDs of the users to remove from the team. If provided as string,
                must be a comma separated string.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        post_args = {"user_ids": list_to_string(user_ids)}
        return self.fetch_json(
            f"teams/{team_id}/remove_users", post_args=post_args, http_method="PUT"
        )

    def remove_all_users_from_team(self, team_id: str | int) -> None:
        """Remove all users from a team.

        Args:
            team_id (str | int): The ID of the team to remove all users from.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        return self.fetch_json(f"teams/{team_id}/remove_all_users", http_method="PUT")

    def delete_team(self, team_id: str | int) -> None:
        """Delete a team from Noko.

        Deleting a team will not delete the users in the team.

        Args:
            team_id (str | int): The ID of the team to delete.

        Returns:
            (None): Doesn't return anything, if unsuccessful, raises an exception.
        """
        return self.fetch_json(f"teams/{team_id}", http_method="DELETE")
