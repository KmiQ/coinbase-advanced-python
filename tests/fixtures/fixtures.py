from unittest import mock


def _fixtured_mock_response(
        ok: bool,
        text: str) -> mock.Mock:
    """
    since we typically test a bunch of different
    requests calls for a service, we are going to do
    a lot of mock responses, so its usually a good idea
    to have a helper function that builds these things
    """
    mock_resp = mock.Mock()
    # set status code and content
    mock_resp.ok = ok
    mock_resp.text = text

    return mock_resp


def fixture_get_account_success_response() -> mock.Mock:
    with open('tests/fixtures/get_account_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_default_failure_response() -> mock.Mock:
    with open('tests/fixtures/default_failure_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=False,
            text=content)


def fixture_list_accounts_success_response() -> mock.Mock:
    with open('tests/fixtures/list_accounts_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_accounts_all_call_1_success_response() -> mock.Mock:
    with open('tests/fixtures/list_accounts_all_call_1_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_accounts_all_call_2_success_response() -> mock.Mock:
    with open('tests/fixtures/list_accounts_all_call_2_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_create_limit_order_success_response() -> mock.Mock:
    with open('tests/fixtures/create_limit_order_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_create_stop_limit_order_success_response() -> mock.Mock:
    with open('tests/fixtures/create_stop_limit_order_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_create_buy_market_order_success_response() -> mock.Mock:
    with open('tests/fixtures/create_buy_market_order_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_create_sell_market_order_success_response() -> mock.Mock:
    with open('tests/fixtures/create_sell_market_order_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_default_order_failure_response() -> mock.Mock:
    with open('tests/fixtures/default_order_failure_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=False,
            text=content)


def fixture_order_failure_no_funds_response() -> mock.Mock:
    with open('tests/fixtures/create_order_failure_no_funds_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_cancel_orders_success_response() -> mock.Mock:
    with open('tests/fixtures/cancel_orders_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_orders_success_response() -> mock.Mock:
    with open('tests/fixtures/list_orders_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_orders_all_call_1_success_response() -> mock.Mock:
    with open('tests/fixtures/list_orders_all_call_1_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_orders_all_call_2_success_response() -> mock.Mock:
    with open('tests/fixtures/list_orders_all_call_2_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_orders_with_extra_unnamed_success_response() -> mock.Mock:
    with open('tests/fixtures/list_orders_with_extra_unnamed_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_fills_success_response() -> mock.Mock:
    with open('tests/fixtures/list_fills_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_fills_all_call_1_success_response() -> mock.Mock:
    with open('tests/fixtures/list_fills_all_call_1_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_fills_all_call_2_success_response() -> mock.Mock:
    with open('tests/fixtures/list_fills_all_call_2_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_order_success_response() -> mock.Mock:
    with open('tests/fixtures/get_order_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_list_products_success_response() -> mock.Mock:
    with open('tests/fixtures/list_products_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_product_success_response() -> mock.Mock:
    with open('tests/fixtures/get_product_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_product_candles_success_response() -> mock.Mock:
    with open('tests/fixtures/get_product_candles_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_product_candles_all_call_1_success_response() -> mock.Mock:
    with open('tests/fixtures/get_product_candles_all_call_1_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_product_candles_all_call_2_success_response() -> mock.Mock:
    with open('tests/fixtures/get_product_candles_all_call_2_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_product_candles_all_call_3_success_response() -> mock.Mock:
    with open('tests/fixtures/get_product_candles_all_call_3_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_best_bid_asks_success_response() -> mock.Mock:
    with open('tests/fixtures/get_best_bid_ask_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_trades_success_response() -> mock.Mock:
    with open('tests/fixtures/get_trades_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)


def fixture_get_transactions_summary_success_response() -> mock.Mock:
    with open('tests/fixtures/get_transactions_summary_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return _fixtured_mock_response(
            ok=True,
            text=content)
