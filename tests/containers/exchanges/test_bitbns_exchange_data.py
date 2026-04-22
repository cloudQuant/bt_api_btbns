"""Tests for BitbnsExchangeData container."""

from __future__ import annotations

from bt_api_bitbns.exchange_data import BitbnsExchangeData


class TestBitbnsExchangeData:
    """Tests for BitbnsExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = BitbnsExchangeData()

        assert exchange.exchange_name == "bitbns"
        assert "bitbns.com" in exchange.rest_url
