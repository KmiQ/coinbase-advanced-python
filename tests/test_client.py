"""
CoinbaseAdvancedTradeAPIClient unit tests.
"""

import unittest
from unittest import mock
from datetime import datetime, timezone

from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient, Side, StopDirection, Granularity
from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError
from coinbaseadvanced.models.portfolios import PortfolioType
from tests.fixtures.fixtures import *


class TestCoinbaseAdvancedTradeAPIClient(unittest.TestCase):
    """
    Unit tests for CoinbaseAdvancedTradeAPIClient.
    """

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

        account = client.get_account('b04445c9853222')

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/accounts/b04445c9853222', args)

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

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_account_failure(self, mock_get):

        mock_resp = fixture_default_failure_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        try:
            client.get_account('b044449a-38a3-5b8f-a506-4a65c9853222')
        except CoinbaseAdvancedTradeAPIError as api_error:
            self.assertDictEqual(api_error.error_dict, {
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
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/accounts?limit=49', args)

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

        for account in page:
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

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_accounts_all_success(self, mock_get):

        mock_get.side_effect = [fixture_list_accounts_all_call_1_success_response(),
                                fixture_list_accounts_all_call_2_success_response()]

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        page = client.list_accounts_all()

        # Check output

        self.assertIsNotNone(page)

        accounts = page.accounts

        self.assertEqual(len(accounts), 98)
        self.assertEqual(page.has_next, False)
        self.assertIsNone(page.cursor)

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

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_accounts_failure(self, mock_get):

        mock_resp = fixture_default_failure_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        # Check output
        try:
            client.list_accounts()
        except CoinbaseAdvancedTradeAPIError as page_error:
            self.assertDictEqual(page_error.error_dict, {
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

        order_created = client.create_limit_order("lknalksdj89asdkl",
                                                  "ALGO-USD",
                                                  Side.BUY,
                                                  .19,
                                                  5)

        # Check input

        call_args = mock_post.call_args_list

        order_config = {'limit_limit_gtc': {
            'limit_price': '0.19', 'base_size': '5'}}

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders', args)

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
        self.assertEqual(order_created.order_id,
                         "07f1e718-8ea8-4ece-a2e1-3f00aad7f040")
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

        order_created = client.create_stop_limit_order(
            "mklansdu8wehr",
            "ALGO-USD",
            Side.BUY,
            .18,
            StopDirection.DOWN,
            .16,
            7,
            datetime(2023, 5, 9, 15))

        # Check input

        call_args = mock_post.call_args_list

        order_config = {'stop_limit_stop_limit_gtd': {'stop_price': '0.18',
                                                      'limit_price': '0.16',
                                                      'base_size': '7',
                                                      'stop_direction': 'STOP_DIRECTION_STOP_DOWN',
                                                      'end_time': '2023-05-09T15:00:00Z'}}

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders', args)

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
        self.assertEqual(order_created.order_id,
                         "1a88f3f2-1a02-4812-a227-a3d2c00e45ce")
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
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders', args)

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
        self.assertEqual(order_created.order_id,
                         "1f71a67f-6964-4a58-9438-411a5a6f22fc")
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

        order_created = client.create_sell_market_order(
            "njkasdh7", "ALGO-USD", 5)

        # Check input

        call_args = mock_post.call_args_list

        order_config = {'market_market_ioc': {'base_size': '5'}}

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders', args)

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
        self.assertEqual(order_created.order_id,
                         "95a50b31-7128-49ac-bba9-0e7200051a92")
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

        # Check output
        try:
            client.create_limit_order("nlksdbnfgjd8y9mn,m234",
                                      "ALGO-USD",
                                      Side.BUY,
                                      ".19",
                                      10000)
        except CoinbaseAdvancedTradeAPIError as order_error:
            self.assertDictEqual(order_error.error_dict, {
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
    def test_create_order_failure_no_funds(self, mock_post):

        mock_resp = fixture_order_failure_no_funds_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        # Check output
        order = client.create_limit_order("nlksdbnfgjd8y9mn,m234",
                                          "ALGO-USD",
                                          Side.BUY,
                                          ".19",
                                          10000)

        self.assertIsNotNone(order.order_error)

    @mock.patch("coinbaseadvanced.client.requests.post")
    def test_cancel_orders_success(self, mock_post):

        mock_resp = fixture_cancel_orders_success_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        cancellation_receipt = client.cancel_orders(
            ["order_id_1", "order_id_2"])

        # Check input

        call_args = mock_post.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders/batch_cancel/', args)

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

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_orders_success(self, mock_get):

        mock_resp = fixture_list_orders_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        orders_page = client.list_orders(start_date=datetime(2023, 1, 25),
                                         end_date=datetime(2023, 1, 30),
                                         limit=10)

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders/historical/batch?limit=10&start_date=2023-01-25T00:00:00Z&end_date=2023-01-30T00:00:00Z',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(orders_page)
        self.assertEqual(orders_page.has_next, True)
        self.assertIsNotNone(orders_page.cursor)

        orders = orders_page.orders
        self.assertEqual(len(orders), 10)

        for order in orders_page:
            self.assertIsNotNone(order)
            self.assertIsNotNone(order.order_id)
            self.assertIsNotNone(order.product_id)
            self.assertIsNotNone(order.status)
            self.assertIsNotNone(order.time_in_force)
            self.assertIsNotNone(order.created_time)
            self.assertIsNotNone(order.settled)
            self.assertIsNotNone(order.filled_size)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_orders_with_extra_unnamed_arg_success(self, mock_get):

        mock_resp = fixture_list_orders_with_extra_unnamed_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        orders_page = client.list_orders(start_date=datetime(2023, 1, 25),
                                         end_date=datetime(2023, 1, 30),
                                         limit=10)

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders/historical/batch?limit=10&start_date=2023-01-25T00:00:00Z&end_date=2023-01-30T00:00:00Z',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(orders_page)
        self.assertEqual(orders_page.has_next, True)
        self.assertIsNotNone(orders_page.cursor)

        orders = orders_page.orders
        self.assertEqual(len(orders), 10)

        first_order = orders[0]
        self.assertEqual(first_order.kwargs['extra_unnamed_arg'], "0")

        for order in orders:
            self.assertIsNotNone(order)
            self.assertIsNotNone(order.order_id)
            self.assertIsNotNone(order.product_id)
            self.assertIsNotNone(order.status)
            self.assertIsNotNone(order.time_in_force)
            self.assertIsNotNone(order.created_time)
            self.assertIsNotNone(order.settled)
            self.assertIsNotNone(order.filled_size)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_orders_all_success(self, mock_get):

        mock_get.side_effect = [
            fixture_list_orders_all_call_1_success_response(),
            fixture_list_orders_all_call_2_success_response()
        ]

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        orders_page = client.list_orders_all(start_date=datetime(2023, 1, 25),
                                             end_date=datetime(2023, 1, 30),
                                             limit=10)

        # Check output

        self.assertIsNotNone(orders_page)
        self.assertEqual(orders_page.has_next, False)
        self.assertIsNotNone(orders_page.cursor)

        orders = orders_page.orders
        self.assertEqual(len(orders), 20)

        for order in orders:
            self.assertIsNotNone(order)
            self.assertIsNotNone(order.order_id)
            self.assertIsNotNone(order.product_id)
            self.assertIsNotNone(order.status)
            self.assertIsNotNone(order.time_in_force)
            self.assertIsNotNone(order.created_time)
            self.assertIsNotNone(order.settled)
            self.assertIsNotNone(order.filled_size)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_fills_success(self, mock_get):

        mock_resp = fixture_list_fills_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        fills_page = client.list_fills(limit=5,
                                       start_date=datetime(2023, 1, 20),
                                       end_date=datetime(2023, 1, 30))

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders/historical/fills?limit=5&start_date=2023-01-20T00:00:00Z&end_date=2023-01-30T00:00:00Z',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(fills_page)
        self.assertIsNotNone(fills_page.cursor)

        fills = fills_page.fills
        self.assertEqual(len(fills), 5)

        for fill in fills_page:
            self.assertIsNotNone(fill)
            self.assertIsNotNone(fill.order_id)
            self.assertIsNotNone(fill.product_id)
            self.assertIsNotNone(fill.commission)
            self.assertIsNotNone(fill.entry_id)
            self.assertIsNotNone(fill.price)
            self.assertIsNotNone(fill.size)
            self.assertIsNotNone(fill.trade_id)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_fills_all_success(self, mock_get):

        mock_get.side_effect = [fixture_list_fills_all_call_1_success_response(),
                                fixture_list_fills_all_call_2_success_response()
                                ]

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        fills_page = client.list_fills_all(limit=5,
                                           start_date=datetime(2023, 1, 20),
                                           end_date=datetime(2023, 1, 30))

        # Check output

        self.assertIsNotNone(fills_page)
        self.assertIsNotNone(fills_page.cursor)

        fills = fills_page.fills
        self.assertEqual(len(fills), 10)

        for fill in fills:
            self.assertIsNotNone(fill)
            self.assertIsNotNone(fill.order_id)
            self.assertIsNotNone(fill.product_id)
            self.assertIsNotNone(fill.commission)
            self.assertIsNotNone(fill.entry_id)
            self.assertIsNotNone(fill.price)
            self.assertIsNotNone(fill.size)
            self.assertIsNotNone(fill.trade_id)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_order_success(self, mock_get):

        mock_resp = fixture_get_order_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        order = client.get_order('5fffa9e8-73db-4a2c-8b3f-08509203ac04')

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/orders/historical/5fffa9e8-73db-4a2c-8b3f-08509203ac04',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(order)
        self.assertIsNotNone(order.order_id)
        self.assertIsNotNone(order.product_id)
        self.assertIsNotNone(order.status)
        self.assertIsNotNone(order.time_in_force)
        self.assertIsNotNone(order.created_time)
        self.assertIsNotNone(order.settled)
        self.assertIsNotNone(order.filled_size)
        self.assertIsNotNone(order.side)
        self.assertIsNotNone(order.order_configuration)
        self.assertIsNotNone(order.order_type)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_products_success(self, mock_get):

        mock_resp = fixture_list_products_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        products_page = client.list_products(limit=5)

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/products?limit=5',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(products_page)

        products = products_page.products
        self.assertEqual(len(products), 5)

        for product in products_page:
            self.assertIsNotNone(product)
            self.assertIsNotNone(product.price)
            self.assertIsNotNone(product.product_id)
            self.assertIsNotNone(product.status)
            self.assertIsNotNone(product.base_name)
            self.assertIsNotNone(product.quote_name)
            self.assertIsNotNone(product.watched)
            self.assertIsNotNone(product.price_percentage_change_24h)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_product_success(self, mock_get):

        mock_resp = fixture_get_product_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        product = client.get_product('BTC-USD')

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/products/BTC-USD',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(product)
        self.assertIsNotNone(product.price)
        self.assertIsNotNone(product.product_id)
        self.assertIsNotNone(product.status)
        self.assertIsNotNone(product.base_name)
        self.assertIsNotNone(product.quote_name)
        self.assertIsNotNone(product.watched)
        self.assertIsNotNone(product.price_percentage_change_24h)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_product_candles(self, mock_get):

        mock_resp = fixture_get_product_candles_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        product_candles = client.get_product_candles(
            "ALGO-USD", start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2023, 1, 31, tzinfo=timezone.utc),
            granularity=Granularity.ONE_DAY)

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/products/ALGO-USD/candles?start=1672531200&end=1675123200&granularity=ONE_DAY',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(product_candles)

        candles = product_candles.candles
        self.assertEqual(len(candles), 30)

        for candle in product_candles:
            self.assertIsNotNone(candle)
            self.assertIsNotNone(candle.start)
            self.assertIsNotNone(candle.high)
            self.assertIsNotNone(candle.low)
            self.assertIsNotNone(candle.open)
            self.assertIsNotNone(candle.close)
            self.assertIsNotNone(candle.volume)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_product_candles_all(self, mock_get):

        mock_get.side_effect = [
            fixture_get_product_candles_all_call_1_success_response(),
            fixture_get_product_candles_all_call_2_success_response(),
            fixture_get_product_candles_all_call_3_success_response(),
        ]

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        product_candles = client.get_product_candles_all(
            "ALGO-USD", start_date=datetime(2021, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2023, 2, 20, tzinfo=timezone.utc),
            granularity=Granularity.ONE_DAY)

        # Check output

        self.assertIsNotNone(product_candles)

        candles = product_candles.candles
        self.assertEqual(len(candles), 781)

        previous_candle_start = float('inf')
        for candle in candles:
            self.assertIsNotNone(candle)

            self.assertIsNotNone(candle.start)
            self.assertLess(int(candle.start), previous_candle_start)
            previous_candle_start = int(candle.start)

            self.assertIsNotNone(candle.high)
            self.assertIsNotNone(candle.low)
            self.assertIsNotNone(candle.open)
            self.assertIsNotNone(candle.close)
            self.assertIsNotNone(candle.volume)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_best_bid_asks(self, mock_get):

        mock_resp = fixture_get_best_bid_asks_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        bid_asks_page = client.get_best_bid_ask(
            product_ids=["BTC-USD", "ETH-USD"])

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/best_bid_ask?product_ids=BTC-USD&product_ids=ETH-USD',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(bid_asks_page)

        pricebooks = bid_asks_page.pricebooks
        self.assertEqual(len(pricebooks), 2)

        for bidask in pricebooks:
            self.assertIsNotNone(bidask)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_product_book(self, mock_get):

        mock_resp = fixture_product_book_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        product_book = client.get_product_book(product_id="BTC-USD", limit=5)

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/product_book?product_id=BTC-USD&limit=5',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(product_book)

        pricebook = product_book.pricebook
        self.assertEqual(len(pricebook.asks), 5)
        self.assertEqual(len(pricebook.bids), 5)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_trades(self, mock_get):

        mock_resp = fixture_get_trades_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        trades_page = client.get_market_trades("BTC-USD", limit=100)

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/products/BTC-USD/ticker?limit=100',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(trades_page)

        for trade in trades_page:
            self.assertIsNotNone(trade)
            self.assertIsNotNone(trade.product_id)
            self.assertIsNotNone(trade.price)
            self.assertIsNotNone(trade.size)
            self.assertIsNotNone(trade.time)
            self.assertIsNotNone(trade.trade_id)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_transactions_summary(self, mock_get):

        mock_resp = fixture_get_transactions_summary_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        transactions_summary = client.get_transactions_summary(datetime(2023, 1, 1),
                                                               datetime(
                                                                   2023, 1, 31)
                                                               )

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/transaction_summary?start_date=2023-01-01T00:00:00Z&end_date=2023-01-31T00:00:00Z&user_native_currency=USD',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(transactions_summary)
        self.assertIsNotNone(transactions_summary.fee_tier)
        self.assertIsNotNone(transactions_summary.total_fees)
        self.assertIsNotNone(transactions_summary.total_volume)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_get_unix_time(self, mock_get):

        mock_resp = fixture_get_unix_time_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        unix_time = client.get_unix_time()

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/time',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(unix_time)
        self.assertIsNotNone(unix_time.iso)
        self.assertIsNotNone(unix_time.epochSeconds)
        self.assertIsNotNone(unix_time.epochMillis)

    @mock.patch("coinbaseadvanced.client.requests.get")
    def test_list_portfolios_success(self, mock_get):

        mock_resp = fixture_list_portfolios_success_response()
        mock_get.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='kjsldfk32234', secret_key='jlsjljsfd89y98y98shdfjksfd')

        portfolios_page = client.list_portfolios()

        # Check input

        call_args = mock_get.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/portfolios',
                args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(portfolios_page)

        portfolios = portfolios_page.portfolios
        self.assertEqual(len(portfolios), 1)

        for p in portfolios:
            self.assertIsNotNone(p)
            self.assertIsNotNone(p.uuid)
            self.assertIsNotNone(p.name)
            self.assertIsNotNone(p.type)
            self.assertEqual(p.deleted, False)

    @mock.patch("coinbaseadvanced.client.requests.post")
    def test_create_portfolio_success(self, mock_post):

        mock_resp = fixture_create_portfolio_success_response()
        mock_post.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        portfolio_created = client.create_portfolio("portf-test3")

        # Check input

        call_args = mock_post.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/portfolios', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

            json = kwargs['json']
            self.assertEqual(json['name'], "portf-test3")
        # Check output

        self.assertIsNotNone(portfolio_created)

        self.assertEqual(portfolio_created.name, "portf-test3")
        self.assertEqual(portfolio_created.uuid,
                         "354808f3-06df-42d7-87ec-488f34ff6f14")
        self.assertEqual(portfolio_created.type, PortfolioType.CONSUMER)
        self.assertEqual(portfolio_created.deleted, False)

    @mock.patch("coinbaseadvanced.client.requests.put")
    def test_edit_portfolio_success(self, mock_put):

        mock_resp = fixture_edit_portfolio_success_response()
        mock_put.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        portfolio_edited = client.edit_portfolio(
            "354808f3-06df-42d7-87ec-488f34ff6f14", "edited-portfolio-name")

        # Check input

        call_args = mock_put.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/portfolios/354808f3-06df-42d7-87ec-488f34ff6f14', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

            json = kwargs['json']
            self.assertEqual(json['name'], "edited-portfolio-name")
        # Check output

        self.assertIsNotNone(portfolio_edited)

        self.assertEqual(portfolio_edited.name, "edited-portfolio-name")
        self.assertEqual(portfolio_edited.uuid,
                         "354808f3-06df-42d7-87ec-488f34ff6f14")
        self.assertEqual(portfolio_edited.type, PortfolioType.CONSUMER)
        self.assertEqual(portfolio_edited.deleted, False)

    @mock.patch("coinbaseadvanced.client.requests.delete")
    def test_delete_portfolio_success(self, mock_delete):

        mock_resp = fixture_delete_portfolio_success_response()
        mock_delete.return_value = mock_resp

        client = CoinbaseAdvancedTradeAPIClient(
            api_key='lknalksdj89asdkl', secret_key='jlsjljsfd89y98y98shdfjksfd')

        empty_response = client.delete_portfolio(
            "354808f3-06df-42d7-87ec-488f34ff6f14")

        # Check input

        call_args = mock_delete.call_args_list

        for call in call_args:
            args, kwargs = call
            self.assertIn(
                'https://api.coinbase.com/api/v3/brokerage/portfolios/354808f3-06df-42d7-87ec-488f34ff6f14', args)

            headers = kwargs['headers']
            self.assertIn('accept', headers)
            self.assertIn('CB-ACCESS-KEY', headers)
            self.assertIn('CB-ACCESS-TIMESTAMP', headers)
            self.assertIn('CB-ACCESS-SIGN', headers)

        # Check output

        self.assertIsNotNone(empty_response)
        self.assertEqual(empty_response.success, True)
