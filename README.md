# Coinbase Advanced
Python library for the Coinbase Advanced Trade API.

## Features
- Support for all the [REST API endpoints](https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-overview) trough convenient methods.
- Automatic parsing of API responses into relevant Python objects.
- Support for [API Key](https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-auth) authentication.

## Example
```
from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient

# Creating the client.
client = CoinbaseAdvancedTradeAPIClient(api_key='apikeyhere', secret_key='yoursecrethere')

# Listing accounts.
accounts_page = client.list_accounts()
print(accounts_page.size)

# Creating a limit order.
order_created = client.create_limit_order(client_order_id="lknalksdj89asdkl", product_id="ALGO-USD", side=Side.BUY, limit_price=".19", base_size=5)
```

## Installation
```
pip install coinbaseadvanced
```
## Contributing/Development
Any and all contributions are welcome! The process is simple:
  1. Fork repo.
  2. Install Requirements: `pip install -r requirements.txt`.
  3. Make your changes.
  4. Run the test suite `python -m unittest -v`.
  5. Submit a pull request.
