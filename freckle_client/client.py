"""
Freckle client implementation.

Idea stolen from here:
https://github.com/sarumont/py-trello/blob/master/trello/__init__.py#L108

"""
import json

import requests

from . import __version__
from . import exceptions


class FreckleClient(object):
    """Simple client implementation to fetch json data from the v1 API."""
    def __init__(self, account_name, api_token):
        """
        Creates a ``FreckleClient`` instance.

        :account_name: Your Freckle account name.
        :api_token: Your Freckle API token.

        """
        self.account_name = account_name
        self.api_token = api_token

    def fetch_json(self, uri_path, http_method='GET', headers=None,
                   query_params=None, post_args=None):
        """
        Fetch some JSON from Letsfreckle.

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
        headers['Accept'] = 'application/json'
        query_params['token'] = self.api_token

        # construct the full URL without query parameters
        url = 'https://{0}.letsfreckle.com/api/{1}.json'.format(
            self.account_name, uri_path)

        # perform the HTTP requests, if possible uses OAuth authentication
        response = requests.request(
            http_method, url, params=query_params, headers=headers,
            data=json.dumps(post_args))

        if response.status_code != 200:
            raise exceptions.FreckleClientException(
                "Freckle API Response is not 200", response.text)

        return json.loads(response.content)


class FreckleClientV2(object):
    """Simple client implementation to fetch json data from the v2 API."""
    def __init__(self, access_token):
        """
        Creates a ``FreckleClient`` instance.

        :account_name: Your Freckle account name.
        :api_token: Your Freckle API token.

        """
        self.access_token = access_token

    def fetch_json(self, uri_path, http_method='GET', headers=None,
                   query_params=None, post_args=None):
        """
        Fetch some JSON from Letsfreckle.

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
        headers['Accept'] = 'application/json'
        headers['User-Agent'] = "python-freckle-client/{}".format(__version__)
        headers['X-FreckleToken'] = self.access_token

        # construct the full URL without query parameters
        url = 'https://api.letsfreckle.com/v2/{0}'.format(uri_path)

        # perform the HTTP requests, if possible uses OAuth authentication
        response = requests.request(
            http_method, url, params=query_params, headers=headers,
            data=json.dumps(post_args))

        # if request failed (i.e. HTTP status code not 20x), raise appropriate
        # error
        response.raise_for_status()

        return json.loads(response.content.decode('utf-8'))
