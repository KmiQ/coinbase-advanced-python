"""
Object models for portfolios related endpoints args and response.
"""

from typing import List
from enum import Enum
from uuid import UUID
from coinbaseadvanced.models.common import BaseModel
from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError

import requests


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
