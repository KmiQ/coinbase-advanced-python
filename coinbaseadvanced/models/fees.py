"""
Object models for fees related endpoints args and response.
"""

from typing import Optional
import requests

from coinbaseadvanced.models.common import BaseModel
from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError


class FeeTier(BaseModel):
    """
    Fee Tier object.
    """

    pricing_tier: str
    usd_from: int
    usd_to: str
    taker_fee_rate: str
    maker_fee_rate: str

    def __init__(self,
                 pricing_tier: str,
                 usd_from: int,
                 usd_to: str,
                 taker_fee_rate: str,
                 maker_fee_rate: str, **kwargs) -> None:
        self.pricing_tier = pricing_tier
        self.usd_from = usd_from
        self.usd_to = usd_to
        self.taker_fee_rate = taker_fee_rate
        self.maker_fee_rate = maker_fee_rate

        self.kwargs = kwargs


class GoodsAndServicesTax(BaseModel):
    """
    Object representing Goods and Services Tax data.
    """

    rate: str
    type: str

    def __init__(self, rate: str, type: str, **kwargs) -> None:
        self.rate = rate
        self.type = type

        self.kwargs = kwargs


class MarginRate(BaseModel):
    """
    Margin Rate.
    """

    value: str

    def __init__(self, value: str, **kwargs) -> None:
        self.value = value

        self.kwargs = kwargs


class TransactionsSummary(BaseModel):
    """
    Transactions Summary.
    """

    total_volume: int
    total_fees: int
    fee_tier: Optional[FeeTier]
    margin_rate: Optional[MarginRate]
    goods_and_services_tax: Optional[GoodsAndServicesTax]
    advanced_trade_only_volume: int
    advanced_trade_only_fees: int
    coinbase_pro_volume: int
    coinbase_pro_fees: int
    total_balance: str
    has_promo_fee: bool

    def __init__(self,
                 total_volume: int,
                 total_fees: int,
                 fee_tier: dict,
                 margin_rate: dict,
                 goods_and_services_tax: dict,
                 advanced_trade_only_volume: int,
                 advanced_trade_only_fees: int,
                 coinbase_pro_volume: int,
                 coinbase_pro_fees: int,
                 total_balance: str,
                 has_promo_fee: bool, **kwargs) -> None:
        self.total_volume = total_volume
        self.total_fees = total_fees
        self.fee_tier = FeeTier(**fee_tier) if fee_tier is not None else None
        self.margin_rate = MarginRate(
            **margin_rate) if margin_rate is not None else None
        self.goods_and_services_tax = GoodsAndServicesTax(
            **goods_and_services_tax) if goods_and_services_tax is not None else None
        self.advanced_trade_only_volume = advanced_trade_only_volume
        self.advanced_trade_only_fees = advanced_trade_only_fees
        self.coinbase_pro_volume = coinbase_pro_volume
        self.coinbase_pro_fees = coinbase_pro_fees

        self.total_balance = total_balance
        self.has_promo_fee = has_promo_fee

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'TransactionsSummary':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result)
