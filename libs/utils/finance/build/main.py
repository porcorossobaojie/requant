# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 11:29:51 2025

@author: Porco Rosso

"""

import numpy as np
import pandas as pd
from typing import Optional, Dict, Any, List, Union

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

def _weight(
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
            w_df = _fillna(w_df, df.index) if axis == 1  else _fillna(w_df, df.columns, axis=1)
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