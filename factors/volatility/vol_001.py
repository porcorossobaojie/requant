# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 15:31:55 2025

@author: Porco Rosso
"""

import flow
from flow.config import COLUMNS_INFO
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union

from factors.meta.main import main as meta
from factors import barra

class main(meta):
    """
    ===========================================================================

    Main class for calculating volatility-related factors, specifically focusing on amount and turnover.

    ---------------------------------------------------------------------------

    用于计算波动率相关因子的主类，特别关注交易量和换手率。

    ---------------------------------------------------------------------------
    """
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
        obj = pd.concat(obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1

        diff_1 = obj.diff()
        diff_1_obj = {i:diff_1.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_1_obj = pd.concat(diff_1_obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_1_obj = diff_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        diff_2 = diff_1_obj.diff()
        diff_2_obj = {i:diff_2.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_2_obj = pd.concat(diff_2_obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_2_obj = diff_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        std_1 = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        std_1_obj = pd.concat(std_1, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        std_1_obj = std_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        std_2 = {i:std_1_obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        std_2_obj = pd.concat(std_2, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        std_2_obj = std_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        fac = pd.concat({i:j for i,j in enumerate([obj, diff_1_obj, diff_2_obj, std_1_obj, std_2_obj])}, axis=1)
        fac = fac.groupby(COLUMNS_INFO.code, axis=1).mean()
        
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
        obj = pd.concat(obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        
        diff_1 = obj.diff()
        diff_1_obj = {i:diff_1.rolling(i, min_periods=rolling_list[0]).mean() / diff_1.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_1_obj = pd.concat(diff_1_obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_1_obj = diff_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        
        diff_2 = diff_1_obj.diff()
        diff_2_obj = {i:diff_2.rolling(i, min_periods=rolling_list[0]).mean() / diff_2.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_2_obj = pd.concat(diff_2_obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_2_obj = diff_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        
        fac = pd.concat({i:j for i,j in enumerate([obj, diff_1_obj, diff_2_obj])}, axis=1)
        fac = fac.groupby(COLUMNS_INFO.code, axis=1).mean()
        
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
        obj = pd.concat(obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1

        diff_1 = obj.diff()
        diff_1_obj = {i:diff_1.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_1_obj = pd.concat(diff_1_obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_1_obj = diff_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        diff_2 = diff_1_obj.diff()
        diff_2_obj = {i:diff_2.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        diff_2_obj = pd.concat(diff_2_obj, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        diff_2_obj = diff_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        std_1 = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        std_1_obj = pd.concat(std_1, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        std_1_obj = std_1_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        std_2 = {i:std_1_obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        std_2_obj = pd.concat(std_2, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean().stats.standard(axis=1)
        std_2_obj = std_2_obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        
        fac = pd.concat({i:j for i,j in enumerate([obj, diff_1_obj, diff_2_obj, std_1_obj, std_2_obj])}, axis=1)
        fac = fac.groupby(COLUMNS_INFO.code, axis=1).mean()
        
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
        fac = fac.groupby(COLUMNS_INFO.code, axis=1).mean()
        
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
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack()
        obj.index.names = pct.index.names
        x = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid 

        return x
