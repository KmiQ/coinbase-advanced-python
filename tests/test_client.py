import unittest
from unittest import mock

from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient


class TestCoinbaseAdvancedTradeAPIClient(unittest.TestCase):
    def test_client_creation_should_pass(self):
        client = CoinbaseAdvancedTradeAPIClient(
            api_key='Jk31IAjyWQEG3BfP', secret_key='HUbLt2GsnPOTTkl0t2wkFWn4RrznDJRM')

        self.assertIsNotNone(client)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_account(self, mock_get):
        client = CoinbaseAdvancedTradeAPIClient(
            api_key='hOOnWpN0x2zsu12i', secret_key='86s3z4DLYrFCw4QonF54u4CdirrbBSnw')

        account = client.get_account('b044449a-38a3-5b8f-a506-4a65c9853222')

        self.assertIsNotNone(account)
