from __future__ import annotations

from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry

from bt_api_bitbns import __version__
from bt_api_bitbns.registry_registration import register_bitbns


def get_plugin_info() -> PluginInfo:
    return PluginInfo(
        name="bt_api_bitbns",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("BITBNS___SPOT",),
        supported_asset_types=("SPOT",),
        plugin_module="bt_api_bitbns.plugin",
    )


def register_plugin(
    registry: ExchangeRegistry | type[ExchangeRegistry],
    runtime_factory: type[GatewayRuntimeRegistrar],
) -> PluginInfo:
    del runtime_factory
    register_bitbns(registry)
    return get_plugin_info()
