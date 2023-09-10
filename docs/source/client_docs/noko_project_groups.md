# Noko Project Groups

The `NokoClient` offers multiple methods to interact with `project_groups` in Noko. On methods where keyword arguments are
supported, parameter validation happens through Pydantic, allowing Python types other than what's supported by the Noko
API to be used when making requests, and providing a validation layer before the request is even made to the API.

```{eval-rst}
.. autoclass:: noko_client.client.NokoClient
    :members: list_project_groups, create_project_group, get_single_project_group, edit_project_group, get_all_entries_for_project_in_project_group, get_all_projects_in_project_group, add_projects_to_group, remove_projects_from_group, remove_all_projects_from_group, delete_project_group
```
