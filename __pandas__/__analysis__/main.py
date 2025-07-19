# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:18:48 2025

@author: Porco Rosso

"""

# Standard library imports

# Third-party library imports
import pandas as pd

# Local project-specific imports
from libs.utils.finance.analysis.main import maxdown, sharpe, effective, expose
from __pandas__.config import ANALYSIS as config


@pd.api.extensions.register_series_accessor(config.CLASS_NAME)
@pd.api.extensions.register_dataframe_accessor(config.CLASS_NAME)
class main:
    """
    ===========================================================================

    Pandas accessor for financial analysis functions.

    This class provides a convenient way to apply financial analysis functions
    (e.g., max drawdown, Sharpe ratio) directly to pandas Series and DataFrames.

    ---------------------------------------------------------------------------

    用于金融分析函数的 Pandas 访问器。

    此类提供了一种方便的方式，可以直接将金融分析函数（例如，最大回撤、夏普比率）
    应用于 pandas Series 和 DataFrame。

    ---------------------------------------------------------------------------
    """
    def __init__(self, pandas_obj: pd.Series | pd.DataFrame):
        """
        ===========================================================================

        Initializes the accessor with a pandas Series or DataFrame.

        Parameters
        ----------
        pandas_obj : pd.Series or pd.DataFrame
            The pandas object to which the accessor is attached.

        ---------------------------------------------------------------------------

        使用 pandas Series 或 DataFrame 初始化访问器。

        参数
        ----------
        pandas_obj : pd.Series 或 pd.DataFrame
            附加访问器的 pandas 对象。

        ---------------------------------------------------------------------------
        """
        self._obj: pd.Series | pd.DataFrame = pandas_obj

    def maxdown(
        self,
        iscumprod: bool = False
    ) -> pd.Series | pd.DataFrame:
        """
        ===========================================================================

        Calculates the maximum drawdown of the Series or DataFrame.

        Parameters
        ----------
        iscumprod : bool, optional
            Whether the input represents cumulative product (e.g., cumulative returns).
            Defaults to False.

        Returns
        -------
        pd.Series or pd.DataFrame
            The maximum drawdown.

        ---------------------------------------------------------------------------

        计算 Series 或 DataFrame 的最大回撤。

        参数
        ----------
        iscumprod : bool, optional
            输入是否表示累积乘积（例如，累积收益）。
            默认为 False。

        返回
        -------
        pd.Series 或 pd.DataFrame
            最大回撤。

        ---------------------------------------------------------------------------
        """
        if isinstance(self._obj, pd.Series):
            return maxdown(self._obj.to_frame(), iscumprod=iscumprod).squeeze()
        else:
            return maxdown(self._obj, iscumprod=iscumprod)

    def sharpe(
        self,
        iscumprod: bool = False,
        periods: int = 252
    ) -> pd.Series | pd.DataFrame:
        """
        ===========================================================================

        Calculates the Sharpe ratio of the Series or DataFrame.

        Parameters
        ----------
        iscumprod : bool, optional
            Whether the input represents cumulative product (e.g., cumulative returns).
            Defaults to False.
        periods : int, optional
            Number of periods per year for annualization. Defaults to 252 (trading days).

        Returns
        -------
        pd.Series or pd.DataFrame
            The Sharpe ratio.

        ---------------------------------------------------------------------------

        计算 Series 或 DataFrame 的夏普比率。

        参数
        ----------
        iscumprod : bool, optional
            输入是否表示累积乘积（例如，累积收益）。
            默认为 False。
        periods : int, optional
            年化周期数。默认为 252（交易日）。

        返回
        -------
        pd.Series 或 pd.DataFrame
            夏普比率。

        ---------------------------------------------------------------------------
        """
        if isinstance(self._obj, pd.Series):
            return sharpe(self._obj.to_frame(), iscumprod, periods).squeeze()
        else:
            return sharpe(self._obj, iscumprod, periods)

    def effective(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the effective exposure of the DataFrame.

        This method is typically applied to a DataFrame representing portfolio weights
        or factor exposures.

        Returns
        -------
        pd.DataFrame
            The effective exposure.

        ---------------------------------------------------------------------------

        计算 DataFrame 的有效暴露。

        此方法通常应用于表示投资组合权重或因子暴露的 DataFrame。

        返回
        -------
        pd.DataFrame
            有效暴露。

        ---------------------------------------------------------------------------
        """
        if isinstance(self._obj, pd.Series):
            raise TypeError("effective method is only applicable to pandas DataFrames.")
        return effective(self._obj)

    def expose(
        self,
        weight: pd.Series | None = None,
        standard_method: str = 'uniform',
        *unnamed_factors: pd.Series | pd.DataFrame,
        **named_factors: pd.Series | pd.DataFrame
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the exposure of the DataFrame to specified factors.

        Parameters
        ----------
        weight : pd.Series, optional
            Weights to apply to the exposure calculation. Defaults to None.
        standard_method : str, optional
            Method for standardization. Defaults to 'uniform'.
        *unnamed_factors : pd.Series or pd.DataFrame
            Positional arguments for unnamed factors.
        **named_factors : pd.Series or pd.DataFrame
            Keyword arguments for named factors.

        Returns
        -------
        pd.DataFrame
            The calculated exposure.

        ---------------------------------------------------------------------------

        计算 DataFrame 对指定因子的暴露。

        参数
        ----------
        weight : pd.Series, optional
            应用于暴露计算的权重。默认为 None。
        standard_method : str, optional
            标准化方法。默认为 'uniform'。
        *unnamed_factors : pd.Series 或 pd.DataFrame
            未命名因子的位置参数。
        **named_factors : pd.Series 或 pd.DataFrame
            命名因子的关键字参数。

        返回
        -------
        pd.DataFrame
            计算出的暴露。

        ---------------------------------------------------------------------------
        """
        if isinstance(self._obj, pd.Series):
            raise TypeError("expose method is only applicable to pandas DataFrames.")
        return expose(self._obj, weight, standard_method, *unnamed_factors, **named_factors)
    













        