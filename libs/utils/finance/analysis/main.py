# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 10:47:51 2025

@author: Porco Rosso

"""
import numpy as np
import pandas as pd
from typing import Optional, Any
from libs.utils.finance.stats.main import standard
from libs.utils.finance.build.main import portfolio

def maxdown(df_obj: pd.DataFrame, iscumprod: bool) -> pd.DataFrame:
    if not iscumprod:
        x = df_obj.add(1, fill_value=0).cumprod()
        x[df_obj.isnull()] = pd.NA
    else:
        x = df_obj
    max_flow = x.expanding(min_periods=1).max()
    down_date = (x / max_flow).idxmin()
    max_down = x / max_flow - 1
    down_infomations = [(x.loc[j, i] if pd.notnull(j) else np.nan, max_down.loc[j, i] if pd.notnull(j) else np.nan) for i, j in down_date.items()]
    down_value, max_down = list(zip(*down_infomations))
    up_value = pd.Series([max_flow.loc[j, i] if pd.notnull(j) else np.nan for i, j in down_date.items()], index=down_date.index)
    up_date = max_flow[max_flow == up_value].idxmin()
    df = pd.DataFrame(
        [up_date.values, up_value, down_date.values, down_value, max_down], 
        columns=df_obj.columns, 
        index=['Maxdown_Start_Date', 'Maxdown_Start_Value', 'Maxdown_End_Date', 'Maxdown_End_Value', 'Maxdwon_Percent']
    )
    return df

def sharpe(df_obj: pd.DataFrame, iscumprod: bool, periods: Optional[int]) -> pd.Series:
    x =  df_obj if not iscumprod else df_obj.pct_change(fill_method=None)
    y = x.mean() / x.std()
    if periods is not None:
        periods = min([len(x), periods])
        y = y * periods ** 0.5
    y.name = 'periods in %s' %(periods)
    return y

def effective(df_obj: pd.DataFrame) -> pd.Series:
    x = df_obj.diff(axis=1)
    x = np.sign(x) * x ** 2
    x = x.sum(axis=1)
    return x

def expose(df_obj: pd.DataFrame, weight: Optional[pd.DataFrame], standard_method='uniform', *unnamed_factors, **named_factors: pd.DataFrame) -> Any:
    factors = {'unnamed_factor_{i}':j for i,j in enumerate(unnamed_factors)} | named_factors
    if standard_method == 'uniform':
        factors = {i:standard(j, method=standard_method, rank=(-1,1)) for i,j in factors.items()}
    elif standard_method == 'gauss':
        factors = {i:standard(j, method=standard_method, rank=(-5,5)) for i,j in factors.items()}
        
    df = {portfolio(df_obj, returns=j, weight=weight, shift=0) for i,j in factors.items()}
    if len(df) > 1:
        df = pd.concat(df, axis=100)
    else:
        df = list(df.values())[0]
    return df

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

