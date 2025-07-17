# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 22:11:13 2025

@author: Porco Rosso
"""
import functools
import inspect
from typing import Any, Callable, Dict, List, Type

from libs.DB.__database_struct__.DuckDB import main as DuckDB
from libs.DB.__database_struct__.MySQL import main as MySQL
from libs.DB.config import DB_RECOMMAND_SOURCE
from libs.utils.functions import flatten_list


DATA_SOURCE_DICT: Dict[str, Any] = {
    'DuckDB': DuckDB(),
    'MySQL': MySQL()
}



class main(type('MainClassBase', (), DATA_SOURCE_DICT)):
    """
    ===========================================================================

    Main class that acts as a dynamic proxy to the underlying database sources.

    It uses a metaclass and a decorator to forward attribute and method calls
    to the currently active database instance specified by the `source` attribute.

    ---------------------------------------------------------------------------

    作为底层数据库源的动态代理的主类。

    它使用元类和装饰器将属性和方法调用转发到由 `source` 属性指定的
    当前活动的数据库实例。

    ---------------------------------------------------------------------------
    """
    source: str = DB_RECOMMAND_SOURCE

    def __init__(self, **kwargs) -> None:
        """
        ===========================================================================

        Initializes the main proxy instance.

        ---------------------------------------------------------------------------

        初始化主代理实例。

        ---------------------------------------------------------------------------
        """

        self.source = kwargs.pop('source', self.source)
        getattr(self, self.source).__init__(**kwargs)
        
    def __call__(self, **kwargs) -> None:
        """
        ===========================================================================

        Initializes the main proxy instance.

        ---------------------------------------------------------------------------

        初始化主代理实例。

        ---------------------------------------------------------------------------
        """
        getattr(self, self.source).__call__(**kwargs)
        
    def __getattr__(self, name: str) -> Any:
        if name == 'source':
            return super().__getattr__(name)
        else:
            return getattr(getattr(self, self.source), name)

    def __setattr__(self, name: str, value: Any) -> None:

        if name == 'source':
            super().__setattr__(name, value)
        else:
            getattr(self, self.source).__setattr__(name, value)

    @classmethod
    def __internal_attrs__(cls) -> List[str]:
        """
        ===========================================================================

        Returns a sorted list of all internal attributes from all data sources.

        Returns
        -------
        List[str]
            A list of internal attribute names.

        ---------------------------------------------------------------------------

        返回一个包含所有数据源的所有内部属性的排序列表。

        返回
        -------
        List[str]
            内部属性名称的列表。

        ---------------------------------------------------------------------------
        """
        attrs = [DATA_SOURCE_DICT[i].__internal_attrs__ for i in DATA_SOURCE_DICT]
        return sorted(flatten_list(attrs))

    @property
    def login_info(self) -> Dict[str, Any]:
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
        return getattr(self, self.source).__login_info__

    def schema_info(self, **kwargs: Any) -> Any:
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
        return getattr(self, self.source).__schema_info__(**kwargs)

    def read(self, **kwargs: Any) -> Any:
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
        return getattr(self, self.source).__read__(**kwargs)

    def command(self, **kwargs: Any) -> Any:
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
        return getattr(self, self.source).__command__(**kwargs)

    def create_table(self, **kwargs: Any) -> Any:
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
        return getattr(self, self.source).__create_table__(**kwargs)

    def drop_table(self, **kwargs: Any) -> Any:
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
        return getattr(self, self.source).__drop_table__(**kwargs)

    def table_exist(self, **kwargs: Any) -> Any:
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
        return getattr(self, self.source).__table_exist__(**kwargs)

    def write(self, df_obj: Any, **kwargs: Any) -> Any:
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
        return getattr(self, self.source).__write__(df_obj, **kwargs)

    def __repr__(self) -> str:
        """
        ===========================================================================

        Returns a string representation of the DB source and login info.

        Returns
        -------
        str
            The string representation.

        ---------------------------------------------------------------------------

        返回数据库源和登录信息的字符串表示形式。

        返回
        -------
        str
            字符串表示形式。

        ---------------------------------------------------------------------------
        """
        login_info_str = str({i:j for i,j in self.login_info.items() if i in ['path', 'file', 'database', 'schema','table', 'columns', 'user', 'password']})[1:-1].replace("'", '')
        sorted_info = ', \n'.join(sorted(login_info_str.split(', ')))
        return f'DB source: {self.source}, \n{sorted_info}'
