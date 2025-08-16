# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 13:14:44 2025

@author: Porco Rosso
"""

import flow
from factors import barra
import numpy as np
import pandas as pd
from factors.meta.main import main as meta
from factors.config import volatility
from typing import Any, Dict, List, Optional, Union

class main(meta, volatility):
    """
    ===========================================================================

    Main class for calculating volatility-related factors.

    ---------------------------------------------------------------------------

    用于计算波动率相关因子的主类。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self
    ):
        """
        ===========================================================================

        Initializes the main class for volatility factor calculations.

        ---------------------------------------------------------------------------

        初始化波动率因子计算的主类。

        ---------------------------------------------------------------------------
        """
        super().__init__()
        
    def AMOUNT(
        self, 
        reversal: str = 'mean', 
        detail: bool = False
    ) -> Union[List[pd.DataFrame], pd.DataFrame]:
        """
        ===========================================================================

        Calculates volatility factors based on trading amount.

        Parameters
        ----------
        reversal : str, optional
            Method for reversal calculation ('mean' or 'max'). Defaults to 'mean'.
        detail : bool, optional
            If True, returns a list of detailed factor DataFrames. If False, returns a merged DataFrame.
            Defaults to False.

        Returns
        -------
        Union[List[pd.DataFrame], pd.DataFrame]
            A list of DataFrames or a single merged DataFrame representing the amount-based volatility factors.

        ---------------------------------------------------------------------------

        计算基于交易量的波动率因子。

        参数
        ----------
        reversal : str, optional
            反转计算方法（'mean' 或 'max'）。默认为 'mean'。
        detail : bool, optional
            如果为 True，则返回详细因子DataFrames列表。如果为 False，则返回合并的DataFrame。
            默认为 False。

        返回
        -------
        Union[List[pd.DataFrame], pd.DataFrame]
            表示基于交易量的波动率因子的DataFrames列表或单个合并的DataFrame。

        ---------------------------------------------------------------------------
        """
        periods = self.__AMOUNT__.periods
        x = flow.stock('S_DQ_AMOUNT')     
        data = {i : np.log(x.rolling(i, min_periods=min(periods)).std().replace(0, np.nan)) for i in periods}
        df = pd.concat(data, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        df = self.reversal(df, reversal) * -1 # rolling(3).max is more effective, but less in fac self corr, so use mean
        
        diff_data = df.diff()
        diff_1 = {i : diff_data.ewm(halflife=i // 4).sum() for i in periods}
        diff_1 = pd.concat(diff_1, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        z_mean = diff_1.copy()
        diff_1 = diff_1.stats.standard(axis=1)
        diff_1 = self.reversal(diff_1, reversal)
        
        diff_std = {i: diff_data.rolling(i, min_periods=periods[0]).std().replace(0, np.nan) for i in periods}
        diff_std = pd.concat(diff_std, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        z_std = diff_std.copy()
        diff_std = diff_std.stats.standard(axis=1)
        diff_std =  self.reversal(diff_std, reversal) * -1
        
        diff_z = self.reversal((z_mean / z_std).stats.standard(axis=1), reversal)
        factors = [self.filter(i) for i in [df, diff_1, diff_std, diff_z]]
        if not detail:
            factors = self.merge(*factors)
        return factors
    
    def TURNOVER(
        self, 
        reversal: str = 'max', 
        detail: bool = False
    ) -> Union[List[pd.DataFrame], pd.DataFrame]:
        """
        ===========================================================================

        Calculates volatility factors based on turnover.

        Parameters
        ----------
        reversal : str, optional
            Method for reversal calculation ('mean' or 'max'). Defaults to 'max'.
        detail : bool, optional
            If True, returns a list of detailed factor DataFrames. If False, returns a merged DataFrame.
            Defaults to False.

        Returns
        -------
        Union[List[pd.DataFrame], pd.DataFrame]
            A list of DataFrames or a single merged DataFrame representing the turnover-based volatility factors.

        ---------------------------------------------------------------------------

        计算基于换手率的波动率因子。

        参数
        ----------
        reversal : str, optional
            反转计算方法（'mean' 或 'max'）。默认为 'max'。
        detail : bool, optional
            如果为 True，则返回详细因子DataFrames列表。如果为 False，则返回合并的DataFrame。
            默认为 False。

        返回
        -------
        Union[List[pd.DataFrame], pd.DataFrame]
            表示基于换手率的波动率因子的DataFrames列表或单个合并的DataFrame。

        ---------------------------------------------------------------------------
        """
        periods = self.__TURNOVER__.periods
        x = flow.stock('S_DQ_FREETURNOVER') / 100
        
        data = {i : np.log(x.rolling(i, min_periods=min(periods)).std().replace(0, np.nan)) for i in periods}
        df = pd.concat(data, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        df = self.reversal(df, reversal) * -1 # rolling(3).max is more effective, but less in fac self corr, so use mean
        
        diff_data = df.diff()
        diff_1 = {i : diff_data.ewm(halflife=i // 1).sum() for i in periods}
        diff_1 = pd.concat(diff_1, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        z_mean = diff_1.copy()
        diff_1 = diff_1.stats.standard(axis=1)
        #diff_1 = self.reversal(diff_1, reversal)
        
        diff_std = {i: diff_data.rolling(i, min_periods=periods[0]).std().replace(0, np.nan) for i in periods}
        diff_std = pd.concat(diff_std, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        z_std = diff_std.copy()
        diff_std = diff_std.stats.standard(axis=1)
        diff_std =  self.reversal(diff_std, reversal) * -1
        
        diff_z = (z_mean / z_std).stats.standard(axis=1)
        factors = [self.filter(i) for i in [df, diff_1, diff_std, diff_z]]
        if not detail:
            factors = self.merge(*factors)
        
        return factors

    def REVERSAL(
        self, 
        reversal: str = 'mean'
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates reversal factors based on price movements.

        Parameters
        ----------
        reversal : str, optional
            Method for reversal calculation ('mean' or 'max'). Defaults to 'mean'.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the reversal factors.

        ---------------------------------------------------------------------------

        计算基于价格变动的反转因子。

        参数
        ----------
        reversal : str, optional
            反转计算方法（'mean' 或 'max'）。默认为 'mean'。

        返回
        -------
        pd.DataFrame
            表示反转因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        periods = self.__REVERSAL__.periods

        pct = flow.stock('s_dq_pctchange')
        obj = {i:{pct.index[j + i]:pct.iloc[j:j + i].cumsum() for j in range(len(pct) - i)} for i in periods}
        obj = {i:{k:(l.max() - l.iloc[-1:].mean()) ** 2 - (l.min() - l.iloc[-1:].mean()) ** 2   for k,l in j.items()} for i,j in obj.items()}
        obj = pd.concat(obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        obj.index.name = flow.COLUMNS_INFO.trade_dt
        obj = self.filter(obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid)
        factor = obj
        return factor

    def RE_CORR_TURN(
        self, 
        reversal: str = 'mean'
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the correlation between returns and turnover.

        Parameters
        ----------
        reversal : str, optional
            Method for reversal calculation ('mean' or 'max'). Defaults to 'mean'.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the correlation factor.

        ---------------------------------------------------------------------------

        计算收益与换手率之间的相关性。

        参数
        ----------
        reversal : str, optional
            反转计算方法（'mean' 或 'max'）。默认为 'mean'。

        返回
        -------
        pd.DataFrame
            表示相关性因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        periods = [5, 6, 7, 8, 9, 10]
        pct = flow.stock('s_dq_pctchange')
        turn = (flow.stock('S_DQ_FREETURNOVER') / 100).replace(0, np.nan).pct_change()    
        obj = {i:pct.rolling(i, min_periods=periods[0]).corr(turn) for i in periods}
        obj = {i: j[(j >= -1) & (j <= 1)] for i,j in obj.items()}
        obj = pd.concat(obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        factor = self.reversal(obj, reversal).stats.standard() * -1
        factor = self.merge(factor)    
        return factor

    def amount_std(
        self, 
        rolling_list: List[int] = [42, 63, 126]
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the standard deviation of trading amount and its derivatives.

        Parameters
        ----------
        rolling_list : List[int], optional
            List of rolling window sizes. Defaults to [42, 63, 126].

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the amount standard deviation factors.

        ---------------------------------------------------------------------------

        计算交易量的标准差及其导数。

        参数
        ----------
        rolling_list : List[int], optional
            滚动窗口大小列表。默认为 [42, 63, 126]。

        返回
        -------
        pd.DataFrame
            表示交易量标准差因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        amount = flow.stock('s_dq_amount')
        pct = flow.stock('s_dq_pctchange')
        obj = {i:amount.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1

        diff_1 = obj.diff()
        diff_1_obj = {i:diff_1.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_1_obj = pd.concat(diff_1_obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_1_obj = diff_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        diff_2 = diff_1_obj.diff()
        diff_2_obj = {i:diff_2.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_2_obj = pd.concat(diff_2_obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_2_obj = diff_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        std_1 = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        std_1_obj = pd.concat(std_1, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        std_1_obj = std_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        std_2 = {i:std_1_obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        std_2_obj = pd.concat(std_2, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        std_2_obj = std_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        fac = pd.concat({i:j for i,j in enumerate([obj, diff_1_obj, diff_2_obj, std_1_obj, std_2_obj])}, axis=1)
        fac = fac.groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        
        #fac = barra.cn4.neutral(fac)
        
        return fac
    
    def amount_z(
        self, 
        rolling_list: List[int] = [10, 20, 30, 40, 50, 60]
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Z-score of trading amount and its derivatives.

        Parameters
        ----------
        rolling_list : List[int], optional
            List of rolling window sizes. Defaults to [10, 20, 30, 40, 50, 60].

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the amount Z-score factors.

        ---------------------------------------------------------------------------

        计算交易量的Z分数及其导数。

        参数
        ----------
        rolling_list : List[int], optional
            滚动窗口大小列表。默认为 [10, 20, 30, 40, 50, 60]。

        返回
        -------
        pd.DataFrame
            表示交易量Z分数因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        pct = flow.stock('s_dq_pctchange')
        obj = flow.stock('s_dq_amount')
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        
        diff_1 = obj.diff()
        diff_1_obj = {i:diff_1.rolling(i, min_periods=rolling_list[0]).mean() / diff_1.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_1_obj = pd.concat(diff_1_obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_1_obj = diff_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        
        diff_2 = diff_1_obj.diff()
        diff_2_obj = {i:diff_2.rolling(i, min_periods=rolling_list[0]).mean() / diff_2.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_2_obj = pd.concat(diff_2_obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_2_obj = diff_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        
        fac = pd.concat({i:j for i,j in enumerate([obj, diff_1_obj, diff_2_obj])}, axis=1)
        fac = fac.groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        
        return fac
        
    def tu_std(
        self, 
        rolling_list: List[int] = [42, 63, 126]
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the standard deviation of turnover and its derivatives.

        Parameters
        ----------
        rolling_list : List[int], optional
            List of rolling window sizes. Defaults to [42, 63, 126].

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the turnover standard deviation factors.

        ---------------------------------------------------------------------------

        计算换手率的标准差及其导数。

        参数
        ----------
        rolling_list : List[int], optional
            滚动窗口大小列表。默认为 [42, 63, 126]。

        返回
        -------
        pd.DataFrame
            表示换手率标准差因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        amount = flow.stock('s_dq_freeturnover')
        pct = flow.stock('s_dq_pctchange')
        obj = {i:amount.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1

        diff_1 = obj.diff()
        diff_1_obj = {i:diff_1.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_1_obj = pd.concat(diff_1_obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_1_obj = diff_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        diff_2 = diff_1_obj.diff()
        diff_2_obj = {i:diff_2.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_2_obj = pd.concat(diff_2_obj, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_2_obj = diff_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        std_1 = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        std_1_obj = pd.concat(std_1, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        std_1_obj = std_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        std_2 = {i:std_1_obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        std_2_obj = pd.concat(std_2, axis=1).groupby(flow.COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        std_2_obj = std_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        fac = pd.concat({i:j for i,j in enumerate([obj, diff_1_obj, diff_2_obj, std_1_obj, std_2_obj])}, axis=1)
        fac = fac.groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        
        #fac = barra.cn4.neutral(fac)
        
        return fac
    
    def volatility(
        self
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates a combined volatility factor from amount and turnover standard deviations and Z-scores.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the combined volatility factor.

        ---------------------------------------------------------------------------

        计算来自交易量和换手率标准差和Z分数的组合波动率因子。

        返回
        -------
        pd.DataFrame
            表示组合波动率因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        amount_std = barra.cn4.neutral(self.amount_std()) * 0.8
        amount_z = barra.cn4.neutral(self.amount_z()) * 1.0
        tu_std = barra.cn4.neutral(self.tu_std()) * 1.6
        
        fac = pd.concat({i:j for i,j in enumerate([amount_std, amount_z, tu_std])}, axis=1)
        fac = fac.groupby(flow.COLUMNS_INFO.code, axis=1).mean()
        fac = self.filter(fac)
        return fac
        
    def abnormal1(
        self, 
        rolling_list: List[int] = [42, 63, 126]
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates an abnormal return factor based on rolling cumulative sums.

        Parameters
        ----------
        rolling_list : List[int], optional
            List of rolling window sizes. Defaults to [42, 63, 126].

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the abnormal return factor.

        ---------------------------------------------------------------------------

        计算基于滚动累积和的异常收益因子。

        参数
        ----------
        rolling_list : List[int], optional
            滚动窗口大小列表。默认为 [42, 63, 126]。

        返回
        -------
        pd.DataFrame
            表示异常收益因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        pct = flow.stock('s_dq_pctchange')
        obj = {i:{pct.index[j + i]:pct.iloc[j:j + i].cumsum() for j in range(len(pct) - i)} for i in rolling_list}
        obj = {i:{k:(l.max() - l.iloc[-1:].mean()) ** 2 - (l.min() - l.iloc[-1:].mean()) ** 2   for k,l in j.items()} for i,j in obj.items()}
        obj = {i:pd.concat(j, axis=1).T for i,j in obj.items()}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack()
        obj.index.names = pct.index.names
        x = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid 
        x = self.filter(x)
        return x










