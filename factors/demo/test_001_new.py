# -*- coding: utf-8 -*-
"""
Created on Mon May 19 11:40:21 2025

@author: Porco Rosso
"""

import flow
from factors import barra
import numpy as np
import pandas as pd
from factors.meta.main import main as meta

# --- Data Loading and Initial Transformations ---
# 加载数据并进行初始转换

amount = flow.stock('s_dq_amount')

g1 = flow.stock('s_dq_freeturnover') / 100

g2 = 1 - g1

g3 = np.log(g2)

price = flow.stock('s_dq_avgprice_adj')

close = flow.stock('s_dq_close_adj')

returns = flow.stock('s_dq_pctchange')

g4 = g3.cumsum()
    
# --- Factor Calculation Block 1: Based on Amount ---
# 因子计算块1：基于成交量

dic1 = amount

dic2 = price * amount

for i in range(1, 126):
    x = amount.shift(i) * np.exp(g4.diff(i))
    dic1 = dic1 + x if dic1 is not None else x
    dic2 = (
        dic2 + price.shift(i) * x 
        if dic2 is not None 
        else price.shift(i) * x
    )

fac = dic2 / dic1 / close

# --- Factor Calculation Block 2: Based on Free Turnover ---
# 因子计算块2：基于自由流通换手率

dic1 = None

dic2 = None

for i in range(1, 126):
    x = g1.shift(i) * np.exp(g3.diff(i))
    dic1 = dic1 + x if dic1 is not None else x
    dic2 = (
        dic2 + price.shift(i) * x 
        if dic2 is not None 
        else price.shift(i) * x
    )

fa1 = dic2 / dic1 / close

# --- Factor Calculation Block 3: Storing Intermediate Results ---
# 因子计算块3：存储中间结果

dic = {}

dic1 = g1

dic2 = price * g1

for i in range(1, 126):
    x = g1.shift(i) * np.exp(g4.diff(i))
    dic1 = dic1 + x if dic1 is not None else x
    dic2 = (
        dic2 + price.shift(i) * x 
        if dic2 is not None 
        else price.shift(i) * x
    )
    dic[i] = dic2 / dic1 / close -1
    
fac = dic2 / dic1 / close
