# Welcome to the Python Noko Client's documentation!

The `python-freckle-client` is a simple client for the [Noko](https://nokotime.com/) (formerly Freckle) API. It supports
two different clients with different levels of flexibility and support to interact with the [Noko API v2](https://developer.nokotime.com/v2/).

## Noko Clients

There are two versions of the client available:

- FreckleClientV2
- NokoClient

The `FreckleClientV2` provides a quick and easy way to interact with NOKO, primarily to fetch JSON from it. The `NokoClient`
is built on top of the `FreckleClientV2` request handling and offers individual methods for different interactions with
parameter type flexibility and validation before the Noko API is even hit.

## Minimum Requirements

The `FreckleClientV2` is available in versions `v0.5.0` and up. The `NokoClient` is only available from version `v1.0.0`.

Notable requirements for v1.0.0:

- Python 3.10
- Pydantic v2

```{toctree}
:maxdepth: 2
:titlesonly:
:caption: "Get Started"

README
```

```{toctree}
:maxdepth: 6
:caption: "Client Documentation"

client_docs/noko_entries
client_docs/noko_tags
client_docs/noko_projects
client_docs/noko_project_groups
client_docs/noko_invoices
client_docs/noko_expenses
client_docs/noko_users
client_docs/noko_teams
```