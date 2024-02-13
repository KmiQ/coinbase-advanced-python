"""
Object models for portfolios related endpoints args and response.
"""

from typing import List
from enum import Enum
from uuid import UUID
from coinbaseadvanced.models.common import BaseModel, ValueCurrency
from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError

import requests

from coinbaseadvanced.models.futures import FuturesPosition, FuturesPositionSide, MarginType


class UserRawCurrency(BaseModel):
    """
    Represents a user's raw currency.

    Attributes:
        user_native_currency (ValueCurrency): The user's native currency.
        raw_currency (ValueCurrency): The raw currency.
    """

    user_native_currency: ValueCurrency
    raw_currency: ValueCurrency

    def __init__(self, userNativeCurrency: dict, rawCurrency: dict):
        self.user_native_currency = ValueCurrency(**userNativeCurrency)
        self.raw_currency = ValueCurrency(**rawCurrency)


class PortfolioType(Enum):
    """
    Enum representing whether "BUY" or "SELL" order.
    """

    UNDEFINED = "UNDEFINED"
    DEFAULT = "DEFAULT"
    CONSUMER = "CONSUMER"
    INTX = "INTX"


class Portfolio(BaseModel):
    """
    Object representing a portfolio.
    """

    uuid: UUID
    name: str
    type: PortfolioType
    deleted: bool

    def __init__(
            self, uuid: UUID, name: str, type: str, deleted: bool, **kwargs) -> None:
        self.uuid = uuid
        self.name = name
        self.type = PortfolioType[type]
        self.deleted = deleted

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'Portfolio':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result['portfolio'])


class PortfolioBalances(BaseModel):
    """
    Object representing a portfolio balances.
    """

    total_balance: ValueCurrency
    total_futures_balance: ValueCurrency
    total_cash_equivalent_balance: ValueCurrency
    total_crypto_balance: ValueCurrency
    futures_unrealized_pnl: ValueCurrency
    perp_unrealized_pnl: ValueCurrency

    def __init__(
        self, total_balance: dict,
            total_futures_balance: dict,
            total_cash_equivalent_balance: dict,
            total_crypto_balance: dict,
            futures_unrealized_pnl: dict,
            perp_unrealized_pnl: dict, **kwargs) -> None:
        self.total_balance = ValueCurrency(**total_balance)
        self.total_futures_balance = ValueCurrency(**total_futures_balance)
        self.total_cash_equivalent_balance = ValueCurrency(
            **total_cash_equivalent_balance)
        self.total_crypto_balance = ValueCurrency(**total_crypto_balance)
        self.futures_unrealized_pnl = ValueCurrency(
            **futures_unrealized_pnl)
        self.perp_unrealized_pnl = ValueCurrency(**perp_unrealized_pnl)

        self.kwargs = kwargs


class SpotPosition(BaseModel):
    """
    Object representing a spot position.
    """

    asset: str
    account_uuid: str
    total_balance_fiat: float
    total_balance_crypto: float
    available_to_trade_fiat: float
    allocation: float
    one_day_change: float
    cost_basis: ValueCurrency
    asset_img_url: str
    is_cash: bool

    def __init__(
            self, asset: str,
            account_uuid: str,
            total_balance_fiat: float,
            total_balance_crypto: float,
            available_to_trade_fiat: float,
            allocation: float,
            one_day_change: float,
            cost_basis: dict,
            asset_img_url: str,
            is_cash: bool,  **kwargs) -> None:

        self.asset = asset
        self.account_uuid = account_uuid
        self.total_balance_fiat = total_balance_fiat
        self.total_balance_crypto = total_balance_crypto
        self.available_to_trade_fiat = available_to_trade_fiat
        self.allocation = allocation
        self.one_day_change = one_day_change
        self.cost_basis = ValueCurrency(**cost_basis)
        self.asset_img_url = asset_img_url
        self.is_cash = is_cash

        self.kwargs = kwargs


class PerpPosition(BaseModel):
    """
    Object representing a perp position.
    """

    product_id: str
    product_uuid: str
    symbol: str
    asset_image_url: str
    vwap: UserRawCurrency
    position_side: FuturesPositionSide
    net_size: str
    buy_order_size: str
    sell_order_size: str
    im_contribution: str
    unrealized_pnl: UserRawCurrency
    mark_price: UserRawCurrency
    liquidation_price: UserRawCurrency
    leverage: str
    im_notional: UserRawCurrency
    mm_notional: UserRawCurrency
    position_notional: UserRawCurrency
    margin_type: MarginType
    liquidation_buffer: str
    liquidation_percentage: str

    def __init__(
            self,
            product_id: str,
            product_uuid: str,
            symbol: str,
            asset_image_url: str,
            vwap: dict,
            position_side: str,
            net_size: str,
            buy_order_size: str,
            sell_order_size: str,
            im_contribution: str,
            unrealized_pnl: dict,
            mark_price: dict,
            liquidation_price: dict,
            leverage: str,
            im_notional: dict,
            mm_notional: dict,
            position_notional: dict,
            margin_type: str,
            liquidation_buffer: str,
            liquidation_percentage: str, **kwargs) -> None:

        self.product_id = product_id
        self.product_uuid = product_uuid
        self.symbol = symbol
        self.asset_image_url = asset_image_url
        self.vwap = UserRawCurrency(**vwap)
        self.position_side = FuturesPositionSide[position_side]
        self.net_size = net_size
        self.buy_order_size = buy_order_size
        self.sell_order_size = sell_order_size
        self.im_contribution = im_contribution
        self.unrealized_pnl = UserRawCurrency(**unrealized_pnl)
        self.mark_price = UserRawCurrency(**mark_price)
        self.liquidation_price = UserRawCurrency(**liquidation_price)
        self.leverage = leverage
        self.im_notional = UserRawCurrency(**im_notional)
        self.mm_notional = UserRawCurrency(**mm_notional)
        self.position_notional = UserRawCurrency(**position_notional)
        self.margin_type = MarginType[margin_type]
        self.liquidation_buffer = liquidation_buffer
        self.liquidation_percentage = liquidation_percentage

        self.kwargs = kwargs


class PortfolioBreakdown(BaseModel):
    """
    Object representing a portfolio breakdown.
    """

    portfolio: Portfolio
    portfolio_balances: PortfolioBalances
    spot_positions: List[SpotPosition]
    perp_positions: List[PerpPosition]
    futures_positions: List[FuturesPosition]

    def __init__(self, portfolio: dict, portfolio_balances: dict, spot_positions: list, perp_positions: list, futures_positions: list,  **kwargs):
        self.portfolio = Portfolio(**portfolio)
        self.portfolio_balances = PortfolioBalances(**portfolio_balances)
        self.spot_positions = [SpotPosition(**x) for x in spot_positions]
        self.perp_positions = [PerpPosition(**x) for x in perp_positions]
        self.futures_positions = [
            FuturesPosition(**x) for x in futures_positions]

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'PortfolioBreakdown':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result['breakdown'])


class PortfoliosPage(BaseModel):
    """
    Portfolio Page.
    """

    portfolios: List[Portfolio]

    def __init__(self, portfolios: List[Portfolio], **kwargs) -> None:
        self.portfolios = list(map(lambda x: Portfolio(**x), portfolios)) \
            if portfolios is not None else None

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'PortfoliosPage':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result)

    def __iter__(self):
        return self.portfolios.__iter__()
