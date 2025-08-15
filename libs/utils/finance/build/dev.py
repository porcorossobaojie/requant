# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 14:04:48 2025

@author: Porco Rosso

"""
from numba import njit, prange
import numpy as np
from numpy.lib.stride_tricks import as_strided
from functools import partial
import scipy as sp
import pandas as pd
import statsmodels.api as sm
from typing import Optional, Union, Tuple, List, Dict, Any, Callable

from libs.utils.functions import flatten_list

def filter_not_nans(array_3D):
    x = np.array([ ~np.isnan(array_3D[i]).any(axis=1) for i in range(array_3D.shape[0])])
    return x

@njit(parallel=True)
def __lstsq_without_w(
        array_2D: np.ndarray,
        not_nan: np.ndarray):
    matrix = array_2D[not_nan, :]
    if (matrix.shape[0] > matrix.shape[1] * 2) and matrix.shape[0] > 5:
        y = matrix[:, 0]
        x = matrix[:, 1:]
        xT = x.T
        params = np.linalg.pinv(xT.dot(x)).dot(xT).dot(y)
    else:
        params = np.array([np.nan] * (matrix.shape[1] - 1))
    return params
        
def _lstsq(
    array_3D: np.ndarray,
    neu_axis: int = 1,
    w: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    ===========================================================================

    Applies least squares regression across a 3D array.

    This function iterates through slices of a 3D array and performs least
    squares regression on each slice.

    ---------------------------------------------------------------------------

    对 3D 数组应用最小二乘回归。

    此函数遍历 3D 数组的切片，并对每个切片执行最小二乘回归。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    array_3D : np.ndarray
        The input 3D array.
    neu_axis : int, optional
        Axis along which to perform regression (0 or 1), by default 1.
    w : Optional[np.ndarray], optional
        Weights for weighted least squares, by default None.

    ---------------------------------------------------------------------------

    参数
    ----------
    array_3D : np.ndarray
        输入的 3D 数组。
    neu_axis : int, optional
        执行回归的轴（0 或 1），默认为 1。
    w : Optional[np.ndarray], optional
        加权最小二乘的权重，默认为 None。

    ---------------------------------------------------------------------------

    Returns
    -------
    np.ndarray
        Array of regression parameters for each slice.

    ---------------------------------------------------------------------------

    返回
    -------
    np.ndarray
        每个切片的回归参数数组。

    ---------------------------------------------------------------------------
    """
    array_3D = array_3D.transpose(1, 0, 2) if neu_axis == 0 else array_3D
    parameters = []
    not_nans = filter_not_nans(array_3D)
    for i in prange(array_3D.shape[0]):
        params = __lstsq_without_w(array_3D[i], not_nans[i])
        parameters.append(params)
    parameters = np.array(parameters)
    return parameters


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
    """
    ===========================================================================

    Performs factor neutralization using linear regression.

    This function neutralizes a target DataFrame against specified factors,
    optionally over rolling periods.

    ---------------------------------------------------------------------------

    使用线性回归执行因子中性化。

    此函数根据指定因子对目标 DataFrame 进行中性化，可选择在滚动周期内进行。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    df_obj : pd.DataFrame
        The target DataFrame to be neutralized.
    const : bool, optional
        If True, includes a constant term in the regression, by default True.
    neu_axis : int, optional
        Axis along which to perform neutralization (0 for rows, 1 for columns),
        by default 1.
    periods : Optional[int], optional
        Rolling window size for neutralization, by default None (full data).
    flatten : bool, optional
        If True, flattens the rolling window data, by default False.
    w : Optional[np.ndarray], optional
        Weights for weighted regression, by default None.
    resid : bool, optional
        If True, returns residuals; otherwise, returns parameters, by default True.
    **key_dfs : pd.DataFrame
        Factor DataFrames for neutralization.

    ---------------------------------------------------------------------------

    参数
    ----------
    df_obj : pd.DataFrame
        要中性化的目标 DataFrame。
    const : bool, optional
        如果为 True，则在回归中包含常数项，默认为 True。
    neu_axis : int, optional
        执行中性化的轴（0 为行，1 为列），默认为 1。
    periods : Optional[int], optional
        中性化的滚动窗口大小，默认为 None（全数据）。
    flatten : bool, optional
        如果为 True，则展平滚动窗口数据，默认为 False。
    w : Optional[np.ndarray], optional
        加权回归的权重，默认为 None。
    resid : bool, optional
        如果为 True，则返回残差；否则返回参数，默认为 True。
    **key_dfs : pd.DataFrame
        用于中性化的因子 DataFrame。

    ---------------------------------------------------------------------------

    Returns
    -------
    Any
        A custom object containing regression parameters and/or residuals.

    ---------------------------------------------------------------------------

    返回
    -------
    Any
        包含回归参数和/或残差的自定义对象。

    ---------------------------------------------------------------------------
    """
    data_obj = _array_3D(df_obj, const, **key_dfs)
    values = data_obj.values

    if periods is not None:
        values = _array_roll(values, periods, flatten)
        if len(values.shape) == 4:
            if neu_axis == 0:
                values = values.transpose(0, 2, 1, 3)
                index = pd.MultiIndex.from_product([data_obj.index[periods - 1:], data_obj.columns], names=[df_obj.index.name, df_obj.columns.name])
            else:
                index = pd.MultiIndex.from_product([data_obj.index[periods - 1:], range(periods)], names=[df_obj.index.name, 'PERIOD'])
            values = values.reshape(values.shape[0] * values.shape[1], values.shape[2], values.shape[3])
        else:
            index = data_obj.index[periods - 1:]
    else:
        if neu_axis == 0:
            index = data_obj.columns
            columns = data_obj.index
            values = values.transpose(1, 0, 2)
        else:
            index = data_obj.index
            columns = data_obj.columns

    parameters = _lstsq(values, w=w)
    parameters = pd.DataFrame(parameters, index=index, columns=data_obj.labels[1:])

    class NeutralObj:
        def __init__(self, params, resid=None):
            self.params = params
            self.resid = resid

    if resid:
        if periods is None:
            resid_values = values[:, :, 0] - np.sum((values[:, :, 1:] * parameters.values[:, np.newaxis, :]), axis=-1)
            resid_df = pd.DataFrame(resid_values, index=index, columns=columns)
        else:
            resid_values = values[:, :, 0].astype(np.float16) - np.sum((values[:, :, 1:].astype(np.float16) * parameters.values[:, np.newaxis, :].astype(np.float16)), axis=-1)
            resid_df = pd.DataFrame(resid_values, index=index)
        return NeutralObj(params=parameters, resid=resid_df)
    else:
        return NeutralObj(params=parameters)        
        
        
        
        
