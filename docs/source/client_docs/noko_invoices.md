# Noko Invoices

The `NokoClient` offers multiple methods to interact with `invoices` in Noko. On methods where keyword arguments are
supported, parameter validation happens through Pydantic, allowing Python types other than what's supported by the Noko
API to be used when making requests, and providing a validation layer before the request is even made to the API.

```{eval-rst}
.. autoclass:: noko_client.client.NokoClient
    :members: list_invoices, get_single_invoice, create_invoice, edit_invoice, mark_invoice_as_paid, mark_invoice_as_unpaid, get_invoice_entries, get_invoice_expenses, add_entries_to_invoice, remove_entries_from_invoice, remove_all_entries_from_invoice, add_expenses_to_invoice, remove_expenses_from_invoice, remove_all_expenses_from_invoice, add_taxes_to_invoice, remove_taxes_from_invoice, remove_all_taxes_from_invoice, delete_invoice
```
