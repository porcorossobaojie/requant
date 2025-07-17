# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 12:54:41 2025

@author: Porco Rosso
"""

import pandas as pd
from typing import Literal, Any

from __pandas__.config import __DB__ as DB_setting
from local.login_info import DB_LOGIN_INFO, SOURCE
from libs.utils.functions import filter_class_attrs
from libs.DB import __DB_CLASS__ as DB_CLASS

DB_CLASS = DB_CLASS(source=SOURCE)
local_config = filter_class_attrs(DB_LOGIN_INFO)
[setattr(DB_CLASS, i, getattr(DB_CLASS, i)(filter_class_attrs(j))) for i,j in filter_class_attrs(DB_LOGIN_INFO).items()]
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
        














