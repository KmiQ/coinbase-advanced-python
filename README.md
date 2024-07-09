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

## Websocket usage

Here is a basic example of how to use the CoinbaseWebSocketClient:

```
import asyncio
import time
from client_websocket import CoinbaseWebSocketClient

def handle_candle_event(event):
    print(f"Received event candle: {event}")

async def main():
    api_key = "your-api-key"
    private_key = "-----BEGIN EC PRIVATE KEY-----\n\n-----END EC PRIVATE KEY-----"
    
    client = CoinbaseWebSocketClient(api_key, private_key)
    client.subscribe(["BTC-EUR"], "candles", callback=handle_candle_event)
    
    while True:
        time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

```

### Callback Functions
You can define your own callback functions to handle different types of events. The callback function will receive an event object that you can process as needed.

### Heartbeat Subscription
For each subscription to a market data channel, a separate heartbeat subscription is automatically created. This helps to ensure that the connection remains open and active.

### Concurrency
Each subscription runs in a separate thread to ensure that multiple subscriptions can operate concurrently without blocking each other.

### Coinbase API Rate Limits
Before using this library, it is highly recommended to read the Coinbase API rate limits (https://docs.cdp.coinbase.com/advanced-trade/docs/ws-best-practices/) to understand the constraints and avoid exceeding the limits.

### Best Practices
It is also recommended to follow the WebSocket best practices (https://docs.cdp.coinbase.com/advanced-trade/docs/ws-best-practices/) provided by Coinbase for optimal performance and reliability.

### Subscription Recommendations
If possible, subscribe to one symbol per subscription to help balance the load on the Coinbase server and improve the reliability of your data stream.

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
