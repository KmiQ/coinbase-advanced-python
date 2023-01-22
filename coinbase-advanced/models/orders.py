from typing import Optional, List
from datetime import datetime
import json
import requests


class OrderError:
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


class LimitLimitGt:
    base_size: str
    limit_price: str
    post_only: bool
    end_time: Optional[datetime]

    def __init__(self, base_size: str, limit_price: str, post_only: bool, end_time: Optional[str]) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.post_only = post_only
        self.end_time = datetime.strptime(end_time if len(
            end_time) <= 27 else end_time[:26]+'Z', "%Y-%m-%dT%H:%M:%S.%fZ") if end_time is not None else None


class MarketMarketIoc:
    quote_size: str
    base_size: str

    def __init__(self, quote_size: str, base_size: str) -> None:
        self.quote_size = quote_size
        self.base_size = base_size


class StopLimitStopLimitGtc:
    base_size: str
    limit_price: str
    stop_price: str
    stop_direction: str

    def __init__(self, base_size: str, limit_price: str, stop_price: str, stop_direction: str) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.stop_direction = stop_direction


class StopLimitStopLimitGtd:
    base_size: float
    limit_price: str
    stop_price: str
    end_time: datetime
    stop_direction: str

    def __init__(self, base_size: float, limit_price: str, stop_price: str, end_time: str, stop_direction: str) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.end_time = datetime.strptime(end_time if len(
            end_time) <= 27 else end_time[:26]+'Z', "%Y-%m-%dT%H:%M:%S.%fZ") if end_time is not None else None
        self.stop_direction = stop_direction


class OrderConfiguration:
    market_market_ioc: MarketMarketIoc
    limit_limit_gtc: LimitLimitGt
    limit_limit_gtd: LimitLimitGt
    stop_limit_stop_limit_gtc: StopLimitStopLimitGtc
    stop_limit_stop_limit_gtd: StopLimitStopLimitGtd

    def __init__(self, market_market_ioc: MarketMarketIoc = None, limit_limit_gtc: LimitLimitGt = None,
                 limit_limit_gtd: LimitLimitGt = None, stop_limit_stop_limit_gtc: StopLimitStopLimitGtc = None,
                 stop_limit_stop_limit_gtd: StopLimitStopLimitGtd = None) -> None:
        self.market_market_ioc = market_market_ioc
        self.limit_limit_gtc = limit_limit_gtc
        self.limit_limit_gtd = limit_limit_gtd
        self.stop_limit_stop_limit_gtc = stop_limit_stop_limit_gtc
        self.stop_limit_stop_limit_gtd = stop_limit_stop_limit_gtd


class Order:
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

    error: str
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

                 error: str = None, order_error: dict = None) -> None:
        self.order_id = order_id
        self.product_id = product_id
        self.side = side
        self.client_order_id = client_order_id
        self.order_configuration = OrderConfiguration(
            **order_configuration) if order_configuration is not None else None

        self.user_id = user_id
        self.status = status
        self.time_in_force = time_in_force
        self.created_time = datetime.strptime(created_time if len(
            created_time) <= 27 else created_time[:26]+'Z', "%Y-%m-%dT%H:%M:%S.%fZ") if created_time is not None else None
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

        self.error = error
        self.order_error = OrderError(**order_error) if order_error is not None else None

    @classmethod
    def from_create_order_response(cls, response: requests.Response) -> 'Order':

        if not response.ok:
            error_result = response.text
            return cls(
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, error_result, None)

        result = json.loads(response.text)

        if not result['success']:
            error_response = result['error_response']
            return cls(
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, result['failure_reason'],
                error_response)

        success_response = result['success_response']
        order_configuration = result['order_configuration']
        return cls(**success_response, order_configuration=order_configuration)

    @classmethod
    def from_get_order_response(cls, response: requests.Response) -> 'Order':

        if not response.ok:
            error_result = response.text
            return cls(
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, error_result, None)

        result = json.loads(response.text)

        order = result['order']

        return cls(**order)


class OrdersPage:
    orders: List[Order]
    has_next: bool
    cursor: str
    sequence: int

    error: dict

    def __init__(self,
                 orders: List[dict],
                 has_next: bool,
                 cursor: str,
                 sequence: int,
                 error=None) -> None:

        self.orders = list(map(lambda x: Order(**x), orders)) if orders is not None else None

        self.has_next = has_next
        self.cursor = cursor
        self.sequence = sequence

        self.error = error

    @classmethod
    def from_response(cls, response: requests.Response) -> 'OrdersPage':

        if not response.ok:
            error_result = json.loads(response.text)
            return cls(None, None, None, None, error=error_result)

        result = json.loads(response.text)
        return cls(**result)


class OrderCancellation:
    success: bool
    failure_reason: str
    order_id: str

    def __init__(self, success: bool, failure_reason: str, order_id: str) -> None:
        self.success = success
        self.failure_reason = failure_reason
        self.order_id = order_id


class OrderBatchCancellation:
    results: List[OrderCancellation]

    error: str

    def __init__(self, results: List[OrderCancellation], error: str = None) -> None:
        self.results = results

    @classmethod
    def from_response(cls, response: requests.Response) -> 'Order':

        if not response.ok:
            error_result = response.text
            return cls(None, error_result)

        result = json.loads(response.text)

        return cls(**result)


class Fill:
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
            self, entry_id: str, trade_id: str, order_id: str, trade_time: str, trade_type: str, price: str,
            size: str, commission: str, product_id: str, sequence_timestamp: str, liquidity_indicator: str,
            size_in_quote: bool, user_id: str, side: str) -> None:
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
            sequence_timestamp if len(sequence_timestamp) <= 27 else sequence_timestamp[: 26] + 'Z',
            "%Y-%m-%dT%H:%M:%S.%fZ") if sequence_timestamp is not None else None
        self.liquidity_indicator = liquidity_indicator
        self.size_in_quote = size_in_quote
        self.user_id = user_id
        self.side = side


class FillsPage:
    fills: List[Fill]
    cursor: str

    error: dict

    def __init__(self,
                 fills: List[dict],
                 cursor: str,
                 error=None) -> None:

        self.fills = list(map(lambda x: Fill(**x), fills)) if fills is not None else None

        self.cursor = cursor

        self.error = error

    @classmethod
    def from_response(cls, response: requests.Response) -> 'FillsPage':

        if not response.ok:
            error_result = json.loads(response.text)
            return cls(None, None, error=error_result)

        result = json.loads(response.text)
        return cls(**result)
