# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 11:29:51 2025

@author: Porco Rosso

"""

import numpy as np
import pandas as pd
from typing import Optional, Dict, Any, List, Union
from libs.utils.finance.tools.main import fillna as fillna_func
def group(
    df: pd.DataFrame, 
    rule: Union[Dict, List], 
    pct: bool = True, 
    order: bool = False, 
    nlevels: Optional[List[Union[int, str]]] = None
) -> pd.DataFrame:

    if isinstance(rule, dict):
        df.index.names = [i if i is not None else 'level_i' + str(j) for j,i in enumerate(df.index.names)]
        df.columns.names = [i if i is not None else 'level_c' + str(j) for j,i in enumerate(df.columns.names)]
        ind_keys = list(df.index.names)
        col_nlevels = [0] if nlevels is None else nlevels
        col_nlevels = [i if isinstance(i, int) else df.columns.name.index(i) for i in col_nlevels]
        df = df.stack(sorted(set(range(df.columns.nlevels)) - set(col_nlevels)))
        df = df.loc[:, list(rule.keys())]
        used_keys = []
        for k, i in enumerate(df.columns):
            df[i] = df.groupby(ind_keys + used_keys)[i].rank(pct=pct)
            df[i] = pd.cut(df[i], rule[i], labels=[str([rule[i][j], rule[i][j+1]]) for j in range(len(rule[i]) - 1)])
            if order:
                used_keys.append(i)
        df = df.unstack(list(range(df.index.nlevels)[-1 * len(col_nlevels):]))
    else:
        df = df.rank(axis=1, pct=pct)
        col_nlevels = df.columns.nlevels
        df = df.stack(list(range(col_nlevels)))
        df = pd.cut(df, rule, labels=[str([rule[i], rule[i+1]]) for i in range(len(rule) - 1)])
        df = df.unstack(list(range(df.index.nlevels)[-1 * col_nlevels:]))
    return df

def weight(
    df: pd.DataFrame, 
    w_df: Optional[pd.DataFrame] = None, 
    fillna: bool = True, 
    pct: bool = True, 
    axis: Optional[int] = None
) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame) or not isinstance(w_df, (pd.DataFrame, type(None))) or not isinstance(fillna, bool) or not isinstance(pct, bool) or axis not in (None, 0, 1):
        raise TypeError('parameters type error.')
    axis = 0 if axis is None else axis
    if w_df is not None:
        if fillna == True:
            w_df = fillna_func(w_df, df.index) if axis == 1  else fillna_func(w_df, df.columns, axis=1)
        w_df = w_df.reindex_like(df)
        w_df[df.isnull()] = pd.NA
        if pct == True:
            w_df = (w_df.T / w_df.sum(axis=1)).T if axis == 1 else w_df / w_df.sum()
        return df * w_df
    else:
        if pct == True:
            x = df / df.notnull().sum() if axis == 0 else (df.T / df.notnull().sum(axis=1)).T
        else:
            x = df
        return x    
    
def portfolio(
    df_obj: pd.DataFrame, 
    returns: pd.DataFrame, 
    weight: Optional[pd.DataFrame] = None, 
    shift: int = 1, 
    roll: int = 1, 
    fillna: bool = False
) -> pd.DataFrame:
    returns = returns.rolling(roll).mean().shift((roll - 1 + shift) * -1)
    df_obj = (fillna_func(df_obj, returns.index) if fillna else df_obj)
    if df_obj.columns.nlevels == 1:
        df_obj.columns = pd.MultiIndex.from_product(
            [['__factor__'], df_obj.columns], 
            names=('VALUE', df_obj.columns.name)
        )
    
    if weight is not None:
        weight = (fillna_func(weight, returns.index) if fillna else weight).reindex_like(returns)
        weight = weight[returns.notnull()]
        df = pd.concat({'__returns__':returns, '__weight__':weight}, axis=1)
    else:
        df = pd.concat({'__returns__':returns}, axis=1)
        
    df = pd.concat([df, df_obj], axis=1).stack()
    df.index.names = [i if i is not None else 'level_i' + str(j) for j,i in enumerate(df.index.names)]
    group_keys = [df.index.names[0]] + list(df_obj.columns.get_level_values(0).unique())
    df.index = df.index.droplevel(-1)
    df = df.set_index(group_keys[1:], append=True)
    df = df.sort_index()
    
    if weight is not None:
        df['__returns__'] = df['__returns__'] * df['__weight__']
        obj = df.groupby(group_keys)
        obj = obj['__returns__'].sum(min_count=1) / obj['__weight__'].sum(min_count=1)
    else:
        obj = df.groupby(group_keys).mean()
        
    obj = obj.unstack(list(range(1, obj.index.nlevels)))
    if len(obj.columns.get_level_values(0).unique()) == 1:
        obj.columns = obj.columns.droplevel(0)
        
    obj = obj.astype('float64')
    obj = obj.shift(shift)
    return obj

def cut(
    df_obj: pd.DataFrame, 
    left: Union[int, float], 
    right: Union[int, float], 
    rng_left: Union[int, float], 
    rng_right: Union[int, float], 
    pct: bool = True, 
    ascending: bool = False
) -> pd.DataFrame:
    role = right - left
    lst = []
    rank = df_obj.rank(axis=1, pct=pct, ascending=ascending)
    j = rank.iloc[0]
    j = (j >= left) & (j <= right)
    lst.append(j.values)
    for i, j in rank.iloc[1:].iterrows():
        hold = (j >= left - rng_left) & (j <= right + rng_right) & lst[-1]
        lens = int(role * j.notnull().sum()) if pct else role
        updates = lens - hold.sum()
        if updates > 0:
            j = j[(~hold) & (j >= left)].sort_values().head(updates)
            hold[j.index] = True
        elif updates < 0:
            hold[~hold.index.isin(j[hold].sort_values().head(lens).index)] = False
        lst.append(hold.values)
    lst = pd.DataFrame(np.vstack(lst), index=df_obj.index, columns=df_obj.columns)
    return lst    
    
    
    