from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient

from bt_api_bitbns.exchange_data import BitbnsExchangeDataSpot


class BitbnsRequestData(Feed):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "BITBNS___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = BitbnsExchangeDataSpot()
        self._params.api_key = str(kwargs.get("public_key") or kwargs.get("api_key") or "")
        self._params.api_secret = str(
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret") or "",
        )
        self.request_logger = self.logger
        self.async_logger = self.logger
        self._http_client = HttpClient(venue=self.exchange_name, timeout=10)

    def _generate_signature(self, timestamp, body=""):
        secret = self._params.api_secret
        if secret:
            message = str(timestamp) + body
            return hmac.new(
                secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha512,
            ).hexdigest()
        return ""

    def _get_headers(self, method: str, request_path: str, params=None, body: str = ""):
        headers = {"Content-Type": "application/json"}
        if self._params.api_key:
            timestamp = int(time.time() * 1000)
            body_str = body if body else ""
            signature = self._generate_signature(timestamp, body_str)
            headers.update(
                {
                    "X-API-KEY": self._params.api_key,
                    "X-API-SIGNATURE": signature,
                    "X-API-TIMESTAMP": str(timestamp),
                },
            )
        return headers

    def _get_base_url(self, path):
        if path.startswith("GET /") and not self._params.api_key:
            return "https://api.bitbns.com/api/trade/v1"
        return self._params.rest_url

    def request(self, path, params=None, body=None, extra_data=None, timeout=10):
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path
        headers = self._get_headers(
            method, request_path, params, body if isinstance(body, str) else "",
        )
        base_url = self._get_base_url(path)

        try:
            response = self._http_client.request(
                method=method,
                url=base_url + request_path,
                headers=headers,
                json_data=body if method == "POST" and isinstance(body, dict) else None,
                params=params,
            )
            return self._process_response(response, extra_data)
        except Exception as e:
            self.request_logger.error(f"Request failed: {e}")
            raise

    async def async_request(self, path, params=None, body=None, extra_data=None, timeout=5):
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path
        headers = self._get_headers(
            method, request_path, params, body if isinstance(body, str) else "",
        )
        base_url = self._get_base_url(path)

        try:
            response = await self._http_client.async_request(
                method=method,
                url=base_url + request_path,
                headers=headers,
                json_data=body if method == "POST" and isinstance(body, dict) else None,
                params=params,
            )
            return self._process_response(response, extra_data)
        except Exception as e:
            self.async_logger.error(f"Async request failed: {e}")
            raise

    def async_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as e:
            self.async_logger.error(f"Async callback error: {e}")

    def _process_response(self, response, extra_data=None):
        if extra_data is None:
            extra_data = {}
        return RequestData(response, extra_data)

    def push_data_to_queue(self, data):
        if self.data_queue is not None:
            self.data_queue.put(data)

    def connect(self):
        pass

    def disconnect(self):
        super().disconnect()

    def is_connected(self):
        return True

    def _get_server_time(self, extra_data=None, **kwargs):
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_server_time",
            },
        )
        return "GET /api/v1/serverTime", {}, extra_data

    def get_server_time(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_server_time(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_tick(self, symbol, extra_data=None, **kwargs):
        sym = symbol.upper()
        if "_" in sym:
            base, market = (
                sym.replace("_USDT", "").replace("_INR", ""),
                "USDT" if "_USDT" in sym else "INR",
            )
        else:
            base, market = sym, "USDT"
        path = "GET /ticker"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_tick",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_tick_normalize_function,
            },
        )
        params = {"symbol": base, "market": market}
        return path, params, extra_data

    @staticmethod
    def _get_tick_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        data = input_data.get("data", {})
        if data and input_data.get("status") == 1:
            return [data], True
        return [], False

    def get_tick(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_tick(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        sym = symbol.upper()
        if "_" in sym:
            base, market = (
                sym.replace("_USDT", "").replace("_INR", ""),
                "USDT" if "_USDT" in sym else "INR",
            )
        else:
            base, market = sym, "USDT"
        path = "GET /orderBook"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_depth",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_depth_normalize_function,
            },
        )
        params = {"symbol": base, "market": market}
        return path, params, extra_data

    @staticmethod
    def _get_depth_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        data = input_data.get("data", {})
        if data and input_data.get("status") == 1:
            return [data], True
        return [], False

    def get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_kline(self, symbol, period="1m", count=20, extra_data=None, **kwargs):
        sym = symbol.upper()
        if "_" in sym:
            base, market = (
                sym.replace("_USDT", "").replace("_INR", ""),
                "USDT" if "_USDT" in sym else "INR",
            )
        else:
            base, market = sym, "USDT"
        path = "GET /kline"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_kline",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "period": period,
                "normalize_function": self._get_kline_normalize_function,
            },
        )
        params = {"symbol": base, "market": market, "period": period, "page": 1}
        return path, params, extra_data

    @staticmethod
    def _get_kline_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        data = input_data.get("data", [])
        if data and input_data.get("status") == 1:
            return [data], True
        return [], False

    def get_kline(self, symbol, period="1m", count=20, extra_data=None, **kwargs):
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_kline(self, symbol, period="1m", count=20, extra_data=None, **kwargs):
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_exchange_info(self, extra_data=None, **kwargs):
        path = "GET /coins"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_exchange_info",
                "symbol_name": "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_exchange_info_normalize_function,
            },
        )
        return path, None, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        data = input_data.get("data", {})
        if data and input_data.get("status") == 1:
            return [data] if not isinstance(data, list) else data, True
        return [], False

    def get_exchange_info(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _make_order(
        self,
        symbol,
        volume,
        price,
        order_type="buy-limit",
        offset="open",
        post_only=False,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        sym = symbol.upper()
        if "_" in sym:
            base, market = (
                sym.replace("_USDT", "").replace("_INR", ""),
                "USDT" if "_USDT" in sym else "INR",
            )
        else:
            base, market = sym, "USDT"
        path = "POST /api/v2/orders"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "make_order",
            },
        )
        params = {
            "symbol": base,
            "market": market,
            "side": offset if offset in ("buy", "sell") else "buy",
            "type": order_type,
            "quantity": str(volume),
            "rate": str(price),
        }
        return path, params, extra_data

    def make_order(
        self,
        symbol,
        volume,
        price,
        order_type="buy-limit",
        offset="open",
        post_only=False,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        path, params, extra_data = self._make_order(
            symbol,
            volume,
            price,
            order_type,
            offset,
            post_only,
            client_order_id,
            extra_data,
            **kwargs,
        )
        return self.request(path, params=params, extra_data=extra_data)

    def _cancel_order(self, symbol, order_id, extra_data=None, **kwargs):
        sym = symbol.upper()
        if "_" in sym:
            base, market = (
                sym.replace("_USDT", "").replace("_INR", ""),
                "USDT" if "_USDT" in sym else "INR",
            )
        else:
            base, market = sym, "USDT"
        path = "POST /api/v2/cancel"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "cancel_order",
                "order_id": order_id,
            },
        )
        params = {"symbol": base, "market": market, "entry_id": order_id}
        return path, params, extra_data

    def cancel_order(self, symbol, order_id, extra_data=None, **kwargs):
        path, params, extra_data = self._cancel_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _query_order(self, symbol, order_id, extra_data=None, **kwargs):
        sym = symbol.upper()
        if "_" in sym:
            base, market = (
                sym.replace("_USDT", "").replace("_INR", ""),
                "USDT" if "_USDT" in sym else "INR",
            )
        else:
            base, market = sym, "USDT"
        path = "GET /api/v2/orderStatus"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "query_order",
                "order_id": order_id,
            },
        )
        params = {"symbol": base, "market": market, "entry_id": order_id}
        return path, params, extra_data

    def query_order(self, symbol, order_id, extra_data=None, **kwargs):
        path, params, extra_data = self._query_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        path = "GET /api/v2/orders"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_open_orders",
            },
        )
        params = {}
        if symbol:
            sym = symbol.upper()
            if "_" in sym:
                base, market = (
                    sym.replace("_USDT", "").replace("_INR", ""),
                    "USDT" if "_USDT" in sym else "INR",
                )
            else:
                base, market = sym, "USDT"
            params = {"symbol": base, "market": market}
        return path, params, extra_data

    def get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra_data = self._get_open_orders(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_account(self, symbol=None, extra_data=None, **kwargs):
        path = "GET /api/v1/currentCoinBalance/EVERYTHING"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_account",
            },
        )
        return path, None, extra_data

    def get_account(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra_data = self._get_account(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_balance(self, symbol=None, extra_data=None, **kwargs):
        path = "GET /api/v1/currentCoinBalance/EVERYTHING"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_balance",
            },
        )
        return path, None, extra_data

    def get_balance(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra_data = self._get_balance(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)
