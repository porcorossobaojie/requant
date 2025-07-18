# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 08:36:25 2025

@author: Porco Rosso

"""
import pandas as pd

class PUBLIC_KEYS:
    
    trade_dt: str = 'TRADE_DT'
    ann_dt: str = 'ANN_DT'
    code: str = 'S_INFO_WINDCODE'
    report_period: str = 'REPORT_PERIOD'
    time_bias = pd.Timedelta(15, 'h')
