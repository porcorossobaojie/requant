# `strategys` Module Documentation

## Introduction

The `strategys` module provides a framework for defining, configuring, and executing quantitative trading strategies. It integrates with account management, data formatting, and factor calculation modules to enable a complete strategy lifecycle, from signal generation to order execution and backtesting.

## File and Module Structure

```
strategys/
├── __init__.py
├── account_system.py
├── config.py
├── data_format.py
├── strategy_files/
│   ├── __init__.py
│   ├── meta.py
│   └── running_001.py
└── README.md
```

## Module Overview and Architecture

The `strategys` module is designed with a modular architecture, separating concerns such as account management, data formatting, strategy logic, and configuration. It builds upon existing `account` and `flow` modules and leverages the `factors` module for signal generation.

**Dependencies and Conceptual Flow:**

*   **`config.py`**: Defines configuration parameters for different strategies, such as `running_001`.
*   **`data_format.py`**: Handles the standardization of data formats, including stock codes and order/settlement data for various trading systems (e.g., 'tonghua').
*   **`account_system.py`**: Integrates with the `account` module for managing trading accounts and provides methods for saving/loading orders and settlement data.
*   **`strategy_files/meta.py`**: Serves as a meta-class for all strategies, providing common functionalities like factor filtering, ranking, and order generation. It defines abstract methods for `__internal_data__` and `__factor__` that concrete strategies must implement.
*   **`strategy_files/running_001.py`**: A concrete implementation of a trading strategy, inheriting from `account_system` and `strategy_files.meta`. It defines its specific `__internal_data__` and `__factor__` logic.

**Conceptual Flow (Box-and-Line Diagram):**

```
+-----------------+
| User/Scheduler  |
+--------+--------+
         |
         v
+--------+--------------------------------+
| strategys/strategy_files/running_001.py|
| (Concrete strategy implementation,     |
|  orchestrates execution)               |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| strategys/account_system.py            |
| (Manages account interactions,         |
|  order/settlement I/O)                 |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| strategys/strategy_files/meta.py       |
| (Base strategy logic: factor, ranking, |
|  order generation)                     |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| strategys/data_format.py               |
| (Standardizes data formats for orders, |
|  settlements, codes)                   |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| strategys/config.py                    |
| (Strategy-specific configurations)     |
+----------------------------------------+
```

## Purpose of Each Module

*   **`__init__.py` (in `strategys/`)**:
    *   Initializes the `strategys` package.

*   **`account_system.py`**:
    *   Extends `account.meta_account` and `strategys.data_format.main`.
    *   Provides methods for:
        *   `code_standard`: Standardizes stock codes using the configured data format.
        *   `order_standard`: Standardizes order DataFrames.
        *   `order_save`: Saves standardized orders.
        *   `settle_load`: Loads settlement data.
        *   `test_save`: Saves test results.
        *   `last_settle`: Loads the most recent settlement file.

*   **`config.py`**:
    *   Contains configuration classes for different strategies.
    *   Example: `running_001` class defines parameters like `count`, `max_filter`, and `not_star` for various accounts.

*   **`data_format.py`**:
    *   Defines classes for handling data formatting specific to different trading systems.
    *   **`meta` Class**: Base class providing common methods:
        *   `code_standard`: Standardizes stock codes (e.g., to 6-digit format, JQData format).
        *   `test_save`: Saves test data to CSV.
    *   **`tonghua` Class**: Specific implementation for the 'tonghua' system, including `order_rename`, `order_columns`, `settle_rename`, `settle_columns`, and methods for `order_standard`, `order_save`, `settle_load` tailored for 'tonghua' format.
    *   **`main` Class**: Acts as a dispatcher for different data format handlers (e.g., `main.tonghua`).

