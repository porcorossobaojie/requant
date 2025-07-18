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
        """
        ===========================================================================
    
        Returns the login information of the current active source.
    
        Returns
        -------
        Dict[str, Any]
            A dictionary containing login info.
    
        ---------------------------------------------------------------------------
    
        返回当前活动源的登录信息。
    
        返回
        -------
        Dict[str, Any]
            包含登录信息的字典。
    
        ---------------------------------------------------------------------------
        """
        return cls.__DB_INSTANCE_DIC__[cls.source].__login_info__
    
    @classmethod
    def schema_info(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================
    
        Retrieves schema information from the active database source.
    
        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments to pass to the underlying schema info method.
    
        Returns
        -------
        Any
            The schema information.
    
        ---------------------------------------------------------------------------
    
        从活动数据库源检索模式信息。
    
        参数
        ----------
        **kwargs : Any
            传递给底层模式信息方法的额外关键字参数。
    
        返回
        -------
        Any
            模式信息。
    
        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__schema_info__(**kwargs)
    
    @classmethod
    def read(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================
    
        Reads data from the active database source.
    
        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments to pass to the underlying read method.
    
        Returns
        -------
        Any
            The data read from the database.
    
        ---------------------------------------------------------------------------
    
        从活动数据库源读取数据。
    
        参数
        ----------
        **kwargs : Any
            传递给底层读取方法的额外关键字参数。
    
        返回
        -------
        Any
            从数据库读取的数据。
    
        ---------------------------------------------------------------------------
        """
        return   cls.__DB_INSTANCE_DIC__[cls.source].__read__(**kwargs)
    
    @classmethod
    def command(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================
    
        Executes a command on the active database source.
    
        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments to pass to the underlying command method.
    
        Returns
        -------
        Any
            The result of the command execution.
    
        ---------------------------------------------------------------------------
    
        在活动数据库源上执行命令。
    
        参数
        ----------
        **kwargs : Any
            传递给底层命令方法的额外关键字参数。
    
        返回
        -------
        Any
            命令执行的结果。
    
        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__command__(**kwargs)
    
    @classmethod
    def create_table(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================
    
        Creates a table in the active database source.
    
        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments to pass to the underlying create table method.
    
        Returns
        -------
        Any
            The result of the table creation operation.
    
        ---------------------------------------------------------------------------
    
        在活动数据库源中创建表。
    
        参数
        ----------
        **kwargs : Any
            传递给底层创建表方法的额外关键字参数。
    
        返回
        -------
        Any
            创建表操作的结果。
    
        ---------------------------------------------------------------------------
        """
        return   cls.__DB_INSTANCE_DIC__[cls.source].__create_table__(**kwargs)
    
    @classmethod
    def drop_table(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================
    
        Drops a table from the active database source.
    
        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments to pass to the underlying drop table method.
    
        Returns
        -------
        Any
            The result of the table drop operation.
    
        ---------------------------------------------------------------------------
    
        从活动数据库源中删除表。
    
        参数
        ----------
        **kwargs : Any
            传递给底层删除表方法的额外关键字参数。
    
        返回
        -------
        Any
            删除表操作的结果。
    
        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__drop_table__(**kwargs)
    
    @classmethod
    def table_exist(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================
    
        Checks if a table exists in the active database source.
    
        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments to pass to the underlying table exist method.
    
        Returns
        -------
        Any
            True if the table exists, False otherwise.
    
        ---------------------------------------------------------------------------
    
        检查活动数据库源中是否存在表。
    
        参数
        ----------
        **kwargs : Any
            传递给底层表存在方法的额外关键字参数。
    
        返回
        -------
        Any
            如果表存在则为 True，否则为 False。
    
        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__table_exist__(**kwargs)
    
    @classmethod
    def write(cls, df_obj: Any, **kwargs: Any) -> Any:
        """
        ===========================================================================
    
        Writes a DataFrame object to the active database source.
    
        Parameters
        ----------
        df_obj : Any
            The DataFrame object to write.
        **kwargs : Any
            Additional keyword arguments to pass to the underlying write method.
    
        Returns
        -------
        Any
            The result of the write operation.
    
        ---------------------------------------------------------------------------
    
        将 DataFrame 对象写入活动数据库源。
    
        参数
        ----------
        df_obj : Any
            要写入的 DataFrame 对象。
        **kwargs : Any
            传递给底层写入方法的额外关键字参数。
    
        返回
        -------
        Any
            写入操作的结果。
    
        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__write__(df_obj, **kwargs)
    
    
