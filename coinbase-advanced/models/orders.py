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

    def __init__(self, base_size: str, limit_price: str, post_only: bool, end_time: Optional[datetime]) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.post_only = post_only
        self.end_time = end_time


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

    def __init__(self, base_size: float, limit_price: str, stop_price: str, end_time: datetime, stop_direction: str) -> None:
        self.base_size = base_size
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.end_time = end_time
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

    error: str
    order_error: OrderError

    def __init__(self, order_id: str, product_id: str, side: str, client_order_id: str,
                 order_configuration: dict, error: str = None, order_error: dict = None) -> None:
        self.order_id = order_id
        self.product_id = product_id
        self.side = side
        self.client_order_id = client_order_id
        self.order_configuration = OrderConfiguration(
            **order_configuration) if order_configuration is not None else None

        self.error = error
        self.order_error = OrderError(**order_error) if order_error is not None else None

    @classmethod
    def from_response(cls, response: requests.Response) -> 'Order':

        if not response.ok:
            error_result = response.text
            return cls(None, None, None, None, None, error_result, None)

        result = json.loads(response.text)

        if not result['success']:
            error_response = result['error_response']
            return cls(None, None, None, None, None, result['failure_reason'], error_response)

        success_response = result['success_response']
        order_configuration = result['order_configuration']
        return cls(**success_response, order_configuration=order_configuration)


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
