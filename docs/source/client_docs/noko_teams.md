# Noko Teams

The `NokoClient` offers multiple methods to interact with `teams` in Noko. On methods where keyword arguments are
supported, parameter validation happens through Pydantic, allowing Python types other than what's supported by the Noko
API to be used when making requests, and providing a validation layer before the request is even made to the API.

```{eval-rst}
.. autoclass:: noko_client.client.NokoClient
    :members: list_teams, get_single_team, create_team, edit_team, get_entries_for_users_in_team, get_users_in_team, add_users_to_team, remove_users_from_team, remove_all_users_from_team, delete_team
```
