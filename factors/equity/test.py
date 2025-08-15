# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 10:09:06 2025

@author: Porco Rosso

"""

import flow
from factors import barra
import numpy as np
import pandas as pd
from factors.meta.main import main as meta

import flow
g1 = flow.index.index_member()
g2 = flow.stock('s_dq_freeturnover')
g3 = flow.stock('s_dq_pctchange')
g4 = flow.index('s_dq_pctchange')



periods = [21,42,126]
dic = {}
for i in index_name:
    j = index_member[i].reindex_like(fac).notnull().astype(int)
    muti_fac = pd.concat({'fac':fac, 'index':j}, axis=1)
    portfolio = muti_fac.build.group({'fac':np.linspace(0,1,11).round(2), 'index':[-0.1, 0.5, 1.1]}, order=True).build.portfolio(returns)
    dic[i] = portfolio
    
    









