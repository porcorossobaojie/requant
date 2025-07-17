# `finance` Module Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction

The `finance` module is a core component of the quantitative analysis project, providing a comprehensive suite of tools for financial data processing, statistical analysis, and portfolio construction. It is designed to handle various aspects of quantitative finance, from basic data manipulation to advanced statistical modeling and backtesting preparation.

## File and Module Structure

```
finance/
├── analysis/               # Financial analysis functions
│   └── main.py             # - maxdown(): Calculates maximum drawdown
│                           # - sharpe(): Computes Sharpe ratio
│                           # - effective(): Calculates effectiveness score
│                           # - expose(): Analyzes factor exposure
├── build/                  # Portfolio construction and data transformation
│   └── main.py             # - group(): Groups and ranks data
│                           # - weight(): Applies weights to data
│                           # - portfolio(): Constructs and evaluates portfolios
│                           # - cut(): Selects data based on rank with hysteresis
├── roll/                   # Rolling window operations
│   ├── base.py             # - ts_rank_unit(): Time-series rank unit
│                           # - ts_sort_unit(): Time-series sort unit
│                           # - ts_argsort_unit(): Time-series argsort unit
│   └── main.py             # - rolls(): Main interface for rolling calculations
│                           #   - max(): Rolling maximum
│                           #   - min(): Rolling minimum
│                           #   - ts_rank(): Time-series rolling rank
├── stats/                  # Statistical functions for quantitative analysis
│   └── main.py             # - standard(): Standardizes data (Gaussian/Uniform)
│                           # - OLS(): Performs Ordinary Least Squares regression
│                           # - neutral(): Performs factor neutralization
├── tools/                  # General utility functions for financial data
│   └── main.py             # - fillna(): Forward fills DataFrame
│                           # - shift(): Conditionally shifts DataFrame columns
│                           # - log(): Applies sign-adjusted logarithmic transformation
└── __init__.py             # Module initialization
```

## Module Overview and Architecture

The `finance` module is structured into several sub-modules, each focusing on a specific aspect of quantitative finance. Data typically flows from `tools` (for basic manipulation) to `build` (for portfolio construction) and `stats` (for advanced analysis), with `roll` providing time-series specific operations, and `analysis` offering higher-level financial metrics.

```
+-----------------+
|  `tools/main.py`|
|  (fillna, shift)|
+--------+--------+
         |
         v
+--------+--------------------------------+
|  `build/main.py`                       |
|  (group, weight, portfolio, cut)       |
+--------+--------------------------------+
         |                                |
         +--------------------------------+
         |                                |
         v                                v
+--------+--------+             +--------+--------+
|  `stats/main.py`|             |  `roll/main.py` |
|  (standard, OLS,|             |  (rolls, _max,  |
|  neutral)       |             |  _min, _rank)   |
+--------+--------+             +--------+--------+
         |
         v
+--------+--------+
|  `analysis/main.py`|
|  (maxdown, sharpe,|
|  effective, expose)|
+-------------------+
```

## Purpose of Each Module

### `analysis` Module

*   **Positioning and Role**: Provides functions for calculating key financial performance metrics and analyzing factor exposures. It sits at a higher level, consuming processed data to derive insights.
*   **Key Components and Usage**:
    *   `maxdown(df_obj: pd.DataFrame, iscumprod: bool) -> pd.DataFrame`: Calculates the maximum drawdown of a return series. Essential for risk assessment.
        ```python
        import pandas as pd
        from libs.utils.finance.analysis.main import maxdown

        returns = pd.DataFrame({'asset1': [0.01, -0.02, 0.03, -0.04, 0.05]})
        drawdown_info = maxdown(returns, iscumprod=False)
        print(drawdown_info)
        ```
    *   `sharpe(df_obj: pd.DataFrame, iscumprod: bool, periods: Optional[int]) -> pd.Series`: Computes the Sharpe ratio, a measure of risk-adjusted return.
        ```python
        import pandas as pd
        from libs.utils.finance.analysis.main import sharpe

        returns = pd.DataFrame({'asset1': [0.01, -0.005, 0.015, -0.002]})
        sharpe_ratio = sharpe(returns, iscumprod=False, periods=252)
        print(sharpe_ratio)
        ```

