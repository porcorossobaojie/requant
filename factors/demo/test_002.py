# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 13:15:16 2025

@author: Porco Rosso

"""

import flow
import pandas as pd
import numpy as np
flow.data_init()
pd.Factorize()
pd.capitalize()

pct = flow.stock('s_dq_pctchange')
fac1 = pct.rolling(42).std()
min_fac1 = fac1.rollings(10).min(2).mean()




rank_fac1 = min_fac1.rank(axis=1,pct=True, )
rank_fac2 = fac1.rank(axis=1,pct=True)

hold_series = rank_fac1.iloc[100].dropna().iloc[100:125]
rank_series = min_fac1.iloc[100].dropna().rank(ascending=False)


def hold_sell_split(hold_series, rank_series, high_limit_series, count, max_filter):
    hold = hold_series.reindex(rank_series)
    if high_limit_series is None:    
        hold = hold[rank_series <= count + max_filter]
    else:
        high_limit_series = high_limit_series.reindex(rank_series).fillna(False)
        hold = hold[(rank_series <= count + max_filter) | high_limit_series]
        
    hold = hold.dropna()
    sell = hold_series[~hold_series.index.isin(hold.index)]
    dic = {'hold':hold, 'sell':sell}
    return dic


    

        
        
        
        