# Noko Client

[![Documentation Status](https://readthedocs.org/projects/python-freckle-client/badge/?version=latest)](https://python-freckle-client.readthedocs.io/en/latest/?badge=latest)

A simple Noko (formerly Freckle) API client implementation. Offers two different clients with different levels of flexibility
to interact with the Noko API v2.

Full documentation on the NokoClient can be found [here](https://python-freckle-client.readthedocs.io/en/latest/).

<!-- HIDE_INTRO -->
## Installation

To get the latest stable release from PyPi:

```shell
pip install python-freckle-client
```

**Requirements:**

Version `v0.5.0` and lower requires at least Python 3.8. Version `v1.0.0` and upper require Python 3.10 and Pydantic v2.

## Usage

The package offers three different clients:

- NokoClient (Noko's v2 API)
- FreckleClientV2 (Noko's v2 API)
- FreckleClient (Noko's v1 API) <- Deprecated!

To use the `NokoClient`, just import the client, create an instance and call the desired method:

```python
from noko_client.client import NokoClient

client = NokoClient('access_token')
entries = client.list_entries(from_="2023-08-01", to=datetime(2023, 8, 15))
```

To use the `FreckleClient` or the `FreckleClientV2`, just import the client, create an instance and call the `fetch_json` method: 

```python
from freckle_client.client import FreckleClient

client = FreckleClient('account_name', 'api_token')
entries = client.fetch_json(
    'entries',
    query_params={
        'per_page': 1000,
        'search[from]': '2015-01-01',
        'search[to]': '2015-01-31',
        'search[projects]': [1423, 24545, ],
    }
)
```

Similarly, to use the V2 API:

```python
from freckle_client.client import FreckleClientV2

client = FreckleClientV2('access_token')
entries = client.fetch_json(
    'entries',
    query_params={
        'from': '2015-01-01',
        'to': '2015-01-31',
        'billable': 'true',
        'project_ids': '12345,67890'
    }
)
```


## Contribute

If you want to contribute to this project, please fork this repository and clone your fork, then set up a virtual environment:

```shell
virtualenv -p 3.10 venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

Create a new branch, implement your feature or fix, and send us a pull request.
