# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 17:58:28 2025

@author: Porco Rosso

"""

import pandas as pd
from __pandas__.config import FACTORIZE
from flow.__factorize__.main import be_list, not_st, members, label, info, shift, sinfo

@pd.api.extensions.register_dataframe_accessor(FACTORIZE.CLASS_NAME)
class factorize():
    def __init__(self, df_obj):
        self._obj = df_obj
        
    def be_list(self, limit=None, inplace=True):
        x = be_list(self._obj, limit=limit, inplace=inplace)
        return x
    
    def not_st(self, limit=0, inplace=True):
        x = not_st(self._obj, limit=limit, inplace=inplace)
        return x
    
    def members(self, name, inplace=True):
        x = members(self._obj, name=name, inplace=inplace)
        return x
    
    def label(self, *key, **label_df):
        x = label(self._obj, *key, **label_df)
        return x
    
    def info(self, key):
        x = info(self._obj, key)
        return x
    
    def corr(self):
        x = self._obj.corrwith(self._obj.shift(), axis=1).describe()
        return x
        
@pd.api.extensions.register_series_accessor(FACTORIZE.CLASS_NAME)
class factorize():
    def __init__(self, df_obj):
        self._obj = df_obj
        
    def shift(self, n=0):
        x = shift(self._obj, n=n, copy=True)
        return x
    
    def info(self, key):
        x = sinfo(self._obj, key)
        return x
            
    
    
