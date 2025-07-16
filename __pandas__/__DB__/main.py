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
        """
        ===========================================================================

        Writes the DataFrame to MySQL. 
        Uses recommended parameters if they are not provided.

        Parameters
        ----------
        if_exists : str, {'fail', 'replace', 'append'}
            How to behave if the table already exists. Defaults to 'append'.
        index : bool
            Write DataFrame index as a column. Defaults to False.
        log : bool
            Log information if the write operation succeeds in MySQL. Defaults to False.
        **kwargs : Any
            Additional keyword arguments for database connection.

        Returns
        -------
        None.

        ---------------------------------------------------------------------------

        将 DataFrame 写入 MySQL。
        如果未提供参数，则使用推荐参数。

        参数
        ----------
        if_exists : str, {'fail', 'replace', 'append'}
            如果表已存在，如何操作。默认为“追加”。
        index : bool
            将DataFrame索引写为一列。默认为 False。
        log : bool
            如果写入操作在MySQL中成功，则记录信息。默认为 False。
        **kwargs : Any
            用于数据库连接的其他关键字参数。

        返回
        -------
        无。

        ---------------------------------------------------------------------------
        """
        DB_CLASS.write(self._obj, if_exists=if_exists, index=index, log=log, **kwargs)         
        














