# Coinbase Advanced
Python library for the Coinbase Advanced Trade API.

## Features
- Support for all the [REST API endpoints](https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-overview) through convenient methods.
- Automatic parsing of API responses into relevant Python objects.
- Unit Tests based on real responses using fixtures.
- [Support for Cloud and Legacy Auth Schemas](https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-auth):
   -  Support for [Cloud API Trading Keys](https://cloud.coinbase.com/access/api) (Recommended)
   -  Support for [Legacy API Keys](https://www.coinbase.com/settings/api) (Deprecated but supported in this library for backward compatibility reasons)

## Example
```
from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient

# Creating the client using Clould API Keys.
client = CoinbaseAdvancedTradeAPIClient.from_cloud_api_keys(API_KEY_NAME, PRIVATE_KEY)

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
