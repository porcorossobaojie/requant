# -*- coding: utf-8 -*-
"""
Created on Wed May 28 11:14:58 2025

@author:Porco Rosso
"""


import flow
from flow.config import COLUMNS_INFO
from factors import barra
import numpy as np
import pandas as pd
from factors.meta.main import main as meta
from factors.config import industry as config
from typing import Any, Dict, List, Optional, Union

class main(meta, config):
    """
    ===========================================================================

    Main class for calculating industry-related factors, including industry momentum and preference.

    ---------------------------------------------------------------------------

    用于计算行业相关因子的主类，包括行业动量和偏好。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self
    ):
        """
        ===========================================================================

        Initializes the main class for industry factor calculations.

        ---------------------------------------------------------------------------

        初始化行业因子计算的主类。

        ---------------------------------------------------------------------------
        """
        super().__init__()
    
    def __industry_momentum__(
        self, 
        keys: List[str]
    ) -> Dict[str, pd.DataFrame]:
        """
        ===========================================================================

        Calculates industry momentum for specified industry classification keys.

        Parameters
        ----------
        keys : List[str]
            A list of industry classification keys (e.g., 'S_SWL1_CODE').

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary where keys are industry classification keys and values are DataFrames 
            representing the industry momentum for each classification.

        ---------------------------------------------------------------------------

        计算指定行业分类键的行业动量。

        参数
        ----------
        keys : List[str]
            行业分类键列表（例如，'S_SWL1_CODE'）。

        返回
        -------
        Dict[str, pd.DataFrame]
            一个字典，其中键是行业分类键，值是表示每个分类的行业动量的DataFrame。

        ---------------------------------------------------------------------------
        """
        me = barra.cn4.L1_Size()
        bm = barra.cn4.L1_Bm()
        pct = flow.stock('s_dq_pctchange')
            
        neu_returns = pct.stats.neutral(me=me, bm=bm).resid
        
        dic: Dict[str, pd.DataFrame] = {}
        for i in keys:
            neu_me = pd.concat({i:flow.stock(i), 'me':me}, axis=1).stack()
            neu_me['sum'] = neu_me.groupby([COLUMNS_INFO.trade_dt, i]).transform('sum')
            neu_me = (neu_me['me'] / neu_me['sum']).unstack()
        
            momentum = pd.concat({i:flow.stock(i), 'me':neu_me, 're':neu_returns}, axis=1).stack()
            momentum['fac'] = momentum['me'] * momentum['re']
            fac = momentum.groupby([COLUMNS_INFO.trade_dt, i])['fac'].transform('sum')
            fac = fac.unstack()
            dic[i] = fac
        
        return dic
    
    def sw(self) -> Dict[str, pd.DataFrame]:
        """
        ===========================================================================

        Calculates industry momentum for Shenwan (SW) industry classifications.

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary of DataFrames representing industry momentum for SW classifications.

        ---------------------------------------------------------------------------

        计算申万（SW）行业分类的行业动量。

        返回
        -------
        Dict[str, pd.DataFrame]
            表示SW分类行业动量的DataFrame字典。

        ---------------------------------------------------------------------------
        """
        keys = self.SW_KEYS
        dic = self.__industry_momentum__(keys)
        return dic
    
    def zjw(self) -> Dict[str, pd.DataFrame]:
        """
        ===========================================================================

        Calculates industry momentum for CSRC (ZJW) industry classifications.

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary of DataFrames representing industry momentum for ZJW classifications.

        ---------------------------------------------------------------------------

        计算证监会（ZJW）行业分类的行业动量。

        返回
        -------
        Dict[str, pd.DataFrame]
            表示ZJW分类行业动量的DataFrame字典。

        ---------------------------------------------------------------------------
        """
        keys = self.ZJ_KEYS
        dic = self.__industry_momentum__(keys)
        return dic
        
    def jq(self) -> Dict[str, pd.DataFrame]:
        """
        ===========================================================================

        Calculates industry momentum for JQData (JQ) industry classifications.

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary of DataFrames representing industry momentum for JQ classifications.

        ---------------------------------------------------------------------------

        计算聚宽（JQ）行业分类的行业动量。

        返回
        -------
        Dict[str, pd.DataFrame]
            表示JQ分类行业动量的DataFrame字典。

        ---------------------------------------------------------------------------
        """
        keys = self.JQ_KEYS
        dic = self.__industry_momentum__(keys)
        return dic
        
    def all_industry(self) -> Dict[str, pd.DataFrame]:
        """
        ===========================================================================

        Calculates industry momentum for all defined industry classifications.

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary of DataFrames representing industry momentum for all classifications.

        ---------------------------------------------------------------------------

        计算所有已定义行业分类的行业动量。

        返回
        -------
        Dict[str, pd.DataFrame]
            表示所有分类行业动量的DataFrame字典。

        ---------------------------------------------------------------------------
        """
        keys = self.IND_KEYS
        dic = self.__industry_momentum__(keys)
        return dic
    
    def industry_momentum(
        self, 
        periods: List[int] = [3,5,7,10]
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates industry momentum across different lookback periods.

        Parameters
        ----------
        periods : List[int], optional
            A list of periods (in months) for which to calculate momentum. Defaults to [3, 5, 7, 10].

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the combined industry momentum across specified periods.

        ---------------------------------------------------------------------------

        计算不同回溯期的行业动量。

        参数
        ----------
        periods : List[int], optional
            要计算动量的周期（以月为单位）列表。默认为 [3, 5, 7, 10]。

        返回
        -------
        pd.DataFrame
            表示指定周期内组合行业动量的DataFrame。

        ---------------------------------------------------------------------------
        """
        dic: Dict[int, pd.DataFrame] = {}
        fac = self.all_industry()
        
        for i in periods:
            temp = {key:j.ewm(halflife=i).mean() for key, j in fac.items()}
            temp = self.merge(*temp.values())
            dic[i] = temp
        
        dic = self.merge(*dic.values())
        return dic
        
    def __industry_prefer__(
        self, 
        factor: pd.DataFrame, 
        ind_keys: List[str]
    ) -> Dict[str, pd.DataFrame]:
        """
        ===========================================================================

        Calculates industry preference based on a given factor and industry classification keys.

        Parameters
        ----------
        factor : pd.DataFrame
            The factor DataFrame to use for preference calculation.
        ind_keys : List[str]
            A list of industry classification keys.

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary where keys are industry classification keys and values are DataFrames 
            representing the industry preference for each classification.

        ---------------------------------------------------------------------------

        根据给定因子和行业分类键计算行业偏好。

        参数
        ----------
        factor : pd.DataFrame
            用于偏好计算的因子DataFrame。
        ind_keys : List[str]
            行业分类键列表。

        返回
        -------
        Dict[str, pd.DataFrame]
            一个字典，其中键是行业分类键，值是表示每个分类的行业偏好的DataFrame。

        ---------------------------------------------------------------------------
        """
        re = flow.stock('s_dq_pctchange')
        lag_factor = factor.shift()
        
        dic: Dict[str, pd.DataFrame] = {}
        for i in ind_keys:
            prefer_obj = pd.concat({i:flow.stock(i), 're':re, 'lag':lag_factor, 'factor':factor}, axis=1).stack()
            prefer_obj['rank'] = prefer_obj.groupby([COLUMNS_INFO.trade_dt, i])['lag'].rank(pct=True) - 0.5
            prefer_obj['fac_rank'] = prefer_obj.groupby([COLUMNS_INFO.trade_dt, i])['factor'].rank(pct=True) - 0.5
            high, low = prefer_obj[prefer_obj['rank'] > 0], prefer_obj[prefer_obj['rank'] <= 0]
            prefer = high.groupby([COLUMNS_INFO.trade_dt, i])['re'].mean() -low.groupby([COLUMNS_INFO.trade_dt, i])['re'].mean()
            prefer_obj = pd.merge(prefer_obj, prefer.rename('prefer_prem'), left_on=[COLUMNS_INFO.trade_dt, i], right_index=True, how='left')
            fac = (prefer_obj['fac_rank'] * prefer_obj['prefer_prem']).unstack()
            dic[i] = fac
            
        return dic
            
    def indust_lag(
        self, 
        keys: List[str]
    ):
        """
        ===========================================================================

        Calculates industry lag based on specified industry classification keys.

        Parameters
        ----------
        keys : List[str]
            A list of industry classification keys.

        ---------------------------------------------------------------------------

        根据指定的行业分类键计算行业滞后。

        参数
        ----------
        keys : List[str]
            行业分类键列表。

        ---------------------------------------------------------------------------
        """
        me = barra.cn4.L1_Size()
        
        dic: Dict[str, pd.DataFrame] = {}
        for i in keys:
            df = pd.concat({i:self.filter(flow.stock(i)), 'me':me}, axis=1).stack()
            df['me_sum'] = df.groupby([COLUMNS_INFO.trade_dt, i])['me'].transform('sum')
            df['me_lag'] = df['me_sum'] - df['me']
            df = df[['me', 'me_lag']].unstack().diff()
            lag = df['me'] - df['me_lag']
            # Further calculations for industry lag would go here.
            # dic[i] = lag # Placeholder
