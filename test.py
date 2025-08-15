# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 21:30:01 2025

@author: Porco Rosso

"""

import pandas as pd
import numpy as np
import flow
from scipy.signal import find_peaks
flow.data_init()
pd.Factorize()

pct = flow.stock('s_dq_pctchange')

periods = [63]
ddic = {}

g1 = pct.cumsum()
for j in range(len(g1.columns)):
    g2 = g1.iloc[:, j]
    g3 = pct.iloc[:, j].rolling(periods[0]).std().fillna(0)
    
    dic = {}
    for i in range(len(g2 - periods[0]) - 1):
        x = g2.iloc[i: i+periods[0]]
        x_max = find_peaks(
                    x, 
                    distance=int(periods[0]/5),
                    prominence=g3.iloc[i: i+periods[0]].values
                )[0]
        x1 = x.iloc[x_max].to_frame()
        x1['period'] = x_max
        max_1 = x1.stats.OLS().params.period if len(x1) >= 3 else None
        x1 =  x.iloc[x_max.tolist()+ [-1]].to_frame()
        x1['period'] = x_max.tolist() + [periods[0]]
        max_2 = x1.stats.OLS().params.period if len(x1) >= 3 else None
        
        x_min =  find_peaks(
                    x * -1, 
                    distance=int(periods[0]/5),
                    prominence=g3.iloc[i: i+periods[0]].values
                )[0]
        x1 = x.iloc[x_min].to_frame()
        x1['period'] = x_min
        min_1 = x1.stats.OLS().params.period if len(x1) >= 3 else None
        x1 =  x.iloc[x_min.tolist()+ [-1]].to_frame()
        x1['period'] = x_min.tolist() + [periods[0]]
        min_2 = x1.stats.OLS().params.period if len(x1) >= 3 else None
        dic[x.index[-1]] = {'max1':max_1, 'max2':max_2, 'min1':min_1, 'min2':min_2}
        
    df = pd.DataFrame(dic).T
    ddic[g1.columns[j]] = df
    print(j)
        
        
        
    
    
    
    
    