def _array_3D(
    target_df: pd.DataFrame,
    const: bool = True,
    **kwargs: pd.DataFrame
) -> Any:
    """
    ===========================================================================

    Converts DataFrames into a 3D NumPy array for regression analysis.

    This function prepares data for multi-variate regression by stacking
    dependent and independent variables into a 3D array.

    ---------------------------------------------------------------------------

    将 DataFrame 转换为用于回归分析的 3D NumPy 数组。

    此函数通过将因变量和自变量堆叠到 3D 数组中来准备多元回归数据。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    target_df : pd.DataFrame
        The dependent variable DataFrame.
    const : bool, optional
        If True, adds a constant array, by default True.
    **kwargs : pd.DataFrame
        Independent variable DataFrames.

    ---------------------------------------------------------------------------

    参数
    ----------
    target_df : pd.DataFrame
        因变量 DataFrame。
    const : bool, optional
        如果为 True，则添加一个常数数组，默认为 True。
    **kwargs : pd.DataFrame
        自变量 DataFrame。

    ---------------------------------------------------------------------------

    Returns
    -------
    Any
        A custom object containing the 3D array and metadata.

    ---------------------------------------------------------------------------

    返回
    -------
    Any
        包含 3D 数组和元数据的自定义对象。

    ---------------------------------------------------------------------------
    """
    target_df = target_df.sort_index(axis=1).sort_index()
    dic = (
        {'target':target_df.values} 
        | ({'const': np.ones_like(target_df)} if const else {}) 
        | {i:j.reindex_like(target_df).values for i,j in kwargs.items()}
    )
    x = type('array_3D', 
             (), 
             {'index': target_df.index, 
              'columns': target_df.columns, 
              'labels': list(dic.keys()), 
              'values': np.array(list(dic.values())).transpose(1,2,0)
              }
    )
    return x


def _array_roll(
    array_3D: np.ndarray,
    periods: int,
    flatten: bool = False
) -> np.ndarray:
    """
    ===========================================================================

    Creates a rolling window view of a 3D NumPy array.

    This function generates a view of the input 3D array, where each element
    is a sub-array representing a rolling window.

    ---------------------------------------------------------------------------

    创建 3D NumPy 数组的滚动窗口视图。

    此函数生成输入 3D 数组的视图，其中每个元素都是表示滚动窗口的子数组。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    array_3D : np.ndarray
        The input 3D NumPy array.
    periods : int
        The size of the rolling window.
    flatten : bool, optional
        If True, flattens the windowed array, by default False.

    ---------------------------------------------------------------------------

    参数
    ----------
    array_3D : np.ndarray
        输入的 3D NumPy 数组。
    periods : int
        滚动窗口的大小。
    flatten : bool, optional
        如果为 True，则展平窗口数组，默认为 False。

    ---------------------------------------------------------------------------

    Returns
    -------
    np.ndarray
        The rolling window view of the array.

    ---------------------------------------------------------------------------

    返回
    -------
    np.ndarray
        数组的滚动窗口视图。

    ---------------------------------------------------------------------------
    """
    axis = 0
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
        
    