# BitBNS Exchange Plugin for bt_api

## English | [中文](#中文)

---

## Overview

**BitBNS** is one of India's leading cryptocurrency exchanges, providing a secure platform for trading a wide variety of cryptocurrencies with INR (Indian Rupee) and USDT trading pairs. Founded with the mission to make cryptocurrency accessible in India, BitBNS offers competitive fees and a user-friendly experience.

This package provides the **BitBNS exchange plugin for bt_api**, offering a unified interface for interacting with BitBNS exchange through the [bt_api](https://github.com/cloudQuant/bt_api_py) framework.

### Key Features

- **REST API Integration**: Full access to BitBNS's REST endpoints for market data and trading
- **Synchronous & Asynchronous**: Supports both sync and async request patterns
- **Unified Interface**: Integrates seamlessly with bt_api's `BtApi` class
- **Multi-Quote Currency**: Support for both INR and USDT trading pairs
- **HMAC-SHA512 Authentication**: Secure API key authentication following BitBNS's signature scheme

### Authentication

BitBNS uses **HMAC-SHA512** signature authentication. The signature is computed as:

```
signature = HMAC-SHA512(secret, timestamp + body)
```

Where:
- `timestamp`: Unix timestamp in milliseconds
- `body`: Request body (empty string for GET requests)

Required headers:
- `X-API-KEY`: Your API key
- `X-API-SIGNATURE`: The HMAC-SHA512 signature
- `X-API-TIMESTAMP`: Unix timestamp in milliseconds

### API Endpoint

| Environment | REST URL | WebSocket URL |
|------------|----------|---------------|
| Production | `https://api.bitbns.com` | `wss://ws.bitbns.com` |

### Supported Operations

| Category | Operations | Status |
|----------|------------|--------|
| **Market Data** | Ticker, OrderBook, Klines/Candles | ✅ Supported |
| **Trading** | Place Order, Cancel Order, Query Order | ✅ Supported |
| **Account** | Balance, Account Info, Open Orders | ✅ Supported |
| **Exchange Info** | Markets, Symbols | ✅ Supported |

### Supported Trading Pairs

BitBNS supports trading with both INR and USDT as quote currencies:

| Quote Currency | Example Pairs |
|---------------|---------------|
| **INR** | BTC_INR, ETH_INR, XRP_INR, SOL_INR |
| **USDT** | BTC_USDT, ETH_USDT, XRP_USDT, SOL_USDT |

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bitbns
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bitbns
cd bt_api_bitbns
pip install -e .
```

### Requirements

- Python 3.9 or higher
- bt_api_base >= 0.15
- Valid BitBNS API key and secret

---

## Quick Start

### Initialize with BtApi

```python
from bt_api_py import BtApi

# Initialize with BitBNS exchange
exchange_config = {
    "BITBNS___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
    }
}

api = BtApi(exchange_kwargs=exchange_config)

# Get ticker data (USDT pair)
ticker = api.get_tick("BITBNS___SPOT", "BTC_USDT")
print(ticker)

# Get ticker (INR pair)
ticker_inr = api.get_tick("BITBNS___SPOT", "BTC_INR")
print(ticker_inr)
```

### Direct Usage

```python
from bt_api_bitbns.feeds.live_bitbns.spot import BitbnsRequestDataSpot

# Initialize the feed directly
feed = BitbnsRequestDataSpot(
    api_key="your_api_key",
    secret="your_api_secret"
)

# Get ticker (USDT pair)
ticker = feed.get_tick("BTC_USDT")
print(ticker)

# Get order book
depth = feed.get_depth("BTC_USDT", count=20)
print(depth)

# Get klines
klines = feed.get_kline("BTC_USDT", period="1h", count=100)
print(klines)
```

### Trading

```python
# Place a limit order
order = feed.make_order(
    symbol="BTC_USDT",
    volume=0.001,
    price=50000,
    order_type="buy-limit",  # buy-limit, sell-limit, buy-market, sell-market
    offset="buy"  # buy or sell
)
print(order)

