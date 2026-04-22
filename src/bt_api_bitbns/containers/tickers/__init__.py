from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float


class BitbnsTickerData(TickerData):
    def __init__(
        self,
        ticker_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "BITBNS"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_data: dict[str, Any] | None = (
            ticker_info if has_been_json_encoded and isinstance(ticker_info, dict) else None
        )
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.volume: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> BitbnsTickerData:
        if not self.has_been_json_encoded:
            self.ticker_data = (
                json.loads(self.ticker_info)
                if isinstance(self.ticker_info, str)
                else self.ticker_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = self.ticker_data or {}
        nested = data.get("data", {}) if isinstance(data, dict) else {}
        ticker = nested if isinstance(nested, dict) else {}
        if isinstance(ticker, dict):
            symbol = self.symbol_name.upper().replace("_USDT", "").replace("_INR", "")
            market_data = ticker.get(symbol, ticker)
            if isinstance(market_data, dict):
                self.ticker_symbol_name = market_data.get("symbol") or self.symbol_name
                self.last_price = from_dict_get_float(market_data, "lastPrice")
                self.bid_price = from_dict_get_float(market_data, "bidPrice")
                self.ask_price = from_dict_get_float(market_data, "askPrice")
                self.high = from_dict_get_float(market_data, "high")
                self.low = from_dict_get_float(market_data, "low")
                self.volume = from_dict_get_float(market_data, "volume")

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_local_update_time(self) -> float:
        return self.local_update_time

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_ticker_symbol_name(self) -> str | None:
        self.init_data()
        return self.ticker_symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_server_time(self) -> float | None:
        return None

    def get_bid_price(self) -> float | None:
        self.init_data()
        return self.bid_price

    def get_ask_price(self) -> float | None:
        self.init_data()
        return self.ask_price

    def get_bid_volume(self) -> float | None:
        return None

    def get_ask_volume(self) -> float | None:
        return None

    def get_last_price(self) -> float | None:
        self.init_data()
        return self.last_price

    def get_last_volume(self) -> float | None:
        self.init_data()
        return self.volume


class BitbnsRequestTickerData(BitbnsTickerData):
    pass


class BitbnsWssTickerData(BitbnsTickerData):
    pass


__all__ = ["BitbnsTickerData", "BitbnsRequestTickerData", "BitbnsWssTickerData"]
