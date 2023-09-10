"""Base client for the Noko client.

Handle the HTTP request to the Noko API.
"""
import json

import requests

from noko_client import __version__


class BaseClient:
    """Base client for the Noko API."""

    def __init__(self, access_token: str):
        """Initialise an instance of the BaseClient.

        Args:
            access_token (str): The Noko access token to authenticate the requests.
        """
        self.access_token = access_token

    def fetch_json(
        self,
        uri_path: str,
        http_method: str,
        headers: dict | None = None,
        query_params: dict | None = None,
        post_args: dict | None = None,
    ) -> list[dict] | None:
        """Fetch some JSON from Noko.

        For example, fetch some entries like so:

            entries = self.fetch_json(
                'entries',
                query_params={
                    'search[from]': '2015-01-01',
                    'search[to]': '2015-01-31',
                    'search[projects]': [1423, 24545, ]),
                }
            )

        Args:
            uri_path (str): The Noko endpoint to make the request to.
            http_method (str): The HTTP verb to use in the request.
            headers (dict | None): Headers for the request. Defaults to None and constructs a simple header with a
                default user agent and the provided access token.
            query_params (dict): Dictionary of parameters to use in GET requests.
            post_args (dict): Dictionary of parameters to use in POST requests.
        """
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
        headers: dict,
        query_params: dict,
        post_args: dict,
    ) -> list[dict] | None:
        # Make the HTTP request to the Noko API and provide the response.
        results: list = []
        while url:
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

            resp_json = response.json()

            if isinstance(resp_json, list):
                results.extend(resp_json)
            else:
                results.append(resp_json)
            next_link = response.links.get("next")

            if not next_link:
                break

            url = next_link["url"]

        return results
