import json
import random
import string

from dotenv import load_dotenv
import os

from datetime import datetime, timezone

from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient, Side, StopDirection, Granularity

from tests.fixtures.fixtures import *

load_dotenv()  # Load environment variables from a .env file

# Cloud API Trading Keys (NEW/Recommended): https://cloud.coinbase.com/access/api
# API_KEY_NAME = os.getenv('API_KEY_NAME')
# PRIVATE_KEY = os.getenv('PRIVATE_KEY').replace('\\n', '\n')
API_KEY_NAME = os.getenv('API_KEY_NAME_FULL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY_FULL').replace('\\n', '\n')

# Legacy API Keys: https://www.coinbase.com/settings/api
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# A real Account Id (ALGO WALLET ID, BTC WALLET ID, or ETH WALLET ID, etc...)
ACCOUNT_ID = os.getenv('ACCOUNT_ID')


def generate_random_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))


def audit(func, args, fixture_obj):
    print(f"endpoint: {func.__name__}")
    result_obj = func() if args is None else func(**args)

    # Checking if Coinbase is returning more items that expected.
    if result_obj.kwargs:
        print(f"  - Response => Object: NEED UPDATE")

    # Checking fixtures files are updated.
    result_obj_atttributes = [
        attr for attr, v in result_obj.__dict__.items()
        if v is not None and not attr.startswith('__') and not callable(attr) and attr != 'kwargs']
    for k in result_obj_atttributes:
        if not k in fixture_obj:
            print(
                f"  - Response => Fixtures: NEED UPDATE, key '{k}' present in live response but not found in fixture.")


# Creating the client per authentication methods.
# client = CoinbaseAdvancedTradeAPIClient.from_legacy_api_keys(API_KEY, SECRET_KEY)
client = CoinbaseAdvancedTradeAPIClient.from_cloud_api_keys(
    API_KEY_NAME, PRIVATE_KEY)
print()

# Accounts

# audit(client.list_accounts, None, json.loads(fixture_list_accounts_success_response().text))
# audit(client.list_accounts_all, None, json.loads(fixture_list_accounts_all_call_1_success_response().text))
# audit(client.get_account, {'account_id': ACCOUNT_ID},
#      json.loads(fixture_get_account_success_response().text)['account'])

# Orders

# Check and Verify here: https://www.coinbase.com/orders)
# when running this section.

# Unccoment below for runnig the post function which are usually commented

# fixture_obj = json.loads(fixture_create_limit_order_success_response().text)
# fixture_obj['success_response']['order_configuration'] = fixture_obj['order_configuration']
# fixture_obj = fixture_obj['success_response']
# audit(client.create_limit_order, {
#     'client_order_id': generate_random_id(),
#     'product_id': "ALGO-USD",
#     'side': Side.BUY,
#     'limit_price': ".15",
#     'base_size': 1000
# },
#     fixture_obj
# )

# audit(client.cancel_orders, {'order_ids': ["42a266d3-591b-43d4-a968-a9a126f7b1a5", "82c6919f-6884-4127-95af-11db89b21ed3",
#       "c1d5ab66-d99a-4329-9c1d-be6a9f32c686"]}, json.loads(fixture_cancel_orders_success_response().text))

# audit(client.list_orders, {'start_date': datetime(2023, 1, 25),
#                            'end_date': datetime(2023, 1, 30),
#                            'limit': 10}, json.loads(fixture_list_orders_success_response().text))

# audit(client.list_orders_all, {'start_date': datetime(2023, 1, 25),
#                                'end_date': datetime(2023, 1, 30),
#                                'limit': 10}, json.loads(fixture_list_orders_all_call_1_success_response().text))

# audit(client.list_fills, {'start_date': datetime(2023, 1, 25),
#                           'end_date': datetime(2023, 1, 30),
#                           'limit': 10}, json.loads(fixture_list_fills_success_response().text))

# audit(client.list_fills_all, {'start_date': datetime(2023, 1, 25),
#                               'end_date': datetime(2023, 1, 30),
#                               'limit': 10}, json.loads(fixture_list_fills_all_call_1_success_response().text))

# audit(client.get_order, {'order_id': 'c1d5ab66-d99a-4329-9c1d-be6a9f32c686'},
#       json.loads(fixture_get_order_success_response().text)['order'])

# Products

# audit(client.list_products, {'limit': 5},
#       json.loads(fixture_list_products_success_response().text))

# audit(client.get_product_candles, {
#     'product_id': "ALGO-USD",
#     'start_date': datetime(2023, 1, 1, tzinfo=timezone.utc),
#     'end_date': datetime(2023, 1, 31, tzinfo=timezone.utc),
#     'granularity': Granularity.ONE_DAY},
#     json.loads(fixture_get_product_candles_success_response().text))

# audit(client.get_product_candles_all, {
#     'product_id': "ALGO-USD",
#     'start_date': datetime(2023, 1, 1, tzinfo=timezone.utc),
#     'end_date': datetime(2023, 1, 31, tzinfo=timezone.utc),
#     'granularity': Granularity.ONE_DAY},
#     json.loads(fixture_get_product_candles_all_call_1_success_response().text))

# audit(client.get_market_trades, {
#     'product_id': "ALGO-USD",
#     'limit': 10},
#     json.loads(fixture_get_trades_success_response().text))

# audit(client.get_best_bid_ask, {"product_ids": ["BTC-USD", "ETH-USD"]},
#       json.loads(fixture_get_best_bid_asks_success_response().text))

# audit(client.get_product_book, {"product_id": "BTC-USD", "limit": 5},
#      json.loads(fixture_product_book_success_response().text))

# Fees

# audit(client.get_transactions_summary, {
#     'start_date': datetime(2023, 1, 1, tzinfo=timezone.utc),
#     'end_date': datetime(2023, 1, 31, tzinfo=timezone.utc)},
#     json.loads(fixture_get_transactions_summary_success_response().text))

# Portfolios

# audit(client.list_portfolios, {},
#      json.loads(fixture_list_portfolios_success_response().text))

# audit(client.create_portfolio, {'name': 'test-portfolio-name-2'},
#      json.loads(fixture_create_portfolio_success_response().text)['portfolio'])

# audit(client.edit_portfolio, {'portfolio_uuid': '354808f3-06df-42d7-87ec-488f34ff6f14', 'name': 'test-edit-portfolio-name'},
#      json.loads(fixture_create_portfolio_success_response().text)['portfolio'])

# EXPECTED: "Response => Fixtures: NEED UPDATE, key 'success' present in live response but not found in fixture."
# audit(client.delete_portfolio, {'portfolio_uuid': 'a78767c7-6d83-4c0c-a736-7f70ef866324'},
#      json.loads(fixture_delete_portfolio_success_response().text))

# Common
# audit(client.get_unix_time, {},
#      json.loads(fixture_get_unix_time_success_response().text))
