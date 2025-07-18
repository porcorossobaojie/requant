# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 12:54:41 2025

@author: Porco Rosso
"""

import pandas as pd
from typing import Literal, Any

from libs import db
from __pandas__.config import DB as DB_setting
setattr(pd, DB_setting.CLASS_NAME, db)

@pd.api.extensions.register_dataframe_accessor(DB_setting.CLASS_NAME)
class DB():
    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj
        
    def write(
        self, 
        if_exists: Literal['fail', 'replace', 'append'] = 'append', 
        index: bool = False, 
        log: bool = True, 
        **kwargs: Any
    ):
        db.write(self._obj, if_exists=if_exists, index=index, log=log, **kwargs)         
        














