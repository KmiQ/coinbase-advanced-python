import hmac
import hashlib
import time
import requests
import json

from models.accounts import AccountsPage, Account
from models.orders import Order


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

    def create_order(self, client_order_id: str, product_id: str, side: str, order_configuration: dict) -> Order:
        request_path = "/api/v3/brokerage/orders"
        method = "POST"

        payload = {
            'client_order_id': client_order_id,
            'product_id': product_id,
            'side': side,
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

order_configuration = {
    "limit_limit_gtc": {
        "limit_price": ".19",
        "base_size": "5"
    }
}
order = client.create_order("nkjsdfnw23", "ALGO-USD", "SELL", order_configuration)

if order.error:
    print(order.error)