*   **`strategy_files/meta.py`**:
    *   The base class for all trading strategies.
    *   **`main` Class**: Provides core strategy functionalities:
        *   `core`: A class variable to hold factor instances (e.g., `factors.volatility`).
        *   `star_filter`: Filters out stocks based on specific code prefixes (e.g., ST, *ST).
        *   `__internal_data__` (abstract): Placeholder for loading and processing internal data (must be implemented by concrete strategies).
        *   `__factor__` (abstract): Placeholder for factor calculation (must be implemented by concrete strategies).
        *   `internal_data` (property): Accesses the internal data.
        *   `factor` (property): Accesses the calculated factor, with optional star stock filtering.
        *   `ranker`: Ranks stocks based on the strategy's factor.
        *   `__order__`: Generates trading orders based on ranking and current holdings.
        *   `order`: Public method to generate trading orders.
        *   `trade`: Executes the trading process (generates, standardizes, and saves orders).
        *   `test`: Performs a back-test and saves results.
        *   `run`: Runs the strategy based on its configured type (e.g., 'trade' or 'test').

*   **`strategy_files/running_001.py`**:
    *   A concrete trading strategy implementation.
    *   **`main` Class**: Inherits from `account_system` and `strategy_files.meta.main`.
        *   Overrides `core` with specific factor instances (e.g., `factors.volatility`).
        *   Implements `__internal_data__` to load and process data specific to `running_001`.
        *   Implements `__factor__` to calculate the main factor for `running_001`.
        *   Includes example usage in `if __name__ == '__main__':` block for running the strategy for multiple accounts.

## Other Helpful Information

*   **Strategy Lifecycle**: The module supports a complete strategy lifecycle: configuration, data preparation, signal generation (factors), order generation, order execution (trade), and performance evaluation (test).
*   **Extensibility**: New strategies can be easily added by inheriting from `strategy_files.meta.main` and implementing the required abstract methods.
*   **Account Management Integration**: Seamless integration with the `account` module allows strategies to manage multiple trading accounts and their specific configurations.
*   **Data Standardization**: The `data_format` module ensures that data exchanged between different components (e.g., strategy and trading system) adheres to predefined formats.
*   **Factor-Based Trading**: The framework is designed to facilitate factor-based quantitative trading, allowing for the easy incorporation and testing of various alpha factors.

---

# `strategys` 模块文档

## 简介

`strategys` 模块提供了一个用于定义、配置和执行量化交易策略的框架。它与账户管理、数据格式化和因子计算模块集成，以实现完整的策略生命周期，从信号生成到订单执行和回测。

## 文件和模块结构

```
strategys/
├── __init__.py
├── account_system.py
├── config.py
├── data_format.py
├── strategy_files/
│   ├── __init__.py
│   ├── meta.py
│   └── running_001.py
└── README.md
```

## 模块概览与架构

`strategys` 模块采用模块化架构设计，将账户管理、数据格式化、策略逻辑和配置等关注点分离。它建立在现有的 `account` 和 `flow` 模块之上，并利用 `factors` 模块进行信号生成。

**依赖关系和概念流程：**

*   **`config.py`**: 定义不同策略的配置参数，例如 `running_001`。
*   **`data_format.py`**: 处理数据格式的标准化，包括股票代码和各种交易系统（例如，'tonghua'）的订单/结算数据。
*   **`account_system.py`**: 与 `account` 模块集成，用于管理交易账户，并提供保存/加载订单和结算数据的方法。
*   **`strategy_files/meta.py`**: 作为所有策略的元类，提供因子过滤、排名和订单生成等通用功能。它定义了具体策略必须实现的 `__internal_data__` 和 `__factor__` 抽象方法。
*   **`strategy_files/running_001.py`**: 交易策略的具体实现，继承自 `account_system` 和 `strategy_files.meta`。它定义了其特定的 `__internal_data__` 和 `__factor__` 逻辑。

**概念流程图（框线图）：**

```
+-----------------+
| 用户/调度器     |
+--------+--------+
         |
         v
+--------+--------------------------------+
| strategys/strategy_files/running_001.py|
| (具体策略实现，协调执行)               |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| strategys/account_system.py            |
| (管理账户交互，订单/结算 I/O)          |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| strategys/strategy_files/meta.py       |
| (基本策略逻辑：因子、排名、订单生成)   |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| strategys/data_format.py               |
| (标准化订单、结算、代码的数据格式)     |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| strategys/config.py                    |
| (策略特定配置)                         |
+----------------------------------------+
```

