# `__back_test__` Module Documentation

## Introduction

This module provides a vectorized backtesting framework for quantitative trading strategies. It is designed to simulate historical performance by managing portfolio data, handling trade executions, and applying market conditions. The core of the module is built around a custom `Series` object that extends pandas Series functionality to represent portfolios, and a `link` class that simulates the daily trading lifecycle.

## File and Module Structure

```
__back_test__/
├── __init__.py
├── config.py
│   ├── DATA_INFO: Defines standard column names for market data.
│   ├── TRADE_INFO: Specifies trading parameters like costs and limits.
│   └── SERIES_ATTRIBUTES: Defines default attributes for the custom Series object.
├── data.py
│   └── __data__: Manages and preprocesses market data for the backtesting engine.
│       ├── __init__: Loads market data and initializes filters.
│       ├── __not_st_init__: Filters for ST (Special Treatment) stocks.
│       ├── __buyable_init__: Determines if stocks are buyable based on price limits.
│       └── __sellable_init__: Determines if stocks are sellable based on price limits.
└── main.py
    ├── Series: A custom pandas Series for portfolio management.
    │   ├── to(): Converts portfolio between units ('assets', 'weight', 'share').
    │   ├── price(): Retrieves price data for the portfolio's state.
    │   ├── total_assets(): Calculates the total asset value of the portfolio.
    │   ├── order_standard(): Prepares a standardized order portfolio.
    │   └── tradeable_standard(): Filters the portfolio based on trading rules.
    └── link: Simulates a single day's trading and settlement process.
        ├── settle_T1: The settled portfolio for the current day (T1).
        ├── order_T1: The remaining order portfolio for the current day (T1).
        ├── turnover: The portfolio turnover rate.
        └── cost: The transaction cost.
```

## Module Overview and Architecture

The `__back_test__` module follows a configuration-driven and vectorized design. The architecture is composed of three main components: configuration, data management, and the backtesting engine.

1.  **Configuration (`config.py`)**: This file centralizes all static parameters, such as data column names and trading costs. This makes the framework easy to configure and maintain without hardcoding values.
2.  **Data Management (`data.py`)**: The `__data__` class acts as a global data source. It loads raw market data (e.g., EOD prices) and preprocesses it to create a clean, analysis-ready dataset that includes trading status and buy/sell flags.
3.  **Backtesting Engine (`main.py`)**: This is the core of the module.
    *   The `Series` class is a powerful, customized data structure that represents a portfolio. It understands different units (assets, weights, shares) and states (order, trade, settle) and can perform conversions and calculations accordingly.
    *   The `link` class orchestrates the daily simulation. It takes the settled portfolio from day T-1 and the target portfolio for day T, simulates the trades that would occur based on market conditions (e.g., price limits, stock suspensions), and calculates the resulting T-day settled portfolio, costs, and turnover.

The data flow is as follows:

```
+-----------------+      +------------------+      +---------------------------+
|   config.py     |----->|  data.py         |----->|      main.py              |
| (Parameters)    |      | (__data__ Class) |      | (Series & link Classes)   |
+-----------------+      +------------------+      +------------+--------------+
                               |                             |
                               v                             v
+--------------------------------------------------------+   |
|                 Backtesting Workflow                     |   |
|                                                        |   |
| 1. `link` takes settle_T0 and hope_T1 `Series` objects.|   |
| 2. `link` calculates the required trades.              |   |
| 3. It checks tradeability using data from `__data__`.  |   |
| 4. `link` computes the actual trades (trade_T1).       |   |
| 5. It calculates the new portfolio (settle_T1) & costs.|   |
+--------------------------------------------------------+   |
                                                             |
             <-----------------------------------------------+
             (Output: settle_T1, order_T1, turnover, cost)
```

## Purpose of Each Module

### `config.py`
*   **Positioning and Role**: This file acts as the central control panel for the backtesting module. Its role is to decouple hardcoded parameters from the core logic, allowing for easy tuning and maintenance. It defines the "vocabulary" for data fields and the "rules of the game" for trading.
*   **Key Components and Usage**:
    *   `DATA_INFO`: A class that holds standardized column names for all market data. This prevents errors from typos and makes the code more readable.
    *   `TRADE_INFO`: Defines global trading parameters. This is where you set transaction costs, and price limits for buy/sell orders.
    *   `SERIES_ATTRIBUTES`: Specifies the default properties for the `Series` object in `main.py`, ensuring consistent behavior for new portfolio instances.

