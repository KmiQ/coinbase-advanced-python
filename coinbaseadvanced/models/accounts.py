"""
Object models for account related endpoints args and response.
"""

from uuid import UUID
from datetime import datetime
from typing import List, Optional
import requests

from coinbaseadvanced.models.common import BaseModel, ValueCurrency
from coinbaseadvanced.models.error import CoinbaseAdvancedTradeAPIError


class Account(BaseModel):
    """
    Object representing an account.
    """

    uuid: UUID
    name: str
    currency: str
    available_balance: Optional[ValueCurrency]
    default: bool
    active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    type: str
    ready: bool
    hold: Optional[ValueCurrency]

    def __init__(
        self, uuid: UUID, name: str, currency: str, available_balance: dict, default: bool,
            active: bool, created_at: datetime, updated_at: datetime, deleted_at: datetime,
            type: str, ready: bool, hold: dict, **kwargs) -> None:
        self.uuid = uuid
        self.name = name
        self.currency = currency
        self.available_balance = ValueCurrency(**available_balance) \
            if available_balance is not None else None
        self.default = default
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.type = type
        self.ready = ready
        self.hold = ValueCurrency(**hold) if hold is not None else None

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'Account':
        """
        Factory method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        account_dict = result['account']
        return cls(**account_dict)


class AccountsPage(BaseModel):
    """
    Page of accounts.
    """

    accounts: List[Account]
    has_next: bool
    cursor: Optional[str]
    size: int

    def __init__(self,
                 accounts: List[dict],
                 has_next: bool,
                 cursor: Optional[str],
                 size: int,
                 **kwargs
                 ) -> None:

        self.accounts = list(map(lambda x: Account(**x), accounts))\
            if accounts is not None else []

        self.has_next = has_next
        self.cursor = cursor
        self.size = size

        self.kwargs = kwargs

    @classmethod
    def from_response(cls, response: requests.Response) -> 'AccountsPage':
        """
        Factory Method.
        """

        if not response.ok:
            raise CoinbaseAdvancedTradeAPIError.not_ok_response(response)

        result = response.json()
        return cls(**result)

    def __iter__(self):
        return self.accounts.__iter__() if self.accounts is not None else [].__iter__()
