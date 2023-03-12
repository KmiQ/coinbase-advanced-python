"""
Encapsulating error types.
"""

import json
import requests


class CoinbaseAdvancedTradeAPIError(Exception):
    """
    Class CoinbaseAdvancedTradeAPIError is derived from super class Exception
    and represent the default generic error when endpoint request fail.
    """

    def __init__(self, error: dict):
        self.error = error

    @classmethod
    def not_ok_response(cls, response: requests.Response) -> 'CoinbaseAdvancedTradeAPIError':
        """
        Factory Method for Coinbase Advanced errors.
        """

        try:
            error_result = json.loads(response.text)
        except ValueError as error:
            error_result = {'reason': response.text}

        return cls(error=error_result)