### `build` Module

*   **Positioning and Role**: Focuses on data transformation and portfolio construction. It provides tools to group, weight, and combine financial data for various analytical purposes.
*   **Key Components and Usage**:
    *   `portfolio(df_obj: pd.DataFrame, returns: pd.DataFrame, weight: Optional[pd.DataFrame] = None, shift: int = 1) -> pd.DataFrame`: Constructs portfolios based on factor exposures and calculates returns.
        ```python
        import pandas as pd
        from libs.utils.finance.build.main import portfolio

        factors = pd.DataFrame({'factor1': [1, 2, 3], 'factor2': [0.5, 1.5, 2.5]})
        asset_returns = pd.DataFrame({'assetA': [0.01, 0.02, 0.03], 'assetB': [0.005, 0.01, 0.015]})
        port_returns = portfolio(factors, asset_returns)
        print(port_returns)
        ```
    *   `weight(df: pd.DataFrame, w_df: Optional[pd.DataFrame] = None, pct: bool = True) -> pd.DataFrame`: Applies weights to a DataFrame, useful for portfolio allocation.
        ```python
        import pandas as pd
        from libs.utils.finance.build.main import weight

        data = pd.DataFrame({'val1': [10, 20], 'val2': [30, 40]})
        weights = pd.DataFrame({'val1': [0.4, 0.6], 'val2': [0.6, 0.4]})
        weighted_data = weight(data, weights)
        print(weighted_data)
        ```

### `roll` Module

*   **Positioning and Role**: Dedicated to time-series rolling window operations. It provides a flexible framework for applying various functions over rolling periods, crucial for dynamic analysis.
*   **Key Components and Usage**:
    *   `rolls(pandas_obj: pd.DataFrame, window: int, min_periods: Optional[int] = None)`: The main class for time-series rolling operations.
        ```python
        import pandas as pd
        from libs.utils.finance.roll.main import rolls

        data = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
        rolling_data = rolls(data, window=3)
        max_values = rolling_data.max()
        print(max_values)
        ```
    *   `ts_rank(pct: bool = True) -> pd.DataFrame`: Calculates the time-series rolling rank.
        ```python
        import pandas as pd
        from libs.utils.finance.roll.main import rolls

        data = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
        rolling_data = rolls(data, window=3)
        ranks = rolling_data.ts_rank(pct=True)
        print(ranks)
        ```

### `stats` Module

*   **Positioning and Role**: Contains statistical functions primarily used for quantitative analysis, including data standardization and regression analysis. It supports advanced modeling techniques.
*   **Key Components and Usage**:
    *   `standard(df_obj: Union[pd.Series, pd.DataFrame], method: str = 'gauss') -> Union[pd.Series, pd.DataFrame]`: Standardizes data using Gaussian or uniform methods.
        ```python
        import pandas as pd
        from libs.utils.finance.stats.main import standard

        data = pd.Series([1, 2, 3, 4, 5])
        standardized_data = standard(data, method='gauss')
        print(standardized_data)
        ```
    *   `neutral(df_obj: pd.DataFrame, const: bool = True, **key_dfs: pd.DataFrame) -> Any`: Performs factor neutralization using linear regression.
        ```python
        import pandas as pd
        from libs.utils.finance.stats.main import neutral

        dependent_var = pd.DataFrame({'Y': [10, 12, 15, 13, 16]})
        factor1 = pd.DataFrame({'X1': [1, 2, 3, 4, 5]})
        factor2 = pd.DataFrame({'X2': [5, 4, 3, 2, 1]})
        neutralized_result = neutral(dependent_var, factor1=factor1, factor2=factor2)
        print(neutralized_result.params)
        ```

