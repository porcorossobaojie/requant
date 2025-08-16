# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:18:48 2025

@author: Porco Rosso

"""

from libs.utils.finance.stats.main import standard, OLS, neutral, const
from libs.utils.finance.build.dev import neutral as neutral_dev
from libs.__pandas__.config import STATS as config

import numpy as np
import pandas as pd
import statsmodels.api as sm
from typing import Optional, Union, Tuple, List, Dict, Any, Callable

@pd.api.extensions.register_series_accessor(config.CLASS_NAME)
class main():
    def __init__(self, pandas_obj: pd.Series):
        self._obj = pandas_obj
        
    def standard(
        self, 
        method: str = 'gauss', 
        rank: Tuple[Optional[float], Optional[float]] = (-5,5)
    ) -> pd.Series:        
        
        return standard(self._obj, method=method, rank=rank, axis=None)
        
    def const(
        self, 
        prefix: Optional[str] = None, 
        sep: str = ''
    ) -> pd.DataFrame:        
        return const(self._obj, prefix=prefix, sep=sep)
        

@pd.api.extensions.register_dataframe_accessor(config.CLASS_NAME)
class main():        
    def __init__(self, pandas_obj: pd.Series):
        self._obj = pandas_obj

    def standard(
        self, 
        method: str = 'gauss', 
        rank: Tuple[Optional[float], Optional[float]] = (-5,5), 
        axis: int = 1
    ) -> pd.DataFrame:
        x = standard(self._obj, method=method, rank=rank, axis=axis)
        return x
        
    def const(
        self, 
        columns: Optional[List[Any]] = None, 
        prefix: Optional[Union[str, List[str]]] = None, 
        sep: str = ''
    ) -> pd.DataFrame:        
        return const(self._obj, columns=columns, prefix=prefix, sep=sep)
        
    def OLS(
        self, 
        const: bool = True, 
        roll: Optional[int] = None, 
        min_periods: Optional[int] = None, 
        dropna: bool = True, 
        keys: Tuple[int, int] = (0, -1), 
        returns: type = list, 
        weight: Optional[pd.DataFrame] = None
    ) -> Union[Dict[Any, sm.regression.linear_model.RegressionResultsWrapper], List[sm.regression.linear_model.RegressionResultsWrapper]]:
        
        return OLS(self._obj, const=const, roll=roll, min_periods=min_periods, dropna=dropna, keys=keys, returns=returns, weight=weight)
          
    def neutral(
        self, 
        const: bool = True, 
        neu_axis: int = 1, 
        periods: Optional[int] = None, 
        flatten: bool = False,  
        weight: Optional[np.ndarray] = None, 
        resid: bool = True, 
        **key_dfs: pd.DataFrame
    ) -> Any:
        return neutral(self._obj, const=const, neu_axis=neu_axis, periods=periods, flatten=flatten, w=weight, resid=resid, **key_dfs)
        
    def neutral_dev(
        self, 
        const: bool = True, 
        neu_axis: int = 1, 
        periods: Optional[int] = None, 
        flatten: bool = False,  
        resid: bool = True, 
        **key_dfs: pd.DataFrame
    ) -> Any:
        return neutral_dev(self._obj, const=const, neu_axis=neu_axis, periods=periods, flatten=flatten, resid=resid, **key_dfs)
        
        
        
        
        