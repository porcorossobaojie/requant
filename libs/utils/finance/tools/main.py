# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 11:48:32 2025

@author: Porco Rosso

"""
import numpy as np
import pandas as pd
from typing import Union, List, Any


def fillna(df_obj: pd.DataFrame, fill_list: List[Any]) -> pd.DataFrame:
    df_obj = df_obj.sort_index()
    old_idx = df_obj.index.to_list()
    index = sorted(fill_list)
    if index[-1] >= old_idx[0]:
        values = df_obj.values
        lst = []
        new_idx = sorted(set(df_obj.index) | set(index))
        position = [new_idx.index(i) for i in old_idx]
        position.append(len(new_idx))
        for i, j in enumerate(position[:-1]):
            repeat = position[i+1] - j
            array = values[i]
            array = array.repeat(repeat)
            lst.append(array.reshape(df_obj.shape[1], -1).T if repeat != 1 else array.reshape(1, -1))
        lst = np.concatenate(lst)
        lst = pd.DataFrame(lst, columns=df_obj.columns, index=new_idx[position[0]:]).reindex(index)
    else:
        lst = pd.DataFrame(np.nan, index=index, columns=df_obj.columns)

    lst.index.name = getattr(fill_list, 'name', df_obj.index.name)
    return lst


def shift(df_obj: pd.DataFrame, n: int) -> pd.DataFrame:
    bools = df_obj.iloc[-1].isnull()
    while n > 0 and bools.any():
        n -= 1
        df_obj.loc[:, bools] = df_obj.loc[:, bools].shift()
        bools = df_obj.iloc[-1].isnull()
        
    return df_obj


def log(
    df_obj: pd.DataFrame,
    bias_adj: Union[int, float] = 1,
    abs_adj: bool = True
) -> pd.DataFrame:
    if abs_adj:
        sign = np.sign(df_obj)
        x = sign * np.log((df_obj + sign * bias_adj).abs())
    else:
        x = np.log(bias_adj + df_obj)
        
    return x