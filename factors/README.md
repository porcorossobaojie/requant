# `factors` Module Documentation

## Introduction

The `factors` module is a comprehensive library for calculating and managing various quantitative factors used in financial analysis and trading strategies. It provides a structured approach to define, compute, and filter factors, integrating with data sources and offering specialized functionalities for different factor categories like volatility, equity, and industry.

## File and Module Structure

```
factors/
├── __init__.py
├── config.py
├── barra/
│   ├── __init__.py
│   ├── barra_cne6_factor.py
│   └── ...
├── equity/
│   ├── __init__.py
│   └── main.py
├── industry/
│   ├── __init__.py
│   └── main.py
├── meta/
│   ├── __init__.py
│   └── main.py
├── volatility/
│   ├── __init__.py
│   └── main.py
└── README.md
```

## Module Overview and Architecture

The `factors` module is designed to be modular and extensible, with each sub-directory representing a distinct category of factors or a specific methodology. It relies on the `flow` module for data access and `__pandas__` for enhanced data manipulation capabilities.

**Dependencies and Conceptual Flow:**

*   **`config.py`**: Centralizes configuration settings for various factor types, including data property attributes, filtering limits (e.g., ST status, listing days), and specific parameters for volatility and industry factors.
*   **`meta/main.py`**: Serves as the base class (`meta`) for all factor calculations. It provides common functionalities such as data filtering (tradeable, on-list, non-ST), parameter standardization, and factor merging.
*   **`barra/barra_cne6_factor.py`**: Implements Barra-style factors (e.g., Size, Volatility, Liquidity, Momentum, Quality, Value, Growth, DividendYield) based on the CNE6 model. It includes complex calculations for various financial metrics and statistical regressions.
*   **`equity/main.py`**: Focuses on calculating equity-specific factors like Assets Premium and Operating Premium.
*   **`industry/main.py`**: Specializes in industry-related factors, including industry momentum and preference, based on different industry classifications (Shenwan, CSRC, JQData).
*   **`volatility/main.py`**: Provides methods for calculating various volatility factors based on trading amount, turnover, and price movements.
*   **`__init__.py`**: Orchestrates the initialization of the `factors` package, including importing `daily` from `__data_source__` and making specific factor classes (like `volatility`) directly accessible.

**Conceptual Flow (Box-and-Line Diagram):**

```
+-----------------+
| User/Application|
+--------+--------+
         |
         v
+--------+--------------------------------+
| factors/__init__.py                    |
| (Initializes package, exposes factors) |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| factors/meta/main.py                   |
| (Base class for all factors, provides  |
|  common filtering and merging)         |
+--------+--------------------------------+
         |
         v
+-----------------------------------------+
| Specific Factor Modules (e.g., barra,  |
|  equity, industry, volatility)         |
| (Implement detailed factor calculations)|
+-----------------------------------------+
         |
         v
+--------+--------------------------------+
| factors/config.py                      |
| (Centralized configuration for factors)|
+----------------------------------------+
         |
         v
+--------+--------------------------------+
| flow (Data Access)                     |
+----------------------------------------+
```

## Purpose of Each Module

*   **`__init__.py` (in `factors/`)**:
    *   Initializes the `factors` package.
    *   Imports `daily` function from `__data_source__` for daily data updates.
    *   Exposes `volatility` factor class for direct access.

*   **`config.py`**:
    *   **`PROPERTY_ATTRS_DIC`**: Dynamically generated dictionary mapping simplified attribute names to their full `S_DQ_` prefixed names from `flow.stock` help information.
    *   **`PROPERTY_ATTRS_CLS`**: A type created from `PROPERTY_ATTRS_DIC` for easy access to data property attributes.
    *   **`LIMIT` Class**: Defines global filtering limits for factors, such as `IS_ST_FILTER` (for ST stocks) and `ON_LIST_LIMIT` (for listing days).
    *   **`volatility` Class**: Contains configuration for volatility-related factors, including `__AMOUNT__`, `__TURNOVER__`, and `__REVERSAL__` classes that specify `periods` for calculations.
    *   **`industry` Class**: Defines keys for different industry classification systems (Shenwan, CSRC, JQData) used in industry factor calculations.

