from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData

_FALLBACK_REST_PATHS = {
    "get_server_time": "GET /api/v1/serverTime",
    "get_exchange_info": "GET /coins",
    "get_tick": "GET /ticker",
    "get_depth": "GET /orderBook",
    "get_kline": "GET /kline",
    "get_trades": "GET /recentTrades",
    "make_order": "POST /api/v2/orders",
    "cancel_order": "POST /api/v2/cancel",
    "query_order": "GET /api/v2/orderStatus",
    "get_open_orders": "GET /api/v2/orders",
    "get_balance": "GET /api/v1/currentCoinBalance/EVERYTHING",
    "get_account": "GET /api/v1/currentCoinBalance/EVERYTHING",
}


class BitbnsExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "bitbns"
        self.rest_url = "https://api.bitbns.com"
        self.wss_url = "wss://ws.bitbns.com"
        self.rest_paths = dict(_FALLBACK_REST_PATHS)
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "2h": "2h",
            "4h": "4h",
            "6h": "6h",
            "12h": "12h",
            "1d": "1d",
            "1w": "1w",
        }
        self.legal_currency = ["INR", "USDT"]

    def get_symbol(self, symbol: str) -> str:
        sym = symbol.upper()
        if "_" in sym:
            return sym
        if "/" in sym:
            return sym.replace("/", "_")
        if "-" in sym:
            return sym.replace("-", "_")
        return sym

    def get_period(self, key: str) -> str:
        return self.kline_periods.get(key, key)

    def get_rest_path(self, key: str, **kwargs) -> str:
        if key not in self.rest_paths or self.rest_paths[key] == "":
            raise ValueError(f"[{self.exchange_name}] REST path not found: {key}")
        return self.rest_paths[key]


class BitbnsExchangeDataSpot(BitbnsExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
