# -*- coding: utf-8 -*-
"""
Created on Mon May 19 11:40:21 2025

@author: Porco Rosso
"""

import flow
import factors
from factors import barra, volatility
import numpy as np
import pandas as pd
from factors.meta.main import main as meta

df = flow.stock('S_DQ_PE_TTM') ** -1 * 0.68 + flow.stock('S_DQ_PCF_TTM')** -1 * 0.21 
g1 = barra.cn4.merge(df.stats.neutral(fac=flow.stock('s_val_mv').tools.log()).resid, flow.stock('s_val_mv').tools.log()**-1).f.be_list().f.not_st()
g2 = df.stats.neutral(fac=flow.stock('s_val_mv').tools.log()).resid.stats.standard('uniform', (0,1)) * (flow.stock('s_val_mv').tools.log()**-1).stats.standard('uniform', (0,1))
g2 = g2.f.be_list().f.not_st()
x1 = flow.stock('s_dq_pe_ttm') ** -1
x2 = flow.stock('S_DQ_PCF_TTM') ** -1
x3 = flow.stock('s_dq_pb') ** -1
x4 = flow.stock('roe')
x5 = flow.stock('roa')

facs = [i.stats.neutral(fac=flow.stock('s_val_mv').tools.log()).resid for i in [x1]]
fac = barra.cn4.merge(barra.cn4.merge(*facs), flow.stock('s_val_mv').tools.log()**-1).f.be_list().f.not_st()