*   **`barra/barra_cne6_factor.py`**:
    *   Implements a wide range of Barra-style factors based on the CNE6 model.
    *   Includes classes for `Size`, `Volatility`, `Liquidity`, `Momentum`, `Quality` (with `Leverage`, `EarningsVariablity`, `EarningsQuality`, `Profitability`, `InvestmentQuality` subclasses), `Value` (with `EarningsYield`, `LongTermReversal` subclasses), `Growth`, and `DividendYield`.
    *   Each factor class contains `@lazyproperty` decorated methods to calculate specific factor values (e.g., `LNCAP`, `BETA`, `STOM`, `RSTR`, `MLEV`, `BTOP`, `EGRO`, `DTOP`).
    *   Utilizes parallel computation (`parallelcal`) and various data cleaning and transformation utilities.

*   **`equity/main.py`**:
    *   **`main` Class**: Calculates equity-specific factors.
        *   `ASSETS_PREM`: Calculates the Assets Premium factor based on total assets, liabilities, and market value.
        *   `OPER_PREM`: Calculates the Operating Premium factor based on operating revenue, cost, and market value.
        *   `PROFIT_PREM`: Placeholder for Profit Premium factor calculation.
        *   `indust_prem`: Placeholder for Industry Premium factor calculation.

*   **`industry/main.py`**:
    *   **`main` Class**: Calculates industry-related factors.
        *   `__industry_momentum__`: Internal method to calculate industry momentum for given classification keys.
        *   `sw`, `zjw`, `jq`, `all_industry`: Public methods to calculate industry momentum for specific or all defined industry classifications.
        *   `industry_momentum`: Calculates combined industry momentum across different lookback periods.
        *   `__industry_prefer__`: Internal method to calculate industry preference based on a factor and industry classification keys.
        *   `indust_lag`: Placeholder for industry lag calculation.

*   **`meta/main.py`**:
    *   **`main` Class**: The base class for all factor calculations.
        *   `trade_days`: Provides access to trading days from the `flow` module.
        *   `is_tradeable`, `is_on_list`, `is_not_st`: Methods to check stock status based on trade status, listing days, and ST status.
        *   `mask`: Generates a combined boolean mask for filtering stocks.
        *   `settle`, `trade`, `filter`: Apply filtering conditions to DataFrames.
        *   `parameter_standard`: Standardizes parameters using a sigmoid-like transformation.
        *   `reversal`: Calculates the reversal component of a DataFrame.
        *   `merge`: Merges multiple factor DataFrames, with optional standardization.

*   **`volatility/main.py`**:
    *   **`main` Class**: Calculates volatility-related factors.
        *   `AMOUNT`: Calculates volatility factors based on trading amount (standard deviation, mean, Z-score of differences).
        *   `TURNOVER`: Calculates volatility factors based on turnover (similar to `AMOUNT`).
        *   `REVERSAL`: Calculates reversal factors based on price movements.
        *   `RE_CORR_TURN`: Calculates the correlation between returns and turnover.
        *   `amount_std`, `amount_z`, `tu_std`: More granular methods for calculating standard deviation and Z-scores of amount and turnover.
        *   `volatility`: Combines various volatility factors into a single factor.
        *   `abnormal1`: Calculates an abnormal return factor.

## Other Helpful Information

*   **Factor Categorization**: Factors are organized into logical categories (e.g., `barra`, `equity`, `industry`, `volatility`) for better management and understanding.
*   **Data Integration**: Seamlessly integrates with the `flow` module to access and process raw financial data, ensuring factors are calculated on up-to-date information.
*   **Extensibility**: The modular design and the `meta` base class make it easy to add new factor calculation methods or entirely new factor categories.
*   **Pandas-Centric**: Leverages pandas DataFrames and Series extensively for efficient data manipulation and numerical operations.
*   **Quantitative Finance Focus**: All factors and methodologies are tailored for quantitative finance applications, providing tools for signal generation in trading strategies.

---

# `factors` 模块文档

