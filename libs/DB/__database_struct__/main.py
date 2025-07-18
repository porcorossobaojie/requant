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
    """
    ===========================================================================

    Main class for database operations, acting as a facade for different database types.

    This class dynamically dispatches calls to the appropriate database implementation
    (MySQL or DuckDB) based on the configured source.

    ---------------------------------------------------------------------------

    数据库操作的主类，作为不同数据库类型的门面。

    此类根据配置的源动态地将调用分派给相应的数据库实现（MySQL 或 DuckDB）。

    ---------------------------------------------------------------------------
    """
    source = SOURCE
    __DB_CLASS_NAME__ = ['MySQL', 'DuckDB']
    __DB_CLASS_DIC__ = {
        i: globals()[f'__{i}_CLASS__'] for i in __DB_CLASS_NAME__
    }
    __DB_INSTANCE_DIC__ = {
        i: globals()[f'__{i}_CLASS__'](
            **__filter_class_attrs__(getattr(config, i))
        ) for i in __DB_CLASS_NAME__
    }
    
    @classmethod
    def __call__(cls, **kwargs):
        """
        ===========================================================================

        Calls the __call__ method of the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        **kwargs : Any
            Keyword arguments to be passed to the underlying database's __call__ method.

        ---------------------------------------------------------------------------

        调用活动数据库实例的 __call__ 方法。

        参数
        ----------
        cls : type
            类本身。
        **kwargs : Any
            要传递给底层数据库的 __call__ 方法的关键字参数。

        ---------------------------------------------------------------------------
        """
        cls.__DB_INSTANCE_DIC__[cls.source].__call__(**kwargs)
        
    @classmethod
    def __parameters__(cls, *args):
        """
        ===========================================================================

        Retrieves parameters from the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        *args : Any
            Arguments to be passed to the underlying database's __parameters__ method.

        Returns
        -------
        Any
            The parameters retrieved from the database instance.

        ---------------------------------------------------------------------------

        从活动数据库实例中检索参数。

        参数
        ----------
        cls : type
            类本身。
        *args : Any
            要传递给底层数据库的 __parameters__ 方法的参数。

        返回
        -------
        Any
            从数据库实例中检索到的参数。

        ---------------------------------------------------------------------------
        """
        return cls.__DB_INSTANCE_DIC__[cls.source].__parameters__(*args)
        
    @classmethod
    def __env_init__(cls):
        """
        ===========================================================================

        Initializes the environment for the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.

        ---------------------------------------------------------------------------

        初始化活动数据库实例的环境。

        参数
        ----------
        cls : type
            类本身。

        ---------------------------------------------------------------------------
        """
        cls.__DB_INSTANCE_DIC__[cls.source].__env_init__()
        
    @classmethod
    def login_info(cls) -> Dict[str, Any]:
        """
        ===========================================================================

        Retrieves login information from the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing login information.

        ---------------------------------------------------------------------------

        从活动数据库实例中检索登录信息。

        参数
        ----------
        cls : type
            类本身。

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

        Retrieves schema information from the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        **kwargs : Any
            Keyword arguments to be passed to the underlying database's __schema_info__ method.

        Returns
        -------
        Any
            The schema information retrieved from the database instance.

        ---------------------------------------------------------------------------

        从活动数据库实例中检索模式信息。

        参数
        ----------
        cls : type
            类本身。
        **kwargs : Any
            要传递给底层数据库的 __schema_info__ 方法的关键字参数。

        返回
        -------
        Any
            从数据库实例中检索到的模式信息。

        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__schema_info__(**kwargs)
    
    @classmethod
    def read(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================

        Reads data from the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        **kwargs : Any
            Keyword arguments to be passed to the underlying database's __read__ method.

        Returns
        -------
        Any
            The data read from the database instance.

        ---------------------------------------------------------------------------

        从活动数据库实例中读取数据。

        参数
        ----------
        cls : type
            类本身。
        **kwargs : Any
            要传递给底层数据库的 __read__ 方法的关键字参数。

        返回
        -------
        Any
            从数据库实例中读取的数据。

        ---------------------------------------------------------------------------
        """
        return   cls.__DB_INSTANCE_DIC__[cls.source].__read__(**kwargs)
    
    @classmethod
    def command(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================

        Executes a command on the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        **kwargs : Any
            Keyword arguments to be passed to the underlying database's __command__ method.

        Returns
        -------
        Any
            The result of the command execution.

        ---------------------------------------------------------------------------

        在活动数据库实例上执行命令。

        参数
        ----------
        cls : type
            类本身。
        **kwargs : Any
            要传递给底层数据库的 __command__ 方法的关键字参数。

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

        Creates a table in the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        **kwargs : Any
            Keyword arguments to be passed to the underlying database's __create_table__ method.

        Returns
        -------
        Any
            The result of the table creation operation.

        ---------------------------------------------------------------------------

        在活动数据库实例中创建表。

        参数
        ----------
        cls : type
            类本身。
        **kwargs : Any
            要传递给底层数据库的 __create_table__ 方法的关键字参数。

        返回
        -------
        Any
            表创建操作的结果。

        ---------------------------------------------------------------------------
        """
        return   cls.__DB_INSTANCE_DIC__[cls.source].__create_table__(**kwargs)
    
    @classmethod
    def drop_table(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================

        Drops a table in the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        **kwargs : Any
            Keyword arguments to be passed to the underlying database's __drop_table__ method.

        Returns
        -------
        Any
            The result of the table dropping operation.

        ---------------------------------------------------------------------------

        在活动数据库实例中删除表。

        参数
        ----------
        cls : type
            类本身。
        **kwargs : Any
            要传递给底层数据库的 __drop_table__ 方法的关键字参数。

        返回
        -------
        Any
            表删除操作的结果。

        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__drop_table__(**kwargs)
    
    @classmethod
    def table_exist(cls, **kwargs: Any) -> Any:
        """
        ===========================================================================

        Checks if a table exists in the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        **kwargs : Any
            Keyword arguments to be passed to the underlying database's __table_exist__ method.

        Returns
        -------
        Any
            The result of the table existence check.

        ---------------------------------------------------------------------------

        检查活动数据库实例中是否存在表。

        参数
        ----------
        cls : type
            类本身。
        **kwargs : Any
            要传递给底层数据库的 __table_exist__ 方法的关键字参数。

        返回
        -------
        Any
            表存在性检查的结果。

        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__table_exist__(**kwargs)
    
    @classmethod
    def write(cls, df_obj: Any, **kwargs: Any) -> Any:
        """
        ===========================================================================

        Writes data to the active database instance.

        Parameters
        ----------
        cls : type
            The class itself.
        df_obj : Any
            The DataFrame object to write.
        **kwargs : Any
            Keyword arguments to be passed to the underlying database's __write__ method.

        Returns
        -------
        Any
            The result of the data writing operation.

        ---------------------------------------------------------------------------

        将数据写入活动数据库实例。

        参数
        ----------
        cls : type
            类本身。
        df_obj : Any
            要写入的 DataFrame 对象。
        **kwargs : Any
            要传递给底层数据库的 __write__ 方法的关键字参数。

        返回
        -------
        Any
            数据写入操作的结果。

        ---------------------------------------------------------------------------
        """
        return  cls.__DB_INSTANCE_DIC__[cls.source].__write__(df_obj, **kwargs)