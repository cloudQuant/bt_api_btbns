from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.accounts.account import AccountData


class BitbnsAccountData(AccountData):
    def __init__(
        self,
        account_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(account_info, has_been_json_encoded)
        self.exchange_name = "BITBNS"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.account_data: dict[str, Any] | str | None = (
            account_info if has_been_json_encoded else None
        )
        self.balances: list[Any] = []
        self.has_been_init_data = False

    def init_data(self) -> BitbnsAccountData:
        if not self.has_been_json_encoded:
            self.account_data = (
                json.loads(self.account_info)
                if isinstance(self.account_info, str)
                else self.account_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.account_data, dict):
            balances = self.account_data.get("balance", self.account_data.get("balances", []))
            if isinstance(balances, list):
                self.balances = balances

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name or "BITBNS"

    def get_asset_type(self) -> str | None:
        return self.asset_type

    def get_server_time(self) -> int | float | None:
        return None

    def get_local_update_time(self) -> int | float | None:
        return self.local_update_time

    def get_account_id(self) -> str | None:
        return None

    def get_account_type(self) -> str | None:
        return None

    def get_can_deposit(self) -> bool | None:
        return None

    def get_can_trade(self) -> bool | None:
        return None

    def get_can_withdraw(self) -> bool | None:
        return None

    def get_fee_tier(self) -> int | str | None:
        return None

    def get_max_withdraw_amount(self) -> float | None:
        return None

    def get_total_margin(self) -> float | None:
        return None

    def get_total_used_margin(self) -> float | None:
        return None

    def get_total_maintain_margin(self) -> float | None:
        return None

    def get_total_available_margin(self) -> float | None:
        return None

    def get_total_open_order_initial_margin(self) -> float | None:
        return None

    def get_total_position_initial_margin(self) -> float | None:
        return None

    def get_total_unrealized_profit(self) -> float | None:
        return None

    def get_total_wallet_balance(self) -> float | None:
        return None

    def get_balances(self) -> list[Any]:
        self.init_data()
        return self.balances

    def get_positions(self) -> list[Any]:
        return []

    def get_spot_maker_commission_rate(self) -> float | None:
        return None

    def get_spot_taker_commission_rate(self) -> float | None:
        return None

    def get_future_maker_commission_rate(self) -> float | None:
        return None

    def get_future_taker_commission_rate(self) -> float | None:
        return None

    def get_option_maker_commission_rate(self) -> float | None:
        return None

    def get_option_taker_commission_rate(self) -> float | None:
        return None

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()


class BitbnsRequestAccountData(BitbnsAccountData):
    pass


class BitbnsWssAccountData(BitbnsAccountData):
    pass


__all__ = ["BitbnsAccountData", "BitbnsRequestAccountData", "BitbnsWssAccountData"]
