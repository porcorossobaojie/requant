# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 17:25:10 2025

@author: Porco Rosso
"""
import flow
import numpy as np
import pandas as pd
from libs.utils.functions import flatten_list
from numpy.lib.stride_tricks import as_strided
from factors.meta.main import main as meta
from typing import Union, List, Dict, Any, Optional, Tuple, Callable

class main(meta):
    """
    ===========================================================================

    Implements the Barra CNE4 factor model for quantitative analysis.
    This class calculates various factors such as Size, Book-to-Market, Beta, 
    Momentum, Earnings, and Residual Volatility.

    ---------------------------------------------------------------------------

    实现用于量化分析的Barra CNE4因子模型。
    该类计算各种因子，如市值、账面市值比、Beta、动量、盈利和残差波动率。

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

    def L1_Size(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Size factor (log of market value).

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Size factor.

        ---------------------------------------------------------------------------

        计算市值因子（市值对数）。

        返回
        -------
        pd.DataFrame
            表示市值因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = flow.stock('s_val_mv')
        df = self.__log__(df)
        return df
    
    def L1_Non_size(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Non-Size factor, which is the residual of Size cubed regressed on Size.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Non-Size factor.

        ---------------------------------------------------------------------------

        计算非市值因子，它是市值立方对市值回归的残差。

        返回
        -------
        pd.DataFrame
            表示非市值因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.L1_Size()
        df = (df ** 3).stats.neutral(me=df).resid.stats.standard()
        return df

    def L1_Bm(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Book-to-Market (Bm) factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Book-to-Market factor.

        ---------------------------------------------------------------------------

        计算账面市值比（Bm）因子。

        返回
        -------
        pd.DataFrame
            表示账面市值比因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_L1_Bm_VALUES'):
            assets = flow.stock_finance('total_assets', shift=4)
            mv = flow.stock('s_val_mv')
            df = assets / mv / 1e8
            df = df.stats.neutral(fac=self.L1_Size()).resid
            setattr(self, '_L1_Bm_VALUES', df)
        return self._L1_Bm_VALUES
    
    def L1_Beta(
        self, 
        periods: int = 252
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Beta factor, and stores Alpha and Residual Volatility.

        Parameters
        ----------
        periods : int, optional
            The number of periods for rolling regression. Defaults to 252.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Beta factor.

        ---------------------------------------------------------------------------

        计算Beta因子，并存储Alpha和残差波动率。

        参数
        ----------
        periods : int, optional
            滚动回归的周期数。默认为 252。

        返回
        -------
        pd.DataFrame
            表示Beta因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_L1_Beta_beta'):
            returns = flow.stock('s_dq_pctchange')
            df = returns.stats.neutral(me=self.L1_Size(), bm=self.L1_Bm()).resid
            #mkt = (returns * mv).sum(axis=1) / mv.sum(axis=1)
            mkt = flow.index('s_dq_pctchange')['000905.XSHG']
            mkt = mkt.reindex(returns.index)
            mkt = pd.DataFrame(mkt.values.repeat(df.shape[-1]).reshape(returns.shape[0], -1), index=df.index, columns=df.columns)
            # standard versiond
            parameters = df.stats.neutral(market=mkt, neu_axis=0, periods=periods, weight=(self.__half_life__(periods, periods // 4)))
            beta = parameters.params['market'].unstack().reindex_like(returns)
            alpha =  parameters.params['const'].unstack().reindex_like(returns)
            resid = parameters.resid.std(axis=1).unstack().reindex_like(returns)
            self._L1_Beta_beta = beta
            self._L1_Beta_alpha = alpha
            self._L1_Beta_resid = resid
        return self._L1_Beta_beta
        
    def L1_Momentum(
        self, 
        periods: int = 504
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Momentum factor.

        Parameters
        ----------
        periods : int, optional
            The number of periods for rolling calculation. Defaults to 504.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Momentum factor.

        ---------------------------------------------------------------------------

        计算动量因子。

        参数
        ----------
        periods : int, optional
            滚动计算的周期数。默认为 504。

        返回
        -------
        pd.DataFrame
            表示动量因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_L1_Momentum_VALUES'):
            w = self.__half_life__(periods, periods//4)
            w = w / w.sum() 
            returns = flow.stock('s_dq_pctchange')
            mkt = flow.index('s_dq_pctchange')['000905.XSHG']
            mkt = mkt.reindex(returns.index)
            mkt = np.log(pd.DataFrame(mkt.values.repeat(returns.shape[-1]).reshape(returns.shape[0], -1), index=returns.index, columns=returns.columns) + 1)
            obj = returns.stats.neutral(neu_axis=1, me=self.L1_Size(), bm=self.L1_Bm()).resid
            obj = np.log(obj+1)
            
            fac = obj - mkt.shift(21)
            array = self.__array_roll__(fac.values, periods)
            array = [np.nansum(i * w[:, np.newaxis], axis=0) for i in array]
            array = pd.DataFrame(np.array(array), index=obj.index[periods-1:], columns=obj.columns)
            self._L1_Momentum_VALUES=array.reindex(obj.index)
        return self._L1_Momentum_VALUES

    def L1_Earning(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Earnings factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Earnings factor.

        ---------------------------------------------------------------------------

        计算盈利因子。

        返回
        -------
        pd.DataFrame
            表示盈利因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        df=flow.stock('S_DQ_PE_TTM') * 0.68 + flow.stock('S_DQ_PCF_TTM') * 0.21
        df=df.stats.neutral(neu_axis=1,  me=self.L1_Size(),
                            beta=self.L1_Beta()).resid
        return df
    
    def L1_Residual_volatility(
        self, 
        periods: int = 252
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Residual Volatility factor.

        Parameters
        ----------
        periods : int, optional
            The number of periods for rolling calculation. Defaults to 252.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Residual Volatility factor.

        ---------------------------------------------------------------------------

        计算残差波动率因子。

        参数
        ----------
        periods : int, optional
            滚动计算的周期数。默认为 252。

        返回
        -------
        pd.DataFrame
            表示残差波动率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_L1_Residual_volatility_VALUES'):
            if not hasattr(self, 'L1_Beta_resid'):
                self.L1_Beta()
            hsigma =  self._L1_Beta_resid
            #periods = 252
            w = self.__half_life__(periods, periods//4)
            array = self.__array_roll__(hsigma.values, periods)
            array = [np.nansum(i * w[:, np.newaxis], axis=0) for i in array]
            hsigma = pd.DataFrame(np.array(array), index=hsigma.index[periods-1:], columns=hsigma.columns)
            
            dastd = flow.stock('s_dq_pctchange').sub(flow.index('s_dq_pctchange')['000905.XSHG'], axis=0)
            array = self.__array_roll__(dastd.values, periods)
            array = [np.nanmean((i * w[:, np.newaxis]) **2, axis=0) for i in array]
            dastd = pd.DataFrame(np.array(array), index=dastd.index[periods-1:], columns=dastd.columns) ** 0.5
            self._L1_Residual_volatility_VALUES = (0.74 * dastd * 0.1 * hsigma) / (0.74 + 0.1)
        return self._L1_Residual_volatility_VALUES
        
    def neutral(
        self, 
        df: pd.DataFrame, 
        neutral_factors: List[str] = ['L1_Size', 'L1_Bm', 'L1_Non_size', 'L1_Beta', 'L1_Momentum', 'L1_Earning']
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Neutralizes a DataFrame against specified factors.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame to be neutralized.
        neutral_factors : List[str], optional
            A list of factor names to neutralize against. Defaults to 
            ['L1_Size', 'L1_Bm', 'L1_Non_size', 'L1_Beta', 'L1_Momentum', 'L1_Earning'].

        Returns
        -------
        pd.DataFrame
            The neutralized DataFrame (residuals).

        ---------------------------------------------------------------------------

        对DataFrame进行指定因子的中性化处理。

        参数
        ----------
        df : pd.DataFrame
            要进行中性化处理的DataFrame。
        neutral_factors : List[str], optional
            要进行中性化处理的因子名称列表。默认为 
            ['L1_Size', 'L1_Bm', 'L1_Non_size', 'L1_Beta', 'L1_Momentum', 'L1_Earning']。

        返回
        -------
        pd.DataFrame
            中性化后的DataFrame（残差）。

        ---------------------------------------------------------------------------
        """
        x=df.stats.neutral(**{i: getattr(self, i)()
                           for i in neutral_factors}).resid
        return x