# Cancel order
result = feed.cancel_order("BTC_USDT", order_id="your_order_id")
print(result)

# Query order
order_info = feed.query_order("BTC_USDT", order_id="your_order_id")
print(order_info)
```

### Account Operations

```python
# Get account balance
balance = feed.get_balance()
print(balance)

# Get open orders
open_orders = feed.get_open_orders()
print(open_orders)
```

---

## API Reference

### Market Data

#### Get Ticker

```python
# USDT pair
ticker = feed.get_tick("BTC_USDT")
# INR pair
ticker_inr = feed.get_tick("BTC_INR")
```

#### Get Order Book

```python
depth = feed.get_depth("BTC_USDT", count=20)
```

#### Get Klines/Candles

```python
# Supported periods: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 1w
klines = feed.get_kline("BTC_USDT", period="1h", count=100)
```

### Trading

#### Place Order

```python
# Limit order
order = feed.make_order(
    symbol="BTC_USDT",
    volume=0.01,
    price=50000,
    order_type="buy-limit",  # buy-limit, sell-limit
    offset="buy"  # buy, sell
)

# Market order
order = feed.make_order(
    symbol="BTC_USDT",
    volume=0.01,
    price=0,  # price is ignored for market orders
    order_type="buy-market",
    offset="buy"
)
```

#### Cancel Order

```python
result = feed.cancel_order("BTC_USDT", order_id="your_order_id")
```

#### Query Order

```python
order_info = feed.query_order("BTC_USDT", order_id="your_order_id")
```

### Account

#### Get Balance

```python
balance = feed.get_balance()
```

#### Get Open Orders

```python
# All open orders
orders = feed.get_open_orders()

# Specific symbol
orders = feed.get_open_orders(symbol="BTC_USDT")
```

---

## Architecture

```
bt_api_bitbns/
├── src/bt_api_bitbns/           # Source code
│   ├── exchange_data/            # Exchange configuration and metadata
│   │   └── __init__.py         # BitbnsExchangeData, BitbnsExchangeDataSpot
│   ├── feeds/                   # API feeds
│   │   └── live_bitbns/       # Live trading feed
│   │       ├── request_base.py  # Base class with HMAC auth
│   │       └── spot.py        # Spot trading implementation
│   ├── containers/             # Data containers
│   │   ├── tickers/          # Ticker containers
│   │   ├── orderbooks/       # OrderBook containers
│   │   ├── bars/             # K线 containers
│   │   ├── orders/           # Order containers
│   │   ├── accounts/         # Account containers
│   │   └── balances/        # Balance containers
│   ├── errors/               # Error definitions
│   └── plugin.py            # Plugin registration
├── tests/                     # Unit tests
├── docs/                     # Documentation
├── pyproject.toml           # Package configuration
└── README.md                # This file
```

---

## Error Handling

BitBNS API errors are translated to standard bt_api exceptions. The plugin handles:

- **Authentication errors**: Invalid API key or signature
- **Permission errors**: Insufficient permissions for the operation
- **Rate limit errors**: Too many requests
- **Parameter errors**: Invalid request parameters

---

## Rate Limits

BitBNS implements rate limiting on their API. The plugin includes built-in rate limiting to stay within acceptable bounds.

---

## Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-btbns.readthedocs.io/ |
| Chinese Docs | https://bt-api-btbns.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_bitbns |
| Issue Tracker | https://github.com/cloudQuant/bt_api_bitbns/issues |
| BitBNS API Docs | https://docs.bitbns.com/ |

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_bitbns/issues)
- Email: yunjinqi@gmail.com

---

## Changelog

### v0.1.0

- Initial release
- REST API support for spot trading
- HMAC-SHA512 authentication
- Support for INR and USDT trading pairs
- Support for ticker, depth, klines, trading, balance operations

---

# 中文

---

## 概述

**BitBNS** 是印度领先的加密货币交易所之一，提供一个安全的平台，可交易多种加密货币，主要以 INR（印度卢比）和 USDT 交易对进行交易。BitBNS 的使命是让加密货币在印度更加普及，提供有竞争力的手续费和用户友好的体验。

本包为 [bt_api](https://github.com/cloudQuant/bt_api_py) 框架提供 **BitBNS 交易所插件**，通过统一接口与 BitBNS 交易所进行交互。

### 核心功能

- **REST API 集成**：全面访问 BitBNS 的市场数据和交易 REST 端点
- **同步与异步**：支持同步和异步请求模式
- **统一接口**：与 bt_api 的 `BtApi` 类无缝集成
- **多报价货币**：支持 INR 和 USDT 交易对
- **HMAC-SHA512 认证**：遵循 BitBNS 签名方案的安全 API 密钥认证

### 认证方式

BitBNS 使用 **HMAC-SHA512** 签名认证。签名计算方式：

```
signature = HMAC-SHA512(secret, timestamp + body)
```

其中：
- `timestamp`：Unix 时间戳（毫秒）
- `body`：请求体（GET 请求为空字符串）

必需的请求头：
- `X-API-KEY`：您的 API 密钥
- `X-API-SIGNATURE`：HMAC-SHA512 签名
- `X-API-TIMESTAMP`：Unix 时间戳（毫秒）

### API 端点

| 环境 | REST URL | WebSocket URL |
|------|----------|---------------|
| 生产环境 | `https://api.bitbns.com` | `wss://ws.bitbns.com` |

