"""
This module contains the definition of the FuturesPosition class and related enums.
"""

from enum import Enum
from coinbaseadvanced.models.common import BaseModel


class MarginType(Enum):
    """
    Enum representing the margin type for futures trading.
    """

    UNSPECIFIED = "MARGIN_TYPE_UNSPECIFIED"
    CROSS = "MARGIN_TYPE_CROSS"
    ISOLATED = "MARGIN_TYPE_ISOLATED"


class FuturesPositionSide(Enum):
    """
    Enum representing the position side for futures contracts.
    """

    UNSPECIFIED = "FUTURES_POSITION_SIDE_UNSPECIFIED"
    LONG = "FUTURES_POSITION_SIDE_LONG"
    SHORT = "FUTURES_POSITION_SIDE_SHORT"


class FuturesPosition(BaseModel):
    """
    Represents a futures position.

    Attributes:
        product_id (str): The ID of the product.
        contract_size (str): The size of the contract.
        side (FuturesPositionSide): The side of the position.
        amount (str): The amount of the position.
        avg_entry_price (str): The average entry price of the position.
        current_price (str): The current price of the position.
        unrealized_pnl (str): The unrealized profit/loss of the position.
        expiry (str): The expiry date of the position.
        underlying_asset (str): The underlying asset of the position.
        asset_img_url (str): The URL of the asset's image.
        product_name (str): The name of the product.
        venue (str): The venue of the position.
        notional_value (str): The notional value of the position.
    """

    def __init__(
            self, product_id: str,
            contract_size: str,
            side: str,
            amount: str,
            avg_entry_price: str,
            current_price: str,
            unrealized_pnl: str,
            expiry: str,
            underlying_asset: str,
            asset_img_url: str,
            product_name: str,
            venue: str,
            notional_value: str, **kwargs) -> None:
        self.product_id = product_id
        self.contract_size = contract_size
        self.side = FuturesPositionSide[side]
        self.amount = amount
        self.avg_entry_price = avg_entry_price
        self.current_price = current_price
        self.unrealized_pnl = unrealized_pnl
        self.expiry = expiry
        self.underlying_asset = underlying_asset
        self.asset_img_url = asset_img_url
        self.product_name = product_name
        self.venue = venue
        self.notional_value = notional_value

        self.kwargs = kwargs
