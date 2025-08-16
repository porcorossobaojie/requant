# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:18:48 2025

@author: Porco Rosso

"""
import pandas as pd
from typing import Union, List, Any

from libs.__pandas__.config import TOOLS as config
from libs.utils.finance.tools.main import fillna, shift, log

@pd.api.extensions.register_dataframe_accessor(config.CLASS_NAME)
class main():
    def __init__(self, pandas_obj: pd.Series):
        self._obj = pandas_obj
        
    def fillna(
        self, 
        fill_list: List[Any]
    ) -> pd.DataFrame:

        return fillna(self._obj, fill_list)

    def shift(
        self, 
        n: int = 1
    ) -> pd.DataFrame:
        return shift(self._obj, n)
    
    def log(
        self, 
        bias_adj: Union[int, float] = 1, 
        abs_adj: bool = True
    ) -> pd.DataFrame:    
    
        return log(self._obj, bias_adj, abs_adj)

    








