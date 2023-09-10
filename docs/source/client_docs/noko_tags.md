# Noko Tags

The `NokoClient` offers multiple methods to interact with `tags` in Noko. On methods where keyword arguments are
supported, parameter validation happens through Pydantic, allowing Python types other than what's supported by the Noko
API to be used when making requests, and providing a validation layer before the request is even made to the API.

```{eval-rst}
.. autoclass:: noko_client.client.NokoClient
    :members: list_tags, create_tags, get_single_tag, get_all_entries_for_tag, edit_tag, merge_tag_into_this_tag, delete_single_tag, delete_tags
```
