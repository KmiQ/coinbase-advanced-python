"""
Object models for order related endpoints args and response.
"""

from typing import List
from datetime import datetime
from enum import Enum

from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError

import json
import requests


class Side(Enum):
    """
    Enum representing whether "BUY" or "SELL" order.
    """

    BUY = "BUY"
    SELL = "SELL"


class StopDirection(Enum):
    """
    Enum direction in an stop order context.
    """

    UNKNOWN = "UNKNOWN_STOP_DIRECTION"
    UP = "STOP_DIRECTION_STOP_UP"
    DOWN = "STOP_DIRECTION_STOP_DOWN"


class OrderType(Enum):
    """
    Enum representing different order types.
    """

    UNKNOWN_ORDER_TYPE = "UNKNOWN_ORDER_TYPE"
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderError:
    """
    Class encapsulating order error fields.
    """

    error: str
    message: str
    error_details: str
    preview_failure_reason: str
    new_order_failure_reason: str

    def __init__(self, error: str = '', message: str = '', error_details: str = '',
                 preview_failure_reason: str = '', new_order_failure_reason: str = '') -> None:
        self.error = error
        self.message = message
        self.error_details = error_details
        self.preview_failure_reason = preview_failure_reason
        self.new_order_failure_reason = new_order_failure_reason


class LimitGTC:
    """
    Limit till cancelled order configuration.
    """

    base_size: str
    limit_price: str
    post_only: bool

    def __init__(self, base_size: str, limit_price: str, post_only: bool) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.post_only = post_only


class LimitGTD:
    """
    Limit till date order configuration.
    """

    base_size: str
    limit_price: str
    post_only: bool
    end_time: datetime

    def __init__(self, base_size: str, limit_price: str, post_only: bool, end_time: str) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.post_only = post_only
        self.end_time = datetime.strptime(end_time if len(
            end_time) <= 27 else end_time[:26]+'Z', "%Y-%m-%dT%H:%M:%SZ")


class MarketIOC:
    """
    Market order configuration.
    """

    quote_size: str
    base_size: str

    def __init__(self, quote_size: str = None, base_size: str = None) -> None:
        self.quote_size = quote_size
        self.base_size = base_size


class StopLimitGTC:
    """
    Stop-Limit till cancelled order configuration.
    """

    base_size: str
    limit_price: str
    stop_price: str
    stop_direction: str

    def __init__(self,
                 base_size: str,
                 limit_price: str,
                 stop_price: str,
                 stop_direction: str) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.stop_direction = stop_direction


class StopLimitGTD:
    """
    Stop-Limit till date order configuration.
    """

    base_size: float
    limit_price: str
    stop_price: str
    end_time: datetime
    stop_direction: str

    def __init__(self,
                 base_size: float,
                 limit_price: str,
                 stop_price: str,
                 end_time: str,
                 stop_direction: str) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.end_time = datetime.strptime(end_time if len(
            end_time) <= 27 else end_time[:26]+'Z', "%Y-%m-%dT%H:%M:%SZ")
        self.stop_direction = stop_direction


class OrderConfiguration:
    """
    Order Configuration. One of four possible fields should only be settled.
    """

    market_market_ioc: MarketIOC
    limit_limit_gtc: LimitGTC
    limit_limit_gtd: LimitGTD
    stop_limit_stop_limit_gtc: StopLimitGTC
    stop_limit_stop_limit_gtd: StopLimitGTD

    def __init__(self, market_market_ioc: dict = None, limit_limit_gtc: dict = None,
                 limit_limit_gtd: dict = None, stop_limit_stop_limit_gtc: dict = None,
                 stop_limit_stop_limit_gtd: dict = None) -> None:
        self.market_market_ioc = MarketIOC(
            **market_market_ioc) if market_market_ioc is not None else None
        self.limit_limit_gtc = LimitGTC(
            **limit_limit_gtc) if limit_limit_gtc is not None else None
        self.limit_limit_gtd = LimitGTD(
            **limit_limit_gtd) if limit_limit_gtd is not None else None
        self.stop_limit_stop_limit_gtc = StopLimitGTC(
            **stop_limit_stop_limit_gtc) if stop_limit_stop_limit_gtc is not None else None
        self.stop_limit_stop_limit_gtd = StopLimitGTD(
            **stop_limit_stop_limit_gtd) if stop_limit_stop_limit_gtd is not None else None


