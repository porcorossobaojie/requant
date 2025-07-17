# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 12:54:41 2025

@author: Porco Rosso
"""

import pandas as pd
from typing import Literal, Any

from __pandas__.config import DB as DB_setting
from __pandas__.local import DB as local_config
from libs.utils.functions import filter_class_attrs
from libs.DB import DB as DB_CLASS

DB_CLASS = DB_CLASS()
local_config = filter_class_attrs(local_config)
[setattr(DB_CLASS, i, getattr(DB_CLASS, i)(filter_class_attrs(j))) for i,j in local_config.items()]
DB_CLASS.source = DB_setting.RECOMMAND_SOURCE
setattr(pd, DB_setting.CLASS_NAME, DB_CLASS)

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
        DB_CLASS.write(self._obj, if_exists=if_exists, index=index, log=log, **kwargs)         
        














