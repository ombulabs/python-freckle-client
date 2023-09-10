# Noko Expenses

The `NokoClient` offers multiple methods to interact with `expenses` in Noko. On methods where keyword arguments are
supported, parameter validation happens through Pydantic, allowing Python types other than what's supported by the Noko
API to be used when making requests, and providing a validation layer before the request is even made to the API.

```{eval-rst}
.. autoclass:: noko_client.client.NokoClient
    :members: list_expenses, get_single_expense, create_expense, edit_expense, delete_expense
```
