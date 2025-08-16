# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 23:33:58 2025

@author: Porco Rosso
"""
import pandas as pd
from libs.__flow__ import config
import re
import jqdatasdk as jq
from typing import Optional, Union

from libs import __pandas__
from libs.__flow__.main.main import stock as __STOCK__, index as __INDEX__, trade_days as __TRADE_DAYS__

__DATA_INIT__ = 'min'
stock = __STOCK__(__DATA_INIT__)
index = __INDEX__()
help = stock.help
data_init = stock.data_init
stock_finance = stock.stock_finance
letter_finance = stock.letter_finance
is_st = stock.is_st
be_list = stock.be_list

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