### `tools` Module

*   **Positioning and Role**: Provides general utility functions for common financial data manipulations. It serves as a foundational layer for other modules.
*   **Key Components and Usage**:
    *   `fillna(df_obj: pd.DataFrame, fill_list: List[Any]) -> pd.DataFrame`: Forward fills a DataFrame based on a new index.
        ```python
        import pandas as pd
        from libs.utils.finance.tools.main import fillna

        data = pd.DataFrame({'A': [1, None, 3]}, index=[1, 3, 5])
        new_index = [1, 2, 3, 4, 5]
        filled_data = fillna(data, new_index)
        print(filled_data)
        ```
    *   `log(df_obj: pd.DataFrame, bias_adj: Union[int, float] = 1, abs_adj: bool = True) -> pd.DataFrame`: Applies a sign-adjusted logarithmic transformation.
        ```python
        import pandas as pd
        from libs.utils.finance.tools.main import log

        data = pd.DataFrame({'A': [-1, 2, -3]})
        logged_data = log(data)
        print(logged_data)
        ```

## Other Helpful Information

### Quick Start / Usage Example

To quickly get started with the `finance` module, you can combine functions from different sub-modules to perform a basic factor analysis:

```python
import pandas as pd
from libs.utils.finance.tools.main import fillna
from libs.utils.finance.stats.main import standard
from libs.utils.finance.build.main import portfolio
from libs.utils.finance.analysis.main import sharpe

# 1. Sample Data
# Assume daily returns for multiple assets
returns_data = {
    'AAPL': [0.01, 0.005, -0.002, 0.015, 0.008],
    'MSFT': [0.008, 0.012, 0.001, -0.005, 0.01],
    'GOOG': [0.005, 0.003, 0.01, 0.007, -0.003]
}
index_dates = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'])
asset_returns = pd.DataFrame(returns_data, index=index_dates)

# Assume a simple factor (e.g., a momentum-like factor)
factor_data = {
    'AAPL': [1, 1.2, 1.1, 1.3, 1.4],
    'MSFT': [0.8, 0.9, 1.0, 0.95, 1.1],
    'GOOG': [1.1, 1.0, 0.9, 0.8, 0.7]
}
factor = pd.DataFrame(factor_data, index=index_dates)

# 2. Standardize the factor
standardized_factor = standard(factor, method='uniform', rank=(-1, 1))
print("\nStandardized Factor:\n", standardized_factor)

# 3. Construct a simple portfolio based on the factor (e.g., equal weight for simplicity)
# For this example, let's assume we want to create a portfolio where assets are weighted by their factor value
# This is a simplified weighting, in a real scenario, 'weight' function would be used more robustly
portfolio_returns = portfolio(standardized_factor, asset_returns)
print("\nPortfolio Returns:\n", portfolio_returns)

# 4. Calculate Sharpe Ratio of the portfolio
sharpe_ratio = sharpe(portfolio_returns, iscumprod=False, periods=252)
print("\nPortfolio Sharpe Ratio:\n", sharpe_ratio)
```

### Core Concepts and Design Philosophy

This module emphasizes:
*   **Vectorization**: Prioritizing `pandas` and `numpy` operations for performance in quantitative analysis.
*   **Modularity**: Each sub-module and function has a clear, focused responsibility.
*   **Type Hinting**: Extensive use of type hints for improved readability, maintainability, and static analysis.
*   **Bilingual Documentation**: All public-facing functions and classes include comprehensive English and Chinese docstrings.

### Known Limitations or Common Pitfalls

*   **Data Alignment**: Ensure all input DataFrames have properly aligned indices and columns to avoid unexpected `NaN` values or miscalculations.
*   **Performance with Large Data**: While vectorized, extremely large datasets might still require memory optimization or chunking strategies.
*   **Assumptions**: Some functions (e.g., `sharpe`) make implicit assumptions about the input data (e.g., daily returns for annualization). Always review function docstrings for specific requirements.

