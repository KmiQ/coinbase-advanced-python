"""
Object models for order related endpoints args and response.
"""

from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError

import requests


class UnixTime:
    """
    Unix time in different formats.
    """

    iso: str
    epochSeconds: str
    epochMillis: str

    def __init__(self,
                 iso: str,
                 epochSeconds: str,
                 epochMillis: str,
                 **kwargs
                 ) -> None:

        self.iso = iso
        self.epochSeconds = epochSeconds
        self.epochMillis = epochMillis

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'UnixTime':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result)

    def __iter__(self):
        return self.fills.__iter__()
