import hmac
import hashlib
import time
import requests
import json

from enum import Enum
from datetime import datetime
from models.accounts import AccountsPage, Account
from models.orders import Order


class SIDE(Enum):
    BUY = "BUY"
    SELL = "SELL"


class STOP_DIRECTION(Enum):
    UNKNOWN = "UNKNOWN_STOP_DIRECTION"
    UP = "STOP_DIRECTION_STOP_UP"
    DOWN = "STOP_DIRECTION_STOP_DOWN"


class CoinbaseAdvancedTradeAPIClient(object):
    def __init__(self, api_key: str, secret_key: str, base_url: str = 'https://coinbase.com') -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._secret_key = secret_key

    # Accounts #

    def list_accounts(self, limit: int = 49, cursor: str = None) -> AccountsPage:
        request_path = '/api/v3/brokerage/accounts'
        method = "GET"
        query_params = '?limit='+str(limit)

        if cursor is not None:
            query_params = query_params + '&cursor='+cursor

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path+query_params, headers=headers)

        page = AccountsPage.from_response(response)
        return page

    def get_account(self, account_id: str) -> Account:
        request_path = f"/api/v3/brokerage/accounts/{account_id}"
        method = "GET"

        headers = self._build_request_headers(method, request_path)

        response = requests.get(self._base_url+request_path, headers=headers)

        account = Account.from_response(response)
        return account

    # Orders #

    def create_buy_market_order(self, client_order_id: str, product_id: str, quote_size: float):
        order_configuration = {
            "market_market_ioc": {
                "quote_size": str(quote_size),
            }
        }

        return self.create_order(client_order_id, product_id, SIDE.BUY, order_configuration)

    def create_sell_market_order(self, client_order_id: str, product_id: str, base_size: float):
        order_configuration = {
            "market_market_ioc": {
                "base_size": str(base_size),
            }
        }

        return self.create_order(client_order_id, product_id, SIDE.SELL, order_configuration)

    def create_limit_order(
            self, client_order_id: str, product_id: str, side: SIDE, limit_price: float, base_size: float,
            cancel_time: datetime = None, post_only: bool = None):

        order_configuration = {}

        limit_order_configuration = {
            "limit_price": str(limit_price),
            "base_size": str(base_size),
        }

        if post_only is not None:
            limit_order_configuration['post_only'] = post_only

        if cancel_time is not None:
            limit_order_configuration['end_time'] = cancel_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            order_configuration['limit_limit_gtd'] = limit_order_configuration
        else:
            order_configuration['limit_limit_gtc'] = limit_order_configuration

        return self.create_order(client_order_id, product_id, side, order_configuration)

    def create_stop_limit_order(
            self, client_order_id: str, product_id: str, side: SIDE, stop_price: float, stop_direction: STOP_DIRECTION,
            limit_price: float, base_size: float, cancel_time: datetime = None):

        order_configuration = {}

        stop_limit_order_configuration = {
            "stop_price": str(stop_price),
            "limit_price": str(limit_price),
            "base_size": str(base_size),
            "stop_direction": stop_direction.value,
        }

        if cancel_time is not None:
            stop_limit_order_configuration['end_time'] = cancel_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            order_configuration['stop_limit_stop_limit_gtd'] = stop_limit_order_configuration
        else:
            order_configuration['stop_limit_stop_limit_gtc'] = stop_limit_order_configuration

        return self.create_order(client_order_id, product_id, side, order_configuration)

    def create_order(self, client_order_id: str, product_id: str, side: SIDE, order_configuration: dict) -> Order:
        request_path = "/api/v3/brokerage/orders"
        method = "POST"

        payload = {
            'client_order_id': client_order_id,
            'product_id': product_id,
            'side': side.value,
            'order_configuration': order_configuration
        }

        headers = self._build_request_headers(method, request_path, json.dumps(payload))
        response = requests.post(self._base_url+request_path, json=payload, headers=headers)

        order = Order.from_response(response)
        return order

    # Helpers #

    def _build_request_headers(self, method, request_path, body=''):
        timestamp = str(int(time.time()))

        message = timestamp+method+request_path+body
        signature = self._create_signature(message)

        return {
            "accept": "application/json",
            'CB-ACCESS-KEY': self._api_key,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-SIGN': signature,
        }

    def _create_signature(self, message):
        signature = hmac.new(
            self._secret_key.encode('utf-8'),
            message.encode('utf-8'),
            digestmod=hashlib.sha256).digest().hex()

        return signature


#################### TESTING ####################

# For Reading
#client = CoinbaseAdvancedTradeAPIClient(api_key='hOOnWpN0x2zsu12i', secret_key='86s3z4DLYrFCw4QonF54u4CdirrbBSnw')

# Full Access to ALGO Wallet
client = CoinbaseAdvancedTradeAPIClient(api_key='Jk31IAjyWQEG3BfP', secret_key='HUbLt2GsnPOTTkl0t2wkFWn4RrznDJRM')

# page = client.list_accounts()  # Accounts: List Accounts

# if page.error:
#    print(page.error)
# else:
#    accounts = page.accounts
#    for a in accounts:
#        if a.name == 'BTC Wallet':
#            print(a.hold)


############

#account = client.get_account('b044449a-38a3-5b8f-a506-4a65c9853222')

# if account.error:
#    print(account.error)
# else:
#    print(account.name)

############

#order = client.create_order("nkjsdfnw23", "ALGO-USD", "SELL", order_configuration)

#order = client.create_limit_order("jalksjd341", "ALGO-USD", "BUY", ".19", 5)

# order = client.create_stop_limit_order("nkjansd89hasi", "ALGO-USD", "BUY", .18,
#                                       "STOP_DIRECTION_STOP_DOWN", .16, 7, datetime(2023, 1, 9, 15))

order = client.create_buy_market_order("asdasd", "ALGO-USD", 3)
#order = client.create_sell_market_order("njkasdh7", "ALGO-USD", 5)

if order.error:
    print(order.error)
