# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 12:54:41 2025

@author: Porco Rosso
"""

# Standard library imports
from typing import Any, Literal

# Third-party library imports
import pandas as pd

# Local project-specific imports
from libs import db
from libs.__pandas__.config import DB as DB_setting

setattr(pd, DB_setting.CLASS_NAME, db)

@pd.api.extensions.register_dataframe_accessor(DB_setting.CLASS_NAME)
class main:
    """
    ===========================================================================

    DataFrame accessor for database write operations.

    This class extends Pandas DataFrames with a `db` accessor, allowing
    for convenient writing of DataFrame content to a database.

    ---------------------------------------------------------------------------

    用于数据库写入操作的 DataFrame 访问器。

    此类通过 `db` 访问器扩展 Pandas DataFrame，方便地将 DataFrame 内容
    写入数据库。

    ---------------------------------------------------------------------------
    """
    def __init__(self, pandas_obj: pd.DataFrame):
        """
        ===========================================================================

        Initializes the DB accessor with a Pandas DataFrame object.

        Parameters
        ----------
        pandas_obj : pd.DataFrame
            The Pandas DataFrame instance to which this accessor is attached.

        ---------------------------------------------------------------------------

        使用 Pandas DataFrame 对象初始化 DB 访问器。

        参数
        ----------
        pandas_obj : pd.DataFrame
            此访问器所附加的 Pandas DataFrame 实例。

        ---------------------------------------------------------------------------
        """
        self._obj: pd.DataFrame = pandas_obj

    def write(
        self,
        if_exists: Literal['fail', 'replace', 'append'] = 'append',
        index: bool = False,
        log: bool = True,
        **kwargs: Any
    ) -> None:
        """
        ===========================================================================

        Writes the DataFrame to the database.

        This method wraps the `db.write` function, providing a convenient way
        to persist the DataFrame's data.

        Parameters
        ----------
        if_exists : Literal['fail', 'replace', 'append'], default 'append'
            How to behave if the table already exists.
            - 'fail': Raise a ValueError.
            - 'replace': Drop the table before inserting new data.
            - 'append': Insert new data into the existing table.
        index : bool, default False
            Whether to write the DataFrame's index as a column.
        log : bool, default True
            Whether to log the write operation.
        **kwargs : Any
            Additional keyword arguments to pass to the underlying `db.write` function.

        ---------------------------------------------------------------------------

        将 DataFrame 写入数据库。

        此方法封装了 `db.write` 函数，提供了一种方便的方式来持久化 DataFrame 的数据。

        参数
        ----------
        if_exists : Literal['fail', 'replace', 'append'], 默认为 'append'
            如果表已存在，如何处理。
            - 'fail': 抛出 ValueError。
            - 'replace': 在插入新数据之前删除表。
            - 'append': 将新数据插入到现有表中。
        index : bool, 默认为 False
            是否将 DataFrame 的索引作为一列写入。
        log : bool, 默认为 True
            是否记录写入操作。
        **kwargs : Any
            传递给底层 `db.write` 函数的额外关键字参数。

        ---------------------------------------------------------------------------
        """
        db.write(self._obj, if_exists=if_exists, index=index, log=log, **kwargs)         
        














