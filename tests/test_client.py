import unittest
from unittest import mock
from datetime import datetime

from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient, SIDE, STOP_DIRECTION
from tests.fixtures.fixtures import fixture_default_failure_response, fixture_get_account_success_response, fixture_list_accounts_success_response, fixture_create_limit_order_success_response, fixture_create_stop_limit_order_success_response, fixture_create_buy_market_order_success_response, fixture_create_sell_market_order_success_response, fixture_default_order_failure_response, fixture_cancel_orders_success_response


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
            self.assertIn('https://api.coinbase.com/api/v3/brokerage/accounts/b044449a-38a3-5b8f-a506-4a65c9853222', args)

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

        mock_resp = fixture_default_failure_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        account = client.get_account('b044449a-38a3-5b8f-a506-4a65c9853222')

        # Check output

        self.assertIsNotNone(account)
        self.assertDictEqual(account.error, {
            "error": "unknown",
            "error_details": "some error details here",
            "message": "some additional message here"
        })

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_accounts_success(self, mock_get):

        mock_resp = fixture_list_accounts_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        page = client.list_accounts()

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn('https://api.coinbase.com/api/v3/brokerage/accounts?limit=49', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(page)

        accounts = page.accounts

        self.assertEqual(len(accounts), page.size)
        self.assertEqual(page.has_next, True)
        self.assertIsNotNone(page.cursor)

        for account in accounts:
            self.assertIsNotNone(account)
            self.assertIsNotNone(account.uuid)
            self.assertIsNotNone(account.name)
            self.assertIsNotNone(account.active)
            self.assertIsNotNone(account.available_balance)
            self.assertIsNotNone(account.created_at)
            self.assertIsNotNone(account.currency)
            self.assertIsNotNone(account.default)
            self.assertIsNotNone(account.hold)
            self.assertIsNotNone(account.ready)

            self.assertIsNone(account.error)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_accounts_failure(self, mock_get):

        mock_resp = fixture_default_failure_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        page = client.list_accounts()

        # Check output

        self.assertIsNotNone(page)
        self.assertDictEqual(page.error, {
            "error": "unknown",
            "error_details": "some error details here",
            "message": "some additional message here"
        })

    @mock.patch("coinbaseadvanced.client.requests.post")
    def test_create_limit_order_success(self, mock_post):

        mock_resp = fixture_create_limit_order_success_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        order_created = client.create_limit_order("lknalksdj89asdkl", "ALGO-USD", SIDE.BUY, ".19", 5)

        # Check input

        call_args = mock_post.call_args_list

        order_config = {'limit_limit_gtc': {'limit_price': '.19', 'base_size': '5'}}

        for call in call_args:
            args, kwargs = call
            self.assertIn('https://api.coinbase.com/api/v3/brokerage/orders', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

            json = kwargs['json']
            self.assertEqual(json['client_order_id'], "lknalksdj89asdkl")
            self.assertEqual(json['product_id'], "ALGO-USD")
            self.assertEqual(json['side'], "BUY")
            self.assertDictEqual(json['order_configuration'], order_config)

        # Check output

        self.assertIsNotNone(order_created)

        self.assertEqual(order_created.client_order_id, "lknalksdj89asdkl")
        self.assertEqual(order_created.order_id, "07f1e718-8ea8-4ece-a2e1-3f00aad7f040")
        self.assertEqual(order_created.product_id, "ALGO-USD")

        order_config_output = order_created.order_configuration
        self.assertIsNotNone(order_config_output.limit_limit_gtc)
        self.assertIsNone(order_config_output.limit_limit_gtd)
        self.assertIsNone(order_config_output.stop_limit_stop_limit_gtc)
        self.assertIsNone(order_config_output.stop_limit_stop_limit_gtd)
        self.assertIsNone(order_config_output.market_market_ioc)

    @mock.patch("coinbaseadvanced.client.requests.post")
    def test_create_stop_limit_order_success(self, mock_post):

        mock_resp = fixture_create_stop_limit_order_success_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        order_created = client.create_stop_limit_order("mklansdu8wehr", "ALGO-USD", SIDE.BUY, .18,
                                                       STOP_DIRECTION.DOWN, .16, 7, datetime(2023, 5, 9, 15))

        # Check input

        call_args = mock_post.call_args_list

        order_config = {'stop_limit_stop_limit_gtd': {'stop_price': '0.18', 'limit_price': '0.16',
                                                      'base_size': '7', 'stop_direction': 'STOP_DIRECTION_STOP_DOWN', 'end_time': '2023-05-09T15:00:00Z'}}

        for call in call_args:
            args, kwargs = call
            self.assertIn('https://api.coinbase.com/api/v3/brokerage/orders', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

            json = kwargs['json']
            self.assertEqual(json['client_order_id'], "mklansdu8wehr")
            self.assertEqual(json['product_id'], "ALGO-USD")
            self.assertEqual(json['side'], "BUY")
            self.assertDictEqual(json['order_configuration'], order_config)

        # Check output

        self.assertIsNotNone(order_created)

        self.assertEqual(order_created.client_order_id, "mklansdu8wehr")
        self.assertEqual(order_created.order_id, "1a88f3f2-1a02-4812-a227-a3d2c00e45ce")
        self.assertEqual(order_created.product_id, "ALGO-USD")
        self.assertEqual(order_created.side, 'BUY')

        order_config_output = order_created.order_configuration
        self.assertIsNone(order_config_output.limit_limit_gtc)
        self.assertIsNone(order_config_output.limit_limit_gtd)
        self.assertIsNone(order_config_output.stop_limit_stop_limit_gtc)
        self.assertIsNotNone(order_config_output.stop_limit_stop_limit_gtd)
        self.assertIsNone(order_config_output.market_market_ioc)

    @mock.patch("coinbaseadvanced.client.requests.post")
    def test_create_buy_market_order_success(self, mock_post):

        mock_resp = fixture_create_buy_market_order_success_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        order_created = client.create_buy_market_order("asdasd", "ALGO-USD", 1)

        # Check input

        call_args = mock_post.call_args_list

        order_config = {'market_market_ioc': {'quote_size': '1'}}

        for call in call_args:
            args, kwargs = call
            self.assertIn('https://api.coinbase.com/api/v3/brokerage/orders', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

            json = kwargs['json']
            self.assertEqual(json['client_order_id'], "asdasd")
            self.assertEqual(json['product_id'], "ALGO-USD")
            self.assertEqual(json['side'], "BUY")
            self.assertDictEqual(json['order_configuration'], order_config)

        # Check output

        self.assertIsNotNone(order_created)

        self.assertEqual(order_created.client_order_id, "asdasd")
        self.assertEqual(order_created.order_id, "1f71a67f-6964-4a58-9438-411a5a6f22fc")
        self.assertEqual(order_created.product_id, "ALGO-USD")
        self.assertEqual(order_created.side, 'BUY')

        order_config_output = order_created.order_configuration
        self.assertIsNone(order_config_output.limit_limit_gtc)
        self.assertIsNone(order_config_output.limit_limit_gtd)
        self.assertIsNone(order_config_output.stop_limit_stop_limit_gtc)
        self.assertIsNone(order_config_output.stop_limit_stop_limit_gtd)
        self.assertIsNotNone(order_config_output.market_market_ioc)

    @mock.patch("coinbaseadvanced.client.requests.post")
    def test_create_sell_market_order_success(self, mock_post):

        mock_resp = fixture_create_sell_market_order_success_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        order_created = client.create_sell_market_order("njkasdh7", "ALGO-USD", 5)

        # Check input

        call_args = mock_post.call_args_list

        order_config = {'market_market_ioc': {'base_size': '5'}}

        for call in call_args:
            args, kwargs = call
            self.assertIn('https://api.coinbase.com/api/v3/brokerage/orders', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

            json = kwargs['json']
            self.assertEqual(json['client_order_id'], "njkasdh7")
            self.assertEqual(json['product_id'], "ALGO-USD")
            self.assertEqual(json['side'], "SELL")
            self.assertDictEqual(json['order_configuration'], order_config)

        # Check output

        self.assertIsNotNone(order_created)

        self.assertEqual(order_created.client_order_id, "njkasdh7")
        self.assertEqual(order_created.order_id, "95a50b31-7128-49ac-bba9-0e7200051a92")
        self.assertEqual(order_created.product_id, "ALGO-USD")
        self.assertEqual(order_created.side, 'SELL')

        order_config_output = order_created.order_configuration
        self.assertIsNone(order_config_output.limit_limit_gtc)
        self.assertIsNone(order_config_output.limit_limit_gtd)
        self.assertIsNone(order_config_output.stop_limit_stop_limit_gtc)
        self.assertIsNone(order_config_output.stop_limit_stop_limit_gtd)
        self.assertIsNotNone(order_config_output.market_market_ioc)

    @mock.patch("coinbaseadvanced.client.requests.post")
    def test_create_order_failure(self, mock_post):

        mock_resp = fixture_default_order_failure_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        order_created = client.create_limit_order("nlksdbnfgjd8y9mn,m234", "ALGO-USD", SIDE.BUY, ".19", 10000)

        # Check output

        self.assertIsNotNone(order_created)
        self.assertDictEqual(order_created.error, {
            "success": False,
            "failure_reason": "UNKNOWN_FAILURE_REASON",
            "order_id": "",
            "error_response": {
                "error": "INSUFFICIENT_FUND",
                "message": "Insufficient balance in source account",
                "error_details": "",
                "preview_failure_reason": "PREVIEW_INSUFFICIENT_FUND"
            },
            "order_configuration": {
                "limit_limit_gtc": {
                    "base_size": "10000",
                    "limit_price": ".19",
                    "post_only": False
                }
            }
        })

    @mock.patch("coinbaseadvanced.client.requests.post")
    def test_cancel_orders_success(self, mock_post):

        mock_resp = fixture_cancel_orders_success_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        cancellation_receipt = client.cancel_orders(["order_id_1", "order_id_2"])

        # Check input

        call_args = mock_post.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn('https://api.coinbase.com/api/v3/brokerage/orders/batch_cancel/', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

            json = kwargs['json']
            self.assertIn('order_id_1', json['order_ids'])
            self.assertIn('order_id_2', json['order_ids'])

        # Check output

        self.assertIsNotNone(cancellation_receipt)

        self.assertEqual(len(cancellation_receipt.results), 2)
