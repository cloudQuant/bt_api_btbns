from __future__ import annotations

from bt_api_base.balance_utils import simple_balance_handler as _bitbns_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_bitbns.exchange_data import BitbnsExchangeDataSpot
from bt_api_bitbns.feeds.live_bitbns.spot import BitbnsRequestDataSpot


def register_bitbns(registry: ExchangeRegistry | type[ExchangeRegistry]) -> None:
    registry.register_feed("BITBNS___SPOT", BitbnsRequestDataSpot)
    registry.register_exchange_data("BITBNS___SPOT", BitbnsExchangeDataSpot)
    registry.register_balance_handler("BITBNS___SPOT", _bitbns_balance_handler)


def register(registry: ExchangeRegistry | type[ExchangeRegistry] | None = None) -> None:
    target = ExchangeRegistry if registry is None else registry
    register_bitbns(target)