### `data.py`
*   **Positioning and Role**: This module is the data provider for the entire backtesting engine. It is responsible for fetching raw data and transforming it into a ready-to-use format with all necessary flags for simulation. It acts as a singleton `DATA_SOURCE` to ensure all parts of the system use the same consistent dataset.
*   **Key Components and Usage**:
    *   `__data__` class: The main class that loads and processes data. It is instantiated as a global `DATA_SOURCE` object.
    *   `__buyable_init__` / `__sellable_init__`: These internal methods are crucial for pre-calculating whether a stock can be traded based on its proximity to the high/low price limits. This is a key vectorization step that avoids checking these conditions one by one during the simulation.

### `main.py`
*   **Positioning and Role**: This is the heart of the backtesting engine, containing the logic for portfolio representation and trade simulation. It uses the configuration from `config.py` and the data from `data.py` to run the backtest.
*   **Key Components and Usage**:
    *   `Series` class: Represents a portfolio. Its main power lies in its ability to manage different views of the same underlying portfolio data.
        *   **Application Scenario**: You use a `Series` object to represent your desired portfolio (`hope_portfolio`) at each time step.
        *   **Call Example**:
            ```python
            # Create a portfolio with equal weights on three stocks
            my_portfolio = Series({'stock_A': 0.33, 'stock_B': 0.33, 'stock_C': 0.34}, name='2025-07-10', unit='weight')
            
            # Convert the portfolio to asset values, assuming total assets of $1,000,000
            assets_portfolio = my_portfolio.to('assets', assets=1000000)
            
            # Convert to the number of shares needed, using unadjusted prices
            share_portfolio = assets_portfolio.to('share', is_adj=False)
            ```
    *   `link` class: Simulates the events of a single trading day, connecting the portfolio from T-1 to T.
        *   **Application Scenario**: In a backtesting loop, you would create a `link` object for each day to calculate the actual trades, the resulting portfolio, and performance metrics.
        *   **Call Example**:
            ```python
            # settle_T0 is the portfolio from the previous day
            # hope_T1 is your target portfolio for today
            daily_link = link(settle_portfolio_T0=settle_T0, order_portfolio_T0=order_T0, hope_portfolio_T1=hope_T1)
            
            # Get the resulting settled portfolio for today
            settle_T1 = daily_link.settle_T1
            
            # Get the turnover rate for the day
            daily_turnover = daily_link.turnover
            ```

## Other Helpful Information

*   **Core Concepts and Design Philosophy**:
    *   **Vectorization**: The framework is built to be highly efficient by using vectorized operations (thanks to pandas) instead of iterating through stocks one by one. This is why data preprocessing in `data.py` is critical.
    *   **State and Unit Management**: The `Series` class abstracts away the complexity of portfolio accounting. By simply changing the `unit` or `state` property, you can get a different view of your portfolio without manual calculations. This is key to the framework's flexibility.
    *   **Configuration-Driven**: All major parameters are defined in `config.py`. This makes it easy to test different scenarios (e.g., higher transaction costs) without changing the core simulation logic.

*   **Quick Start / Usage Example**:
    Here is a simplified example of a backtesting loop:
    ```python
    import pandas as pd
    from __back_test__.main import Series, link

    # 1. Define your strategy's target portfolios for each day
    trade_dates = pd.to_datetime(['2025-07-10', '2025-07-11'])
    hope_portfolios = {
        trade_dates[0]: Series({'stock_A': 0.5, 'stock_B': 0.5}, name=trade_dates[0], unit='weight'),
        trade_dates[1]: Series({'stock_A': 0.4, 'stock_C': 0.6}, name=trade_dates[1], unit='weight')
    }

    # 2. Initialize variables
    settle_portfolio = None
    order_portfolio = None
    initial_assets = 1000000

    # 3. Run the backtest loop
    for date in trade_dates:
        hope_portfolio = hope_portfolios[date]
        
        # Simulate the day's trading
        daily_link = link(settle_portfolio, order_portfolio, hope_portfolio, init_assets=initial_assets)
        
        # Update portfolios for the next iteration
        settle_portfolio = daily_link.settle_T1
        order_portfolio = daily_link.order_T1
        initial_assets = None # Only used on the first day
        
        print(f"Date: {date.date()}, Assets: {settle_portfolio.total_assets():.2f}, Turnover: {daily_link.turnover:.2%}")

    ```

---

# `__back_test__` 模块文档

## 简介

