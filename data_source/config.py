# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 08:36:25 2025

@author: Porco Rosso

"""
import pandas as pd

class DATABASE:
    """
    ===========================================================================

    Configuration settings for the database connection and table structure.

    This class defines standard column names and the data source type.

    ---------------------------------------------------------------------------

    数据库连接和表结构的配置设置。

    该类定义了标准的列名和数据源类型。

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

    Configuration for data filtering.

    Specifies the start date for historical data retrieval.

    ---------------------------------------------------------------------------

    数据筛选配置。

    指定历史数据检索的开始日期。

    ---------------------------------------------------------------------------
    """
    trade_start: str = '2010-01-01'