---

# `finance` 模块文档

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 简介

`finance` 模块是量化分析项目的核心组成部分，提供了一套全面的工具，用于金融数据处理、统计分析和投资组合构建。它旨在处理量化金融的各个方面，从基本数据操作到高级统计建模和回测准备。

## 文件和模块结构

```
finance/
├── analysis/               # 金融分析函数
│   └── main.py             # - maxdown(): 计算最大回撤
│                           # - sharpe(): 计算夏普比率
│                           # - effective(): 计算有效性得分
│                           # - expose(): 分析因子暴露
├── build/                  # 投资组合构建和数据转换
│   └── main.py             # - group(): 对数据进行分组和排名
│                           # - weight(): 对数据应用权重
│                           # - portfolio(): 构建和评估投资组合
│                           # - cut(): 基于排名和迟滞效应选择数据
├── roll/                   # 滚动窗口操作
│   ├── base.py             # - ts_rank_unit(): 时间序列排名单元
│                           # - ts_sort_unit(): 时间序列排序单元
│                           # - ts_argsort_unit(): 时间序列 argsort 单元
│   └── main.py             # - rolls(): 滚动计算的主接口
│                           #   - max(): 滚动最大值
│                           #   - min(): 滚动最小值
│                           #   - ts_rank(): 时间序列滚动排名
├── stats/                  # 量化分析的统计函数
│   └── main.py             # - standard(): 标准化数据（高斯/均匀）
│                           # - OLS(): 执行普通最小二乘回归
│                           # - neutral(): 执行因子中性化
├── tools/                  # 金融数据的通用实用函数
│   └── main.py             # - fillna(): 前向填充 DataFrame
│                           # - shift(): 有条件地移动 DataFrame 列
│                           # - log(): 应用符号调整的对数变换
└── __init__.py             # 模块初始化
```

## 模块概览与架构

`finance` 模块由几个子模块组成，每个子模块都专注于量化金融的特定方面。数据通常从 `tools`（用于基本操作）流向 `build`（用于投资组合构建）和 `stats`（用于高级分析），其中 `roll` 提供时间序列特定操作，`analysis` 提供更高级别的金融指标。

```
+-----------------+
|  `tools/main.py`|
|  (fillna, shift)|
+--------+--------+
         |
         v
+--------+--------------------------------+
|  `build/main.py`                       |
|  (group, weight, portfolio, cut)       |
+--------+--------------------------------+
         |                                |
         +--------------------------------+
         |                                |
         v                                v
+--------+--------+             +--------+--------+
|  `stats/main.py`|             |  `roll/main.py` |
|  (standard, OLS,|             |  (rolls, _max,  |
|  neutral)       |             |  _min, _rank)   |
+--------+--------+             +--------+--------+
         |
         v
+--------+--------+
|  `analysis/main.py`|
|  (maxdown, sharpe,|
|  effective, expose)|
+-------------------+
```

## 各个模块的用途

### `analysis` 模块

*   **定位与角色**: 提供用于计算关键财务绩效指标和分析因子暴露的函数。它处于更高级别，消费处理后的数据以获取洞察。
*   **核心组件与用法**:
    *   `maxdown(df_obj: pd.DataFrame, iscumprod: bool) -> pd.DataFrame`: 计算收益序列的最大回撤。对风险评估至关重要。
        ```python
        import pandas as pd
        from libs.utils.finance.analysis.main import maxdown

        returns = pd.DataFrame({'asset1': [0.01, -0.02, 0.03, -0.04, 0.05]})
        drawdown_info = maxdown(returns, iscumprod=False)
        print(drawdown_info)
        ```
    *   `sharpe(df_obj: pd.DataFrame, iscumprod: bool, periods: Optional[int]) -> pd.Series`: 计算夏普比率，衡量风险调整后收益的指标。
        ```python
        import pandas as pd
        from libs.utils.finance.analysis.main import sharpe

        returns = pd.DataFrame({'asset1': [0.01, -0.005, 0.015, -0.002]})
        sharpe_ratio = sharpe(returns, iscumprod=False, periods=252)
        print(sharpe_ratio)
        ```

