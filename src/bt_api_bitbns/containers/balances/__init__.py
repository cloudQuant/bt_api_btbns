from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class BitbnsBalanceData(BalanceData):
    def __init__(
        self,
        balance_info: Any,
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "BITBNS"
        self.asset_type = asset_type
        self.balance_data: dict[str, Any] | None = balance_info if has_been_json_encoded else None
        self.currency: str | None = None
        self.available: float | None = None
        self.locked: float | None = None
        self.local_update_time = time.time()
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> BitbnsBalanceData:
        if not self.has_been_json_encoded:
            self.balance_data = (
                json.loads(self.balance_info)
                if isinstance(self.balance_info, str)
                else self.balance_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.balance_data, dict):
            self.currency = from_dict_get_string(self.balance_data, "currency")
            self.available = from_dict_get_float(self.balance_data, "available", 0.0)
            self.locked = from_dict_get_float(self.balance_data, "locked", 0.0)

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "asset_type": self.asset_type,
            "local_update_time": self.local_update_time,
            "currency": self.currency,
            "available": self.available,
            "locked": self.locked,
            "total": self.get_total(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_server_time(self) -> float | None:
        return None

    def get_local_update_time(self) -> float | None:
        return self.local_update_time

    def get_asset_type(self) -> str | None:
        return self.asset_type

    def get_currency(self) -> str | None:
        self.init_data()
        return self.currency

    def get_available(self) -> float | None:
        self.init_data()
        return self.available

    def get_locked(self) -> float | None:
        self.init_data()
        return self.locked

    def get_total(self) -> float:
        return (self.available or 0.0) + (self.locked or 0.0)

    def is_zero_balance(self) -> bool:
        return self.get_total() == 0.0

    def get_account_id(self) -> str | None:
        return None

    def get_account_type(self) -> str | None:
        return None

    def get_fee_tier(self) -> int | str | None:
        return None

    def get_max_withdraw_amount(self) -> float | None:
        return None

    def get_margin(self) -> float | None:
        return None

    def get_used_margin(self) -> float | None:
        return None

    def get_maintain_margin(self) -> float | None:
        return None

    def get_available_margin(self) -> float | None:
        return None

    def get_open_order_initial_margin(self) -> float | None:
        return None

    def get_open_order_maintenance_margin(self) -> float | None:
        return None

    def get_position_initial_margin(self) -> float | None:
        return None

    def get_position_maintenance_margin(self) -> float | None:
        return None

    def get_unrealized_profit(self) -> float | None:
        return None

    def get_wallet_balance(self) -> float | None:
        return self.get_total()

    def get_equity(self) -> float | None:
        return self.get_total()

    def get_cross_wallet_balance(self) -> float | None:
        return None

    def get_cross_unrealized_pnl(self) -> float | None:
        return None

    def get_available_balance(self) -> float | None:
        return self.get_available()

    def get_max_withdrawal_balance(self) -> float | None:
        return self.get_available()


class BitbnsRequestBalanceData(BitbnsBalanceData):
    pass


class BitbnsWssBalanceData(BitbnsBalanceData):
    pass