## 简介

`factors` 模块是一个用于计算和管理金融分析和交易策略中使用的各种量化因子的综合库。它提供了一种结构化的方法来定义、计算和过滤因子，与数据源集成，并为波动率、股票和行业等不同因子类别提供专业功能。

## 文件和模块结构

```
factors/
├── __init__.py
├── config.py
├── barra/
│   ├── __init__.py
│   ├── barra_cne6_factor.py
│   └── ...
├── equity/
│   ├── __init__.py
│   └── main.py
├── industry/
│   ├── __init__.py
│   └── main.py
├── meta/
│   ├── __init__.py
│   └── main.py
├── volatility/
│   ├── __init__.py
│   └── main.py
└── README.md
```

## 模块概览与架构

`factors` 模块被设计为模块化和可扩展的，每个子目录代表一个不同的因子类别或特定的方法。它依赖 `flow` 模块进行数据访问，并依赖 `__pandas__` 进行增强的数据操作功能。

**依赖关系和概念流程：**

*   **`config.py`**: 集中管理各种因子类型的配置设置，包括数据属性、过滤限制（例如，ST 状态、上市天数）以及波动率和行业因子的特定参数。
*   **`meta/main.py`**: 作为所有因子计算的基类（`meta`）。它提供通用功能，例如数据过滤（可交易、已上市、非 ST）、参数标准化和因子合并。
*   **`barra/barra_cne6_factor.py`**: 基于 CNE6 模型实现 Barra 风格的因子（例如，规模、波动率、流动性、动量、质量、价值、增长、股息收益率）。它包括各种财务指标和统计回归的复杂计算。
*   **`equity/main.py`**: 专注于计算股票特定因子，如资产溢价和营业溢价。
*   **`industry/main.py`**: 专注于行业相关因子，包括基于不同行业分类（申万、证监会、聚宽）的行业动量和偏好。
*   **`volatility/main.py`**: 提供基于交易量、换手率和价格变动计算各种波动率因子。
*   **`__init__.py`**: 协调 `factors` 包的初始化，包括从 `__data_source__` 导入 `daily` 并使特定因子类（如 `volatility`）直接可访问。

**概念流程图（框线图）：**

```
+-----------------+
| 用户/应用程序   |
+--------+--------+
         |
         v
+--------+--------------------------------+
| factors/__init__.py                    |
| (初始化包，暴露因子)                   |
+--------+--------------------------------+
         |
         v
+--------+--------------------------------+
| factors/meta/main.py                   |
| (所有因子的基类，提供通用过滤和合并)   |
+--------+--------------------------------+
         |
         v
+-----------------------------------------+
| 特定因子模块（例如，barra，             |
|  equity，industry，volatility）         |
| (实现详细的因子计算)                   |
+-----------------------------------------+
         |
         v
+--------+--------------------------------+
| factors/config.py                      |
| (因子的集中配置)                       |
+----------------------------------------+
         |
         v
+--------+--------------------------------+
| flow (数据访问)                        |
+----------------------------------------+
```

## 各个模块的用途

*   **`__init__.py` (在 `factors/`)**:
    *   初始化 `factors` 包。
    *   从 `__data_source__` 导入 `daily` 函数，用于每日数据更新。
    *   暴露 `volatility` 因子类以供直接访问。

*   **`config.py`**:
    *   **`PROPERTY_ATTRS_DIC`**: 动态生成的字典，将简化属性名称映射到 `flow.stock` 帮助信息中带有 `S_DQ_` 前缀的完整名称。
    *   **`PROPERTY_ATTRS_CLS`**: 从 `PROPERTY_ATTRS_DIC` 创建的类型，用于轻松访问数据属性。
    *   **`LIMIT` 类**: 定义因子的全局过滤限制，例如 `IS_ST_FILTER`（用于 ST 股票）和 `ON_LIST_LIMIT`（用于上市天数）。
    *   **`volatility` 类**: 包含波动率相关因子的配置，包括 `__AMOUNT__`、`__TURNOVER__` 和 `__REVERSAL__` 类，它们指定计算的 `periods`。
    *   **`industry` 类**: 定义用于行业因子计算的不同行业分类系统（申万、证监会、聚宽）的键。

