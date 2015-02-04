Freckle Client
==============

A super simple Freckle API client implementation.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install python-freckle-client

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/python-freckle-client.git#egg=freckle_client


Usage
-----

Just import the client, create an instance and call the ``fetch_json`` method: 

.. code-block:: python

    from freckle_client.client import FreckleClient

    client = FreckleClient('account_name', 'api_token')
    entries = self.fetch_json(
        'entries',
        query_params={
            'per_page': 1000,
            'search[from]': '2015-01-01',
            'search[to]': '2015-01-31',
            'search[projects]': [1423, 24545, ]),
        }
    )

Or if you want to use the V2 API:

.. code-block:: python

    from freckle_client.client import FreckleClientV2

    client = FreckleClientV2('access_token')
    entries = self.fetch_json(
        'entries',
        query_params={
            'per_page': 1000,
            'search[from]': '2015-01-01',
            'search[to]': '2015-01-31',
            'search[projects]': [1423, 24545, ]),
        }
    )


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 freckle-client
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
