"""
API Client for Coinbase Advanced Trade endpoints.
"""

from typing import List
from enum import Enum
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization

import jwt
import hmac
import hashlib
import time
import json
import requests
from coinbaseadvanced.models.common import UnixTime

from coinbaseadvanced.models.fees import TransactionsSummary
from coinbaseadvanced.models.portfolios import Portfolio, PortfolioType, PortfoliosPage
from coinbaseadvanced.models.products import BidAsksPage, ProductBook, ProductsPage, Product, CandlesPage, \
    TradesPage, ProductType, Granularity, GRANULARITY_MAP_IN_MINUTES
from coinbaseadvanced.models.accounts import AccountsPage, Account
from coinbaseadvanced.models.orders import OrderPlacementSource, OrdersPage, Order, \
    OrderBatchCancellation, FillsPage, Side, StopDirection, OrderType


class AuthSchema(Enum):
    """
    Enum representing authetication schema:
    https://docs.cloud.coinbase.com/advanced-trade-api/docs/auth#authentication-schemes
    """

    CLOUD_API_TRADING_KEYS = "CLOUD_API_TRADING_KEYS"
    LEGACY_API_KEYS = "LEGACY_API_KEYS"


class CoinbaseAdvancedTradeAPIClient(object):
    """
    API Client for Coinbase Advanced Trade endpoints.
    """

    def __init__(self,
                 api_key: str,
                 secret_key: str,
                 base_url: str = 'https://api.coinbase.com',
                 timeout: int = 10,
                 auth_schema: AuthSchema = AuthSchema.LEGACY_API_KEYS
                 ) -> None:
        self._base_url = base_url
        self._host = base_url[8:]
        self._api_key = api_key
        self._secret_key = secret_key
        self.timeout = timeout
        self._auth_schema = auth_schema

    @staticmethod
    def from_legacy_api_keys(api_key: str,
                             secret_key: str):
        """
        Factory method for legacy auth schema.
        API keys for this schema are generated via: https://www.coinbase.com/settings/api
        """
        return CoinbaseAdvancedTradeAPIClient(api_key=api_key, secret_key=secret_key)

    @staticmethod
    def from_cloud_api_keys(api_key_name: str,
                            private_key: str):
        """
        Factory method for cloud auth schema (recommended by Coinbase).
        API keys for this schema are generated via: https://cloud.coinbase.com/access/api
        """
        return CoinbaseAdvancedTradeAPIClient(api_key=api_key_name, secret_key=private_key,
                                              auth_schema=AuthSchema.CLOUD_API_TRADING_KEYS)

        # Accounts #

    # Accounts #

    def list_accounts(self, limit: int = 49, cursor: str = None) -> AccountsPage:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getaccounts

        Get a list of authenticated accounts for the current user.

        Args:
        - limit: A pagination limit with default of 49 and maximum of 250.
               If has_next is true, additional orders are available to be fetched
               with pagination and the cursor value in the response can be passed
               as cursor parameter in the subsequent request.

        - cursor: Cursor used for pagination. When provided, the response returns
                  responses after this cursor.

        """

        request_path = '/api/v3/brokerage/accounts'
        method = "GET"
        query_params = '?limit='+str(limit)

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        if cursor is not None:
            query_params = query_params + '&cursor='+cursor

        response = requests.get(self._base_url+request_path+query_params,
                                headers=headers,
                                timeout=self.timeout)

        page = AccountsPage.from_response(response)
        return page

    def list_accounts_all(self, limit: int = 250, cursor: str = None) -> AccountsPage:
        """
        Get all authenticated accounts for the current user

        To minimize the number of calls the default limit has been
        increased to the maximum coinbase allows.
        """

        full_page = AccountsPage([], has_next=True, cursor=cursor, size=0)

        # if there are more accounts to request, do so
        while full_page.has_next:
            page = self.list_accounts(limit, cursor=full_page.cursor)
            # update the statistics and transfer the cursor and has_next flag
            full_page.size += page.size
            full_page.cursor = page.cursor
            full_page.has_next = page.has_next
            # extend the accounts list
            full_page.accounts.extend(page.accounts)

        return full_page

    def get_account(self, account_id: str) -> Account:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getaccount

        Get a list of information about an account, given an account UUID.

        Args:
        - account_id: The account's UUID.

        """

        request_path = f"/api/v3/brokerage/accounts/{account_id}"
        method = "GET"

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(
            self._base_url+request_path, headers=headers, timeout=self.timeout)

        account = Account.from_response(response)
        return account

    # Orders #

    def create_buy_market_order(self,
                                client_order_id: str,
                                product_id: str,
                                quote_size: float) -> Order:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder

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

        return self.create_order(client_order_id, product_id, Side.BUY, order_configuration)

    def create_sell_market_order(self,
                                 client_order_id: str,
                                 product_id: str,
                                 base_size: float) -> Order:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder

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

        return self.create_order(client_order_id, product_id, Side.SELL, order_configuration)

    def create_limit_order(
            self,
            client_order_id: str,
            product_id: str,
            side: Side,
            limit_price: float,
            base_size: float,
            cancel_time: datetime = None,
            post_only: bool = None) -> Order:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder

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
            limit_order_configuration['end_time'] = cancel_time.strftime(
                "%Y-%m-%dT%H:%M:%SZ")
            order_configuration['limit_limit_gtd'] = limit_order_configuration
        else:
            order_configuration['limit_limit_gtc'] = limit_order_configuration

        return self.create_order(client_order_id, product_id, side, order_configuration)

    def create_stop_limit_order(
            self,
            client_order_id: str,
            product_id: str,
            side: Side,
            stop_price: float,
            stop_direction: StopDirection,
            limit_price: float,
            base_size: float,
            cancel_time: datetime = None) -> Order:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder

        Create a stop-limit order.

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
            stop_limit_order_configuration['end_time'] = cancel_time.strftime(
                "%Y-%m-%dT%H:%M:%SZ")
            order_configuration['stop_limit_stop_limit_gtd'] = stop_limit_order_configuration
        else:
            order_configuration['stop_limit_stop_limit_gtc'] = stop_limit_order_configuration

        return self.create_order(client_order_id, product_id, side, order_configuration)

    def create_order(self, client_order_id: str,
                     product_id: str,
                     side: Side,
                     order_configuration: dict) -> Order:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder

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

        headers = self._build_request_headers(method, request_path, json.dumps(payload)) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)
        response = requests.post(self._base_url+request_path,
                                 json=payload, headers=headers,
                                 timeout=self.timeout)

        order = Order.from_create_order_response(response)
        return order

    def cancel_orders(self, order_ids: list) -> OrderBatchCancellation:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_cancelorders

        Initiate cancel requests for one or more orders.

        Args:
        - order_ids: The IDs of orders cancel requests should be initiated for.
        """

        request_path = "/api/v3/brokerage/orders/batch_cancel/"
        method = "POST"

        payload = {
            'order_ids': order_ids,
        }

        headers = self._build_request_headers(method, request_path, json.dumps(payload)) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)
        response = requests.post(self._base_url+request_path,
                                 json=payload,
                                 headers=headers,
                                 timeout=self.timeout)

        cancellation_result = OrderBatchCancellation.from_response(response)
        return cancellation_result

    def list_orders(
            self,
            product_id: str = None,
            order_status: List[str] = None,
            limit: int = 999,
            start_date: datetime = None,
            end_date: datetime = None,
            user_native_currency: str = None,
            order_type: OrderType = None,
            order_side: Side = None,
            cursor: str = None,
            product_type: ProductType = None,
            order_placement_source: OrderPlacementSource = None,
    ) -> OrdersPage:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_gethistoricalorders

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
        - order_placement_source: String. Only orders matching this placement source are returned.
                                  Default is to return RETAIL_ADVANCED placement source.
        """

        request_path = '/api/v3/brokerage/orders/historical/batch'
        method = "GET"

        query_params = ''

        if product_id is not None:
            query_params = self._next_param(
                query_params) + 'product_id='+product_id

        if order_status is not None:
            query_params = self._next_param(
                query_params) + 'order_status='+','.join(order_status)

        if limit is not None:
            query_params = self._next_param(query_params) + 'limit='+str(limit)

        if start_date is not None:
            query_params = self._next_param(query_params) \
                + 'start_date=' + start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if end_date is not None:
            query_params = self._next_param(query_params) \
                + 'end_date=' + end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if user_native_currency is not None:
            query_params = self._next_param(query_params) \
                + 'user_native_currency=' + user_native_currency

        if order_type is not None:
            query_params = self._next_param(
                query_params) + 'order_type=' + order_type.value

        if order_side is not None:
            query_params = self._next_param(
                query_params) + 'order_side=' + order_side.value

        if cursor is not None:
            query_params = self._next_param(query_params) + 'cursor=' + cursor

        if product_type is not None:
            query_params = self._next_param(
                query_params) + 'product_type=' + product_type.value

        if order_placement_source is not None:
            query_params = self._next_param(
                query_params) + 'order_placement_source=' + order_placement_source.value

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(self._base_url+request_path+query_params,
                                headers=headers,
                                timeout=self.timeout)

        page = OrdersPage.from_response(response)
        return page

    def list_orders_all(
            self,
            product_id: str = None,
            order_status: List[str] = None,
            limit: int = 999,
            start_date: datetime = None,
            end_date: datetime = None,
            user_native_currency: str = None,
            order_type: OrderType = None,
            order_side: Side = None,
            cursor: str = None,
            product_type: ProductType = None) -> OrdersPage:

        orders_page = OrdersPage([], has_next=True, cursor=cursor, sequence=0)

        while orders_page.has_next:
            page = self.list_orders(
                product_id=product_id,
                order_status=order_status,
                limit=limit,
                start_date=start_date,
                end_date=end_date,
                user_native_currency=user_native_currency,
                order_type=order_type,
                order_side=order_side,
                cursor=orders_page.cursor,
                product_type=product_type)
            orders_page.has_next = page.has_next
            orders_page.cursor = page.cursor
            orders_page.sequence = page.sequence
            orders_page.orders.extend(page.orders)

        return orders_page

    def list_fills(self, order_id: str = None, product_id: str = None, start_date: datetime = None,
                   end_date: datetime = None, cursor: str = None, limit: int = 100) -> FillsPage:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getfills

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
            query_params = self._next_param(
                query_params) + 'order_id='+order_id

        if product_id is not None:
            query_params = self._next_param(
                query_params) + 'product_id='+product_id

        if limit is not None:
            query_params = self._next_param(query_params) + 'limit='+str(limit)

        if start_date is not None:
            query_params = self._next_param(query_params) \
                + 'start_date=' + start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if end_date is not None:
            query_params = self._next_param(query_params) \
                + 'end_date=' + end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if cursor is not None:
            query_params = self._next_param(query_params) + 'cursor=' + cursor

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(self._base_url+request_path+query_params,
                                headers=headers,
                                timeout=self.timeout)

        page = FillsPage.from_response(response)
        return page

    def list_fills_all(self, order_id: str = None, product_id: str = None, start_date: datetime = None,
                       end_date: datetime = None, cursor: str = None, limit: int = 100) -> FillsPage:

        fills = FillsPage(fills=[], cursor=cursor)

        while fills.cursor != '':
            response = self.list_fills(order_id=order_id, product_id=product_id, start_date=start_date,
                                       end_date=end_date, cursor=fills.cursor, limit=limit)
            fills.cursor = response.cursor
            fills.fills.extend(response.fills)

        return fills

    def get_order(self, order_id: str) -> Order:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_gethistoricalorder

        Get a single order by order ID.

        Args:
        - order_id: ID of order.
        """

        request_path = f"/api/v3/brokerage/orders/historical/{order_id}"
        method = "GET"

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(
            self._base_url+request_path, headers=headers, timeout=self.timeout)

        order = Order.from_get_order_response(response)
        return order

    # Products #

    def list_products(self,
                      limit: int = None,
                      offset: int = None,
                      product_type: ProductType = None) -> ProductsPage:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getproducts

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
            query_params = self._next_param(
                query_params) + 'offset='+str(offset)

        if product_type is not None:
            query_params = self._next_param(
                query_params) + 'product_type=' + product_type.value

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(self._base_url+request_path+query_params,
                                headers=headers,
                                timeout=self.timeout)

        page = ProductsPage.from_response(response)
        return page

    def get_product(self, product_id: str) -> Product:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getproduct

        Get information on a single product by product ID.

        Args:
        - product_id: The trading pair to get information for.
        """

        request_path = f"/api/v3/brokerage/products/{product_id}"
        method = "GET"

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(
            self._base_url+request_path, headers=headers, timeout=self.timeout)

        product = Product.from_response(response)
        return product

    def get_product_candles(
            self,
            product_id: str,
            start_date: datetime,
            end_date: datetime,
            granularity: Granularity) -> CandlesPage:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getcandles

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

        query_params = self._next_param(
            query_params) + 'start=' + str(int(start_date.timestamp()))
        query_params = self._next_param(
            query_params) + 'end=' + str(int(end_date.timestamp()))
        query_params = self._next_param(
            query_params) + 'granularity=' + granularity.value

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(self._base_url+request_path+query_params,
                                headers=headers,
                                timeout=self.timeout)

        product_candles = CandlesPage.from_response(response)
        return product_candles

    def get_product_candles_all(
        self,
            product_id: str,
            start_date: datetime,
            end_date: datetime,
            granularity: Granularity) -> CandlesPage:
        """
        Gets all requested product candles
        """

        # step_size: pre-calculate granularity entries in minutes.
        step_size_in_mins = timedelta(
            minutes=GRANULARITY_MAP_IN_MINUTES[granularity.value])

        # Max amount of candles that can be returned.
        # Coinbase API enforcement/error if you try to retrieve >= 300 below:
        # "start and end argument is invalid - number of candles requested should be less than 300."
        max_candles_amount = 299

        # request size of 299 (max allowed by coinbase)
        time_window_in_mins = step_size_in_mins * max_candles_amount

        product_candles = CandlesPage({})

        # run through from most recent to oldest to preserve time order in list

        end = end_date

        # while we still have not gotten all the requested candles loop until all are requested
        while end > start_date:
            # calculate start for the previous (older) 299 candles
            begin = end - time_window_in_mins

            # avoid asking for more than requested
            begin = max(begin, start_date)

            # get the next batch and extend the list
            batch_candles = self.get_product_candles(
                product_id, begin, end, granularity).candles
            product_candles.candles.extend(batch_candles)

            # offset end by one granularity to avoid duplicates
            end = begin - step_size_in_mins

        return product_candles

    def get_market_trades(
            self, product_id: str, limit: int) -> TradesPage:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getmarkettrades

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

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(self._base_url+request_path+query_params,
                                headers=headers,
                                timeout=self.timeout)

        trades_page = TradesPage.from_response(response)
        return trades_page

    def get_product_book(self, product_id: str, limit: int = None) -> ProductBook:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getproductbook

        Get a list of bids/asks for a single product.
        The amount of detail shown can be customized with the limit parameter.

        Args:
        - product_id: The trading pair.
        - limit: A pagination limit.
        """

        request_path = f"/api/v3/brokerage/product_book"
        method = "GET"

        query_params = ''
        if product_id is not None:
            query_params = self._next_param(
                query_params) + 'product_id='+product_id

        if limit is not None:
            query_params = self._next_param(query_params) + 'limit='+str(limit)

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(
            self._base_url+request_path+query_params, headers=headers, timeout=self.timeout)

        bid_asks_page = ProductBook.from_response(response)
        return bid_asks_page

    def get_best_bid_ask(self, product_ids: List[str] = None) -> BidAsksPage:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getbestbidask

        Get the best bid/ask for all products. A subset of all products can be returned instead by using the product_ids input.

        Args:
        - product_ids: Subset of all products to be returned instead.
        """

        request_path = f"/api/v3/brokerage/best_bid_ask"
        method = "GET"

        query_params = ''
        if product_ids is not None:
            query_params = self._next_param(
                query_params) + 'product_ids='+'&product_ids='.join(product_ids)

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(
            self._base_url+request_path+query_params, headers=headers, timeout=self.timeout)

        bid_asks_page = BidAsksPage.from_response(response)
        return bid_asks_page

    # Fees #

    def get_transactions_summary(self,
                                 start_date: datetime = None,
                                 end_date: datetime = None,
                                 user_native_currency: str = "USD",
                                 product_type: ProductType = None):
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_gettransactionsummary

        Get a summary of transactions with fee tiers, total volume, and fees.
        """

        request_path = '/api/v3/brokerage/transaction_summary'
        method = "GET"

        query_params = ''

        if start_date is not None:
            query_params = self._next_param(query_params) \
                + 'start_date=' + start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if end_date is not None:
            query_params = self._next_param(query_params) \
                + 'end_date=' + end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        if user_native_currency is not None:
            query_params = self._next_param(query_params) \
                + 'user_native_currency='+user_native_currency

        if product_type is not None:
            query_params = self._next_param(
                query_params) + 'product_type='+product_type.value

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(self._base_url+request_path+query_params,
                                headers=headers,
                                timeout=self.timeout)

        page = TransactionsSummary.from_response(response)
        return page

    # Portfolios

    def list_portfolios(self, portfolio_type: PortfolioType = None) -> PortfoliosPage:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getportfolios

        Get a list of all portfolios of a user.

        Args:
        - portfolio_type: Type of portfolios to return.

        """

        request_path = '/api/v3/brokerage/portfolios'
        method = "GET"
        query_params = ''

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        if portfolio_type is not None:
            query_params = '?portfolio_type='+portfolio_type.value

        response = requests.get(self._base_url+request_path+query_params,
                                headers=headers,
                                timeout=self.timeout)

        page = PortfoliosPage.from_response(response)
        return page

    def create_portfolio(self, name: str) -> Portfolio:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_createportfolio

        Create a portfolio.

        """

        request_path = "/api/v3/brokerage/portfolios"
        method = "POST"

        payload = {
            'name': name,
        }

        headers = self._build_request_headers(method, request_path, json.dumps(payload)) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)
        response = requests.post(self._base_url+request_path,
                                 json=payload, headers=headers,
                                 timeout=self.timeout)

        portfolio = Portfolio.from_response(response)
        return portfolio

    # Common #

    def get_unix_time(self) -> UnixTime:
        """
        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getunixtime

        Get the current time from the Coinbase Advanced API.

        """

        request_path = f"/api/v3/brokerage/time"
        method = "GET"

        headers = self._build_request_headers(method, request_path) if self._is_legacy_auth(
        ) else self._build_request_headers_for_cloud(method, self._host, request_path)

        response = requests.get(
            self._base_url+request_path, headers=headers, timeout=self.timeout)

        time = UnixTime.from_response(response)
        return time

    # Helpers Methods #

    ## Cloud Auth ##

    def _build_request_headers_for_cloud(self, method, host, request_path):
        uri = f"{method} {host}{request_path}"
        jwt_token = self._build_jwt("retail_rest_api_proxy", uri)

        return {
            "Authorization": f"Bearer {jwt_token}",
        }

    def _build_jwt(self, service, uri):
        private_key_bytes = self._secret_key.encode('utf-8')
        private_key = serialization.load_pem_private_key(
            private_key_bytes, password=None)
        jwt_payload = {
            'sub': self._api_key,
            'iss': "coinbase-cloud",
            'nbf': int(time.time()),
            'exp': int(time.time()) + 60,
            'aud': [service],
            'uri': uri,
        }
        jwt_token = jwt.encode(
            jwt_payload,
            private_key,
            algorithm='ES256',
            headers={'kid': self._api_key, 'nonce': str(int(time.time()))},
        )
        return jwt_token

    ## Legacy Auth ##

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

    def _is_legacy_auth(self) -> bool:
        return self._auth_schema == AuthSchema.LEGACY_API_KEYS

    ## Others ##

    def _next_param(self, query_params: str) -> str:
        return query_params + ('?' if query_params == '' else '&')
