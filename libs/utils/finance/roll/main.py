# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 12:56:19 2025

@author: Porco Rosso

"""

import numpy as np
import pandas as pd
from typing import Optional, Dict, Any, List, Union, Callable

from libs.utils.finance.roll.base import ts_argsort_unit, ts_rank_unit, ts_sort_unit


class _meta:
    """
    ===========================================================================

    Base class for rolling window operations.

    Provides common functionalities for handling rolling windows on DataFrames,
    including masking, min_periods handling, and applying time-series functions.

    ---------------------------------------------------------------------------

    滚动窗口操作的基类。

    提供处理 DataFrame 滚动窗口的通用功能，包括掩码、最小周期处理和应用时间序列函数。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self,
        df_obj: pd.DataFrame,
        window: int,
        min_periods: int,
        ts_func: Callable,
        ascending: bool
    ):
        """
        ===========================================================================

        Initializes the _meta class.

        Parameters
        ----------
        df_obj : pd.DataFrame
            The input DataFrame.
        window : int
            The size of the rolling window.
        min_periods : int
            Minimum number of observations in window required to have a value.
        ts_func : Callable
            The time-series function to apply.
        ascending : bool
            Whether to sort in ascending order.

        ---------------------------------------------------------------------------

        初始化 _meta 类。

        参数
        ----------
        df_obj : pd.DataFrame
            输入 DataFrame。
        window : int
            滚动窗口的大小。
        min_periods : int
            窗口中需要有值的最小观察数。
        ts_func : Callable
            要应用的时间序列函数。
        ascending : bool
            是否按升序排序。

        ---------------------------------------------------------------------------
        """
        self._obj = df_obj
        self.window = window
        self.min_periods = min_periods
        self._ts_func = ts_func
        self._ascending = ascending
        self._count = self.window  # Default value for count


    def __call__(
        self,
        count: Optional[int] = None
    ) -> Any:
        """
        ===========================================================================

        Allows setting the 'count' parameter for the rolling operation.

        Parameters
        ----------
        count : Optional[int], optional
            The count value to set, by default None.

        ---------------------------------------------------------------------------

        允许为滚动操作设置“count”参数。

        参数
        ----------
        count : Optional[int], optional
            要设置的计数，默认为 None。

        ---------------------------------------------------------------------------

        Returns
        -------
        Any
            Returns self for chaining.

        ---------------------------------------------------------------------------

        返回
        -------
        Any
            返回自身以进行链式调用。

        ---------------------------------------------------------------------------
        """
        if count is not None:
            self._count = count
        return self


    @property
    def count(self) -> int:
        """
        ===========================================================================

        Returns the current count value.

        ---------------------------------------------------------------------------

        返回当前计数。

        ---------------------------------------------------------------------------

        Returns
        -------
        int
            The count value.

        ---------------------------------------------------------------------------

        返回
        -------
        int
            计数。

        ---------------------------------------------------------------------------
        """
        x = getattr(self, '_count', self.window)
        return x

    @property
    def _masked_obj(self) -> np.ma.MaskedArray:
        """
        ===========================================================================

        Returns a masked NumPy array of the input DataFrame.

        NaN values in the DataFrame are masked.

        ---------------------------------------------------------------------------

        返回输入 DataFrame 的掩码 NumPy 数组。

        DataFrame 中的 NaN 值被掩码。

        ---------------------------------------------------------------------------

        Returns
        -------
        np.ma.MaskedArray
            The masked array.

        ---------------------------------------------------------------------------

        返回
        -------
        np.ma.MaskedArray
            掩码数组。

    ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_masked_obj_'):
            obj = self._obj.values
            self._masked_obj_ = np.ma.array(obj, mask=np.isnan(obj))
        return self._masked_obj_


    @property
    def _min_periods_mask(self) -> pd.DataFrame:
        """
        ===========================================================================

        Returns a DataFrame indicating where min_periods condition is met.

        ---------------------------------------------------------------------------

        返回一个 DataFrame，指示满足 min_periods 条件的位置。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with boolean mask.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            带有布尔掩码的 DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_min_periods_mask_'):
            obj = self._obj.notnull().rolling(self.window, min_periods=self.window).sum()
            self._min_periods_mask_ = obj
        return self._min_periods_mask_


    def _rolling_obj(
        self,
        array_obj: np.ndarray,
        pct: Optional[bool],
        group_func: Optional[Callable],
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Performs the core rolling window calculation.

        Applies the time-series function (`_ts_func`) to each rolling window.

        ---------------------------------------------------------------------------

        执行核心滚动窗口计算。

        将时间序列函数（`_ts_func`）应用于每个滚动窗口。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        array_obj : np.ndarray
            The input array for rolling calculation.
        pct : Optional[bool]
            Whether to return percentage (passed to ts_func).
        group_func : Optional[Callable]
            An optional function to apply to the result of ts_func.
        **kwargs : Any
            Additional keyword arguments for group_func.

        ---------------------------------------------------------------------------

        参数
        ----------
        array_obj : np.ndarray
            用于滚动计算的输入数组。
        pct : Optional[bool]
            是否返回百分比（传递给 ts_func）。
        group_func : Optional[Callable]
            应用于 ts_func 结果的可选函数。
        **kwargs : Any
            group_func 的附加关键字参数。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame containing the rolling results.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含滚动结果的 DataFrame。

        ---------------------------------------------------------------------------
        """
        idx_0, idx_1 = array_obj.shape
        outer = []
        window = self.window
        ascending = self._ascending
        count = self.count * (1 if ascending else -1)

        for i in range(window, idx_0 + 1):
            obj = array_obj[i - window: i]
            obj = self._ts_func(obj, cut=count, pct=pct, func=group_func, **kwargs)
            outer.append(obj)

        df = np.ma.concatenate(outer).reshape(-1, idx_1)
        lens = int(df.shape[0] / (idx_0 - window + 1))
        index = pd.MultiIndex.from_product(
            [self._obj.index[window - 1:], range(lens)],
            names=[self._obj.index.name, 'RANGE']
        ) if lens > 1 else self._obj.index[window - 1:]
        df = pd.DataFrame(df, index=index, columns=self._obj.columns)
        return df


    def _apply(
        self,
        array_obj: np.ndarray,
        group_func: Callable,
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Applies a function to the rolling window results.

        ---------------------------------------------------------------------------

        将函数应用于滚动窗口结果。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        array_obj : np.ndarray
            The input array.
        group_func : Callable
            The function to apply.
        **kwargs : Any
            Additional keyword arguments for the function.

        ---------------------------------------------------------------------------

        参数
        ----------
        array_obj : np.ndarray
            输入数组。
        group_func : Callable
            要应用的函数。
        **kwargs : Any
            函数的附加关键字参数。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with applied function results.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            应用函数结果的 DataFrame。

        ---------------------------------------------------------------------------
        """
        return self._rolling_obj(array_obj, pct=None, group_func=group_func, **kwargs)


class _max(_meta):
    """
    ===========================================================================

    Class for rolling maximum operations.

    Inherits from _meta and provides methods for calculating mean, std, sum,
    and applying custom functions on rolling maximums.

    ---------------------------------------------------------------------------

    滚动最大值操作的类。

    继承自 _meta，并提供计算滚动最大值的均值、标准差、总和以及应用自定义函数的方法。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self,
        df_obj: pd.DataFrame,
        window: int,
        min_periods: int
    ):
        """
        ===========================================================================

        Initializes the _max class.

        Parameters
        ----------
        df_obj : pd.DataFrame
            The input DataFrame.
        window : int
            The size of the rolling window.
        min_periods : int
            Minimum number of observations in window required to have a value.

        ---------------------------------------------------------------------------

        初始化 _max 类。

        参数
        ----------
        df_obj : pd.DataFrame
            输入 DataFrame。
        window : int
            滚动窗口的大小。
        min_periods : int
            窗口中需要有值的最小观察数。

        ---------------------------------------------------------------------------
        """
        super().__init__(df_obj, window, min_periods, ts_sort_unit, False)


    def mean(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the mean of the rolling maximums.

        ---------------------------------------------------------------------------

        计算滚动最大值的均值。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with rolling maximum means.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含滚动最大值均值的 DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self._rolling_obj(self._masked_obj, False, np.nanmean)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x


    def std(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the standard deviation of the rolling maximums.

        ---------------------------------------------------------------------------

        计算滚动最大值的标准差。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with rolling maximum standard deviations.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含滚动最大值标准差的 DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self._rolling_obj(self._masked_obj, False, np.nanstd)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x


    def sum(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the sum of the rolling maximums.

        ---------------------------------------------------------------------------

        计算滚动最大值的总和。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with rolling maximum sums.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含滚动最大值总和的 DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self._rolling_obj(self._masked_obj, False, np.nansum)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x


    def apply(
        self,
        function: Callable,
        **func_kwds: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Applies a custom function to the rolling maximums.

        Parameters
        ----------
        function : Callable
            The function to apply.
        **func_kwds : Any
            Additional keyword arguments for the function.

        ---------------------------------------------------------------------------

        将自定义函数应用于滚动最大值。

        参数
        ----------
        function : Callable
            要应用的函数。
        **func_kwds : Any
            函数的附加关键字参数。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with applied function results.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            应用函数结果的 DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self._apply(self._masked_obj, function, **func_kwds)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x


    @property
    def values(self) -> pd.DataFrame:
        """
        ===========================================================================

        Returns the raw rolling maximum values.

        ---------------------------------------------------------------------------

        返回原始滚动最大值。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with raw rolling maximum values.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含原始滚动最大值的 DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self._rolling_obj(self._masked_obj, False, None)
        return x


class _min(_max):
    """
    ===========================================================================

    Class for rolling minimum operations.

    Inherits from _max and reconfigures for minimum calculations.

    ---------------------------------------------------------------------------

    滚动最小值操作的类。

    继承自 _max 并重新配置以进行最小值计算。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self,
        df_obj: pd.DataFrame,
        window: int,
        min_periods: int
    ):
        """
        ===========================================================================

        Initializes the _min class.

        Parameters
        ----------
        df_obj : pd.DataFrame
            The input DataFrame.
        window : int
            The size of the rolling window.
        min_periods : int
            Minimum number of observations in window required to have a value.

        ---------------------------------------------------------------------------

        初始化 _min 类。

        参数
        ----------
        df_obj : pd.DataFrame
            输入 DataFrame。
        window : int
            滚动窗口的大小。
        min_periods : int
            窗口中需要有值的最小观察数。

        ---------------------------------------------------------------------------
        """
        super().__init__(df_obj, window, min_periods, ts_sort_unit, True)


class _rank(_meta):
    """
    ===========================================================================

    Class for rolling rank operations.

    Inherits from _meta and provides methods for calculating rolling ranks.

    ---------------------------------------------------------------------------

    滚动排名操作的类。

    继承自 _meta 并提供计算滚动排名的方法。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self,
        df_obj: pd.DataFrame,
        window: int,
        min_periods: int
    ):
        """
        ===========================================================================

        Initializes the _rank class.

        Parameters
        ----------
        df_obj : pd.DataFrame
            The input DataFrame.
        window : int
            The size of the rolling window.
        min_periods : int
            Minimum number of observations in window required to have a value.

        ---------------------------------------------------------------------------

        初始化 _rank 类。

        参数
        ----------
        df_obj : pd.DataFrame
            输入 DataFrame。
        window : int
            滚动窗口的大小。
        min_periods : int
            窗口中需要有值的最小观察数。

        ---------------------------------------------------------------------------
        """
        super().__init__(df_obj, window, min_periods, ts_rank_unit, False)


    def __call__(
        self,
        pct: bool
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the rolling rank.

        Parameters
        ----------
        pct : bool
            If True, return rank as a percentage.

        ---------------------------------------------------------------------------

        计算滚动排名。

        参数
        ----------
        pct : bool
            如果为 True，则以百分比形式返回排名。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with rolling ranks.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含滚动排名的 DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self._rolling_obj(self._obj.values, pct, None)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x


class rolls:
    """
    ===========================================================================

    Main class for time-series rolling operations.

    Provides an interface to perform various rolling calculations like max,
    min, and rank on a DataFrame.

    ---------------------------------------------------------------------------

    时间序列滚动操作的主类。

    提供对 DataFrame 执行各种滚动计算（如最大值、最小值和排名）的接口。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self,
        pandas_obj: pd.DataFrame,
        window: int,
        min_periods: Optional[int] = None
    ):
        """
        ===========================================================================

        Initializes the rolls class.

        Parameters
        ----------
        pandas_obj : pd.DataFrame
            The input DataFrame.
        window : int
            The size of the rolling window.
        min_periods : Optional[int], optional
            Minimum number of observations in window required to have a value,
            by default None (defaults to window).

        ---------------------------------------------------------------------------

        初始化 rolls 类。

        参数
        ----------
        pandas_obj : pd.DataFrame
            输入 DataFrame。
        window : int
            滚动窗口的大小。
        min_periods : Optional[int], optional
            窗口中需要有值的最小观察数，默认为 None（默认为 window）。

        ---------------------------------------------------------------------------
        """
        self._obj = pandas_obj
        self.window = window
        self.min_periods = min_periods if min_periods is not None else window
        self._max_class = _max(pandas_obj, self.window, self.min_periods)
        self._min_class = _min(pandas_obj, self.window, self.min_periods)
        self._rank_class = _rank(pandas_obj, self.window, self.min_periods)


    def max(
        self,
        count: Optional[int] = None
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the rolling maximum.

        Parameters
        ----------
        count : Optional[int], optional
            The number of maximum values to return, by default None (defaults to window).

        ---------------------------------------------------------------------------

        计算滚动最大值。

        参数
        ----------
        count : Optional[int], optional
            要返回的最大值数量，默认为 None（默认为 window）。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with rolling maximums.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含滚动最大值的 DataFrame。

        ---------------------------------------------------------------------------
        """
        count = self.window if count is None else count
        x = self._max_class(count)
        return x


    def min(
        self,
        count: Optional[int] = None
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the rolling minimum.

        Parameters
        ----------
        count : Optional[int], optional
            The number of minimum values to return, by default None (defaults to window).

        ---------------------------------------------------------------------------

        计算滚动最小值。

        参数
        ----------
        count : Optional[int], optional
            要返回的最小值数量，默认为 None（默认为 window）。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with rolling minimums.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含滚动最小值的 DataFrame。

        ---------------------------------------------------------------------------
        """
        count = self.window if count is None else count
        x = self._min_class(count)
        return x


    def ts_rank(
        self,
        pct: bool = True
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the time-series rolling rank.

        Parameters
        ----------
        pct : bool, optional
            If True, return rank as a percentage, by default True.

        ---------------------------------------------------------------------------

        计算时间序列滚动排名。

        参数
        ----------
        pct : bool, optional
            如果为 True，则以百分比形式返回排名，默认为 True。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            DataFrame with time-series rolling ranks.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            包含时间序列滚动排名的 DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self._rank_class(pct)
        return x