## 各个模块的用途

*   **`__init__.py` (在 `strategys/`)**:
    *   初始化 `strategys` 包。

*   **`account_system.py`**:
    *   扩展 `account.meta_account` 和 `strategys.data_format.main`。
    *   提供以下方法：
        *   `code_standard`: 使用配置的数据格式标准化股票代码。
        *   `order_standard`: 标准化订单 DataFrame。
        *   `order_save`: 保存标准化订单。
        *   `settle_load`: 加载结算数据。
        *   `test_save`: 保存测试结果。
        *   `last_settle`: 加载最新的结算文件。

*   **`config.py`**:
    *   包含不同策略的配置类。
    *   示例：`running_001` 类定义了各种账户的 `count`、`max_filter` 和 `not_star` 等参数。

*   **`data_format.py`**:
    *   定义用于处理不同交易系统特定数据格式的类。
    *   **`meta` 类**: 基类，提供通用方法：
        *   `code_standard`: 标准化股票代码（例如，6 位格式，JQData 格式）。
        *   `test_save`: 将测试数据保存到 CSV。
    *   **`tonghua` 类**: 'tonghua' 系统的具体实现，包括 `order_rename`、`order_columns`、`settle_rename`、`settle_columns`，以及针对 'tonghua' 格式的 `order_standard`、`order_save`、`settle_load` 方法。
    *   **`main` 类**: 作为不同数据格式处理程序的调度器（例如，`main.tonghua`）。

*   **`strategy_files/meta.py`**:
    *   所有交易策略的基类。
    *   **`main` 类**: 提供核心策略功能：
        *   `core`: 一个类变量，用于保存因子实例（例如，`factors.volatility`）。
        *   `star_filter`: 根据特定代码前缀（例如，ST，*ST）过滤股票。
        *   `__internal_data__`（抽象）：用于加载和处理内部数据的占位符（必须由具体策略实现）。
        *   `__factor__`（抽象）：用于因子计算的占位符（必须由具体策略实现）。
        *   `internal_data`（属性）：访问内部数据。
        *   `factor`（属性）：访问计算出的因子，可选进行星级股票过滤。
        *   `ranker`: 根据策略因子对股票进行排名。
        *   `__order__`: 根据排名和当前持仓生成交易订单。
        *   `order`: 生成交易订单的公共方法。
        *   `trade`: 执行交易过程（生成、标准化和保存订单）。
        *   `test`: 执行回测并保存结果。
        *   `run`: 根据配置的类型（例如，'trade' 或 'test'）运行策略。

*   **`strategy_files/running_001.py`**:
    *   一个具体的交易策略实现。
    *   **`main` 类**: 继承自 `account_system` 和 `strategy_files.meta.main`。
        *   使用特定因子实例（例如，`factors.volatility`）覆盖 `core`。
        *   实现 `__internal_data__` 以加载和处理 `running_001` 特定的数据。
        *   实现 `__factor__` 以计算 `running_001` 的主因子。
        *   在 `if __name__ == '__main__':` 块中包含用于为多个账户运行策略的示例用法。

## 其他有用的信息

*   **策略生命周期**: 该模块支持完整的策略生命周期：配置、数据准备、信号生成（因子）、订单生成、订单执行（交易）和绩效评估（测试）。
*   **可扩展性**: 通过继承 `strategy_files.meta.main` 并实现所需的抽象方法，可以轻松添加新策略。
*   **账户管理集成**: 与 `account` 模块的无缝集成允许策略管理多个交易账户及其特定配置。
*   **数据标准化**: `data_format` 模块确保不同组件（例如，策略和交易系统）之间交换的数据符合预定义格式。
*   **基于因子的交易**: 该框架旨在促进基于因子的量化交易，允许轻松地整合和测试各种 Alpha 因子。
