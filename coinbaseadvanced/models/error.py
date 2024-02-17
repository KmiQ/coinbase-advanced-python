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

    def __init__(self, error_dict: dict):
        self.error_dict = error_dict

    def __str__(self):
        return str(self.error_dict)

    @classmethod
    def not_ok_response(cls, response: requests.Response) -> 'CoinbaseAdvancedTradeAPIError':
        """
        Factory Method for Coinbase Advanced errors.
        """

        try:
            error_result = json.loads(response.text)
        except ValueError:
            error_result = {'reason': response.text}

        return cls(error_dict=error_result)