### 支持的操作

| 类别 | 操作 | 状态 |
|------|------|------|
| **市场数据** | 行情、订单簿、K线 | ✅ 已支持 |
| **交易** | 下单、撤单、查询订单 | ✅ 已支持 |
| **账户** | 余额、账户信息、开放订单 | ✅ 已支持 |
| **交易所信息** | 市场、交易对 | ✅ 已支持 |

### 支持的交易对

BitBNS 支持以 INR 和 USDT 作为报价货币进行交易：

| 报价货币 | 示例交易对 |
|----------|------------|
| **INR** | BTC_INR, ETH_INR, XRP_INR, SOL_INR |
| **USDT** | BTC_USDT, ETH_USDT, XRP_USDT, SOL_USDT |

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bitbns
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bitbns
cd bt_api_bitbns
pip install -e .
```

### 系统要求

- Python 3.9 或更高版本
- bt_api_base >= 0.15
- 有效的 BitBNS API 密钥和密钥

---

## 快速开始

### 使用 BtApi 初始化

```python
from bt_api_py import BtApi

# 使用 BitBNS 交易所初始化
exchange_config = {
    "BITBNS___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
    }
}

api = BtApi(exchange_kwargs=exchange_config)

# 获取 USDT 交易对的行情数据
ticker = api.get_tick("BITBNS___SPOT", "BTC_USDT")
print(ticker)

# 获取 INR 交易对的行情数据
ticker_inr = api.get_tick("BITBNS___SPOT", "BTC_INR")
print(ticker_inr)
```

### 直接使用

```python
from bt_api_bitbns.feeds.live_bitbns.spot import BitbnsRequestDataSpot

# 直接初始化 feed
feed = BitbnsRequestDataSpot(
    api_key="your_api_key",
    secret="your_api_secret"
)

# 获取行情（USDT 交易对）
ticker = feed.get_tick("BTC_USDT")
print(ticker)

# 获取订单簿
depth = feed.get_depth("BTC_USDT", count=20)
print(depth)

# 获取 K 线
klines = feed.get_kline("BTC_USDT", period="1h", count=100)
print(klines)
```

### 交易

```python
# 下限价单
order = feed.make_order(
    symbol="BTC_USDT",
    volume=0.001,
    price=50000,
    order_type="buy-limit",  # buy-limit, sell-limit, buy-market, sell-market
    offset="buy"  # buy 或 sell
)
print(order)