*   **`barra/barra_cne6_factor.py`**:
    *   实现基于 CNE6 模型的各种 Barra 风格因子。
    *   包括 `Size`、`Volatility`、`Liquidity`、`Momentum`、`Quality`（包含 `Leverage`、`EarningsVariablity`、`EarningsQuality`、`Profitability`、`InvestmentQuality` 子类）、`Value`（包含 `EarningsYield`、`LongTermReversal` 子类）、`Growth` 和 `DividendYield` 的类。
    *   每个因子类都包含 `@lazyproperty` 装饰的方法来计算特定的因子值（例如，`LNCAP`、`BETA`、`STOM`、`RSTR`、`MLEV`、`BTOP`、`EGRO`、`DTOP`）。
    *   利用并行计算（`parallelcal`）和各种数据清理和转换实用程序。

*   **`equity/main.py`**:
    *   **`main` 类**: 计算股票特定因子。
        *   `ASSETS_PREM`: 根据总资产、负债和市值计算资产溢价因子。
        *   `OPER_PREM`: 根据营业收入、成本和市值计算营业溢价因子。
        *   `PROFIT_PREM`: 利润溢价因子计算的占位符。
        *   `indust_prem`: 行业溢价因子计算的占位符。

*   **`industry/main.py`**:
    *   **`main` 类**: 计算行业相关因子。
        *   `__industry_momentum__`: 内部方法，用于计算给定分类键的行业动量。
        *   `sw`、`zjw`、`jq`、`all_industry`: 用于计算特定或所有已定义行业分类的行业动量的公共方法。
        *   `industry_momentum`: 计算不同回溯期内的组合行业动量。
        *   `__industry_prefer__`: 内部方法，用于根据因子和行业分类键计算行业偏好。
        *   `indust_lag`: 行业滞后计算的占位符。

*   **`meta/main.py`**:
    *   **`main` 类**: 所有因子计算的基类。
        *   `trade_days`: 提供从 `flow` 模块访问交易日。
        *   `is_tradeable`、`is_on_list`、`is_not_st`: 根据交易状态、上市天数和 ST 状态检查股票状态的方法。
        *   `mask`: 生成用于过滤股票的组合布尔掩码。
        *   `settle`、`trade`、`filter`: 将过滤条件应用于 DataFrame。
        *   `parameter_standard`: 使用类似 sigmoid 的变换标准化参数。
        *   `reversal`: 计算 DataFrame 的反转分量。
        *   `merge`: 合并多个因子 DataFrame，可选进行标准化。

*   **`volatility/main.py`**:
    *   **`main` 类**: 计算波动率相关因子。
        *   `AMOUNT`: 根据交易量计算波动率因子（标准差、均值、差异的 Z 分数）。
        *   `TURNOVER`: 根据换手率计算波动率因子（类似于 `AMOUNT`）。
        *   `REVERSAL`: 根据价格变动计算反转因子。
        *   `RE_CORR_TURN`: 计算收益与换手率之间的相关性。
        *   `amount_std`、`amount_z`、`tu_std`: 更细粒度的方法，用于计算交易量和换手率的标准差和 Z 分数。
        *   `volatility`: 将各种波动率因子组合成一个因子。
        *   `abnormal1`: 计算异常收益因子。

## 其他有用的信息

*   **因子分类**: 因子被组织成逻辑类别（例如，`barra`、`equity`、`industry`、`volatility`），以便更好地管理和理解。
*   **数据集成**: 与 `flow` 模块无缝集成，以访问和处理原始财务数据，确保因子在最新信息上计算。
*   **可扩展性**: 模块化设计和 `meta` 基类使得添加新的因子计算方法或全新的因子类别变得容易。
*   **以 Pandas 为中心**: 广泛利用 Pandas DataFrame 和 Series 进行高效的数据操作和数值运算。
*   **量化金融焦点**: 所有因子和方法都专为量化金融应用量身定制，为交易策略中的信号生成提供工具。
