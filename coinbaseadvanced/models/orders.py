"""
Object models for order related endpoints args and response.
"""

from typing import List, Optional
from datetime import datetime
from enum import Enum

import requests

from coinbaseadvanced.models.common import BaseModel
from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError


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


class OrderPlacementSource(Enum):
    """
    Enum representing placements source for an order.
    """
    UNKNOWN = "UNKNOWN_PLACEMENT_SOURCE"
    RETAIL_ADVANCDED = "RETAIL_ADVANCED"


class OrderError(BaseModel):
    """
    Class encapsulating order error fields.
    """

    error: str
    message: str
    error_details: str
    preview_failure_reason: str
    new_order_failure_reason: str

    def __init__(self,
                 error: str = '',
                 message: str = '',
                 error_details: str = '',
                 preview_failure_reason: str = '',
                 new_order_failure_reason: str = '', **kwargs) -> None:
        self.error = error
        self.message = message
        self.error_details = error_details
        self.preview_failure_reason = preview_failure_reason
        self.new_order_failure_reason = new_order_failure_reason

        self.kwargs = kwargs


class LimitGTC(BaseModel):
    """
    Limit till cancelled order configuration.
    """

    base_size: str
    limit_price: str
    post_only: bool

    def __init__(self, base_size: str, limit_price: str, post_only: bool, **kwargs) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.post_only = post_only

        self.kwargs = kwargs


class LimitGTD(BaseModel):
    """
    Limit till date order configuration.
    """

    base_size: str
    limit_price: str
    post_only: bool
    end_time: datetime

    def __init__(self,
                 base_size: str,
                 limit_price: str,
                 post_only: bool,
                 end_time: str, **kwargs) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.post_only = post_only
        self.end_time = datetime.strptime(end_time if len(
            end_time) <= 27 else end_time[:26]+'Z', "%Y-%m-%dT%H:%M:%SZ")

        self.kwargs = kwargs


class MarketIOC(BaseModel):
    """
    Market order configuration.
    """

    quote_size: Optional[str]
    base_size: Optional[str]

    def __init__(self,
                 quote_size: Optional[str] = None,
                 base_size: Optional[str] = None, **kwargs) -> None:
        self.quote_size = quote_size
        self.base_size = base_size

        self.kwargs = kwargs


class StopLimitGTC(BaseModel):
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
                 stop_direction: str, **kwargs) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.stop_direction = stop_direction

        self.kwargs = kwargs


class StopLimitGTD(BaseModel):
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
                 stop_direction: str, **kwargs) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.end_time = datetime.strptime(end_time if len(
            end_time) <= 27 else end_time[:26]+'Z', "%Y-%m-%dT%H:%M:%SZ")
        self.stop_direction = stop_direction

        self.kwargs = kwargs


class OrderEditRecord(BaseModel):
    """
    Stop-Limit till date order configuration.
    """

    def __init__(self,
                 price: str,
                 size: str,
                 replace_accept_timestamp: str,
                 **kwargs) -> None:
        self.price = price
        self.size = size
        self.replace_accept_timestamp = replace_accept_timestamp

        self.kwargs = kwargs


class OrderConfiguration(BaseModel):
    """
    Order Configuration. One of four possible fields should only be settled.
    """

    market_market_ioc: Optional[MarketIOC]
    limit_limit_gtc: Optional[LimitGTC]
    limit_limit_gtd: Optional[LimitGTD]
    stop_limit_stop_limit_gtc: Optional[StopLimitGTC]
    stop_limit_stop_limit_gtd: Optional[StopLimitGTD]

    def __init__(self,
                 market_market_ioc: Optional[dict] = None,
                 limit_limit_gtc: Optional[dict] = None,
                 limit_limit_gtd: Optional[dict] = None,
                 stop_limit_stop_limit_gtc: Optional[dict] = None,
                 stop_limit_stop_limit_gtd: Optional[dict] = None, **kwargs) -> None:
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

        self.kwargs = kwargs


