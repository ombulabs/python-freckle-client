"""Exceptions for the freckle_client app."""


class FreckleClientException(Exception):
    """
    Is raised when the Freckle API response is not status 200.

    You can access ``ex.response`` to inspect the response (an instance from
    the Requests module).

    """

    def __init__(self, message: str, response: str):
        super().__init__(message)
        self.response = response
