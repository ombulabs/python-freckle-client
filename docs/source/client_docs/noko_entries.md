# Noko Entries

The `NokoClient` offers multiple methods to interact with `entries` in Noko. On methods where keyword arguments are
supported, parameter validation happens through Pydantic, allowing Python types other than what's supported by the Noko
API to be used when making requests, and providing a validation layer before the request is even made to the API.

```{eval-rst}
.. autoclass:: noko_client.client.NokoClient
    :members: list_entries, get_single_entry, create_entry, edit_entry, mark_as_invoiced, mark_as_approved, mark_as_unapproved, delete_entry
```
