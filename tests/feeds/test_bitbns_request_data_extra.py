from __future__ import annotations

from unittest.mock import MagicMock

from bt_api_bitbns.feeds.live_bitbns.request_base import BitbnsRequestData


def test_bitbns_disconnect_closes_http_client() -> None:
    request_data = BitbnsRequestData()
    request_data._http_client.close = MagicMock()

    request_data.disconnect()

    request_data._http_client.close.assert_called_once_with()


def test_bitbns_accepts_public_private_key_aliases() -> None:
    request_data = BitbnsRequestData(public_key="public-key", private_key="secret-key")
    headers = request_data._get_headers("GET", "/api/trade/v1/orders")

    assert request_data._params.api_key == "public-key"
    assert request_data._params.api_secret == "secret-key"
    assert headers["X-API-KEY"] == "public-key"
