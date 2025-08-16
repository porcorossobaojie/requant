# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:46:46 2025

@author: Porco Rosso
"""

import flow
from flow import COLUMNS_INFO
import numpy as np
import pandas as pd
from libs.utils.functions import flatten_list
from numpy.lib.stride_tricks import as_strided
from factors.meta.main import main as meta
from typing import Union, List, Dict, Any, Optional, Tuple, Callable

class main(meta):
    """
    ===========================================================================

    Implements the Barra CNE6 factor model for quantitative analysis.
    This class calculates various factors such as Size, Volatility, Liquidity, 
    Momentum, Quality, Value, and Growth.

    ---------------------------------------------------------------------------

    实现用于量化分析的Barra CNE6因子模型。
    该类计算各种因子，如市值、波动率、流动性、动量、质量和增长。

    ---------------------------------------------------------------------------
    """
    def __half_life__(
        self, 
        window: int, 
        half_life: Union[int, float]
    ) -> np.ndarray:
        """
        ===========================================================================

        Calculates a half-life weighted array for a given window.

        Parameters
        ----------
        window : int
            The size of the window.
        half_life : Union[int, float]
            The half-life value for weighting.

        Returns
        -------
        np.ndarray
            A NumPy array of half-life weights.

        ---------------------------------------------------------------------------

        计算给定窗口的半衰期加权数组。

        参数
        ----------
        window : int
            窗口大小。
        half_life : Union[int, float]
            用于加权的半衰期值。

        返回
        -------
        np.ndarray
            半衰期权重的NumPy数组。

        ---------------------------------------------------------------------------
        """
        L, Lambda = 0.5**(1/half_life), 0.5**(1/half_life)
        W = []
        for i in range(window):
            W.append(Lambda)
            Lambda *= L        
        W = np.array(W[::-1])
        return W

    def __log__(
        self, 
        df: pd.DataFrame, 
        abs: bool = True
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Applies logarithmic transformation to a DataFrame, with optional absolute value handling.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame.
        abs : bool, optional
            If True, takes the absolute value before log and reapplies the sign. Defaults to True.

        Returns
        -------
        pd.DataFrame
            The DataFrame with logarithmic transformed values.

        ---------------------------------------------------------------------------

        对DataFrame应用对数变换，可选处理绝对值。

        参数
        ----------
        df : pd.DataFrame
            输入DataFrame。
        abs : bool, optional
            如果为 True，则在取对数之前取绝对值并重新应用符号。默认为 True。

        返回
        -------
        pd.DataFrame
            经过对数变换值的DataFrame。

        ---------------------------------------------------------------------------
        """
        x = np.log(df.abs())
        if abs:
            x =  np.sign(df) * x
        return x
    
    def __array_roll__(
        self, 
        array_2D: np.ndarray, 
        periods: int
    ) -> np.ndarray:
        """
        ===========================================================================

        Creates rolling windows from a 2D NumPy array.

        Parameters
        ----------
        array_2D : np.ndarray
            The input 2D NumPy array.
        periods : int
            The size of the rolling window.

        Returns
        -------
        np.ndarray
            A 3D NumPy array representing the rolling windows.

        ---------------------------------------------------------------------------

        从2D NumPy数组创建滚动窗口。

        参数
        ----------
        array_2D : np.ndarray
            输入的2D NumPy数组。
        periods : int
            滚动窗口的大小。

        返回
        -------
        np.ndarray
            表示滚动窗口的3D NumPy数组。

        ---------------------------------------------------------------------------
        """
        axis=0
        
        new_shape = list(array_2D.shape)
        new_shape[axis] = [periods, new_shape[axis] - periods + 1, ]
        new_shape = tuple(flatten_list(new_shape))
        
        new_strides = list(array_2D.strides)
        new_strides[axis] = [array_2D.strides[axis], array_2D.strides[axis]]
        new_strides = tuple(flatten_list(new_strides))
        
        window = as_strided(array_2D, shape=new_shape, strides=new_strides)
        window = window.transpose(1, 0, 2)
        return window
    
    def __factors_merge__(
        self, 
        periods: int = 42, 
        how: str = 'std', 
        **factors: pd.DataFrame
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Merges multiple factor DataFrames, applying weights based on their historical volatility or mean.

        Parameters
        ----------
        periods : int, optional
            The number of periods for rolling calculation of weights. Defaults to 42.
        how : str, optional
            The method to calculate weights: 'std' for rolling standard deviation, 
            or 'mean' for rolling mean. Defaults to 'std'.
        **factors : pd.DataFrame
            Keyword arguments where keys are factor names and values are factor DataFrames.

        Returns
        -------
        pd.DataFrame
            A single DataFrame representing the merged and weighted factors.

        ---------------------------------------------------------------------------

        合并多个因子DataFrame，根据其历史波动率或均值应用权重。

        参数
        ----------
        periods : int, optional
            用于计算权重的滚动周期数。默认为 42。
        how : str, optional
            计算权重的方法：'std' 表示滚动标准差，
            'mean' 表示滚动均值。默认为 'std'。
        **factors : pd.DataFrame
            关键字参数，其中键是因子名称，值是因子DataFrame。

        返回
        -------
        pd.DataFrame
            一个表示合并和加权因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        returns = flow.stock('S_DQ_PCTCHANGE')
        if how == 'std':
            weights = {i:j.shift().stats.neutral(fac=returns, resid=False).params['fac'].rolling(periods, min_periods=periods//4).std() for i,j in factors.items()}
        else:
            weights = {i:j.shift().stats.neutral(fac=returns, resid=False).params['fac'].rolling(periods, min_periods=periods//4).mean() for i,j in factors.items()}
        fac = pd.concat({i:factors[i].mul(weights[i], axis=0) for i in factors.keys()}, axis=1)
        fac = fac.stack().sum(axis=1, min_count=len(factors.keys())).unstack()
        return fac

        
    
    def L3_LNCAP(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the natural logarithm of market capitalization (Size factor).

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the LNCAP factor.

        ---------------------------------------------------------------------------

        计算市值（Size因子）的自然对数。

        返回
        -------
        pd.DataFrame
            表示LNCAP因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.__log__(flow.stock('S_VAL_MV') * 1e8)
        return df
    
    def L3_MIDCAP(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Mid-Cap factor, which is the residual of LNCAP cubed regressed on LNCAP.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the MIDCAP factor.

        ---------------------------------------------------------------------------

        计算中市值因子，它是LNCAP立方对LNCAP回归的残差。

        返回
        -------
        pd.DataFrame
            表示MIDCAP因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.L3_LNCAP()
        x = df ** 3
        w = (df ** 0.5)
        x = x.stats.neutral(fac=df, weight=w.values).resid.stats.standard(axis=1)
        return x
    
    def L2_Size(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L2 Size factor, which is equivalent to L3_LNCAP.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Size factor.

        ---------------------------------------------------------------------------

        表示L2市值因子，等同于L3_LNCAP。

        返回
        -------
        pd.DataFrame
            表示L2市值因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L3_LNCAP()
    
    def L2_Mid_Cap(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L2 Mid-Cap factor, which is equivalent to L3_MIDCAP.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Mid-Cap factor.

        ---------------------------------------------------------------------------

        表示L2中市值因子，等同于L3_MIDCAP。

        返回
        -------
        pd.DataFrame
            表示L2中市值因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L3_MIDCAP()
    
    def L1_Size(
        self, 
        periods: int = 42
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L1 Size factor by merging L2 Size and L2 Mid-Cap factors.

        Parameters
        ----------
        periods : int, optional
            The number of periods for factor merging. Defaults to 42.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L1 Size factor.

        ---------------------------------------------------------------------------

        通过合并L2市值和L2中市值因子计算L1市值因子。

        参数
        ----------
        periods : int, optional
            因子合并的周期数。默认为 42。

        返回
        -------
        pd.DataFrame
            表示L1市值因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    periods = periods,
                                    fac1 = self.L2_Size(),
                                    fac2 = self.L2_Mid_Cap()
                                    )
        return fac
    
    def L3_BETA(
        self, 
        periods: int = 252
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Beta factor.

        Parameters
        ----------
        periods : int, optional
            The number of periods for rolling regression. Defaults to 252.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Beta factor.

        ---------------------------------------------------------------------------

        计算L3 Beta因子。

        参数
        ----------
        periods : int, optional
            滚动回归的周期数。默认为 252。

        返回
        -------
        pd.DataFrame
            表示L3 Beta因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_L3_BETA_periods'):
            self._L3_BETA_periods = periods
        if (periods != self._L3_BETA_periods):
            self._L3_BETA_periods = periods
            try:
                delattr(self, '_L3_BETA_beta')
            except:
                pass
            
        if not hasattr(self, '_L3_BETA_beta'):
            returns = flow.stock('S_DQ_PCTCHANGE')
            w = self.L3_LNCAP()
            market = (returns * w).sum(axis=1) / w.sum(axis=1)
            market = pd.DataFrame(market.values.repeat(returns.shape[1]).reshape(returns.shape[0], -1), index=returns.index, columns=returns.columns)            
            parameters = returns.stats.neutral(market=market, neu_axis=0, periods=periods, weight=(self.__half_life__(periods, periods // 4)), resid=False)
            beta = parameters.params['market'].unstack().reindex_like(returns)
            alpha =  parameters.params['const'].unstack().reindex_like(returns)
            self._L3_BETA_beta = beta
            self._L3_BETA_alpha = alpha
            
        return self._L3_BETA_beta
    
    def L3_HIST_SIGMA(
        self, 
        periods: int = 252
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Historical Sigma (residual volatility).

        Parameters
        ----------
        periods : int, optional
            The number of periods for rolling calculation. Defaults to 252.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Historical Sigma factor.

        ---------------------------------------------------------------------------

        计算L3历史Sigma（残差波动率）。

        参数
        ----------
        periods : int, optional
            滚动计算的周期数。默认为 252。

        返回
        -------
        pd.DataFrame
            表示L3历史Sigma因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        returns = flow.stock('S_DQ_PCTCHANGE')
        w = self.L3_LNCAP()
        market = (returns * w).sum(axis=1) / w.sum(axis=1)
        market = pd.DataFrame(market.values.repeat(returns.shape[1]).reshape(returns.shape[0], -1), index=returns.index, columns=returns.columns)    
        beta = self.L3_BETA()
        alpha = self._L3_BETA_alpha
        
        resid = (returns - market * beta - alpha).rolling(periods, min_periods=periods // 4).std()
        return resid
    
    def L3_DAILY_STD(
        self, 
        periods: int = 252
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Daily Standard Deviation factor.

        Parameters
        ----------
        periods : int, optional
            The number of periods for rolling calculation. Defaults to 252.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Daily Standard Deviation factor.

        ---------------------------------------------------------------------------

        计算L3日标准差因子。

        参数
        ----------
        periods : int, optional
            滚动计算的周期数。默认为 252。

        返回
        -------
        pd.DataFrame
            表示L3日标准差因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        w = self.__half_life__(periods, periods // 4)
        w = w / w.sum()
        
        returns = flow.stock('S_DQ_PCTCHANGE')
        x = returns.rolling(periods, min_periods=periods // 4).var()
        x_array = self.__array_roll__(x.values, periods)
        x_array = np.array([np.nansum(x_array[i] * w[:, np.newaxis], axis=0) ** 0.5 for i in range(x_array.shape[0])])
        x_array = pd.DataFrame(x_array, index=x.index[periods-1:], columns=x.columns)
        nan = returns.isnull().rolling(periods).sum()
        x_array = x_array[nan <= periods // 4].replace(0, np.nan).reindex_like(returns)
        
        return x_array
        
    def L3_CMRA(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Cumulative Market Return Amplitude (CMRA) factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 CMRA factor.

        ---------------------------------------------------------------------------

        计算L3累积市场回报幅度（CMRA）因子。

        返回
        -------
        pd.DataFrame
            表示L3 CMRA因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        returns = np.log(flow.stock('S_DQ_CLOSE_ADJ').pct_change(21) + 1)
        x_array = self.__array_roll__(returns.values, 252)
        x_array = np.array([x_array[i][range(20, 252, 21)] for i in range(x_array.shape[0])])
        x_array = np.array([np.nanmax(x_array[i], axis=0) - np.nanmin(x_array[i], axis=0) for i in range(x_array.shape[0])])
        x_array = pd.DataFrame(x_array, index=returns.index[-1 * x_array.shape[0]:], columns=returns.columns).reindex_like(returns)
        return x_array
        
    def L2_Beta(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L2 Beta factor, which is equivalent to L3_BETA.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Beta factor.

        ---------------------------------------------------------------------------

        表示L2 Beta因子，等同于L3_BETA。

        返回
        -------
        pd.DataFrame
            表示L2 Beta因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L3_BETA()
    
    def L2_Residual_Volatility(
        self, 
        periods: int = 42
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Residual Volatility factor by merging related L3 factors.

        Parameters
        ----------
        periods : int, optional
            The number of periods for factor merging. Defaults to 42.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Residual Volatility factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2残差波动率因子。

        参数
        ----------
        periods : int, optional
            因子合并的周期数。默认为 42。

        返回
        -------
        pd.DataFrame
            表示L2残差波动率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    periods = periods,
                                    fac1 = self.L3_CMRA(),
                                    fac2 = self.L3_HIST_SIGMA(),
                                    fac3 = self.L3_DAILY_STD()
                                    )
        return fac

    def L1_Volatility(
        self, 
        periods: int = 42
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L1 Volatility factor by merging L2 Beta and L2 Residual Volatility factors.

        Parameters
        ----------
        periods : int, optional
            The number of periods for factor merging. Defaults to 42.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L1 Volatility factor.

        ---------------------------------------------------------------------------

        通过合并L2 Beta和L2残差波动率因子计算L1波动率因子。

        参数
        ----------
        periods : int, optional
            因子合并的周期数。默认为 42。

        返回
        -------
        pd.DataFrame
            表示L1波动率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    periods = periods,
                                    fac1 = self.L2_Beta(),
                                    fac2 = self.L2_Residual_Volatility(),
                                    )
        return fac

    def L3_TRUNVOER_M(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Monthly Turnover factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Monthly Turnover factor.

        ---------------------------------------------------------------------------

        计算L3月度换手率因子。

        返回
        -------
        pd.DataFrame
            表示L3月度换手率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = flow.stock('S_DQ_FREETURNOVER') / 100
        df = np.log(df.rolling(21, min_periods=21//4).sum() + 1)
        return df
    
    def L3_TRUNVOER_Q(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Quarterly Turnover factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Quarterly Turnover factor.

        ---------------------------------------------------------------------------

        计算L3季度换手率因子。

        返回
        -------
        pd.DataFrame
            表示L3季度换手率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = flow.stock('S_DQ_FREETURNOVER') / 100
        df = np.log(df.rolling(21 * 3, min_periods=21 * 3//4).sum() + 1)
        return df

    def L3_TRUNVOER_Y(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Yearly Turnover factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Yearly Turnover factor.

        ---------------------------------------------------------------------------

        计算L3年度换手率因子。

        返回
        -------
        pd.DataFrame
            表示L3年度换手率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = flow.stock('S_DQ_FREETURNOVER') / 100
        df = np.log(df.rolling(21 * 12, min_periods=21 * 12//4).sum() + 1)
        return df


    def L3_TURNOVER_RATIO(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Turnover Ratio factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Turnover Ratio factor.

        ---------------------------------------------------------------------------

        计算L3换手率因子。

        返回
        -------
        pd.DataFrame
            表示L3换手率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        w = self.__half_life__(252, 252 // 4)
        w = w / w.sum()
        turnover = flow.stock('S_DQ_FREETURNOVER') / 100
        
        x_array = self.__array_roll__(turnover.values, 252)
        df =  np.array([np.nansum(x_array[i] * w[:, np.newaxis], axis=0) for i in range(x_array.shape[0])])
        df = pd.DataFrame(df, index=turnover.index[-df.shape[0]:], columns=turnover.columns).reindex_like(turnover)
        return df
    
    def L2_Liquidity(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Liquidity factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Liquidity factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2流动性因子。

        返回
        -------
        pd.DataFrame
            表示L2流动性因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_TRUNVOER_M(),
                                    fac2 = self.L3_TRUNVOER_Q(),
                                    fac3 = self.L3_TRUNVOER_Y(),
                                    fac4 = self.L3_TURNOVER_RATIO(),
                                    )
        return fac

    def L1_Liquidity(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L1 Liquidity factor, which is equivalent to L2_Liquidity.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L1 Liquidity factor.

        ---------------------------------------------------------------------------

        表示L1流动性因子，等同于L2_Liquidity。

        返回
        -------
        pd.DataFrame
            表示L1流动性因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L2_Liquidity()
    
    def L3_SHORT_REVERSAL(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Short Reversal factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Short Reversal factor.

        ---------------------------------------------------------------------------

        计算L3短期反转因子。

        返回
        -------
        pd.DataFrame
            表示L3短期反转因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        returns = flow.stock('S_DQ_PCTCHANGE')
        w = self.__half_life__(21, 21 // 4)
        w = w / w.sum()

        df = np.log(returns.rolling(21, min_periods=12 // 4).mean() + 1)
        x_array = self.__array_roll__(df.values, 21)
        df =  np.array([np.nansum(x_array[i] * w[:, np.newaxis], axis=0) for i in range(x_array.shape[0])])
        df = pd.DataFrame(df, index=returns.index[-df.shape[0]:], columns=returns.columns).reindex_like(returns)
        return df

    def L3_SEASONLITY(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Seasonality factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Seasonality factor.

        ---------------------------------------------------------------------------

        计算L3季节性因子。

        返回
        -------
        pd.DataFrame
            表示L3季节性因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        returns = flow.stock('S_DQ_PCTCHANGE')
        
        df = returns.rolling(21, min_periods=21//4).mean().shift(21)
        dic = pd.concat({i:df.shift(252 * i) for i in range(5)}, axis=1).stack()
        dic = dic.mean(axis=1).unstack()
        dic = dic.reindex_like(returns)
        return dic
    
    def L3_INDUSTRY_MOMENTUM(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Industry Momentum factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Industry Momentum factor.

        ---------------------------------------------------------------------------

        计算L3行业动量因子。

        返回
        -------
        pd.DataFrame
            表示L3行业动量因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        w = self.__half_life__(126, 21)
        w = w / w.sum()
        returns = flow.stock('S_DQ_PCTCHANGE')
        industry_sw = flow.stock('s_swl3_code')
        mv = flow.stock('S_VAL_MV')
        
        x_array = self.__array_roll__(returns.values, 126)
        df = np.array([np.nansum(x_array[i] * w[:, np.newaxis], axis=0) for i in range(x_array.shape[0])])
        df = pd.DataFrame(df, index=returns.index[-df.shape[0]:], columns=returns.columns).reindex_like(returns)
        mom = pd.concat({'industry':industry_sw, 'fac':df, 'mv':mv ** 0.5, 'log_mv':np.log(mv * 1e8)}, axis=1).stack()
        mom['fac_mul_mv'] = mom['fac'] * mom['mv']
        ind_mom = mom.groupby([COLUMNS_INFO.trade_dt, 'industry']).transform('sum', min_count=1)
        fac = (-mom['fac'] + ind_mom['fac_mul_mv']  / ind_mom['mv']).unstack()        
        # fac = (-mom['fac']* mom['log_mv'] + ind_mom['fac_mul_mv']  / ind_mom['mv'] * ind_mom['log_mv']).unstack()
        return fac
    
    def L3_RELATIVE_STRENGTH(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Relative Strength factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Relative Strength factor.

        ---------------------------------------------------------------------------

        计算L3相对强度因子。

        返回
        -------
        pd.DataFrame
            表示L3相对强度因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        w = self.__half_life__(252, 252//2)
        w = w / w.sum()
        returns = flow.stock('S_DQ_PCTCHANGE')
        
        x_array = self.__array_roll__(returns.values, 252)
        df = np.array([np.nansum(x_array[i] * w[:, np.newaxis], axis=0) for i in range(x_array.shape[0])])
        df = pd.DataFrame(df, index=returns.index[-df.shape[0]:], columns=returns.columns).reindex_like(returns)
        df = df.rolling(11).mean()
        return df
    
    def L3_HISTORY_ALPHA(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Historical Alpha factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Historical Alpha factor.

        ---------------------------------------------------------------------------

        计算L3历史Alpha因子。

        返回
        -------
        pd.DataFrame
            表示L3历史Alpha因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        self.L3_BETA()
        return self._L3_BETA_alpha

    def L2_Short_Reversal(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L2 Short Reversal factor, which is equivalent to L3_SHORT_REVERSAL.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Short Reversal factor.

        ---------------------------------------------------------------------------

        表示L2短期反转因子，等同于L3_SHORT_REVERSAL。

        返回
        -------
        pd.DataFrame
            表示L2短期反转因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L3_SHORT_REVERSAL()
    
    def L2_Seasonality(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L2 Seasonality factor, which is equivalent to L3_SEASONLITY.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Seasonality factor.

        ---------------------------------------------------------------------------

        表示L2季节性因子，等同于L3_SEASONLITY。

        返回
        -------
        pd.DataFrame
            表示L2季节性因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L3_SEASONLITY()
    
    def L2_Industry_Momentum(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L2 Industry Momentum factor, which is equivalent to L3_INDUSTRY_MOMENTUM.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Industry Momentum factor.

        ---------------------------------------------------------------------------

        表示L2行业动量因子，等同于L3_INDUSTRY_MOMENTUM。

        返回
        -------
        pd.DataFrame
            表示L2行业动量因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L3_INDUSTRY_MOMENTUM()
    
    def L2_Momentum(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Momentum factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Momentum factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2动量因子。

        返回
        -------
        pd.DataFrame
            表示L2动量因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_HISTORY_ALPHA(),
                                    fac2 = self.L3_RELATIVE_STRENGTH(),
                                    )
        return fac
        
    def L1_Momentum(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L1 Momentum factor by merging related L2 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L1 Momentum factor.

        ---------------------------------------------------------------------------

        通过合并相关的L2因子计算L1动量因子。

        返回
        -------
        pd.DataFrame
            表示L1动量因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L2_Short_Reversal(),
                                    fac2 = self.L2_Seasonality(),
                                    fac3 = self.L2_Industry_Momentum(),
                                    fac4 = self.L2_Momentum(),
                                    )
        return fac

    def L3_MARKET_LEVERAGE(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Market Leverage factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Market Leverage factor.

        ---------------------------------------------------------------------------

        计算L3市场杠杆因子。

        返回
        -------
        pd.DataFrame
            表示L3市场杠杆因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        mv = flow.stock('S_VAL_MV') * 1e8
        debt = flow.stock_finance('TOTAL_NON_CURRENT_LIABILITY',periods=1, shift=4)
        df = (mv + debt) /mv
        return df
    
    def L3_BOOK_LEVERAGE(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Book Leverage factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Book Leverage factor.

        ---------------------------------------------------------------------------

        计算L3账面杠杆因子。

        返回
        -------
        pd.DataFrame
            表示L3账面杠杆因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        mv = flow.stock('S_VAL_MV') * 1e8
        assets = flow.stock_finance('TOTAL_ASSETS',periods=1, shift=4)
        df = (mv + assets) /mv
        return df
    
    def L3_DEBT_TO_ASSET(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Debt-to-Asset factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Debt-to-Asset factor.

        ---------------------------------------------------------------------------

        计算L3资产负债率因子。

        返回
        -------
        pd.DataFrame
            表示L3资产负债率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        assets = flow.stock_finance('TOTAL_ASSETS',periods=1, shift=4)
        debt = flow.stock_finance('TOTAL_NON_CURRENT_LIABILITY',periods=1, shift=4)
        df = debt / assets
        return df
    
    def L3_VAR_IN_SALES(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Variance in Sales factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Variance in Sales factor.

        ---------------------------------------------------------------------------

        计算L3销售额方差因子。

        返回
        -------
        pd.DataFrame
            表示L3销售额方差因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        operation = flow.stock_finance('OPERATING_REVENUE', periods=24)
        df = np.log(operation.abs()) * np.sign(operation)
        df = df.groupby([COLUMNS_INFO.trade_dt]).diff(4)
        df = df.groupby([COLUMNS_INFO.trade_dt]).std()
        return df        

    def L3_VAR_IN_EARNING(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Variance in Earnings factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Variance in Earnings factor.

        ---------------------------------------------------------------------------

        计算L3盈利方差因子。

        返回
        -------
        pd.DataFrame
            表示L3盈利方差因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        operation = flow.stock_finance('OPERATING_PROFIT', periods=24)
        df = np.log(operation.abs()) * np.sign(operation)
        df = df.groupby([COLUMNS_INFO.trade_dt]).diff(4)
        df = df.groupby([COLUMNS_INFO.trade_dt]).std()
        return df
    
    def L3_VAR_IN_CASHFLOW(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Variance in Cash Flow factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Variance in Cash Flow factor.

        ---------------------------------------------------------------------------

        计算L3现金流方差因子。

        返回
        -------
        pd.DataFrame
            表示L3现金流方差因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        operation = flow.stock_finance('CASH_AND_EQUIVALENTS_AT_END', periods=24)
        df = np.log(operation.abs()) * np.sign(operation)
        df = df.groupby([COLUMNS_INFO.trade_dt]).diff(1)
        df = df.groupby([COLUMNS_INFO.trade_dt]).std()
        return df
    
    def L3_ASSET_TURNOVER(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Asset Turnover factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Asset Turnover factor.

        ---------------------------------------------------------------------------

        计算L3资产周转率因子。

        返回
        -------
        pd.DataFrame
            表示L3资产周转率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = flow.stock('S_DQ_PS_TTM').replace(0, np.nan) ** -1  * flow.stock('S_VAL_MV') * 1e8
        assets = flow.stock_finance('TOTAL_ASSETS',periods=1, shift=4)
        df = df / assets
        return df
    
    def L3_GROSS_PROFITABILITY(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Gross Profitability factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Gross Profitability factor.

        ---------------------------------------------------------------------------

        计算L3毛利率因子。

        返回
        -------
        pd.DataFrame
            表示L3毛利率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = flow.stock_finance('OPERATING_PROFIT', shift=4, periods=4, quarter_adj=3)
        df = df.groupby([COLUMNS_INFO.trade_dt]).sum()
        assets = flow.stock_finance('TOTAL_ASSETS',periods=1, shift=4)
        df = df / assets
        return df
        
    def L3_GROSS_PROFIT_MARGIN(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Gross Profit Margin factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Gross Profit Margin factor.

        ---------------------------------------------------------------------------

        计算L3毛利率因子。

        返回
        -------
        pd.DataFrame
            表示L3毛利率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return flow.stock('GROSS_PROFIT_MARGIN')
    
    def L3_ROA(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Return on Assets (ROA) factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 ROA factor.

        ---------------------------------------------------------------------------

        计算L3资产回报率（ROA）因子。

        返回
        -------
        pd.DataFrame
            表示L3 ROA因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return flow.stock('ROA')

    def L3_ASSETS_GROWTH(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Assets Growth factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Assets Growth factor.

        ---------------------------------------------------------------------------

        计算L3资产增长因子。

        返回
        -------
        pd.DataFrame
            表示L3资产增长因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        assets = flow.stock_finance('TOTAL_ASSETS', shift=4, periods=24)
        df = np.log(assets.abs()) * np.sign(assets)
        df = df.groupby([COLUMNS_INFO.trade_dt]).diff()
        df = df.groupby([COLUMNS_INFO.trade_dt]).mean()
        return df
    
    def L3_CAPITAL_GROWTH(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Capital Growth factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Capital Growth factor.

        ---------------------------------------------------------------------------

        计算L3资本增长因子。

        返回
        -------
        pd.DataFrame
            表示L3资本增长因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        assets = flow.stock_finance('fix_intan_other_asset_acqui_cash', shift=4, periods=24)
        df = np.log(assets.abs()) * np.sign(assets)
        df = df.groupby([COLUMNS_INFO.trade_dt]).diff()
        df = df.groupby([COLUMNS_INFO.trade_dt]).mean()
        return df
    
    def L2_Leverage(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Leverage factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Leverage factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2杠杆因子。

        返回
        -------
        pd.DataFrame
            表示L2杠杆因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_MARKET_LEVERAGE(),
                                    fac2 = self.L3_BOOK_LEVERAGE(),
                                    fac3 = self.L3_DEBT_TO_ASSET()
                                    )
        return fac

    def L2_Earnings_Var(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Earnings Variance factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Earnings Variance factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2盈利方差因子。

        返回
        -------
        pd.DataFrame
            表示L2盈利方差因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_VAR_IN_SALES(),
                                    fac2 = self.L3_VAR_IN_EARNING(),
                                    fac3 = self.L3_VAR_IN_CASHFLOW(),
                                    )
        return fac

    def L2_Profitability(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Profitability factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Profitability factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2盈利能力因子。

        返回
        -------
        pd.DataFrame
            表示L2盈利能力因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_ASSET_TURNOVER(),
                                    fac2 = self.L3_GROSS_PROFITABILITY(),
                                    fac3 = self.L3_ROA(),
                                    )
        return fac
    
    def L2_Investment_Qty(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Investment Quantity factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Investment Quantity factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2投资量因子。

        返回
        -------
        pd.DataFrame
            表示L2投资量因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_ASSETS_GROWTH(),
                                    fac2 = self.L3_CAPITAL_GROWTH(),
                                    )
        return fac

    def L1_Quality(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L1 Quality factor by merging related L2 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L1 Quality factor.

        ---------------------------------------------------------------------------

        通过合并相关的L2因子计算L1质量因子。

        返回
        -------
        pd.DataFrame
            表示L1质量因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L2_Leverage(),
                                    fac2 = self.L2_Earnings_Var(),
                                    fac3 = self.L2_Profitability(),
                                    fac4 = self.L2_Investment_Qty()
                                    )
        return fac

    def L3_BP(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Book-to-Price (BP) factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 BP factor.

        ---------------------------------------------------------------------------

        计算L3账面市值比（BP）因子。

        返回
        -------
        pd.DataFrame
            表示L3 BP因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return flow.stock('S_DQ_PB') ** -1

    def L3_EP(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Earnings-to-Price (EP) factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 EP factor.

        ---------------------------------------------------------------------------

        计算L3市盈率倒数（EP）因子。

        返回
        -------
        pd.DataFrame
            表示L3 EP因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return flow.stock('EPS')
    
    def L3_CP(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Cash Flow-to-Price (CP) factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 CP factor.

        ---------------------------------------------------------------------------

        计算L3现金流市值比（CP）因子。

        返回
        -------
        pd.DataFrame
            表示L3 CP因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return flow.stock('S_DQ_POCF_TTM').replace(0, np.nan) ** -1
    
    def L3_EBITP(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 EBIT-to-Price (EBITP) factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 EBITP factor.

        ---------------------------------------------------------------------------

        计算L3息税前利润市值比（EBITP）因子。

        返回
        -------
        pd.DataFrame
            表示L3 EBITP因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = flow.stock_finance('OPERATING_PROFIT', periods=4, shift=4,quarter_adj=3)
        df = df.groupby([COLUMNS_INFO.trade_dt]).sum()
        mv = flow.stock('S_VAL_MV') * 1e8
        df = df / mv
        return df
    
    def L3_LONG_TERM_STRENGTH(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Long-Term Strength factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Long-Term Strength factor.

        ---------------------------------------------------------------------------

        计算L3长期强度因子。

        返回
        -------
        pd.DataFrame
            表示L3长期强度因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        w = self.__half_life__(252*2, 252)
        w = w / w.sum()
        returns  = flow.stock('S_DQ_PCTCHANGE')
        
        x_array = self.__array_roll__(returns.values, 252*2)
        df = np.array([np.nansum(x_array[i] * w[:, np.newaxis], axis=0) for i in range(x_array.shape[0])])
        df = pd.DataFrame(df, index=returns.index[-df.shape[0]:], columns=returns.columns).reindex_like(returns)
        df = df.rolling(11).mean().shift(126)
        return df
    
    def L3_LONG_TERM_ALPHA(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Long-Term Alpha factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 Long-Term Alpha factor.

        ---------------------------------------------------------------------------

        计算L3长期Alpha因子。

        返回
        -------
        pd.DataFrame
            表示L3长期Alpha因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        self.L3_BETA()
        w = self.__half_life__(252*2, 252)
        w = w / w.sum()
        returns = self._L3_BETA_alpha
        
        x_array = self.__array_roll__(returns.values, 252*2)
        df = np.array([np.nansum(x_array[i] * w[:, np.newaxis], axis=0) for i in range(x_array.shape[0])])
        df = pd.DataFrame(df, index=returns.index[-df.shape[0]:], columns=returns.columns).reindex_like(returns)
        df = df.rolling(11).mean().shift(126)
        return df

    def L2_Book_to_Price(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L2 Book-to-Price factor, which is equivalent to L3_BP.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Book-to-Price factor.

        ---------------------------------------------------------------------------

        表示L2账面市值比因子，等同于L3_BP。

        返回
        -------
        pd.DataFrame
            表示L2账面市值比因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L3_BP()
    
    def L2_Earning_Yield(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Earning Yield factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Earning Yield factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2盈利收益率因子。

        返回
        -------
        pd.DataFrame
            表示L2盈利收益率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_EP(),
                                    fac2 = self.L3_CP(),
                                    fac3 = self.L3_EBITP(),
                                    )
        return fac
    
    def L2_Long_Term_Reversal(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Long-Term Reversal factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Long-Term Reversal factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2长期反转因子。

        返回
        -------
        pd.DataFrame
            表示L2长期反转因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_LONG_TERM_STRENGTH(),
                                    fac2 = self.L3_LONG_TERM_ALPHA(),
                                    )
        return fac

    def L1_Value(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L1 Value factor by merging related L2 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L1 Value factor.

        ---------------------------------------------------------------------------

        通过合并相关的L2因子计算L1价值因子。

        返回
        -------
        pd.DataFrame
            表示L1价值因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L2_Book_to_Price(),
                                    fac2 = self.L2_Earning_Yield(),
                                    fac3 = self.L2_Long_Term_Reversal(),
                                    )
        return fac
    
    def L3_EP_GROWTH(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Earnings-to-Price Growth factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 EP Growth factor.

        ---------------------------------------------------------------------------

        计算L3市盈率倒数增长因子。

        返回
        -------
        pd.DataFrame
            表示L3 EP增长因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        w = self.__half_life__(252 * 2, 252 // 2)
        w = w / w.sum()
        eps = flow.stock('EPS')
        
        x_array = self.__array_roll__(eps.values, 252 * 2)
        df = np.array([np.nanmean(x_array[i] * w[:, np.newaxis], axis=0)  / np.nanstd(x_array[i] * w[:, np.newaxis], axis=0) for i in range(x_array.shape[0])])
        df = pd.DataFrame(df, index=eps.index[-df.shape[0]:], columns=eps.columns).reindex_like(eps)
        df = df[df.abs() != np.inf]
        return df
    
    def L3_PS_GROWTH(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Price-to-Sales Growth factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 PS Growth factor.

        ---------------------------------------------------------------------------

        计算L3市销率增长因子。

        返回
        -------
        pd.DataFrame
            表示L3 PS增长因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        w = self.__half_life__(252 * 2, 252 // 2)
        w = w / w.sum()
        eps = flow.stock('S_DQ_PS_TTM')
        
        x_array = self.__array_roll__(eps.values, 252 * 2)
        df = np.array([np.nanmean(x_array[i] * w[:, np.newaxis], axis=0)  / np.nanstd(x_array[i] * w[:, np.newaxis], axis=0) for i in range(x_array.shape[0])])
        df = pd.DataFrame(df, index=eps.index[-df.shape[0]:], columns=eps.columns).reindex_like(eps)
        df = df[df.abs() != np.inf]
        return df 

    def L2_Growth(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L2 Growth factor by merging related L3 factors.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Growth factor.

        ---------------------------------------------------------------------------

        通过合并相关的L3因子计算L2增长因子。

        返回
        -------
        pd.DataFrame
            表示L2增长因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        fac = self.__factors_merge__(
                                    fac1 = self.L3_EP_GROWTH(),
                                    fac2 = self.L3_PS_GROWTH(),
                                    )
        return fac

    def L1_Growth(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L1 Growth factor, which is equivalent to L2_Growth.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L1 Growth factor.

        ---------------------------------------------------------------------------

        表示L1增长因子，等同于L2_Growth。

        返回
        -------
        pd.DataFrame
            表示L1增长因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L2_Growth()
    
    def L3_DP(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the L3 Dividend Yield (DP) factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L3 DP factor.

        ---------------------------------------------------------------------------

        计算L3股息率（DP）因子。

        返回
        -------
        pd.DataFrame
            表示L3 DP因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = flow.stock('S_DQ_DIVRATIO_TTM')
        return df
    
    def L2_Dividend(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L2 Dividend factor, which is equivalent to L3_DP.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L2 Dividend factor.

        ---------------------------------------------------------------------------

        表示L2股息因子，等同于L3_DP。

        返回
        -------
        pd.DataFrame
            表示L2股息因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L3_DP()
    
    def L1_Dividend(self) -> pd.DataFrame:
        """
        ===========================================================================

        Represents the L1 Dividend factor, which is equivalent to L2_Dividend.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the L1 Dividend factor.

        ---------------------------------------------------------------------------

        表示L1股息因子，等同于L2_Dividend。

        返回
        -------
        pd.DataFrame
            表示L1股息因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        return self.L2_Dividend()
    
    def neutral(
        self, 
        factor: pd.DataFrame, 
        neu_factors: List[str] = ['L3_LNCAP', 'L3_MIDCAP', 'L3_BETA','L3_BOOK_LEVERAGE', 'L3_HISTORY_ALPHA', 'L3_SEASONLITY', 'L3_EP', 'L3_CP']
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Neutralizes a given factor against a list of specified neutralization factors.

        Parameters
        ----------
        factor : pd.DataFrame
            The factor DataFrame to be neutralized.
        neu_factors : List[str], optional
            A list of factor names to neutralize against. Defaults to 
            ['L3_LNCAP', 'L3_MIDCAP', 'L3_BETA','L3_BOOK_LEVERAGE', 'L3_HISTORY_ALPHA', 'L3_SEASONLITY', 'L3_EP', 'L3_CP'].

        Returns
        -------
        pd.DataFrame
            The neutralized factor DataFrame (residuals).

        ---------------------------------------------------------------------------

        对给定因子进行指定中性化因子列表的中性化处理。

        参数
        ----------
        factor : pd.DataFrame
            要进行中性化处理的因子DataFrame。
        neu_factors : List[str], optional
            要进行中性化处理的因子名称列表。默认为 
            ['L3_LNCAP', 'L3_MIDCAP', 'L3_BETA','L3_BOOK_LEVERAGE', 'L3_HISTORY_ALPHA', 'L3_SEASONLITY', 'L3_EP', 'L3_CP']。

        返回
        -------
        pd.DataFrame
            中性化后的因子DataFrame（残差）。

        ---------------------------------------------------------------------------
        """
        dic = {}
        for i in neu_factors:
            if not hasattr(self, '_' + i + '_VALUES'):
                x = getattr(self, i)()
                setattr(self, '_' + i + '_VALUES', x)
            dic[i] = getattr(self, '_' + i + '_VALUES').replace({np.inf:np.nan, -np.inf:np.nan})
            
        df = factor.stats.neutral(**dic).resid
        return df
