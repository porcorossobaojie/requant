# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:12:37 2025

@author: Porco Rosso

"""
from libs.utils.finance.build.main import group, weight, portfolio, cut

from __pandas__.config import build as config
import pandas as pd
from typing import Optional, Dict, Any, List, Union
import numpy as np


@pd.api.extensions.register_dataframe_accessor(config.CLASS_NAME)
class main():
    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj
    
    def group(
        self, 
        rule: Optional[Union[Dict, List]] = None, 
        pct: bool = True, 
        order: bool = False, 
        nlevels: Optional[Any] = None, 
    ) -> pd.DataFrame:    
        rule = np.linspace(0,1,11).round(2) if rule is None else rule
        df = group(self._obj, rule=rule, pct=pct, order=order, nlevels=nlevels)
        return df
    
    def weight(
        self, 
        w_df: Optional[pd.DataFrame] = None, 
        fillna: bool = True, 
        pct: bool = True, 
    ) -> pd.DataFrame:        
        return weight(self._obj, w_df=w_df, fillna=fillna, pct=pct)        
        
    def portfolio(
        self, 
        returns: pd.DataFrame, 
        weight: Optional[pd.DataFrame] = None, 
        shift: int = 1, 
        roll: int = 1, 
        fillna: bool = True
    ) -> pd.DataFrame:    
        return portfolio(self._obj, returns=returns, weight=weight, shift=shift, roll=roll, fillna=fillna)
        
    def cut(
        self, 
        right: Union[int, float], 
        rng_right: Union[int, float] = 0, 
        left: Union[int, float] = 0, 
        rng_left: Union[int, float] = 0, 
        pct: bool = False, 
        ascending: bool = False
    ) -> pd.DataFrame:    
        return cut(self._obj, left, right, rng_left, rng_right, pct, ascending)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    