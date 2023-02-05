from typing import List
from datetime import datetime

import hmac
import hashlib
import time
import json
import requests

from coinbaseadvanced.models.fees import TransactionsSummary
from coinbaseadvanced.models.products import ProductsPage, Product, CandlesPage, TradesPage, PRODUCT_TYPE, GRANULARITY
from coinbaseadvanced.models.accounts import AccountsPage, Account
from coinbaseadvanced.models.orders import OrdersPage, Order, OrderBatchCancellation, FillsPage, SIDE, STOP_DIRECTION, ORDER_TYPE


class CoinbaseAdvancedTradeAPIClient(object):
    def __init__(self, api_key: str, secret_key: str, base_url: str = 'https://api.coinbase.com') -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._secret_key = secret_key

    # Accounts #

    def list_accounts(self, limit: int = 49, cursor: str = None) -> AccountsPage:
        """
        Get a list of authenticated accounts for the current user.

        Args:
        - limit: A pagination limit with default of 49 and maximum of 250.
               If has_next is true, additional orders are available to be fetched
               with pagination and the cursor value in the response can be passed
               as cursor parameter in the subsequent request.

        - cursor: Cursor used for pagination. When provided, the response returns responses after this cursor.

        """

        request_path = '/api/v3/brokerage/accounts'
        method = "GET"
        query_params = '?limit='+str(limit)

        if cursor is not None:
            query_params = query_params + '&cursor='+cursor

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path+query_params, headers=headers, timeout=10)

        page = AccountsPage.from_response(response)
        return page

    def get_account(self, account_id: str) -> Account:
        """
        Get a list of information about an account, given an account UUID.

        Args:
        - account_id: The account's UUID.

        """

        request_path = f"/api/v3/brokerage/accounts/{account_id}"
        method = "GET"

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path, headers=headers, timeout=10)

        account = Account.from_response(response)
        return account

    # Orders #

    def create_buy_market_order(self, client_order_id: str, product_id: str, quote_size: float) -> Order:
        """
        Create a buy type market order.

        Args:
        - client_order_id: Client set unique uuid for this order
        - product_id: The product this order was created for e.g. 'BTC-USD'
        - quote_size: Amount of quote currency to spend on order. Required for BUY orders.
        """

        order_configuration = {
            "market_market_ioc": {
                "quote_size": str(quote_size),
            }
        }

        return self.create_order(client_order_id, product_id, SIDE.BUY, order_configuration)

    def create_sell_market_order(self, client_order_id: str, product_id: str, base_size: float) -> Order:
        """
        Create a sell type market order.

        Args:
        - client_order_id: Client set unique uuid for this order
        - product_id: The product this order was created for e.g. 'BTC-USD'
        - base_size: Amount of base currency to spend on order. Required for SELL orders.
        """

        order_configuration = {
            "market_market_ioc": {
                "base_size": str(base_size),
            }
        }

        return self.create_order(client_order_id, product_id, SIDE.SELL, order_configuration)

    def create_limit_order(
            self, client_order_id: str, product_id: str, side: SIDE, limit_price: float, base_size: float,
            cancel_time: datetime = None, post_only: bool = None) -> Order:
        """
        Create a limit order.

        Args:
        - client_order_id: Client set unique uuid for this order
        - product_id: The product this order was created for e.g. 'BTC-USD'
        - side: Possible values: [UNKNOWN_ORDER_SIDE, BUY, SELL]
        - limit_price: Ceiling price for which the order should get filled
        - base_size: Amount of base currency to spend on order
        - cancel_time: Time at which the order should be cancelled if it's not filled.
        - post_only: Post only limit order
        """

        order_configuration = {}

        limit_order_configuration = {
            "limit_price": str(limit_price),
            "base_size": str(base_size),
        }

        if post_only is not None:
            limit_order_configuration['post_only'] = post_only

        if cancel_time is not None:
            limit_order_configuration['end_time'] = cancel_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            order_configuration['limit_limit_gtd'] = limit_order_configuration
        else:
            order_configuration['limit_limit_gtc'] = limit_order_configuration

        return self.create_order(client_order_id, product_id, side, order_configuration)

    def create_stop_limit_order(
            self, client_order_id: str, product_id: str, side: SIDE, stop_price: float, stop_direction: STOP_DIRECTION,
            limit_price: float, base_size: float, cancel_time: datetime = None) -> Order:
        """
        Create a limit order.

        Args:
        - client_order_id: Client set unique uuid for this order
        - product_id: The product this order was created for e.g. 'BTC-USD'
        - side: Possible values: [UNKNOWN_ORDER_SIDE, BUY, SELL]
        - stop_price: Price at which the order should trigger
            - if stop direction is Up, then the order will trigger when
              the last trade price goes above this, otherwise order will trigger
              when last trade price goes below this price.
        - stop_direction: Possible values:
            - [UNKNOWN_STOP_DIRECTION, STOP_DIRECTION_STOP_UP, STOP_DIRECTION_STOP_DOWN]
        - limit_price: Ceiling price for which the order should get filled
        - base_size: Amount of base currency to spend on order
        - cancel_time: Time at which the order should be cancelled if it's not filled.
        - post_only: Post only limit order
        """

        order_configuration = {}

        stop_limit_order_configuration = {
            "stop_price": str(stop_price),
            "limit_price": str(limit_price),
            "base_size": str(base_size),
            "stop_direction": stop_direction.value,
        }

        if cancel_time is not None:
            stop_limit_order_configuration['end_time'] = cancel_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            order_configuration['stop_limit_stop_limit_gtd'] = stop_limit_order_configuration
        else:
            order_configuration['stop_limit_stop_limit_gtc'] = stop_limit_order_configuration

        return self.create_order(client_order_id, product_id, side, order_configuration)

    def create_order(self, client_order_id: str,
                     product_id: str,
                     side: SIDE,
                     order_configuration: dict) -> Order:
        """
        Create an order with a specified product_id (asset-pair), side (buy/sell), etc.

        Maximum Open Orders Per Product:
        The maximum number of OPEN orders you can have for a given product_id is 500.
        If you have 500 open orders for a product_id at submission, new orders placed
        for that product enter a failed state immediately.
        """

        request_path = "/api/v3/brokerage/orders"
        method = "POST"

        payload = {
            'client_order_id': client_order_id,
            'product_id': product_id,
            'side': side.value,
            'order_configuration': order_configuration
        }

        headers = self._build_request_headers(method, request_path, json.dumps(payload))
        response = requests.post(self._base_url+request_path, json=payload, headers=headers, timeout=10)

        order = Order.from_create_order_response(response)
        return order

    def cancel_orders(self, order_ids: list) -> OrderBatchCancellation:
        """
        Initiate cancel requests for one or more orders.

        Args:
        - order_ids: The IDs of orders cancel requests should be initiated for.
        """

        request_path = "/api/v3/brokerage/orders/batch_cancel/"
        method = "POST"

        payload = {
            'order_ids': order_ids,
        }

        headers = self._build_request_headers(method, request_path, json.dumps(payload))
        response = requests.post(self._base_url+request_path, json=payload, headers=headers, timeout=10)

        cancellation_result = OrderBatchCancellation.from_response(response)
        return cancellation_result

    def list_orders(
            self, product_id: str = None, order_status: List[str] = None, limit: int = 999, start_date: datetime = None,
            end_date: datetime = None, user_native_currency: str = None, order_type: ORDER_TYPE = None, order_side: SIDE = None,
            cursor: str = None, product_type: PRODUCT_TYPE = None) -> OrdersPage:
        """
        Get a list of orders filtered by optional query parameters (product_id, order_status, etc).

        Args:
        - product_id: Optional string of the product ID.
                      Defaults to null, or fetch for all products.
        - order_status: A list of order statuses.
        - limit: A pagination limit with no default set.
                 If has_next is true, additional orders are available
                 to be fetched with pagination; also the cursor value
                 in the response can be passed as cursor parameter in
                 the subsequent request.
        - start_date: Start date to fetch orders from, inclusive.
        - end_date: An optional end date for the query window, exclusive.
                    If provided only orders with creation time before
                    this date will be returned.
        - user_native_currency: String of the users native currency. Default is USD.
        - order_type: Type of orders to return. Default is to return all order types.
            - MARKET: A market order
            - LIMIT: A limit order
            - STOP: A stop order is an order that becomes a market order when triggered
            - STOP_LIMIT: A stop order is a limit order that doesn't go on the book until
                          it hits the stop price.
        - order_side: Only orders matching this side are returned. Default is to return all sides.
        - cursor: Cursor used for pagination.
                  When provided, the response returns responses after this cursor.
        - product_type: Only orders matching this product type are returned.
                        Default is to return all product types.
        """

        request_path = '/api/v3/brokerage/orders/historical/batch'
        method = "GET"

        query_params = ''

        if product_id is not None:
            query_params = self._next_param(query_params) + 'product_id='+product_id

        if order_status is not None:
            query_params = self._next_param(query_params) + 'order_status='+','.join(order_status)

        if limit is not None:
            query_params = self._next_param(query_params) + 'limit='+str(limit)

        if start_date is not None:
            query_params = self._next_param(query_params) + 'start_date=' + start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if end_date is not None:
            query_params = self._next_param(query_params) + 'end_date=' + end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if user_native_currency is not None:
            query_params = self._next_param(query_params) + 'user_native_currency=' + user_native_currency

        if order_type is not None:
            query_params = self._next_param(query_params) + 'order_type=' + order_type.value

        if order_side is not None:
            query_params = self._next_param(query_params) + 'order_side=' + order_side.value

        if cursor is not None:
            query_params = self._next_param(query_params) + 'cursor=' + cursor

        if product_type is not None:
            query_params = self._next_param(query_params) + 'product_type=' + product_type.value

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path+query_params, headers=headers, timeout=10)

        page = OrdersPage.from_response(response)
        return page

    def list_fills(self, order_id: str = None, product_id: str = None, start_date: datetime = None,
                   end_date: datetime = None, cursor: str = None, limit: int = 100) -> FillsPage:
        """
        Get a list of fills filtered by optional query parameters (product_id, order_id, etc).

        Args:
        - order_id: ID of order.
        - product_id: Optional string of the product ID.
                      Defaults to null, or fetch for all products.
        - start_date: Start date to fetch orders from, inclusive.
        - end_date: An optional end date for the query window, exclusive.
                    If provided only orders with creation time before
                    this date will be returned.
        - cursor: Cursor used for pagination.
                  When provided, the response returns responses after this cursor.
                - limit: A pagination limit with no default set.
                 If has_next is true, additional orders are available
                 to be fetched with pagination; also the cursor value
                 in the response can be passed as cursor parameter in
                 the subsequent request.
        - limit: A pagination limit with no default set.
                 If has_next is true, additional orders are available
                 to be fetched with pagination; also the cursor value
                 in the response can be passed as cursor parameter in
                 the subsequent request.
        """

        request_path = '/api/v3/brokerage/orders/historical/fills'
        method = "GET"

        query_params = ''

        if order_id is not None:
            query_params = self._next_param(query_params) + 'order_id='+order_id

        if product_id is not None:
            query_params = self._next_param(query_params) + 'product_id='+product_id

        if limit is not None:
            query_params = self._next_param(query_params) + 'limit='+str(limit)

        if start_date is not None:
            query_params = self._next_param(query_params) + 'start_date=' + start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if end_date is not None:
            query_params = self._next_param(query_params) + 'end_date=' + end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if cursor is not None:
            query_params = self._next_param(query_params) + 'cursor=' + cursor

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path+query_params, headers=headers, timeout=10)

        page = FillsPage.from_response(response)
        return page

    def get_order(self, order_id: str) -> Order:
        """
        Get a single order by order ID.

        Args:
        - order_id: ID of order.
        """

        request_path = f"/api/v3/brokerage/orders/historical/{order_id}"
        method = "GET"

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path, headers=headers, timeout=10)

        order = Order.from_get_order_response(response)
        return order

    # Products #

    def list_products(self,
                      limit: int = None,
                      offset: int = None,
                      product_type: PRODUCT_TYPE = None) -> ProductsPage:
        """
        Get a list of the available currency pairs for trading.

         Args:
        - limit: A limit describing how many products to return.
        - offset: Number of products to offset before returning.
        - product_type: Type of products to return.
        """

        request_path = '/api/v3/brokerage/products'
        method = "GET"

        query_params = ''

        if limit is not None:
            query_params = self._next_param(query_params) + 'limit='+str(limit)

        if offset is not None:
            query_params = self._next_param(query_params) + 'offset='+str(offset)

        if product_type is not None:
            query_params = self._next_param(query_params) + 'product_type=' + product_type.value

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path+query_params, headers=headers, timeout=10)

        page = ProductsPage.from_response(response)
        return page

    def get_product(self, product_id: str) -> Product:
        """
        Get information on a single product by product ID.

        Args:
        - product_id: The trading pair to get information for.
        """

        request_path = f"/api/v3/brokerage/products/{product_id}"
        method = "GET"

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path, headers=headers, timeout=10)

        product = Product.from_response(response)
        return product

    def get_product_candles(
            self,
            product_id: str,
            start_date: datetime,
            end_date: datetime,
            granularity: GRANULARITY) -> CandlesPage:
        """
        Get rates for a single product by product ID, grouped in buckets.

        Args:
        - product_id: The trading pair.
        - start: Timestamp for starting range of aggregations, in UNIX time.
        - end: Timestamp for ending range of aggregations, in UNIX time.
        - granularity: The time slice value for each candle.
        """

        request_path = f"/api/v3/brokerage/products/{product_id}/candles"
        method = "GET"

        query_params = ''

        query_params = self._next_param(query_params) + 'start=' + str(int(start_date.timestamp()))
        query_params = self._next_param(query_params) + 'end=' + str(int(end_date.timestamp()))
        query_params = self._next_param(query_params) + 'granularity=' + granularity.value

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path+query_params, headers=headers, timeout=10)

        product_candles = CandlesPage.from_response(response)
        return product_candles

    def get_market_trades(
            self, product_id: str, limit: int) -> TradesPage:
        """
        Get snapshot information, by product ID, about the last trades (ticks),
        best bid/ask, and 24h volume.

        Args:
        - product_id: The trading pair, i.e., 'BTC-USD'.
        - limit: Number of trades to return.
        """

        request_path = f"/api/v3/brokerage/products/{product_id}/ticker"
        method = "GET"

        query_params = ''

        query_params = self._next_param(query_params) + 'limit=' + str(limit)

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path+query_params, headers=headers, timeout=10)

        trades_page = TradesPage.from_response(response)
        return trades_page

    # Fees #

    def get_transactions_summary(self,
                                 start_date: datetime = None,
                                 end_date: datetime = None,
                                 user_native_currency: str = "USD",
                                 product_type: PRODUCT_TYPE = None):
        """
        Get a summary of transactions with fee tiers, total volume, and fees.
        """

        request_path = '/api/v3/brokerage/transaction_summary'
        method = "GET"

        query_params = ''

        if start_date is not None:
            query_params = self._next_param(query_params) + 'start_date=' + start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if end_date is not None:
            query_params = self._next_param(query_params) + 'end_date=' + end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if user_native_currency is not None:
            query_params = self._next_param(query_params) + 'user_native_currency='+user_native_currency

        if product_type is not None:
            query_params = self._next_param(query_params) + 'product_type='+product_type.value

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path+query_params, headers=headers, timeout=10)

        page = TransactionsSummary.from_response(response)
        return page

    # Helpers #

    def _build_request_headers(self, method, request_path, body=''):
        timestamp = str(int(time.time()))

        message = timestamp+method+request_path+body
        signature = self._create_signature(message)

        return {
            "accept": "application/json",
            'CB-ACCESS-KEY': self._api_key,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-SIGN': signature,
        }

    def _create_signature(self, message):
        signature = hmac.new(
            self._secret_key.encode('utf-8'),
            message.encode('utf-8'),
            digestmod=hashlib.sha256).digest().hex()

        return signature

    def _next_param(self, query_params: str) -> str:
        return query_params + ('?' if query_params == '' else '&')