### `build` 模块

*   **定位与角色**: 专注于数据转换和投资组合构建。它提供工具来分组、加权和组合金融数据，以用于各种分析目的。
*   **核心组件与用法**:
    *   `portfolio(df_obj: pd.DataFrame, returns: pd.DataFrame, weight: Optional[pd.DataFrame] = None, shift: int = 1) -> pd.DataFrame`: 根据因子暴露构建投资组合并计算回报。
        ```python
        import pandas as pd
        from libs.utils.finance.build.main import portfolio

        factors = pd.DataFrame({'factor1': [1, 2, 3], 'factor2': [0.5, 1.5, 2.5]})
        asset_returns = pd.DataFrame({'assetA': [0.01, 0.02, 0.03], 'assetB': [0.005, 0.01, 0.015]})
        port_returns = portfolio(factors, asset_returns)
        print(port_returns)
        ```
    *   `weight(df: pd.DataFrame, w_df: Optional[pd.DataFrame] = None, pct: bool = True) -> pd.DataFrame`: 对 DataFrame 应用权重，适用于投资组合分配。
        ```python
        import pandas as pd
        from libs.utils.finance.build.main import weight

        data = pd.DataFrame({'val1': [10, 20], 'val2': [30, 40]})
        weights = pd.DataFrame({'val1': [0.4, 0.6], 'val2': [0.6, 0.4]})
        weighted_data = weight(data, weights)
        print(weighted_data)
        ```

### `roll` 模块

*   **定位与角色**: 专注于时间序列滚动窗口操作。它提供了一个灵活的框架，用于在滚动周期内应用各种函数，这对于动态分析至关重要。
*   **核心组件与用法**:
    *   `rolls(pandas_obj: pd.DataFrame, window: int, min_periods: Optional[int] = None)`: 时间序列滚动操作的主类。
        ```python
        import pandas as pd
        from libs.utils.finance.roll.main import rolls

        data = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
        rolling_data = rolls(data, window=3)
        max_values = rolling_data.max()
        print(max_values)
        ```
    *   `ts_rank(pct: bool = True) -> pd.DataFrame`: 计算时间序列滚动排名。
        ```python
        import pandas as pd
        from libs.utils.finance.roll.main import rolls

        data = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
        rolling_data = rolls(data, window=3)
        ranks = rolling_data.ts_rank(pct=True)
        print(ranks)
        ```

### `stats` 模块

*   **定位与角色**: 包含主要用于量化分析的统计函数，包括数据标准化和回归分析。它支持高级建模技术。
*   **核心组件与用法**:
    *   `standard(df_obj: Union[pd.Series, pd.DataFrame], method: str = 'gauss') -> Union[pd.Series, pd.DataFrame]`: 使用高斯或均匀方法标准化数据。
        ```python
        import pandas as pd
        from libs.utils.finance.stats.main import standard

        data = pd.Series([1, 2, 3, 4, 5])
        standardized_data = standard(data, method='gauss')
        print(standardized_data)
        ```
    *   `neutral(df_obj: pd.DataFrame, const: bool = True, **key_dfs: pd.DataFrame) -> Any`: 使用线性回归执行因子中性化。
        ```python
        import pandas as pd
        from libs.utils.finance.stats.main import neutral

        dependent_var = pd.DataFrame({'Y': [10, 12, 15, 13, 16]})
        factor1 = pd.DataFrame({'X1': [1, 2, 3, 4, 5]})
        factor2 = pd.DataFrame({'X2': [5, 4, 3, 2, 1]})
        neutralized_result = neutral(dependent_var, factor1=factor1, factor2=factor2)
        print(neutralized_result.params)
        ```

