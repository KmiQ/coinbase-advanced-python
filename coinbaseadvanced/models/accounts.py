import json
from uuid import UUID
from datetime import datetime
from typing import List
import requests


class AvailableBalance:
    value: str
    currency: str

    def __init__(self, value: str, currency: str) -> None:
        self.value = value
        self.currency = currency


class Account:
    uuid: UUID
    name: str
    currency: str
    available_balance: AvailableBalance
    default: bool
    active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    type: str
    ready: bool
    hold: AvailableBalance

    error: dict

    def __init__(
            self, uuid: UUID, name: str, currency: str, available_balance: dict, default: bool,
        active: bool, created_at: datetime, updated_at: datetime, deleted_at: datetime, type: str, ready: bool,
            hold: dict,  error=None) -> None:
        self.uuid = uuid
        self.name = name
        self.currency = currency
        self.available_balance = AvailableBalance(**available_balance) if available_balance is not None else None
        self.default = default
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.type = type
        self.ready = ready
        self.hold = AvailableBalance(**hold) if hold is not None else None

        self.error = error

    @classmethod
    def from_response(cls, response: requests.Response) -> 'Account':

        if not response.ok:
            error_result = json.loads(response.text)
            return cls(None, None, None, None, None, None, None, None, None, None, None, None, error=error_result)

        result = json.loads(response.text)
        account_dict = result['account']
        return cls(**account_dict)


class AccountsPage:
    accounts: List[Account]
    has_next: bool
    cursor: str
    size: int

    error: dict

    def __init__(self,
                 accounts: List[dict],
                 has_next: bool,
                 cursor: str,
                 size: int,
                 error=None) -> None:

        self.accounts = list(map(lambda x: Account(**x), accounts)) if accounts is not None else None

        self.has_next = has_next
        self.cursor = cursor
        self.size = size

        self.error = error

    @classmethod
    def from_response(cls, response: requests.Response) -> 'AccountsPage':

        if not response.ok:
            error_result = json.loads(response.text)
            return cls(None, None, None, None, error=error_result)

        result = json.loads(response.text)
        return cls(**result)