该模块为量化交易策略提供了一个向量化的回测框架。它旨在通过管理投资组合数据、处理交易执行和应用市场条件来模拟历史表现。该模块的核心是围绕一个自定义的 `Series` 对象构建的，该对象扩展了 pandas Series 的功能以表示投资组合，以及一个 `link` 类，用于模拟每日的交易生命周期。

## 文件和模块结构

```
__back_test__/
├── __init__.py
├── config.py
│   ├── DATA_INFO: 定义市场数据的标准列名。
│   ├── TRADE_INFO: 指定交易参数，如成本和限制。
│   └── SERIES_ATTRIBUTES: 定义自定义 Series 对象的默认属性。
├── data.py
│   └── __data__: 管理和预处理回测引擎的市场数据。
│       ├── __init__: 加载市场数据并初始化过滤器。
│       ├── __not_st_init__: 筛选ST（特殊处理）股票。
│       ├── __buyable_init__: 根据价格限制确定股票是否可买。
│       └── __sellable_init__: 根据价格限制确定股票是否可卖。
└── main.py
    ├── Series: 用于投资组合管理的自定义 pandas Series。
    │   ├── to(): 在单位（'assets', 'weight', 'share'）之间转换投资组合。
    │   ├── price(): 检索投资组合状态的价格数据。
    │   ├── total_assets(): 计算投资组合的总资产价值。
    │   ├── order_standard(): 准备标准化的订单投资组合。
    │   └── tradeable_standard(): 根据交易规则筛选投资组合。
    └── link: 模拟单日的交易和结算过程。
        ├── settle_T1: 当前交易日（T1）的结算投资组合。
        ├── order_T1: 当前交易日（T1）的剩余订单投资组合。
        ├── turnover: 投资组合换手率。
        └── cost: 交易成本。
```

## 模块概览与架构

`__back_test__` 模块遵循配置驱动和向量化的设计。其架构由三个主要部分组成：配置、数据管理和回测引擎。

1.  **配置 (`config.py`)**: 此文件集中了所有静态参数，例如数据列名和交易成本。这使得框架易于配置和维护，而无需硬编码值。
2.  **数据管理 (`data.py`)**: `__data__` 类充当全局数据源。它加载原始市场数据（例如，EOD价格）并对其进行预处理，以创建一个干净、可供分析的数据集，其中包括交易状态和买/卖标志。
3.  **回测引擎 (`main.py`)**: 这是模块的核心。
    *   `Series` 类是一个功能强大的自定义数据结构，用于表示投资组合。它能理解不同的单位（资产、权重、股份）和状态（订单、交易、结算），并能相应地执行转换和计算。
    *   `link` 类负责协调每日的模拟。它接收 T-1 日的结算投资组合和 T 日的目标投资组合，模拟在市场条件下（例如，价格限制、股票停牌）将发生的交易，并计算得出 T 日的结算投资组合、成本和换手率。

数据流如下：

```
+-----------------+      +------------------+      +---------------------------+
|   config.py     |----->|  data.py         |----->|      main.py              |
| (参数)          |      | (__data__ 类)    |      | (Series & link 类)        |
+-----------------+      +------------------+      +------------+--------------+
                               |                             |
                               v                             v
+--------------------------------------------------------+   |
|                 回测工作流                               |   |
|                                                        |   |
| 1. `link` 接收 settle_T0 和 hope_T1 `Series` 对象。    |   |
| 2. `link` 计算所需的交易。                             |   |
| 3. 使用 `__data__` 的数据检查可交易性。                |   |
| 4. `link` 计算实际交易 (trade_T1)。                    |   |
| 5. 计算新的投资组合 (settle_T1) 和成本。               |   |
+--------------------------------------------------------+   |
                                                             |
             <-----------------------------------------------+
             (输出: settle_T1, order_T1, 换手率, 成本)
```

## 各个模块的用途

### `config.py`
*   **定位与角色**: 该文件充当回测模块的中央控制面板。其作用是将硬编码的参数与核心逻辑解耦，从而便于调整和维护。它定义了数据字段的“词汇表”和交易的“游戏规则”。
*   **核心组件与用法**:
    *   `DATA_INFO`: 一个包含所有市场数据标准列名的类。这可以防止因拼写错误而导致的错误，并使代码更具可读性。
    *   `TRADE_INFO`: 定义全局交易参数。您可以在此处设置交易成本和买/卖订单的价格限制。
    *   `SERIES_ATTRIBUTES`: 指定 `main.py` 中 `Series` 对象的默认属性，确保新投资组合实例的行为一致。

