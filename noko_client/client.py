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
    CreateNokoProjectGroupsParameters,
    CreateNokoProjectParameters,
    EditNokoEntryParameters,
    EditNokoProjectParameters,
    GetNokoEntriesParameters,
    GetNokoProjectGroupsParameters,
    GetNokoProjectsParameters,
    GetNokoTagsParameters,
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

    def list_tags(self, **kwargs: dict) -> list[dict] | None:
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

    def create_tags(self, names: list[str]) -> list[dict] | None:
        """Create new Noko tags.

        If any one tag cannot be created for any reason, it will be ignored and will not affect the response.

        Args:
            names (list[str]): A list of the names of the tags to create. Adding a "*" at the end of a string
                indicates that the tag is unbillable.

        Returns:
            (list[dict]): A list of all created tags.
        """
        return self.fetch_json("tags", post_args={"names": names}, http_method="POST")

    def get_single_tag(self, tag_id: int | str) -> list[dict] | None:
        """Retrieve a single tag based on the tag ID.

        Args:
            tag_id (str | int): the ID of the tag to retrieve.

        Returns:
            (list[dict]): The retrieved tag as a dictionary.
        """
        return self.fetch_json(f"tags/{tag_id}", http_method="GET")

    def get_all_entries_for_tag(
        self, tag_id: str | int, **kwargs: dict
    ) -> list[dict] | None:
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

    def edit_tag(self, tag_id: str | int, name: str) -> list[dict] | None:
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

    def list_projects(self, **kwargs: dict) -> list[dict] | None:
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

    def get_single_project(self, project_id: str | int) -> list[dict] | None:
        """Retrieve a single project based on the project ID.

        Args:
            project_id (str | int): the ID of the entry to retrieve.

        Returns:
            (list[dict]): The retrieved project as a dictionary.
        """
        return self.fetch_json(f"projects/{project_id}", http_method="GET")

    def create_project(self, **kwargs: dict) -> list[dict] | None:
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
        self, project_id: str | int, **kwargs: dict
    ) -> list[dict] | None:
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

    def get_expenses_for_project(self) -> None:
        """Retrieve expenses associated with a project."""
        raise NotImplementedError("Uh oh! This method has not been implemented yet.")

    def edit_project(self, project_id: str | int, **kwargs: dict) -> list[dict] | None:
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

    def list_project_groups(self, **kwargs: dict) -> list[dict] | None:
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

    def create_project_group(self, **kwargs: dict) -> list[dict] | None:
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

    def get_single_project_group(
        self, project_group_id: str | int
    ) -> list[dict] | None:
        """Retrieve a single project group.

        Args:
            project_group_id (str | int): The ID of the project group to retrieve.

        Returns:
            (list[dict]): The project group retrieved as a dictionary.
        """
        return self.fetch_json(f"project_groups/{project_group_id}", http_method="GET")

    def edit_project_group(
        self, project_group_id: str | int, name: str
    ) -> list[dict] | None:
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
        self, project_group_id: str | int, **kwargs: dict
    ) -> list[dict] | None:
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
        self, project_group_id: str | int, **kwargs: dict
    ) -> list[dict] | None:
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
    ) -> list[dict] | None:
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
