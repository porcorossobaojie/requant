# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 08:36:25 2025

@author: Porco Rosso

"""
import pandas as pd

class DATABASE:
    """
    ===========================================================================

    Configuration for database schema and key column names.

    ---------------------------------------------------------------------------

    数据库模式和关键列名的配置。

    ---------------------------------------------------------------------------
    """
    source: str = 'DuckDB'
    trade_dt: str = 'TRADE_DT'
    ann_dt: str = 'ANN_DT'
    code: str = 'S_INFO_WINDCODE'
    report_period: str = 'REPORT_PERIOD'
    time_bias = pd.Timedelta(15, 'h')
class FILTER:
    """
    ===========================================================================

    Configuration for data filtering parameters.

    ---------------------------------------------------------------------------

    数据过滤参数的配置。

    ---------------------------------------------------------------------------
    """
    trade_start: str = '2010-01-01'