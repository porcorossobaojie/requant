# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from typing import Optional, Any, List

from libs.utils.finance.build.main import portfolio


def maxdown(df_obj: pd.DataFrame, iscumprod: bool) -> pd.DataFrame:
    """
    ===========================================================================

    Calculates the maximum drawdown of a return series.

    This function computes the maximum drawdown, including the start date,
    end date, and the percentage of the drop.

    ---------------------------------------------------------------------------

    计算收益序列的最大回撤。

    此函数计算最大回撤，包括开始日期、结束日期和下跌百分比。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    df_obj : pd.DataFrame
        DataFrame of returns or cumulative returns.
    iscumprod : bool
        If True, the input is already a cumulative product series.

    ---------------------------------------------------------------------------

    参数
    ----------
    df_obj : pd.DataFrame
        收益率或累积收益率的 DataFrame。
    iscumprod : bool
        如果为 True，则输入已经是累积乘积序列。

    ---------------------------------------------------------------------------

    Returns
    -------
    pd.DataFrame
        A DataFrame containing max drawdown details.

    ---------------------------------------------------------------------------

    返回
    -------
    pd.DataFrame
        一个包含最大回撤详细信息的 DataFrame。

    ---------------------------------------------------------------------------
    """
    if not iscumprod:
        x = df_obj.add(1, fill_value=0).cumprod()
        x[df_obj.isnull()] = pd.NA
    else:
        x = df_obj

    max_flow = x.expanding(min_periods=1).max()
    down_date = (x / max_flow).idxmin()
    max_down_series = x / max_flow - 1

    down_info = [(x.loc[j, i] if pd.notnull(j) else np.nan, max_down_series.loc[j, i] if pd.notnull(j) else np.nan) for i, j in down_date.items()]
    down_value, max_down_value = list(zip(*down_info))

    up_value = pd.Series([max_flow.loc[j, i] if pd.notnull(j) else np.nan for i, j in down_date.items()], index=down_date.index)
    up_date = max_flow[max_flow == up_value].idxmin()

    df = pd.DataFrame(
        [up_date.values, up_value.values, down_date.values, down_value, max_down_value],
        columns=df_obj.columns,
        index=['Maxdown_Start_Date', 'Maxdown_Start_Value', 'Maxdown_End_Date', 'Maxdown_End_Value', 'Maxdwon_Percent']
    )
    return df


def sharpe(df_obj: pd.DataFrame, iscumprod: bool, periods: Optional[int]) -> pd.Series:
    """
    ===========================================================================

    Calculates the Sharpe ratio.

    Computes the Sharpe ratio, annualized if a period is provided.

    ---------------------------------------------------------------------------

    计算夏普比率。

    计算夏普比率，如果提供周期则进行年化处理。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    df_obj : pd.DataFrame
        DataFrame of returns or cumulative returns.
    iscumprod : bool
        If True, the input is a cumulative product series.
    periods : Optional[int]
        The number of periods to annualize the Sharpe ratio (e.g., 252 for daily).

    ---------------------------------------------------------------------------

    参数
    ----------
    df_obj : pd.DataFrame
        收益率或累积收益率的 DataFrame。
    iscumprod : bool
        如果为 True，则输入是累积乘积序列。
    periods : Optional[int]
        用于年化夏普比率的周期数（例如，日度数据为 252）。

    ---------------------------------------------------------------------------

    Returns
    -------
    pd.Series
        The calculated Sharpe ratio.

    ---------------------------------------------------------------------------

    返回
    -------
    pd.Series
        计算出的夏普比率。

    ---------------------------------------------------------------------------
    """
    x = df_obj if not iscumprod else df_obj.pct_change(fill_method=None)
    y = x.mean() / x.std()

    if periods is not None:
        periods = min(len(x), periods)
        y = y * (periods ** 0.5)

    y.name = f'sharpe_ratio(periods={periods})'
    return y


def effective(df_obj: pd.DataFrame) -> pd.Series:
    """
    ===========================================================================

    Calculates a row-wise effectiveness score based on horizontal changes.

    This function computes a score for each row by taking the difference
    across columns, squaring it, and summing the result.

    ---------------------------------------------------------------------------

    基于水平变化计算逐行的有效性得分。

    该函数通过计算跨列差异、平方并求和来为每行计算一个分数。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    df_obj : pd.DataFrame
        The DataFrame to process.

    ---------------------------------------------------------------------------

    参数
    ----------
    df_obj : pd.DataFrame
        要处理的 DataFrame。

    ---------------------------------------------------------------------------

    Returns
    -------
    pd.Series
        A Series containing the effectiveness score for each row.

    ---------------------------------------------------------------------------

    返回
    -------
    pd.Series
        一个包含每行有效性得分的 Series。

    ---------------------------------------------------------------------------
    """
    x = df_obj.diff(axis=1)
    x = np.sign(x) * x ** 2
    x = x.sum(axis=1)
    return x


def expose(df_obj: pd.DataFrame, weight: Optional[pd.DataFrame], standard_method='uniform', *unnamed_factors, **named_factors: pd.DataFrame) -> Any:
    """
    ===========================================================================

    Calculates portfolio returns exposed to specified risk factors.

    This function standardizes risk factors and then calculates the portfolio
    returns based on exposure to these factors.

    ---------------------------------------------------------------------------

    计算暴露于指定风险因子下的投资组合收益。

    此函数将风险因子标准化，然后基于对这些因子的暴露度计算投资组合收益。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    df_obj : pd.DataFrame
        The primary data, typically returns.
    weight : Optional[pd.DataFrame]
        The weights for the portfolio construction.
    standard_method : str, optional
        The standardization method ('uniform' or 'gauss'), by default 'uniform'.
    unnamed_factors : pd.DataFrame
        Unnamed factor DataFrames.
    named_factors : pd.DataFrame
        Named factor DataFrames.

    ---------------------------------------------------------------------------

    参数
    ----------
    df_obj : pd.DataFrame
        主数据，通常是收益率。
    weight : Optional[pd.DataFrame]
        用于构建投资组合的权重。
    standard_method : str, optional
        标准化方法（'uniform' 或 'gauss'），默认为 'uniform'。
    unnamed_factors : pd.DataFrame
        未命名的因子 DataFrame。
    named_factors : pd.DataFrame
        命名的因子 DataFrame。

    ---------------------------------------------------------------------------

    Returns
    -------
    Any
        A DataFrame or Series representing the factor-exposed returns.

    ---------------------------------------------------------------------------

    返回
    -------
    Any
        一个表示因子暴露收益的 DataFrame 或 Series。

    ---------------------------------------------------------------------------
    """
    # Lazy import to avoid circular dependency
    from libs.utils.finance.stats.main import standard

    factors = {f'unnamed_factor_{i}': j for i, j in enumerate(unnamed_factors)} | named_factors

    if standard_method == 'uniform':
        factors = {i: standard(j, method=standard_method, rank=(-1, 1)) for i, j in factors.items()}
    elif standard_method == 'gauss':
        factors = {i: standard(j, method=standard_method, rank=(-5, 5)) for i, j in factors.items()}

    df = {i: portfolio(df_obj, returns=j, weight=weight, shift=0) for i, j in factors.items()}

    if len(df) > 1:
        df = pd.concat(df, axis=100)
    else:
        df = list(df.values())[0]
    return df
