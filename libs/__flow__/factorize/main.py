# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 13:35:28 2025

@author: Porco Rosso

"""

from libs.__flow__.__init__ import stock, index, trade_days
from libs.__flow__.config import FACTORIZE, COLUMNS_INFO
import pandas as pd


def be_list(df_obj=None, limit=None, inplace=True):
    x = stock.be_list(limit=limit if limit is not None else FACTORIZE.on_list_limit)
    if df_obj is not None:
        x = x.reindex_like(df_obj).fillna(False)
    if inplace and df_obj is not None:
        return df_obj[x]
    else:
        return x
    
def not_st(df_obj=None, limit=0, inplace=True):
    x = stock.is_st() <= limit
    if df_obj is not None:
        x = x.reindex_like(df_obj).fillna(False)
    if inplace and df_obj is not None:
        return df_obj[x]
    else:
        return x

def members(df_obj=None, name=None, inplace=True):
    if name == 'star':
        x = be_list(df_obj=None, limit=1)
        x = x.loc[:, [i[:3] not in FACTORIZE.star_info for i in x.columns]]
    else:
        name = FACTORIZE.index_mapping[name]
        x = index.index_member()[name].notnull()
    if df_obj is not None:
        x = x.reindex_like(df_obj).fillna(False)
    if inplace and df_obj is not None:
        return df_obj[x]
    else:
        return x

def label(df_obj, *key, **label_df):
    if len(key):
        key = key[0]
        if isinstance(key, str):
            key, label_obj = key.upper(), stock(key)
        else:
            key, label_obj = 'S_INFO_LABEL', key
    else:
        key, label_obj = list(label_df.keys())[0], list(label_df.values())[0]
        
    if COLUMNS_INFO.code not in label_obj.index.names:
        x = pd.concat({key:label_obj, '__FACTOR__': df_obj}, axis=1).stack(COLUMNS_INFO.code)
    else:
        df_obj = df_obj.stack(COLUMNS_INFO.code)
        x = pd.merge(label_obj.iloc[:, -1].to_frame(key), df_obj.to_frame('__FACTOR__'), left_index=True, right_index=True, how='left')
    x = x.set_index(key, append=True)['__FACTOR__']
    x = x.unstack([key, COLUMNS_INFO.code])
    return x
    
def info(df_obj, key):
    x = stock(key).reindex_like(df_obj)
    return x

def sinfo(series, key):
    x = stock(key)
    if x.index.name == COLUMNS_INFO.trade_dt:
        x = x.loc[series.name].reindex(series.index)
    else:
        x = stock(key, end=series.name)
    return x
    
def shift(series, n=1, copy=True):
    days = trade_days()
    day = days.get_loc(series.name) + n
    day = days[day]
    if copy:
        x = series.copy()
        x.name = day
        return x
    else:
        series.name = day


    
    
    
    
        
        
    