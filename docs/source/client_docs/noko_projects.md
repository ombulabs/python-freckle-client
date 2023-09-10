# Noko Projects

The `NokoClient` offers multiple methods to interact with `projects` in Noko. On methods where keyword arguments are
supported, parameter validation happens through Pydantic, allowing Python types other than what's supported by the Noko
API to be used when making requests, and providing a validation layer before the request is even made to the API.

```{eval-rst}
.. autoclass:: noko_client.client.NokoClient
    :members: list_projects, get_single_project, create_project, get_all_entries_for_project, get_expenses_for_project, edit_project, merge_project_into_this_project, delete_single_project, archive_single_project, unarchive_single_project, archive_projects, unarchive_projects, delete_projects
```