# 撤单
result = feed.cancel_order("BTC_USDT", order_id="your_order_id")
print(result)

# 查询订单
order_info = feed.query_order("BTC_USDT", order_id="your_order_id")
print(order_info)
```

### 账户操作

```python
# 获取账户余额
balance = feed.get_balance()
print(balance)

# 获取开放订单
open_orders = feed.get_open_orders()
print(open_orders)
```

---

## API 参考

### 市场数据

#### 获取行情

```python
# USDT 交易对
ticker = feed.get_tick("BTC_USDT")
# INR 交易对
ticker_inr = feed.get_tick("BTC_INR")
```

#### 获取订单簿

```python
depth = feed.get_depth("BTC_USDT", count=20)
```

#### 获取 K 线

```python
# 支持的周期：1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 1w
klines = feed.get_kline("BTC_USDT", period="1h", count=100)
```

### 交易

#### 下单

```python
# 限价单
order = feed.make_order(
    symbol="BTC_USDT",
    volume=0.01,
    price=50000,
    order_type="buy-limit",  # buy-limit, sell-limit
    offset="buy"  # buy, sell
)

# 市价单
order = feed.make_order(
    symbol="BTC_USDT",
    volume=0.01,
    price=0,  # 市价单不需要价格
    order_type="buy-market",
    offset="buy"
)
```

#### 撤单

```python
result = feed.cancel_order("BTC_USDT", order_id="your_order_id")
```

#### 查询订单

```python
order_info = feed.query_order("BTC_USDT", order_id="your_order_id")
```

### 账户

#### 获取余额

```python
balance = feed.get_balance()
```

#### 获取开放订单

```python
# 所有开放订单
orders = feed.get_open_orders()

# 指定交易对
orders = feed.get_open_orders(symbol="BTC_USDT")
```

---

## 架构

```
bt_api_bitbns/
├── src/bt_api_bitbns/           # 源代码
│   ├── exchange_data/            # 交易所配置和元数据
│   │   └── __init__.py         # BitbnsExchangeData, BitbnsExchangeDataSpot
│   ├── feeds/                   # API feeds
│   │   └── live_bitbns/       # 实时交易 feed
│   │       ├── request_base.py  # 带有 HMAC 认证的基类
│   │       └── spot.py        # 现货交易实现
│   ├── containers/             # 数据容器
│   │   ├── tickers/          # 行情容器
│   │   ├── orderbooks/       # 订单簿容器
│   │   ├── bars/             # K线容器
│   │   ├── orders/           # 订单容器
│   │   ├── accounts/         # 账户容器
│   │   └── balances/        # 余额容器
│   ├── errors/               # 错误定义
│   └── plugin.py            # 插件注册
├── tests/                     # 单元测试
├── docs/                     # 文档
├── pyproject.toml           # 包配置
└── README.md                # 本文件
```

---

## 错误处理

BitBNS API 错误会转换为标准的 bt_api 异常。插件处理：

- **认证错误**：API 密钥或签名无效
- **权限错误**：操作权限不足
- **频率限制错误**：请求过于频繁
- **参数错误**：请求参数无效

---

## 频率限制

BitBNS 在其 API 上实施了频率限制。插件内置了频率限制以保持在可接受的范围内。

---

## 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-btbns.readthedocs.io/ |
| 中文文档 | https://bt-api-btbns.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_bitbns |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitbns/issues |
| BitBNS API 文档 | https://docs.bitbns.com/ |

---

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

---

## 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_bitbns/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com

---

## 更新日志

### v0.1.0

- 初始版本发布
- 支持现货交易的 REST API
- HMAC-SHA512 认证
- 支持 INR 和 USDT 交易对
- 支持行情、订单簿、K线、交易、余额操作