class Order(BaseModel):
    """
    Class reprensenting an order. This support the `create_order*` endpoints
    and the `get_order` endpoint.
    Fields will be filled depending on which endpoint generated the order since
    not all of them are returned at creation time.
    """

    order_id: Optional[str]
    product_id: Optional[str]
    side: Optional[str]
    client_order_id: Optional[str]
    order_configuration: Optional[OrderConfiguration]

    user_id: Optional[str]
    status: Optional[str]
    time_in_force: Optional[str]
    created_time: Optional[datetime]
    completion_percentage: Optional[int]
    filled_size: Optional[str]
    average_filled_price: Optional[int]
    fee: Optional[str]
    number_of_fills: Optional[int]
    filled_value: Optional[int]
    pending_cancel: Optional[bool]
    size_in_quote: Optional[bool]
    total_fees: Optional[str]
    size_inclusive_of_fees: Optional[bool]
    total_value_after_fees: Optional[str]
    trigger_status: Optional[str]
    order_type: Optional[str]
    reject_reason: Optional[str]
    settled: Optional[str]
    product_type: Optional[str]
    reject_message: Optional[str]
    cancel_message: Optional[str]
    order_placement_source: Optional[str]
    outstanding_hold_amount: Optional[str]

    is_liquidation: Optional[bool]
    last_fill_time: Optional[str]
    edit_history: Optional[List[OrderEditRecord]]
    leverage: Optional[str]
    margin_type: Optional[str]

    order_error: Optional[OrderError]

    def __init__(self,
                 order_id: Optional[str],
                 product_id: Optional[str],
                 side: Optional[str],
                 client_order_id: Optional[str],
                 order_configuration: Optional[dict],
                 user_id: Optional[str] = None,
                 status: Optional[str] = None,
                 time_in_force: Optional[str] = None,
                 created_time: Optional[str] = None,
                 completion_percentage: Optional[int] = None,
                 filled_size: Optional[str] = None,
                 average_filled_price: Optional[int] = None,
                 fee: Optional[str] = None,
                 number_of_fills: Optional[int] = None,
                 filled_value: Optional[int] = None,
                 pending_cancel: Optional[bool] = None,
                 size_in_quote: Optional[bool] = None,
                 total_fees: Optional[str] = None,
                 size_inclusive_of_fees: Optional[bool] = None,
                 total_value_after_fees: Optional[str] = None,
                 trigger_status: Optional[str] = None,
                 order_type: Optional[str] = None,
                 reject_reason: Optional[str] = None,
                 settled: Optional[str] = None,
                 product_type: Optional[str] = None,
                 reject_message: Optional[str] = None,
                 cancel_message: Optional[str] = None,
                 order_placement_source: Optional[str] = None,
                 outstanding_hold_amount: Optional[str] = None,

                 is_liquidation: Optional[bool] = None,
                 last_fill_time: Optional[str] = None,
                 edit_history: Optional[List[OrderEditRecord]] = None,
                 leverage: Optional[str] = None,
                 margin_type: Optional[str] = None,

                 order_error: Optional[dict] = None, **kwargs) -> None:
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

        self.is_liquidation = is_liquidation
        self.last_fill_time = last_fill_time
        self.edit_history = edit_history if edit_history is not None else None
        self.leverage = leverage
        self.margin_type = margin_type

        self.order_error = OrderError(
            **order_error) if order_error is not None else None

        self.kwargs = kwargs

    @classmethod
    def from_create_order_response(cls, response: requests.Response) -> 'Order':
        """
        Factory method from the `create_order` response object.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()

        if not result['success']:
            error_response = result['error_response']
            return cls(
                None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, error_response)

        success_response = result['success_response']
        order_configuration = result['order_configuration']
        return cls(**success_response, order_configuration=order_configuration)

    @classmethod
    def from_get_order_response(cls, response: requests.Response) -> 'Order':
        """
        Factory method for creation from the `get_order` response object.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()

        order = result['order']

        return cls(**order)


class OrdersPage(BaseModel):
    """
    Orders page.
    """

    orders: List[Order]
    has_next: bool
    cursor: Optional[str]
    sequence: int

    def __init__(self,
                 orders: List[dict],
                 has_next: bool,
                 cursor: Optional[str],
                 sequence: int, **kwargs
                 ) -> None:

        self.orders = list(map(lambda x: Order(**x), orders)
                           ) if orders is not None else []

        self.has_next = has_next
        self.cursor = cursor
        self.sequence = sequence

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'OrdersPage':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result)

    def __iter__(self):
        return self.orders.__iter__()


class OrderEdit(BaseModel):
    """
    Order edit.
    """

    success: bool
    errors: List[dict]
    edit_failure_reason: str
    preview_failure_reason: str

    def __init__(self, success: bool, errors: List[dict], **kwargs) -> None:
        self.success = success
        self.errors = errors if errors is not None else None

        self.kwargs = kwargs
    
    @classmethod
    def from_get_edit_response(cls, response: requests.Response) -> 'OrderEdit':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result)


class OrderCancellation(BaseModel):
    """
    Order cancellation.
    """

    success: bool
    failure_reason: str
    order_id: str

    def __init__(self, success: bool, failure_reason: str, order_id: str, **kwargs) -> None:
        self.success = success
        self.failure_reason = failure_reason
        self.order_id = order_id

        self.kwargs = kwargs


class OrderBatchCancellation(BaseModel):
    """
    Batch/Page of order cancellations.
    """

    results: List[OrderCancellation]

    def __init__(self, results: List[OrderCancellation], **kwargs) -> None:
        self.results = results

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'OrderBatchCancellation':
        """
        Factory method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()

        return cls(**result)


class Fill(BaseModel):
    """
    Object representing an order filled.
    """

    entry_id: str
    trade_id: str
    order_id: str
    trade_time: Optional[datetime]
    trade_type: str
    price: str
    size: str
    commission: str
    product_id: str
    sequence_timestamp: Optional[datetime]
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
            side: str, **kwargs) -> None:
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
            sequence_timestamp if len(
                sequence_timestamp) <= 27 else sequence_timestamp[:26] + 'Z',
            "%Y-%m-%dT%H:%M:%S.%fZ") if sequence_timestamp is not None else None
        self.liquidity_indicator = liquidity_indicator
        self.size_in_quote = size_in_quote
        self.user_id = user_id
        self.side = side

        self.kwargs = kwargs


class FillsPage(BaseModel):
    """
    Page of orders filled.
    """

    fills: List[Fill]
    cursor: Optional[str]

    def __init__(self,
                 fills: List[dict],
                 cursor:  Optional[str], **kwargs
                 ) -> None:

        self.fills = list(map(lambda x: Fill(**x), fills)
                          ) if fills is not None else []

        self.cursor = cursor

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'FillsPage':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result)

    def __iter__(self):
        return self.fills.__iter__()
