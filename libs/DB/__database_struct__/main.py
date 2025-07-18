# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 22:11:13 2025

@author: Porco Rosso
"""
from typing import Any, Dict

from libs.DB.__database_struct__.DuckDB import main as __DuckDB_CLASS__
from libs.DB.__database_struct__.MySQL import main as __MySQL_CLASS__
from libs.utils.functions import filter_class_attrs as __filter_class_attrs__
from local.login_info import SOURCE 
from libs.DB import config


class main():
    source = SOURCE
    __DB_CLASS_NAME__ = ['MySQL', 'DuckDB']
    __DB_CLASS_DIC__ = {i: globals()[f'__{i}_CLASS__'] for i in __DB_CLASS_NAME__}
    __DB_INSTANCE_DIC__ = {i: globals()[f'__{i}_CLASS__'](**__filter_class_attrs__(getattr(config, i))) for i in __DB_CLASS_NAME__}
    
    @classmethod
    def __call__(cls, **kwargs):
        cls.__DB_INSTANCE_DIC__[cls.source].__call__(**kwargs)
        
    @classmethod
    def __parameters__(cls, *args):
        return cls.__DB_INSTANCE_DIC__[cls.source].__parameters__(*args)
        
    @classmethod
    def __env_init__(cls):
        cls.__DB_INSTANCE_DIC__[cls.source].__env_init__()
        
    @classmethod
    def login_info(cls) -> Dict[str, Any]:
        return cls.__DB_INSTANCE_DIC__[cls.source].__login_info__
    
    @classmethod
    def schema_info(cls, **kwargs: Any) -> Any:
        return  cls.__DB_INSTANCE_DIC__[cls.source].__schema_info__(**kwargs)
    
    @classmethod
    def read(cls, **kwargs: Any) -> Any:
        return   cls.__DB_INSTANCE_DIC__[cls.source].__read__(**kwargs)
    
    @classmethod
    def command(cls, **kwargs: Any) -> Any:
        return  cls.__DB_INSTANCE_DIC__[cls.source].__command__(**kwargs)
    
    @classmethod
    def create_table(cls, **kwargs: Any) -> Any:
        return   cls.__DB_INSTANCE_DIC__[cls.source].__create_table__(**kwargs)
    
    @classmethod
    def drop_table(cls, **kwargs: Any) -> Any:
        return  cls.__DB_INSTANCE_DIC__[cls.source].__drop_table__(**kwargs)
    
    @classmethod
    def table_exist(cls, **kwargs: Any) -> Any:
        return  cls.__DB_INSTANCE_DIC__[cls.source].__table_exist__(**kwargs)
    
    @classmethod
    def write(cls, df_obj: Any, **kwargs: Any) -> Any:
        return  cls.__DB_INSTANCE_DIC__[cls.source].__write__(df_obj, **kwargs)