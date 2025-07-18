# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 23:33:58 2025

@author: Porco Rosso
"""
import pandas as pd
from flow import config
import re
import jqdatasdk as jq
from typing import List, Optional, Union

__DATA_INIT__ = 'min'

from flow.main.main import stock as __STOCK__, index as __INDEX__, trade_days as __TRADE_DAYS__

stock = __STOCK__(__DATA_INIT__)
index = __INDEX__()

def trade_days() -> list:
    """
    ===========================================================================

    Get trade days.

    Returns
    -------

    list
        A list of trade days.

    ---------------------------------------------------------------------------


    获取交易日。

    返回
    -------

    list
        交易日列表。

    ---------------------------------------------------------------------------

    """
    return __TRADE_DAYS__

help = stock.help
data_init = stock.data_init
stock_finance = stock.stock_finance
letter_finance = stock.letter_finance
is_st = stock.is_st
be_list = stock.be_list


def code_standard(
    obj: Union[pd.DataFrame, pd.Series, list],
    how: Optional[str] = None
) -> Union[pd.DataFrame, pd.Series, list]:
    """
    ===========================================================================

    Standardize the code format.

    Parameters
    ----------
    obj : Union[pd.DataFrame, pd.Series, list]
        The object to be standardized.
    how : Optional[str], optional
        The standardization method. Defaults to None.

    Returns
    -------

    Union[pd.DataFrame, pd.Series, list]
        The standardized object.

    ---------------------------------------------------------------------------


    标准化代码格式。

    参数
    ----------
    obj : Union[pd.DataFrame, pd.Series, list]
        要标准化的对象。
    how : Optional[str], optional
        标准化方法。默认为 None。

    返回
    -------

    Union[pd.DataFrame, pd.Series, list]
        标准化后的对象。

    ---------------------------------------------------------------------------

    """
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        if config.COLUMNS_INFO.code == obj.index.name:
            x = [''.join(re.findall(r'\d+', str(i))).zfill(6) for i in obj.index]
            if how =='jq':
                x = jq.normalize_code(x)
            obj.index = pd.Index(x, name=obj.index.name)
        elif config.DATABASE.code == obj.columns.name:
            x = [''.join(re.findall(r'\d+', str(i))).zfill(6) for i in obj.columns]
            if how =='jq':
                x = jq.normalize_code(x)
            obj.columns = pd.Index(x, name=obj.columns.name)
        return obj
    else:
        x = [''.join(re.findall(r'\d+', str(i))).zfill(6) for i in obj]
        if how =='jq':
            x = jq.normalize_code(x)
        return x

def summary(
    df: pd.DataFrame,
    how: List[str] = ['corr', 'portfolio', 'effective']
) -> object:
    """
    ===========================================================================

    Summarize the given DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be summarized.
    how : List[str], optional
        The summary methods. Defaults to ['corr', 'portfolio', 'effective'].

    Returns
    -------

    object
        An object containing the summary results.

    ---------------------------------------------------------------------------


    汇总给定的DataFrame。

    参数
    ----------
    df : pd.DataFrame
        要汇总的DataFrame。
    how : List[str], optional
        汇总方法。默认为 ['corr', 'portfolio', 'effective']。

    返回
    -------

    object
        包含汇总结果的对象。

    ---------------------------------------------------------------------------

    """
    class obj():
        if 'corr' in how:
            corr = df.corrwith(df.shift(), axis=1).describe()
        if 'portfolio' or 'effecrive' in how:
            portfolio = df.build.group().build.portfolio(stock('s_dq_pctchange')).loc['2017':]
        if 'effective' in how:
            effective = portfolio.analysis.effective()
            
    return obj

def indust_merge(
    industry: Union[str, pd.DataFrame],
    **factors
) -> pd.DataFrame:
    """
    ===========================================================================

    Merge industry data with factors.

    Parameters
    ----------
    industry : Union[str, pd.DataFrame]
        The industry data.
    **factors
        The factors to be merged.

    Returns
    -------

    pd.DataFrame
        The merged DataFrame.

    ---------------------------------------------------------------------------


    将行业数据与因子合并。

    参数
    ----------
    industry : Union[str, pd.DataFrame]
        行业数据。
    **factors
        要合并的因子。

    返回
    -------

    pd.DataFrame
        合并后的DataFrame。

    ---------------------------------------------------------------------------

    """
    if isinstance(industry, str):
        industry = stock(industry)
    try:
        df = pd.concat({'INDUSTRY':industry} | factors, axis=1)
        df = df.stack().set_index('INDUSTRY', append=True)
    except:
        df = pd.concat(factors, axis=1).stack()
        indust = pd.concat({'INDUSTRY':industry.iloc[:, 0]}, axis=1)
        df = pd.merge(indust, df, left_index=True, right_index=True).set_index('INDUSTRY', append=True)
    df.columns.name = 'FACTORS'
    if df.shape[1] == 1:
        df = df.iloc[:, 0]
        df = df.unstack(['INDUSTRY', config.DATABASE.code])
    else:
        df = df.unstack(['INDUSTRY', config.DATABASE.code])
        df.columns = df.columns.reorder_levels(['FACTORS', 'INDUSTRY', config.DATABASE.code])

    return df

def mask(
    df: pd.DataFrame,
    high_limit: bool = True,
    low_limit: bool = True,
    trade_status: bool = True,
    be_list_limit: Optional[int] = 126,
    st_limit: bool = True
) -> pd.DataFrame:
    """
    ===========================================================================

    Mask the given DataFrame based on specified conditions.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be masked.
    high_limit : bool, optional
        Whether to filter out stocks that have reached their high limit. Defaults to True.
    low_limit : bool, optional
        Whether to filter out stocks that have reached their low limit. Defaults to True.
    trade_status : bool, optional
        Whether to filter out stocks that are not trading. Defaults to True.
    be_list_limit : Optional[int], optional
        The minimum number of days a stock has been listed. Defaults to 126.
    st_limit : bool, optional
        Whether to filter out ST stocks. Defaults to True.

    Returns
    -------

    pd.DataFrame
        The masked DataFrame.

    ---------------------------------------------------------------------------


    根据指定条件屏蔽给定的DataFrame。

    参数
    ----------
    df : pd.DataFrame
        要屏蔽的DataFrame。
    high_limit : bool, optional
        是否过滤掉涨停的股票。默认为 True。
    low_limit : bool, optional
        是否过滤掉跌停的股票。默认为 True。
    trade_status : bool, optional
        是否过滤掉未交易的股票。默认为 True。
    be_list_limit : Optional[int], optional
        股票上市的最少天数。默认为 126。
    st_limit : bool, optional
        是否过滤掉ST股票。默认为 True。

    返回
    -------

    pd.DataFrame
        屏蔽后的DataFrame。

    ---------------------------------------------------------------------------

    """
    if high_limit:
        df = df[stock('s_dq_close') != stock('s_dq_high_limit')]
    if low_limit:
        df = df[stock('s_dq_close') != stock('s_dq_high_limit')]
    if trade_status:
        df = df[stock('s_dq_tradestatus') == 0]
    if be_list_limit is not None:
        df = df[be_list(be_list_limit)]
    if st_limit:
        df = df[is_st() == 0]
        
    return df
