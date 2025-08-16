# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:18:48 2025

@author: Porco Rosso

"""

# Standard library imports

# Third-party library imports
import pandas as pd

# Local project-specific imports
from libs.utils.finance.analysis.main import maxdown, sharpe, effective, expose
from libs.__pandas__.config import ANALYSIS as config

@pd.api.extensions.register_series_accessor(config.CLASS_NAME)
class main():
    def __init__(self, pandas_obj: pd.Series):
        self._obj = pandas_obj
        
    def maxdown(
        self, 
        iscumprod: bool = False
    ) -> pd.DataFrame:
        series = maxdown(self._obj.to_frame(), iscumprod=iscumprod)
        return series

    def sharpe(
        self, 
        iscumprod: bool = False, 
        periods: int = 252
    ) -> pd.Series:
        series = sharpe(self._obj.to_frame(), iscumprod, periods)        
        return series
    
@pd.api.extensions.register_dataframe_accessor(config.CLASS_NAME)
class main():
    def __init__(self, pandas_obj: pd.Series):
        self._obj = pandas_obj
        
    def maxdown(
        self, 
        iscumprod: bool = False
    ) -> pd.DataFrame:
        df = maxdown(self._obj.to_frame(), iscumprod=iscumprod)
        return df

    def sharpe(
        self, 
        iscumprod: bool = False, 
        periods: int = 252
    ) -> pd.DataFrame:
        df = sharpe(self._obj.to_frame(), iscumprod, periods)        
        return df

    def effective(self, df_obj):
        df = effective(self._obj)
        return df
    
    def expose(self, weight=None, standard_method='uniform', *unnamed_factors, **named_factors):
        df = expose(self._obj, weight, standard_method, *unnamed_factors, **named_factors)
        return df    













        