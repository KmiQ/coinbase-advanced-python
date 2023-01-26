from unittest import mock


def fixtured_mock_response(
        ok: bool,
        text: str):
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


def fixture_get_account_success_response() -> str:
    with open('tests/fixtures/get_account_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return fixtured_mock_response(
            ok=True,
            text=content)


def fixture_standard_failure_response() -> str:
    with open('tests/fixtures/default_failure_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return fixtured_mock_response(
            ok=False,
            text=content)


def fixture_list_accounts_success_response() -> str:
    with open('tests/fixtures/list_accounts_success_response.json', 'r', encoding="utf-8") as file:
        content = file.read()
        return fixtured_mock_response(
            ok=True,
            text=content)
