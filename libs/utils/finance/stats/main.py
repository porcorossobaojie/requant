# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 12:51:00 2025

@author: Porco Rosso

"""

import numpy as np
from numpy.lib.stride_tricks import as_strided
from functools import partial
from tools import flatten_list
import scipy as sp
import pandas as pd
import statsmodels.api as sm
from typing import Optional, Union, Tuple, List, Dict, Any, Callable

def standard(
    df_obj: Union[pd.Series, pd.DataFrame], 
    method: str = 'gauss', 
    rank: Tuple[Optional[float], Optional[float]] = (-5,5), 
    axis: Optional[int] = None
) -> Union[pd.Series, pd.DataFrame]:
    axis = 0 if axis is None else axis
    if method == 'gauss':
        y = df_obj.sub(df_obj.mean(axis=axis), axis=0 if axis or isinstance(df_obj, pd.Series) else 1).div(df_obj.std(axis=axis), axis=0 if axis or isinstance(df_obj, pd.Series) else 1)
        y = y.clip(*rank)
    elif method == 'uniform':
        y = df_obj.rank(pct=True, axis=axis)
        rank = (0 if rank[0] is None else rank[0], 1 if rank[1] is None else rank[1])
        y = y * (rank[1] - rank[0]) + rank[0]
    else:
        y = df_obj
    return y

def OLS(
    df_obj: pd.DataFrame, 
    const: bool = False, 
    roll: Optional[int] = None, 
    min_periods: Optional[int] = None, 
    dropna: bool = True, 
    keys: Tuple[int, int] = (0, -1), 
    returns: type = dict, 
    weight: Optional[pd.DataFrame] = None
) -> Union[Dict[Any, sm.regression.linear_model.RegressionResultsWrapper], List[sm.regression.linear_model.RegressionResultsWrapper]]:
    df = df_obj.copy()
    roll = len(df) if roll is None or roll > len(df) else roll
    min_periods = 0 if min_periods is None else min_periods
    df.insert(1, 'const', 1) if const is True else None
    dic = {}
    for i in range(len(df) - roll + 1):
        y = df.iloc[i: i + roll]
        w = weight.iloc[i : i + roll] if weight is not None else 1.0
        key = y.index[keys[1]] if keys[0] == 0 else y.columns[keys[1]]
        if len(y.dropna()) >= min_periods:
            dic[key] = sm.WLS(y.iloc[:, 0].astype(float), y.iloc[:,1:].astype(float), weights=w, missing='drop').fit()
        elif dropna == False:
            dic[key] = None
        if returns is dict:
            return dic
    if isinstance(returns, dict):
        return dic
    else:
        dic = list(dic.values())
        if len(dic) == 1:
            dic = dic[0]
        return dic
        
def _const(
    df_obj: Union[pd.Series, pd.DataFrame], 
    columns: Optional[List[Any]] = None, 
    prefix: Optional[Union[str, List[str]]] = None, 
    sep: str = ''
) -> pd.DataFrame:
    return pd.get_dummies(df_obj, prefix=prefix, prefix_sep=sep, columns=columns)

def _array_3D(
    target_df: pd.DataFrame, 
    const: bool = True, 
    **kwargs: pd.DataFrame
) -> Any:
    target_df = target_df.sort_index(axis=1).sort_index()
    dic = {'target':target_df.values} | ({'const': np.ones_like(target_df)} if const else {}) | {i:j.reindex_like(target_df).values for i,j in kwargs.items()}
    x = type('array_3D', (), {'index':target_df.index, 'columns':target_df.columns, 'labels':list(dic.keys()), 'values':np.array(list(dic.values())).transpose(1,2,0)})
    return x

def _array_roll(
    array_3D: np.ndarray, 
    periods: int, 
    flatten: bool = False
) -> np.ndarray:
    axis=0
    new_shape = list(array_3D.shape)
    new_shape[axis] = [periods, new_shape[axis] - periods + 1, ]
    new_shape = tuple(flatten_list(new_shape))
    
    new_strides = list(array_3D.strides)
    new_strides[axis] = [array_3D.strides[axis], array_3D.strides[axis]]
    new_strides = tuple(flatten_list(new_strides))
    
    window = as_strided(array_3D, shape=new_shape, strides=new_strides)
    window = window.transpose(1, 0, 2, 3)
    if flatten:
        window = window.reshape(window.shape[0], -1, window.shape[-1])
    return window

def __lstsq(
    array_2D: np.ndarray, 
    w: Optional[np.ndarray] = None
) -> np.ndarray:
    not_nan = ~np.isnan(array_2D).any(axis=1)
    matrix = array_2D[not_nan, :]
    if w is not None:
        w =  w[not_nan]
    y = matrix[:, 0]
    if (matrix.shape[0] > matrix.shape[1] * 2) and matrix.shape[0] > 5:
        x = matrix[:, 1:]
        xT = x.T
        y =  matrix[:, 0]
        if w is None:
            params = sp.linalg.pinv(xT.dot(x)).dot(xT).dot(y)
        else:
            params = sp.linalg.pinv((xT * w).dot(x)).dot(xT * w).dot(y)
        #params = np.linalg.pinv(xT.dot(x)).dot(xT).dot(y)
    else:
        params = np.array([np.nan] * (matrix.shape[1] - 1))
    return params

def _lstsq(
    array_3D: np.ndarray, 
    neu_axis: int = 1, 
    w: Optional[np.ndarray] = None
) -> np.ndarray:
    array_3D = array_3D.transpose(1,0,2) if neu_axis == 0 else array_3D   
    if w is not None and array_3D.shape[:2] == w.shape:
        params = np.array(list(map(__lstsq, array_3D, w)))
    else:
        partial_func = partial(__lstsq, w=w)
        params = np.array(list(map(partial_func, array_3D)))
    return params
        
def neutral(
    df_obj: pd.DataFrame, 
    const: bool = True, 
    neu_axis: int = 1, 
    periods: Optional[int] = None, 
    flatten: bool = False,  
    w: Optional[np.ndarray] = None, 
    resid: bool = True, 
    **key_dfs: pd.DataFrame
) -> Any:
    data_obj = _array_3D(df_obj, const, **key_dfs)
    values = data_obj.values
    if periods is not None:
        values = _array_roll(values, periods, flatten)
        if len(values.shape) == 4:
            if neu_axis == 0:
                values = values.transpose(0,2,1,3)
                index = pd.MultiIndex.from_product([data_obj.index[periods-1:], data_obj.columns], names=[df_obj.index.name, df_obj.columns.name])
            else:
                index = pd.MultiIndex.from_product([data_obj.index[periods-1:], range(periods)], names=[df_obj.index.name, 'PERIOD'])
                
            values = values.reshape(values.shape[0] * values.shape[1], values.shape[2], values.shape[3])
        else:
            index = data_obj.index[periods-1:]
    else:
        if neu_axis == 0:
            index = data_obj.columns
            columns = data_obj.index
            values = values.transpose(1,0,2)
        else:
            index = data_obj.index
            columns = data_obj.columns
                
    parameters = _lstsq(values, w=w)
    parameters = pd.DataFrame(parameters, index=index, columns=data_obj.labels[1:])
    if resid:
        if periods is None:
            resid = values[:, :, 0] - np.sum((values[:, :, 1:] * parameters.values[:, np.newaxis, :]), axis=-1)
            resid = pd.DataFrame(resid, index=index, columns=columns)
        else:
            resid = values[:, :, 0].astype(np.float16) - np.sum((values[:, :, 1:].astype(np.float16) * parameters.values[:, np.newaxis, :].astype(np.float16)), axis=-1)
            resid = pd.DataFrame(resid, index=index)
        return type('neutral_obj', (), {'params':parameters, 'resid':resid})
    else:
        return type('neutral_obj', (), {'params':parameters})
