# Noko Users

The `NokoClient` offers multiple methods to interact with `users` in Noko. On methods where keyword arguments are
supported, parameter validation happens through Pydantic, allowing Python types other than what's supported by the Noko
API to be used when making requests, and providing a validation layer before the request is even made to the API.

```{eval-rst}
.. autoclass:: noko_client.client.NokoClient
    :members: list_users, get_single_user, get_user_entries, get_user_expenses, create_user, edit_user, reactivate_user, give_user_access_to_projects, revoke_user_access_to_projects, revoke_user_access_to_all_projects, delete_user, deactivate_user 
```