### `tools` 模块

*   **定位与角色**: 提供用于常见金融数据操作的通用实用函数。它作为其他模块的基础层。
*   **核心组件与用法**:
    *   `fillna(df_obj: pd.DataFrame, fill_list: List[Any]) -> pd.DataFrame`: 根据新索引前向填充 DataFrame。
        ```python
        import pandas as pd
        from libs.utils.finance.tools.main import fillna

        data = pd.DataFrame({'A': [1, None, 3]}, index=[1, 3, 5])
        new_index = [1, 2, 3, 4, 5]
        filled_data = fillna(data, new_index)
        print(filled_data)
        ```
    *   `log(df_obj: pd.DataFrame, bias_adj: Union[int, float] = 1, abs_adj: bool = True) -> pd.DataFrame`: 应用符号调整的对数变换。
        ```python
        import pandas as pd
        from libs.utils.finance.tools.main import log

        data = pd.DataFrame({'A': [-1, 2, -3]})
        logged_data = log(data)
        print(logged_data)
        ```

## 其他有用的信息

### 快速上手 / 用法示例

要快速开始使用 `finance` 模块，您可以结合不同子模块的函数来执行基本的因子分析：

```python
import pandas as pd
from libs.utils.finance.tools.main import fillna
from libs.utils.finance.stats.main import standard
from libs.utils.finance.build.main import portfolio
from libs.utils.finance.analysis.main import sharpe

# 1. 示例数据
# 假设多个资产的每日收益
returns_data = {
    'AAPL': [0.01, 0.005, -0.002, 0.015, 0.008],
    'MSFT': [0.008, 0.012, 0.001, -0.005, 0.01],
    'GOOG': [0.005, 0.003, 0.01, 0.007, -0.003]
}
index_dates = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'])
asset_returns = pd.DataFrame(returns_data, index=index_dates)

# 假设一个简单的因子（例如，类似动量的因子）
factor_data = {
    'AAPL': [1, 1.2, 1.1, 1.3, 1.4],
    'MSFT': [0.8, 0.9, 1.0, 0.95, 1.1],
    'GOOG': [1.1, 1.0, 0.9, 0.8, 0.7]
}
factor = pd.DataFrame(factor_data, index=index_dates)

# 2. 标准化因子
standardized_factor = standard(factor, method='uniform', rank=(-1, 1))
print("\n标准化因子:\n", standardized_factor)

# 3. 根据因子构建一个简单的投资组合（例如，为简单起见，等权重）
# 对于此示例，假设我们希望创建一个投资组合，其中资产按其因子值加权
# 这是一个简化的加权，在实际场景中，'weight' 函数将更稳健地使用
portfolio_returns = portfolio(standardized_factor, asset_returns)
print("\n投资组合收益:\n", portfolio_returns)

# 4. 计算投资组合的夏普比率
sharpe_ratio = sharpe(portfolio_returns, iscumprod=False, periods=252)
print("\n投资组合夏普比率:\n", sharpe_ratio)
```

### 核心概念与设计哲学

此模块强调：
*   **向量化**: 优先使用 `pandas` 和 `numpy` 操作以提高量化分析的性能。
*   **模块化**: 每个子模块和函数都有清晰、集中的职责。
*   **类型提示**: 广泛使用类型提示以提高可读性、可维护性和静态分析。
*   **双语文档**: 所有面向公众的函数和类都包含全面的英文和中文文档字符串。

### 已知限制或常见陷阱

*   **数据对齐**: 确保所有输入 DataFrame 具有正确对齐的索引和列，以避免意外的 `NaN` 值或错误计算。
*   **大数据性能**: 尽管是向量化的，但超大型数据集可能仍需要内存优化或分块策略。
*   **假设**: 某些函数（例如 `sharpe`）对输入数据（例如，用于年化的每日收益）做出隐式假设。请务必查阅函数文档字符串以了解具体要求。
