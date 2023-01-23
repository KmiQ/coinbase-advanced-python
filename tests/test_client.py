import unittest
from unittest import mock

from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient
from tests.fixtures.fixtures import fixture_get_account_failure_response, fixture_get_account_success_response


class TestCoinbaseAdvancedTradeAPIClient(unittest.TestCase):

    def test_client_creation_should_pass(self):
        client = CoinbaseAdvancedTradeAPIClient(
            api_key='Jk31IAjyWQEG3BfP', secret_key='HUbLt2GsnPOTTkl0t2wkFWn4RrznDJRM')

        self.assertIsNotNone(client)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_account_success(self, mock_get):

        mock_resp = fixture_get_account_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        account = client.get_account('b044449a-38a3-5b8f-a506-4a65c9853222')

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn('https://coinbase.com/api/v3/brokerage/accounts/b044449a-38a3-5b8f-a506-4a65c9853222', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(account)

        self.assertEqual(account.name, "BTC Wallet")
        self.assertEqual(account.uuid, "b044449a-38a3-5b8f-a506-4a65c9853222")
        self.assertEqual(account.currency, "BTC")

        self.assertEqual(account.available_balance.currency, "BTC")
        self.assertEqual(account.available_balance.value, "0.2430140900000000")

        self.assertEqual(account.default, True)
        self.assertEqual(account.active, True)
        self.assertEqual(account.created_at, "2021-02-12T06:25:40.515Z")
        self.assertEqual(account.updated_at, "2022-12-26T19:27:01.554Z")

        self.assertEqual(account.type, "ACCOUNT_TYPE_CRYPTO")
        self.assertEqual(account.ready, False)

        self.assertDictEqual(account.hold, {
            "value": "0.0000000000000000",
            "currency": "BTC"
        })

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_account_failure(self, mock_get):

        mock_resp = fixture_get_account_failure_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        account = client.get_account('b044449a-38a3-5b8f-a506-4a65c9853222')

        # Check output

        self.assertIsNotNone(account)
        self.assertDictEqual(account.error, {
            "error": "unknown",
            "error_details": "Could not find users account information",
            "message": "Could not find users account information"
        })
