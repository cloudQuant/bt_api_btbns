# BTBNS

Exchange plugin for bt_api framework.

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_btbns.svg)](https://pypi.org/project/bt_api_btbns/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_btbns.svg)](https://pypi.org/project/bt_api_btbns/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_btbns/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_btbns/actions)
[![Docs](https://readthedocs.org/projects/bt-api-btbns/badge/?version=latest)](https://bt-api-btbns.readthedocs.io/)

---

## English | [中文](#中文)

### Overview

This package provides **Bitbns exchange plugin for bt_api framework** for the [bt_api](https://github.com/cloudQuant/bt_api_py) framework. It offers a unified interface for interacting with **BTBNS** exchange.

### Features

- Exchange integration with bt_api
- REST API support
- Market data access
- Basic trading operations

### Installation

```bash
pip install bt_api_btbns
```

Or install from source:

```bash
git clone https://github.com/cloudQuant/bt_api_btbns
cd bt_api_btbns
pip install -e .
```

### Quick Start

```python
from bt_api_btbns import BtbnsApi

# Initialize
feed = BtbnsApi(api_key="your_key", secret="your_secret")

# Get ticker data
ticker = feed.get_ticker("BTCUSDT")
print(ticker)
```

### Supported Operations

| Operation | Status |
|-----------|--------|
| Ticker | ✅ |
| OrderBook | ✅ |
| Trades | ✅ |
| Bars/Klines | ✅ |
| Orders | ✅ |
| Balances | ✅ |
| Positions | ✅ |

### Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-btbns.readthedocs.io/ |
| Chinese Docs | https://bt-api-btbns.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_btbns |
| Issue Tracker | https://github.com/cloudQuant/bt_api_btbns/issues |

### Requirements

- Python 3.9+
- bt_api_base >= 0.15

### Architecture

```
bt_api_btbns/
├── src/bt_api_btbns/     # Source code
│   ├── containers/     # Data containers
│   ├── feeds/          # API feeds
│   ├── gateway/       # Gateway adapter
│   └── plugin.py      # Plugin registration
├── tests/             # Unit tests
└── docs/             # Documentation
```

### License

MIT License - see [LICENSE](LICENSE) for details.

### Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_btbns/issues)
- Email: yunjinqi@gmail.com

---

## 中文

### 概述

本包为 [bt_api](https://github.com/cloudQuant/bt_api_py) 框架提供 **Bitbns exchange plugin for bt_api framework**。它提供了与 **BTBNS** 交易所交互的统一接口。

### 功能特点

- bt_api交易所集成
- REST API支持
- 市场数据访问
- 基本交易操作

### 安装

```bash
pip install bt_api_btbns
```

或从源码安装：

```bash
git clone https://github.com/cloudQuant/bt_api_btbns
cd bt_api_btbns
pip install -e .
```

### 快速开始

```python
from bt_api_btbns import BtbnsApi

# 初始化
feed = BtbnsApi(api_key="your_key", secret="your_secret")

# 获取行情数据
ticker = feed.get_ticker("BTCUSDT")
print(ticker)
```

### 支持的操作

| 操作 | 状态 |
|------|------|
| Ticker | ✅ |
| OrderBook | ✅ |
| Trades | ✅ |
| Bars/Klines | ✅ |
| Orders | ✅ |
| Balances | ✅ |
| Positions | ✅ |

### 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-btbns.readthedocs.io/ |
| 中文文档 | https://bt-api-btbns.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_btbns |
| 问题反馈 | https://github.com/cloudQuant/bt_api_btbns/issues |

### 系统要求

- Python 3.9+
- bt_api_base >= 0.15

### 架构

```
bt_api_btbns/
├── src/bt_api_btbns/     # 源代码
│   ├── containers/     # 数据容器
│   ├── feeds/          # API 源
│   ├── gateway/        # 网关适配器
│   └── plugin.py       # 插件注册
├── tests/             # 单元测试
└── docs/             # 文档
```

### 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

### 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_btbns/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com
