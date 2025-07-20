# -*- coding: utf-8 -*-
"""
Created on Fri May  2 14:31:17 2025

@author: Porco Rosso
"""


import flow
from factors import barra
import numpy as np
import pandas as pd
from factors.meta.main import main as meta
from typing import Any, Dict, List, Optional, Union


class main(meta):
    """
    ===========================================================================

    Main class for calculating equity-related factors.

    ---------------------------------------------------------------------------

    用于计算股票相关因子的主类。

    ---------------------------------------------------------------------------
    """
    
    def ASSETS_PREM(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Assets Premium factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Assets Premium factor.

        ---------------------------------------------------------------------------

        计算资产溢价因子。

        返回
        -------
        pd.DataFrame
            表示资产溢价因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        tot_assets = flow.stock_finance('total_assets', shift=2, periods=8)
        tot_liab = flow.stock_finance('TOTAL_LIABILITY', shift=2, periods=8)
        assets_gth = tot_assets.groupby('TRADE_DT').pct_change(fill_method=None)
        gth_trend = assets_gth.unstack('TRADE_DT').T
        asset_mean = gth_trend.ewm(halflife=0.5, axis=1).mean().iloc[:, -1]
        asset_mean = asset_mean.unstack(0)
        asset_abnor = gth_trend.iloc[:, -1] - gth_trend.iloc[:, :-1].mean(axis=1)
        asset_abnor = asset_abnor.unstack(0)
        assets = tot_assets.groupby('TRADE_DT').apply(lambda x: x.iloc[-1])
        
        gth_trend = (tot_liab / tot_assets).unstack('TRADE_DT').T      
        liab_mean = gth_trend.ewm(halflife=0.5, axis=1).mean().iloc[:, -1]
        liab_mean = liab_mean.unstack(0)
        liab_abnor =  (gth_trend.iloc[:, -1] - gth_trend.iloc[:, :-1].mean(axis=1)).unstack(0)
        
        mv = flow.stock('s_val_mv')
        
        fac = np.log(self.filter(mv)).stats.neutral(assets=np.log(assets))
        fac_prem = (np.log(mv) - fac.resid) / np.log(mv)
        gth_prem = (fac_prem**-1).stats.neutral(fac1=asset_mean, fac2=asset_abnor, fac3=liab_mean, fac4=liab_abnor)
        asset_prem = (np.log(mv) - gth_prem.resid) / np.log(mv)
        asset_prem = self.reversal(asset_prem, 'mean')
        
        return asset_prem
        """
        mv_diff = np.log(self.filter(mv)).diff()
        asset_diff = np.log(assets).diff()
        asset_diff = asset_diff[asset_diff !=0] 
        asset_mean_diff = asset_mean.diff()
        asset_mean_diff = asset_mean_diff[asset_mean_diff != 0]
        liab_mean_diff = liab_mean.diff()
        liab_mean_diff = liab_mean_diff[liab_mean_diff != 0]
        asset_abnor_diff = asset_abnor.diff()
        asset_abnor_diff = asset_abnor_diff[asset_abnor_diff !=0]
        liab_abnor_diff = liab_abnor.diff()
        liab_abnor_diff = liab_abnor_diff[liab_abnor_diff !=0]
        facs = {'fac1':asset_diff, 'fac2':asset_mean_diff, 'fac3':liab_mean_diff, 'fac4':asset_abnor_diff, 'fac5':liab_abnor_diff}
        g4 =  (g2**-1).stats.neutral(neu_axis=1, periods=252, flatten=True, resid=False, **facs).params
        g5 = pd.concat({i:j.mul(g4[i], axis=0) for i,j in facs.items()}, axis=1)
        g5 = g5.groupby('S_INFO_WINDCODE', axis=1).sum(min_count=1)
        g5 = g5.add(g4['const'], axis=0)
        g5 = g2 - g5
        
        fac3 = (np.log(mv) - g3.resid + g5.ffill(limit=21).fillna(0)) / np.log(mv)
        """
        
    def OPER_PREM(self) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the Operating Premium factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Operating Premium factor.

        ---------------------------------------------------------------------------

        计算营业溢价因子。

        返回
        -------
        pd.DataFrame
            表示营业溢价因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        tot_assets = flow.stock_finance('TOTAL_OPERATING_REVENUE', shift=2, periods=12, quarter_adj=3)
        tot_assets = tot_assets[tot_assets > 0]
        tot_liab = flow.stock_finance('TOTAL_OPERATING_COST', shift=2, periods=12, quarter_adj=3)
        tot_liab = tot_liab[tot_liab > 0]
        assets_gth = tot_assets.replace(0, np.nan).groupby('TRADE_DT').pct_change(fill_method=None, periods=4)
        gth_trend = assets_gth.unstack('TRADE_DT').T
        asset_mean = gth_trend.ewm(halflife=0.5, axis=1).mean().iloc[:, -1]
        asset_mean = asset_mean.unstack(0)
        asset_abnor = gth_trend.iloc[:, -1] - gth_trend.iloc[:, :-1].mean(axis=1)
        asset_abnor = asset_abnor.unstack(0)
        assets = tot_assets.groupby('TRADE_DT').apply(lambda x: x.iloc[-4:].sum(min_count=4))
        
        gth_trend = (tot_liab / tot_assets).unstack('TRADE_DT').T      
        liab_mean = gth_trend.ewm(halflife=0.5, axis=1).mean().iloc[:, -1]
        liab_mean = liab_mean.unstack(0)
        liab_abnor =  (gth_trend.iloc[:, -1] - gth_trend.iloc[:, :-1].mean(axis=1)).unstack(0)
        
        mv = flow.stock('s_val_mv')
        
        fac = np.log(self.filter(mv)).stats.neutral(assets=np.log(assets))
        fac_prem = (np.log(mv) - fac.resid) / np.log(mv)
        gth_prem = (fac_prem**-1).stats.neutral(fac1=asset_mean, fac2=asset_abnor, fac3=liab_mean, fac4=liab_abnor)
        asset_prem = (np.log(mv) - gth_prem.resid) / np.log(mv)
        asset_prem = self.reversal(asset_prem, 'mean')
        return asset_prem
    
    def PROFIT_PREM(self):
        """
        ===========================================================================

        Calculates the Profit Premium factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Profit Premium factor.

        ---------------------------------------------------------------------------

        计算利润溢价因子。

        返回
        -------
        pd.DataFrame
            表示利润溢价因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        tot_profit = flow.stock_finance('TOTAL_PROFIT', shift=2, periods=12, quarter_adj=3)
        # Further calculations for PROFIT_PREM would go here.
        return tot_profit # Placeholder
        
    def indust_prem(self):
        """
        ===========================================================================

        Calculates the Industry Premium factor.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the Industry Premium factor.

        ---------------------------------------------------------------------------

        计算行业溢价因子。

        返回
        -------
        pd.DataFrame
            表示行业溢价因子的DataFrame。

        ---------------------------------------------------------------------------
        """
        ind_keys = ['S_SWL1_CODE', 'S_SWL2_CODE', 'S_SWL3_CODE', 'S_ZJW_CODE', 'S_JQL1_CODE', 'S_JQL1_CODE']
        df = flow.stock(ind_keys + ['s_dq_pctchange'])
        # Further calculations for indust_prem would go here.
        return df # Placeholder