### `data.py`
*   **定位与角色**: 该模块是整个回测引擎的数据提供者。它负责获取原始数据并将其转换为包含所有必要模拟标志的即用格式。它充当单例 `DATA_SOURCE`，以确保系统的所有部分都使用相同的一致数据集。
*   **核心组件与用法**:
    *   `__data__` 类: 加载和处理数据的主类。它被实例化为全局 `DATA_SOURCE` 对象。
    *   `__buyable_init__` / `__sellable_init__`: 这些内部方法对于根据股票与最高/最低价格限制的接近程度预先计算其是否可交易至关重要。这是一个关键的向量化步骤，避免了在模拟过程中逐个检查这些条件。

### `main.py`
*   **定位与角色**: 这是回测引擎的核心，包含投资组合表示和交易模拟的逻辑。它使用 `config.py` 中的配置和 `data.py` 中的数据来运行回测。
*   **核心组件与用法**:
    *   `Series` 类: 表示一个投资组合。其主要优势在于能够管理同一基础投资组合数据的不同视图。
        *   **应用场景**: 您可以使用 `Series` 对象来表示每个时间步长所需的投资组合 (`hope_portfolio`)。
        *   **调用示例**:
            ```python
            # 创建一个在三只股票上具有相等权重的投资组合
            my_portfolio = Series({'stock_A': 0.33, 'stock_B': 0.33, 'stock_C': 0.34}, name='2025-07-10', unit='weight')
            
            # 假设总资产为 1,000,000 美元，将投资组合转换为资产价值
            assets_portfolio = my_portfolio.to('assets', assets=1000000)
            
            # 使用未复权价格转换为所需股份数
            share_portfolio = assets_portfolio.to('share', is_adj=False)
            ```
    *   `link` 类: 模拟单个交易日的事件，将投资组合从 T-1 连接到 T。
        *   **应用场景**: 在回测循环中，您将为每一天创建一个 `link` 对象，以计算实际交易、最终的投资组合和性能指标。
        *   **调用示例**:
            ```python
            # settle_T0 是前一天的投资组合
            # hope_T1 是您今天的目标投资组合
            daily_link = link(settle_portfolio_T0=settle_T0, order_portfolio_T0=order_T0, hope_portfolio_T1=hope_T1)
            
            # 获取今天的最终结算投资组合
            settle_T1 = daily_link.settle_T1
            
            # 获取当天的换手率
            daily_turnover = daily_link.turnover
            ```

## 其他有用的信息

*   **核心概念与设计哲学**:
    *   **向量化**: 该框架旨在通过使用向量化操作（得益于 pandas）而不是逐个迭代股票来提高效率。这就是为什么 `data.py` 中的数据预处理至关重要。
    *   **状态和单位管理**: `Series` 类抽象了投资组合会计的复杂性。只需更改 `unit` 或 `state` 属性，您就可以获得投资组合的不同视图，而无需手动计算。这是该框架灵活性的关键。
    *   **配置驱动**: 所有主要参数都在 `config.py` 中定义。这使得测试不同的情景（例如，更高的交易成本）变得容易，而无需更改核心模拟逻辑。

*   **快速上手 / 用法示例**:
    这是一个简化的回测循环示例：
    ```python
    import pandas as pd
    from __back_test__.main import Series, link

    # 1. 定义策略每天的目标投资组合
    trade_dates = pd.to_datetime(['2025-07-10', '2025-07-11'])
    hope_portfolios = {
        trade_dates[0]: Series({'stock_A': 0.5, 'stock_B': 0.5}, name=trade_dates[0], unit='weight'),
        trade_dates[1]: Series({'stock_A': 0.4, 'stock_C': 0.6}, name=trade_dates[1], unit='weight')
    }

    # 2. 初始化变量
    settle_portfolio = None
    order_portfolio = None
    initial_assets = 1000000

    # 3. 运行回测循环
    for date in trade_dates:
        hope_portfolio = hope_portfolios[date]
        
        # 模拟当天的交易
        daily_link = link(settle_portfolio, order_portfolio, hope_portfolio, init_assets=initial_assets)
        
        # 为下一次迭代更新投资组合
        settle_portfolio = daily_link.settle_T1
        order_portfolio = daily_link.order_T1
        initial_assets = None # 仅在第一天使用
        
        print(f"日期: {date.date()}, 资产: {settle_portfolio.total_assets():.2f}, 换手率: {daily_link.turnover:.2%}")

    ```