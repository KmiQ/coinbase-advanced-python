from enum import Enum

from coinbaseadvanced.models.common import BaseModel


class MarginType(Enum):
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
    product_id: str
    contract_size: str
    side: FuturesPositionSide
    amount: str
    avg_entry_price: str
    current_price: str
    unrealized_pnl: str
    expiry: str
    underlying_asset: str
    asset_img_url: str
    product_name: str
    venue: str
    notional_value: str

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
