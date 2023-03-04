"""
Object models for products related endpoints args and response.
"""

from uuid import UUID
from datetime import datetime
from typing import List
from enum import Enum

from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError

import json
import requests


class ProductType(Enum):
    """
    Enum representing different product types.
    """

    SPOT = "SPOT"

Gran = {"ONE_MINUTE": 1, "FIVE_MINUTE": 5, "FIFTEEN_MINUTE": 15, "THIRTY_MINUTE": 30, "ONE_HOUR": 60, "TWO_HOUR": 120, "SIX_HOUR": 360, "ONE_DAY": 720}

class Granularity(Enum):
    """
    Enum representing time range for product candles.
    """

    UNKNOWN = "UNKNOWN_GRANULARITY"
    ONE_MINUTE = "ONE_MINUTE"
    FIVE_MINUTE = "FIVE_MINUTE"
    FIFTEEN_MINUTE = "FIFTEEN_MINUTE"
    THIRTY_MINUTE = "THIRTY_MINUTE"
    ONE_HOUR = "ONE_HOUR"
    TWO_HOUR = "TWO_HOUR"
    SIX_HOUR = "SIX_HOUR"
    ONE_DAY = "ONE_DAY"


class Product:
    """
    Object representing a product.
    """

    product_id: str
    price: str
    price_percentage_change_24h: str
    volume_24h: int
    volume_percentage_change_24h: str
    base_increment: str
    quote_increment: str
    quote_min_size: str
    quote_max_size: int
    base_min_size: str
    base_max_size: int
    base_name: str
    quote_name: str
    watched: bool
    is_disabled: bool
    new: bool
    status: str
    cancel_only: bool
    limit_only: bool
    post_only: bool
    trading_disabled: bool
    auction_mode: bool
    product_type: str
    quote_currency_id: str
    base_currency_id: str
    mid_market_price: str
    fcm_trading_session_details: str
    alias: str
    alias_to: list
    base_display_symbol: str
    quote_display_symbol: str

    def __init__(self,
                 product_id: str,
                 price: str,
                 price_percentage_change_24h: str,
                 volume_24h: int,
                 volume_percentage_change_24h: str,
                 base_increment: str,
                 quote_increment: str,
                 quote_min_size: str,
                 quote_max_size: int,
                 base_min_size: str,
                 base_max_size: int,
                 base_name: str,
                 quote_name: str,
                 watched: bool,
                 is_disabled: bool,
                 new: bool,
                 status: str,
                 cancel_only: bool,
                 limit_only: bool,
                 post_only: bool,
                 trading_disabled: bool,
                 auction_mode: bool,
                 product_type: str,
                 quote_currency_id: str,
                 base_currency_id: str,
                 mid_market_price: str,
                 fcm_trading_session_details: str,
                 alias: str,
                 alias_to: list,
                 base_display_symbol: str,
                 quote_display_symbol: str,
                 ) -> None:
        self.product_id = product_id
        self.price = price
        self.price_percentage_change_24h = price_percentage_change_24h
        self.volume_24h = volume_24h
        self.volume_percentage_change_24h = volume_percentage_change_24h
        self.base_increment = base_increment
        self.quote_increment = quote_increment
        self.quote_min_size = quote_min_size
        self.quote_max_size = quote_max_size
        self.base_min_size = base_min_size
        self.base_max_size = base_max_size
        self.base_name = base_name
        self.quote_name = quote_name
        self.watched = watched
        self.is_disabled = is_disabled
        self.new = new
        self.status = status
        self.cancel_only = cancel_only
        self.limit_only = limit_only
        self.post_only = post_only
        self.trading_disabled = trading_disabled
        self.auction_mode = auction_mode
        self.product_type = product_type
        self.quote_currency_id = quote_currency_id
        self.base_currency_id = base_currency_id
        self.mid_market_price = mid_market_price
        self.fcm_trading_session_details = fcm_trading_session_details
        self.alias = alias
        self.alias_to = alias_to
        self.base_display_symbol = base_display_symbol
        self.quote_display_symbol = quote_display_symbol

    @classmethod
    def from_response(cls, response: requests.Response) -> 'Product':
        """
        Factory Method.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)
        product_dict = result
        return cls(**product_dict)


class ProductsPage:
    """
    Products Page.
    """

    products: List[Product]
    num_products: int

    def __init__(self, products: List[Product], num_products: int) -> None:
        self.products = list(map(lambda x: Product(**x), products)) \
            if products is not None else None

        self.num_products = num_products

    @classmethod
    def from_response(cls, response: requests.Response) -> 'ProductsPage':
        """
        Factory Method.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)
        return cls(**result)


class Candle:
    """
    Candle object.
    """

    start: int
    low: str
    high: str
    open: str
    close: str
    volume: int

    def __init__(self, start: int, low: str, high: str, open: str, close: str, volume: int) -> None:
        self.start = start
        self.low = low
        self.high = high
        self.open = open
        self.close = close
        self.volume = volume


class CandlesPage:
    """
    Page of product candles.
    """

    candles: List[Candle]

    def __init__(self, candles: List[Candle]) -> None:
        self.candles = list(map(lambda x: Candle(**x), candles)) if candles is not None else None

    @classmethod
    def from_response(cls, response: requests.Response) -> 'CandlesPage':
        """
        Factory Method.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)
        return cls(**result)


class Trade:
    """
    Trade object data.
    """

    trade_id: UUID
    product_id: str
    price: str
    size: int
    time: datetime
    side: str
    bid: str
    ask: str

    def __init__(self,
                 trade_id: UUID,
                 product_id: str,
                 price: str,
                 size: int,
                 time: datetime,
                 side: str,
                 bid: str,
                 ask: str) -> None:
        self.trade_id = trade_id
        self.product_id = product_id
        self.price = price
        self.size = size
        self.time = time
        self.side = side
        self.bid = bid
        self.ask = ask


class TradesPage:
    """
    Page of trades.
    """

    trades: List[Trade]
    best_bid: str
    best_ask: str

    def __init__(self,
                 trades: List[Trade],
                 best_bid: str,
                 best_ask: str,
                 ) -> None:
        self.trades = list(map(lambda x: Trade(**x), trades)) if trades is not None else None
        self.best_bid = best_bid
        self.best_ask = best_ask

    @classmethod
    def from_response(cls, response: requests.Response) -> 'TradesPage':
        """
        Factory Method.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)
        return cls(**result)
