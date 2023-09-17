"""
Freckle client implementation.

Idea stolen from here:
https://github.com/sarumont/py-trello/blob/master/trello/__init__.py#L108

"""
import json
import warnings
from typing import Callable

import requests

from . import __version__, exceptions


def deprecated(func: Callable) -> Callable:
    """Decorate a function to flag a method as deprecated."""

    def deprecated_func(*args, **kwargs) -> Callable:  # noqa: ANN002, ANN003
        warnings.warn(
            "The FreckleClient is deprecated. Please use the NokoClient or the FreckleClientV2 instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    return deprecated_func


class FreckleClient:
    """Simple client implementation to fetch json data from the v1 API."""

    def __init__(self, account_name: str, api_token: str):
        """
        Create a ``FreckleClient`` instance.

        :account_name: Your Freckle account name.
        :api_token: Your Freckle API token.

        """
        self.account_name = account_name
        self.api_token = api_token

    @deprecated
    def fetch_json(
        self,
        uri_path: str,
        http_method: str = "GET",
        headers: dict | None = None,
        query_params: dict | None = None,
        post_args: dict | None = None,
    ) -> list[dict] | None:
        """
        Fetch some JSON from Noko.

        For example, fetch some entries like so:

            entries = self.fetch_json(
                'entries',
                query_params={
                    'per_page': 1000,
                    'search[from]': '2015-01-01',
                    'search[to]': '2015-01-31',
                    'search[projects]': [1423, 24545, ]),
                }
            )

        """
        # explicit values here to avoid mutable default values
        if headers is None:
            headers = {}
        if query_params is None:
            query_params = {}
        if post_args is None:
            post_args = {}

        # set content type and accept headers to handle JSON
        headers["Accept"] = "application/json"
        query_params["token"] = self.api_token

        # construct the full URL without query parameters
        url = f"https://{self.account_name}.nokotime.com/api/{uri_path}.json"

        # perform the HTTP requests, if possible uses OAuth authentication
        response = requests.request(
            http_method,
            url,
            params=query_params,
            headers=headers,
            data=json.dumps(post_args),
        )

        if response.status_code != 200:
            raise exceptions.FreckleClientException(
                "Freckle API Response is not 200", response.text
            )

        # return content if successful response with content,
        # otherwise return None
        return json.loads(response.content) if response.content else None


class FreckleClientV2:
    """Simple client implementation to fetch json data from the v2 API."""

    def __init__(self, access_token: str):
        """
        Create a ``FreckleClient`` instance.

        :account_name: Your Freckle account name.
        :api_token: Your Freckle API token.

        """
        self.access_token = access_token

    def fetch_json(
        self,
        uri_path: str,
        http_method: str = "GET",
        headers: dict | None = None,
        query_params: dict | None = None,
        post_args: dict | None = None,
    ) -> list[dict] | None:
        """
        Fetch some JSON from Noko.

        For example, fetch some entries like so:

            entries = self.fetch_json(
                'entries',
                query_params={
                    'search[from]': '2015-01-01',
                    'search[to]': '2015-01-31',
                    'search[projects]': [1423, 24545, ]),
                }
            )

        """
        # explicit values here to avoid mutable default values
        if headers is None:
            headers = {}
        if query_params is None:
            query_params = {}
        if post_args is None:
            post_args = {}

        # set content type and accept headers to handle JSON
        headers["Accept"] = "application/json"
        headers["User-Agent"] = f"python-freckle-client/{__version__}"
        headers["X-FreckleToken"] = self.access_token

        # construct the full URL without query parameters
        url = f"https://api.nokotime.com/v2/{uri_path}"
        response = self._make_request(
            http_method, url, headers, query_params, post_args
        )
        # return content if successful response with content,
        # otherwise return None
        return response

    # private

    @staticmethod
    def _make_request(
        http_method: str,
        url: str,
        headers: dict | None = None,
        query_params: dict | None = None,
        post_args: dict | None = None,
    ) -> list[dict] | None:
        results: list = []
        while url:
            # perform the HTTP requests, if possible uses OAuth authentication
            response = requests.request(
                http_method,
                url,
                params=query_params,
                headers=headers,
                data=json.dumps(post_args),
            )
            # if request failed (i.e. HTTP status code not 20x),
            # raise appropriate error
            response.raise_for_status()

            if not response.content:
                return None

            results.extend(response.json())
            next_link = response.links.get("next")

            if not next_link:
                break

            url = next_link["url"]

        return results
