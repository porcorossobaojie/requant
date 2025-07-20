# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 23:25:51 2025

@author: Porco Rosso
"""

import numpy as np
import pandas as pd
import flow
from flow.config import COLUMNS_INFO
from factors.config import PROPERTY_ATTRS_DIC, LIMIT
from typing import Any, Dict, List, Optional, Union

class main(LIMIT):
    """
    ===========================================================================

    Meta-class for factor calculation, providing common functionalities 
    such as filtering, data standardization, and factor merging.

    ---------------------------------------------------------------------------

    因子计算的元类，提供通用功能，
    例如过滤、数据标准化和因子合并。

    ---------------------------------------------------------------------------
    """
    trade_days: pd.DatetimeIndex = flow.trade_days()
    flow: Any = flow
    
    def __init__(
        self
    ):
        """
        ===========================================================================

        Initializes the meta-class for factor calculation.

        ---------------------------------------------------------------------------

        初始化因子计算的元类。

        ---------------------------------------------------------------------------
        """
        pass
    
    def is_tradeable(self) -> pd.DataFrame:
        """
        ===========================================================================

        Checks if a stock is currently tradeable.

        Returns
        -------
        pd.DataFrame
            A boolean DataFrame indicating tradeable status.

        ---------------------------------------------------------------------------

        检查股票当前是否可交易。

        返回
        -------
        pd.DataFrame
            指示可交易状态的布尔DataFrame。

        ---------------------------------------------------------------------------
        """
        return (flow.stock('S_DQ_TRADESTATUS') == 0)
    
                           
    def is_on_list(self) -> pd.DataFrame:
        """
        ===========================================================================

        Checks if a stock has been listed for at least the specified limit.

        Returns
        -------
        pd.DataFrame
            A boolean DataFrame indicating if the stock is on the list.

        ---------------------------------------------------------------------------

        检查股票是否已上市至少达到指定限制。

        返回
        -------
        pd.DataFrame
            指示股票是否在列表中的布尔DataFrame。

        ---------------------------------------------------------------------------
        """
        return flow.stock.be_list(self.ON_LIST_LIMIT)
    
    def is_not_st(self) -> pd.DataFrame:
        """
        ===========================================================================

        Checks if a stock is not marked as ST (Special Treatment).

        Returns
        -------
        pd.DataFrame
            A boolean DataFrame indicating if the stock is not ST.

        ---------------------------------------------------------------------------

        检查股票是否未被标记为ST（特别处理）。

        返回
        -------
        pd.DataFrame
            指示股票是否非ST的布尔DataFrame。

        ---------------------------------------------------------------------------
        """
        return (flow.is_st() <= self.IS_ST_FILTER)
        
    def mask(self) -> pd.DataFrame:
        """
        ===========================================================================

        Generates a combined mask for tradeable, on-list, and non-ST stocks.

        Returns
        -------
        pd.DataFrame
            A boolean DataFrame representing the combined mask.

        ---------------------------------------------------------------------------

        生成可交易、已上市和非ST股票的组合掩码。

        返回
        -------
        pd.DataFrame
            表示组合掩码的布尔DataFrame。

        ---------------------------------------------------------------------------
        """
        return (self.is_on_list() & self.is_not_st()).dropna(how='all', axis=1)
        
    def settle(
        self, 
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Filters a DataFrame based on the combined mask for settlement.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame to filter.

        Returns
        -------
        pd.DataFrame
            The filtered DataFrame.

        ---------------------------------------------------------------------------

        根据用于结算的组合掩码过滤DataFrame。

        参数
        ----------
        df : pd.DataFrame
            要过滤的输入DataFrame。

        返回
        -------
        pd.DataFrame
            过滤后的DataFrame。

        ---------------------------------------------------------------------------
        """
        return df[self.mask().reindex_like(df).fillna(False)]
    
    def trade(
        self, 
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Filters a DataFrame based on tradeable status and the combined mask.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame to filter.

        Returns
        -------
        pd.DataFrame
            The filtered DataFrame.

        ---------------------------------------------------------------------------

        根据可交易状态和组合掩码过滤DataFrame。

        参数
        ----------
        df : pd.DataFrame
            要过滤的输入DataFrame。

        返回
        -------
        pd.DataFrame
            过滤后的DataFrame。

        ---------------------------------------------------------------------------
        """
        return df[self.is_tradeable().reindex_like(df).fillna(False) & self.mask().reindex_like(df).fillna(False)]
            
    def filter(
        self, 
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Applies all filtering conditions (non-ST, on-list, tradeable) to a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame to filter.

        Returns
        -------
        pd.DataFrame
            The filtered DataFrame.

        ---------------------------------------------------------------------------

        将所有过滤条件（非ST、已上市、可交易）应用于DataFrame。

        参数
        ----------
        df : pd.DataFrame
            要过滤的输入DataFrame。

        返回
        -------
        pd.DataFrame
            过滤后的DataFrame。

        ---------------------------------------------------------------------------
        """
        is_not_st = self.is_not_st().reindex_like(df).fillna(False)
        is_on_list = self.is_on_list().reindex_like(df).fillna(False)
        is_trade = self.is_tradeable().reindex_like(df).fillna(False)
        return df[is_not_st & is_on_list & is_trade]
    
    def parameter_standard(
        self, 
        parameters: pd.DataFrame, 
        sub: float = 0.95
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Standardizes parameters using a sigmoid-like transformation.

        Parameters
        ----------
        parameters : pd.DataFrame
            The input DataFrame of parameters.
        sub : float, optional
            A subtraction factor for the transformation. Defaults to 0.95.

        Returns
        -------
        pd.DataFrame
            The standardized DataFrame of parameters.

        ---------------------------------------------------------------------------

        使用类似S型函数的变换标准化参数。

        参数
        ----------
        parameters : pd.DataFrame
            参数的输入DataFrame。
        sub : float, optional
            变换的减法因子。默认为 0.95。

        返回
        -------
        pd.DataFrame
            标准化后的参数DataFrame。

        ---------------------------------------------------------------------------
        """
        x = (np.exp(parameters) - sub) / (1 + np.exp(parameters))
        return x
    
    def reversal(
        self, 
        df: pd.DataFrame, 
        how: str = 'max'
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the reversal component of a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame.
        how : str, optional
            The method to calculate percentage change ('max' or 'mean'). Defaults to 'max'.

        Returns
        -------
        pd.DataFrame
            The DataFrame with the reversal component.

        ---------------------------------------------------------------------------

        计算DataFrame的反转分量。

        参数
        ----------
        df : pd.DataFrame
            输入DataFrame。
        how : str, optional
            计算百分比变化的方法（'max' 或 'mean'）。默认为 'max'。

        返回
        -------
        pd.DataFrame
            包含反转分量的DataFrame。

        ---------------------------------------------------------------------------
        """
        if how == 'max':
            pct = flow.stock('s_dq_pctchange').rolling(3).max()
        elif how == 'mean':
            pct = flow.stock('s_dq_pctchange').rolling(3).mean()
        return df.stats.neutral(pct=pct).resid
    
    def merge(
        self, 
        *factors: pd.DataFrame, 
        standard: bool = True
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Merges multiple factor DataFrames, optionally standardizing them.

        Parameters
        ----------
        *factors : pd.DataFrame
            Variable number of factor DataFrames to merge.
        standard : bool, optional
            Whether to standardize factors before merging. Defaults to True.

        Returns
        -------
        pd.DataFrame
            A single DataFrame representing the merged factors.

        ---------------------------------------------------------------------------

        合并多个因子DataFrame，可选地对其进行标准化。

        参数
        ----------
        *factors : pd.DataFrame
            要合并的因子DataFrame的可变数量参数。
        standard : bool, optional
            是否在合并前标准化因子。默认为 True。

        返回
        -------
        pd.DataFrame
            表示合并因子的单个DataFrame。

        ---------------------------------------------------------------------------
        """
        factors_dict = {i:(j.stats.standard() if standard else j) for i,j in enumerate(factors)}
        for i,j in factors_dict.items():
            parameters = flow.stock('s_dq_pctchange').stats.neutral(fac=j.shift()).params.fac
            parameters = self.parameter_standard(parameters).rolling(5).mean()
            factors_dict[i] = factors_dict[i].mul(parameters, axis=0)
        factors_merged = pd.concat(factors_dict, axis=1).groupby(COLUMNS_INFO.code, axis=1).mean()
        return factors_merged