class Order:
    """
    Class reprensenting an order. This support the `create_order*` endpoints
    and the `get_order` endpoint.
    Fields will be filled depending on which endpoint generated the order since
    not all of them are returned at creation time.
    """

    order_id: str
    product_id: str
    side: str
    client_order_id: str
    order_configuration: OrderConfiguration

    user_id: str
    status: str
    time_in_force: str
    created_time: datetime
    completion_percentage: int
    filled_size: str
    average_filled_price: int
    fee: str
    number_of_fills: int
    filled_value: int
    pending_cancel: bool
    size_in_quote: bool
    total_fees: str
    size_inclusive_of_fees: bool
    total_value_after_fees: str
    trigger_status: str
    order_type: str
    reject_reason: str
    settled: str
    product_type: str
    reject_message: str
    cancel_message: str
    order_placement_source: str
    outstanding_hold_amount: str

    order_error: OrderError

    def __init__(self, order_id: str, product_id: str, side: str, client_order_id: str,
                 order_configuration: dict,

                 user_id: str = None,
                 status: str = None,
                 time_in_force: str = None,
                 created_time: str = None,
                 completion_percentage: int = None,
                 filled_size: str = None,
                 average_filled_price: int = None,
                 fee: str = None,
                 number_of_fills: int = None,
                 filled_value: int = None,
                 pending_cancel: bool = None,
                 size_in_quote: bool = None,
                 total_fees: str = None,
                 size_inclusive_of_fees: bool = None,
                 total_value_after_fees: str = None,
                 trigger_status: str = None,
                 order_type: str = None,
                 reject_reason: str = None,
                 settled: str = None,
                 product_type: str = None,
                 reject_message: str = None,
                 cancel_message: str = None,
                 order_placement_source: str = None,
                 outstanding_hold_amount: str = None,

                 order_error: dict = None) -> None:
        self.order_id = order_id
        self.product_id = product_id
        self.side = side
        self.client_order_id = client_order_id
        self.order_configuration = OrderConfiguration(
            **order_configuration) if order_configuration is not None else None

        self.user_id = user_id
        self.status = status
        self.time_in_force = time_in_force
        self.created_time = datetime.strptime(
            created_time if len(created_time) <= 27 else
            created_time[:26]+'Z', "%Y-%m-%dT%H:%M:%S.%fZ") if created_time is not None else None
        self.completion_percentage = completion_percentage
        self.filled_size = filled_size
        self.average_filled_price = average_filled_price
        self.fee = fee
        self.number_of_fills = number_of_fills
        self.filled_value = filled_value
        self.pending_cancel = pending_cancel
        self.size_in_quote = size_in_quote
        self.total_fees = total_fees
        self.size_inclusive_of_fees = size_inclusive_of_fees
        self.total_value_after_fees = total_value_after_fees
        self.trigger_status = trigger_status
        self.order_type = order_type
        self.reject_reason = reject_reason
        self.settled = settled
        self.product_type = product_type
        self.reject_message = reject_message
        self.cancel_message = cancel_message
        self.order_placement_source = order_placement_source
        self.outstanding_hold_amount = outstanding_hold_amount

        self.order_error = OrderError(**order_error) if order_error is not None else None

    @classmethod
    def from_create_order_response(cls, response: requests.Response) -> 'Order':
        """
        Factory method from the `create_order` response object.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)

        if not result['success']:
            error_response = result['error_response']
            return cls(
                None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None,
                error_response)

        success_response = result['success_response']
        order_configuration = result['order_configuration']
        return cls(**success_response, order_configuration=order_configuration)

    @classmethod
    def from_get_order_response(cls, response: requests.Response) -> 'Order':
        """
        Factory method for creation from the `get_order` response object.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)

        order = result['order']

        return cls(**order)


class OrdersPage:
    """
    Orders page.
    """

    orders: List[Order]
    has_next: bool
    cursor: str
    sequence: int

    def __init__(self,
                 orders: List[dict],
                 has_next: bool,
                 cursor: str,
                 sequence: int,
                 ) -> None:

        self.orders = list(map(lambda x: Order(**x), orders)) if orders is not None else None

        self.has_next = has_next
        self.cursor = cursor
        self.sequence = sequence

    @classmethod
    def from_response(cls, response: requests.Response) -> 'OrdersPage':
        """
        Factory Method.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)
        return cls(**result)


class OrderCancellation:
    """
    Order cancellation.
    """

    success: bool
    failure_reason: str
    order_id: str

    def __init__(self, success: bool, failure_reason: str, order_id: str) -> None:
        self.success = success
        self.failure_reason = failure_reason
        self.order_id = order_id


class OrderBatchCancellation:
    """
    Batch/Page of order cancellations.
    """

    results: List[OrderCancellation]

    def __init__(self, results: List[OrderCancellation]) -> None:
        self.results = results

    @classmethod
    def from_response(cls, response: requests.Response) -> 'Order':
        """
        Factory method.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)

        return cls(**result)


class Fill:
    """
    Object representing an order filled.
    """

    entry_id: str
    trade_id: str
    order_id: str
    trade_time: datetime
    trade_type: str
    price: str
    size: str
    commission: str
    product_id: str
    sequence_timestamp: datetime
    liquidity_indicator: str
    size_in_quote: bool
    user_id: str
    side: str

    def __init__(
            self,
            entry_id: str,
            trade_id: str,
            order_id: str,
            trade_time: str,
            trade_type: str,
            price: str,
            size: str,
            commission: str,
            product_id: str,
            sequence_timestamp: str,
            liquidity_indicator: str,
            size_in_quote: bool,
            user_id: str,
            side: str) -> None:
        self.entry_id = entry_id
        self.trade_id = trade_id
        self.order_id = order_id
        self.trade_time = datetime.strptime(
            trade_time if len(trade_time) <= 27 else trade_time[:26]+'Z',
            "%Y-%m-%dT%H:%M:%S.%fZ") if trade_time is not None else None
        self.trade_type = trade_type
        self.price = price
        self.size = size
        self.commission = commission
        self.product_id = product_id
        self.sequence_timestamp = datetime.strptime(
            sequence_timestamp if len(sequence_timestamp) <= 27 else sequence_timestamp[:26] + 'Z',
            "%Y-%m-%dT%H:%M:%S.%fZ") if sequence_timestamp is not None else None
        self.liquidity_indicator = liquidity_indicator
        self.size_in_quote = size_in_quote
        self.user_id = user_id
        self.side = side


class FillsPage:
    """
    Page of orders filled.
    """

    fills: List[Fill]
    cursor: str

    def __init__(self,
                 fills: List[dict],
                 cursor: str,
                 ) -> None:

        self.fills = list(map(lambda x: Fill(**x), fills)) if fills is not None else None

        self.cursor = cursor

    @classmethod
    def from_response(cls, response: requests.Response) -> 'FillsPage':
        """
        Factory Method.
        """

        if not response.ok:
            error_result = json.loads(response.text)
            raise CoinbaseAdvancedTradeAPIError(error=error_result)

        result = json.loads(response.text)
        return cls(**result)
