# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:36:49 2025

@author: Porco Rosso

"""

import inspect
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Tuple

import pandas as pd
import pymysql
from numpy import isreal
from sqlalchemy import Engine, create_engine

from libs.DB.__data_type__.main import main as data_trans
from libs.DB.__database_struct__.meta import main as meta
from libs.utils.functions import filter_class_attrs


class main(meta):
    """
    ===========================================================================

    Main class for MySQL database operations.

    This class provides methods for interacting with a MySQL database,
    including environment initialization, command execution, data reading,
    and table management.

    ---------------------------------------------------------------------------

    MySQL 数据库操作的主类。

    此类提供与 MySQL 数据库交互的方法，包括环境初始化、命令执行、数据读取和表管理。

    ---------------------------------------------------------------------------
    """
    __data_trans__ = data_trans('MySQL')
    __internal_attrs__ = []
    
    def __init__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Initializes the MySQL main class.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Keyword arguments to set internal attributes.

        ---------------------------------------------------------------------------

        初始化 MySQL 主类。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            用于设置内部属性的关键字参数。

        ---------------------------------------------------------------------------
        """
        self.__internal_attrs__ = list(
            set(self.__internal_attrs__) | set(kwargs.keys())
        )
        [setattr(self, i, j) for i, j in kwargs.items()]

    def __env_init__(self, schema: Optional[str] = None) -> None:
        """
        ===========================================================================

        Initializes the database environment by creating a schema if it doesn't exist.

        Parameters
        ----------
        self : object
            The instance of the class.
        schema : Optional[str], optional
            The schema name to create, by default None. If None, uses the instance's schema.

        ---------------------------------------------------------------------------

        通过创建模式（如果不存在）来初始化数据库环境。

        参数
        ----------
        self : object
            类的实例。
        schema : Optional[str], optional
            要创建的模式名称，默认为 None。如果为 None，则使用实例的模式。

        ---------------------------------------------------------------------------
        """
        schema = self.schema if schema is None else schema
        self.__command__(f'CREATE SCHEMA IF NOT EXISTS {schema}')

    def __engine__(
        self,
        **kwargs: Any
    ) -> Engine:
        """
        ===========================================================================

        Establishes a connection to the MySQL database.

        Parameters
        ----------
        self : object
            The instance of the class.
        schema : str
            The database schema to connect to.
        **kwargs : Any
            Keyword arguments for database connection parameters.

        Returns
        -------
        Engine
            A SQLAlchemy Engine object for the MySQL database.

        ---------------------------------------------------------------------------

        建立与 MySQL 数据库的连接。

        参数
        ----------
        self : object
            类的实例。
        schema : str
            要连接的数据库模式。
        **kwargs : Any
            数据库连接参数的关键字参数。

        返回
        -------
        Engine
            MySQL 数据库的 SQLAlchemy Engine 对象。

        ---------------------------------------------------------------------------
        """
        parameters = self.__parameters__(kwargs)
        connection_string = self.__URL__(**parameters)
        engine = create_engine(connection_string)
        return engine

    def __command__(self, command: str, **kwargs: Any) -> Tuple:
        """
        ===========================================================================

        Executes a SQL command on the MySQL database.

        Parameters
        ----------
        self : object
            The instance of the class.
        command : str
            The SQL command to execute.
        **kwargs : Any
            Additional keyword arguments for the command execution.

        Returns
        -------
        Tuple
            The result of the command execution.

        ---------------------------------------------------------------------------

        在 MySQL 数据库上执行 SQL 命令。

        参数
        ----------
        self : object
            类的实例。
        command : str
            要执行的 SQL 命令。
        **kwargs : Any
            命令执行的额外关键字参数。

        返回
        -------
        Tuple
            命令执行的结果。

        ---------------------------------------------------------------------------
        """
        parameters = self.__parameters__(kwargs)
        pymysql_keys = ['host', 'port', 'user', 'password', 'charset']
        pymysql_parameters = {i: parameters[i] for i in pymysql_keys}
        pymysql_parameters['db'] = parameters['schema']

        con = pymysql.connect(**pymysql_parameters)
        cur = con.cursor()
        cur.execute(command)
        x = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return x

    def __columns_connect__(
        self,
        columns_obj: Any,
        type_position: Optional[int] = None,
        comment_position: Optional[int] = None
    ) -> str:
        """
        ===========================================================================

        Connects and formats column information for MySQL.

        Parameters
        ----------
        self : object
            The instance of the class.
        columns_obj : Any
            Column object, can be None, string, list, or dictionary.
        type_position : Optional[int], optional
            Position of the type in the column object, by default None.
        comment_position : Optional[int], optional
            Position of the comment in the column object, by default None.

        Returns
        -------
        str
            Formatted column information as a string.

        ---------------------------------------------------------------------------

        连接并格式化 MySQL 的列信息。

        参数
        ----------
        self : object
            类的实例。
        columns_obj : Any
            列对象，可以是 None、字符串、列表或字典。
        type_position : Optional[int], optional
            列对象中类型的位置，默认为 None。
        comment_position : Optional[int], optional
            列对象中注释的位置，默认为 None。

        返回
        -------
        str
            格式化的列信息字符串。

        ---------------------------------------------------------------------------
        """
        if columns_obj is None:
            x = '*'    
        elif isinstance(columns_obj, str):
            x = columns_obj
        elif isinstance(columns_obj, list):
            x = ', '.join([str(i) for i in columns_obj])
        elif isinstance(columns_obj, dict):
            type_position = 0 if type_position is None else type_position
            comment_position = 1 if comment_position is None else comment_position
            x = {}
            for i, j in columns_obj.items():
                x[i] = [
                    self.__data_trans__(j[type_position].upper()),
                    '' if len(j) == 1 else j[comment_position]
                ]
            x = ', \n'.join(
                [f'`{i}` {j[0]} DEFAULT NULL COMMENT "{j[1]}"' for i, j in x.items()]
            )
        return x

    def __read__(
        self,
        chunksize: Optional[int] = None,
        log: bool = False,
        show_time: bool = False,
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Reads data from the MySQL database.

        Parameters
        ----------
        self : object
            The instance of the class.
        chunksize : Optional[int], optional
            Number of rows to read at a time, by default None.
        log : bool, optional
            Whether to log the SQL command, by default False.
        show_time : bool, optional
            Whether to show the execution time, by default False.
        **kwargs : Any
            Additional keyword arguments for query parameters.

        Returns
        -------
        pd.DataFrame
            The read data as a pandas DataFrame.

        ---------------------------------------------------------------------------

        从 MySQL 数据库读取数据。

        参数
        ----------
        self : object
            类的实例。
        chunksize : Optional[int], optional
            每次读取的行数，默认为 None。
        log : bool, optional
            是否记录 SQL 命令，默认为 False。
        show_time : bool, optional
            是否显示执行时间，默认为 False。
        **kwargs : Any
            查询参数的额外关键字参数。

        返回
        -------
        pd.DataFrame
            读取的数据作为 pandas DataFrame。

        ---------------------------------------------------------------------------
        """
        args = inspect.getargvalues(inspect.currentframe())
        args = {i: args.locals[i] for i in args.args if i != 'self'}
        parameters = self.__parameters__(args, kwargs)
        schema = kwargs.get('schema', getattr(self, 'schema', None))
        table = kwargs.get('table', getattr(self, 'table', None))

        @self.__timing_decorator__(
            schema=schema, table=table, show_time=show_time
        )
        def wraps_function() -> pd.DataFrame:
            columns = parameters.get('columns', None)
            columns = list(columns.keys()) if isinstance(columns, dict) else columns
            columns = self.__columns_connect__(columns)

            parameters['columns'] = columns

            sql_command = 'SELECT {columns} FROM {schema}.{table}'.format(**parameters)
            if parameters.get('where', None) is not None:
                sql_command = '{} WHERE {where}'.format(sql_command, **parameters)

            if log:
                print(sql_command)

            engine = self.__engine__(**parameters)

            if parameters.get('chunksize', None) is not None:
                offset = 0
                chunks = []
                while True:
                    order_params = {
                        **parameters,
                        'offset': offset,
                        'sql_command': sql_command
                    }
                    order = ('{sql_command} LIMIT {chunksize} OFFSET {offset}').format_map(order_params)
                    obj = pd.read_sql(order, con=engine)
                    chunks.append(obj)
                    if len(obj) < parameters.get('chunksize', 1):
                        break
                    else:
                        offset += parameters.get('chunksize', 1)
                return pd.concat(chunks)
            else:
                return pd.read_sql(sql_command, con=engine)
        return wraps_function()

    def __schema_info__(self, **kwargs: Any) -> pd.DataFrame:
        info_params = {
            'schema': 'INFORMATION_SCHEMA',
            'table': 'COLUMNS',
            'columns': '*'
        }
        parameters = self.__parameters__(info_params, kwargs)
        return self.__read__(**parameters)

    def __table_exist__(
        self,
        schema: Optional[str] = None,
        table: Optional[str] = None,
        schema_column: str = 'TABLE_SCHEMA',
        table_column: str = 'TABLE_NAME'
    ) -> bool:
        df = self.__schema_info__(table='tables')
        args = inspect.getargvalues(inspect.currentframe())
        args = {i: args.locals[i] for i in args.args if i != 'self'}
        parameters = self.__parameters__(args)

        df_filtered = df[
            (df[schema_column] == parameters.get('schema')) &
            (df[table_column] == parameters.get('table'))
        ]
        return True if len(df_filtered) > 0 else False

    def __drop_table__(self, log: bool = False, **kwargs: Any) -> None:
        parameters = self.__parameters__(kwargs)
        sql_command = 'DROP TABLE IF EXISTS {table}'.format(**parameters)
        self.__command__(sql_command, **kwargs)
        if log:
            print(sql_command)

    def __create_table__(
        self,
        primary_key: Optional[str] = None,
        keys: Optional[List[str]] = None,
        partition: Optional[Dict[str, List[Any]]] = None,
        log: bool = False,
        **kwargs: Any
    ) -> None:
        args = inspect.getargvalues(inspect.currentframe())
        args = {i: args.locals[i] for i in args.args if i != 'self'}
        parameters = self.__parameters__(args, kwargs)

        sql_command = 'CREATE TABLE IF NOT EXISTS `{schema}`.`{table}` (\n'.format(**parameters)
        if primary_key:
            if partition is None:
                primary_command = (
                    f'`{primary_key}` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, '
                )
            else:
                partition_key = list(partition.keys())[0]
                primary_command = (
                    f'`{primary_key}` INT NOT NULL AUTO_INCREMENT, UNIQUE KEY (`{primary_key}`, `{partition_key}`), '
                )
            sql_command += primary_command

        columns_text = self.__columns_connect__(parameters.get('columns', {}))
        sql_command += columns_text

        if keys:
            keys_command = ',\n' + ',\n'.join([f'key ({i})' if isinstance(i, str) else f'key({",".join(i)})' for i in ([keys] if isinstance(keys, str) else keys)])
            sql_command += keys_command

        char_col_command = (
            ')\n ENGINE = InnoDB DEFAULT CHARSET = {charset} COLLATE = {collate}'
        ).format(**parameters)
        sql_command += char_col_command

        if partition:
            part_key = list(partition.keys())[0]
            key_part = f'\n PARTITION BY RANGE COLUMNS(`{part_key}`)(\n'

            part_values = list(partition.values())[0]
            partition_values_str = []
            for val in part_values:
                if not isreal(val) or isinstance(val, datetime):
                    partition_values_str.append(f'"{val}"')
                else:
                    partition_values_str.append(str(val))
            partition_values_str.append('MAXVALUE')

            partition_parts = [
                f'PARTITION p{i} VALUES LESS THAN ({j})' for i, j in enumerate(partition_values_str)
                ]

            partition_command = key_part + ',\n'.join(partition_parts) + ')'
            sql_command += partition_command

        if log:
            print(sql_command)
        self.__command__(sql_command, **kwargs)

    def __write__(
        self,
        df_obj: pd.DataFrame,
        if_exists: Literal['fail', 'replace', 'append'] = 'append',
        index: bool = False,
        log: bool = False,
        **kwargs: Any
    ) -> None:
        """
        ===========================================================================

        Writes a pandas DataFrame to the MySQL database.

        Parameters
        ----------
        self : object
            The instance of the class.
        df_obj : pd.DataFrame
            The DataFrame to write.
        if_exists : Literal['fail', 'replace', 'append'], optional
            How to behave if the table already exists. 'fail': Raise a ValueError.
            'replace': Drop the table before inserting new values. 'append': Insert new values to the existing table.
            By default 'append'.
        index : bool, optional
            Whether to write the DataFrame index as a column, by default False.
        log : bool, optional
            Whether to log the write operation, by default False.
        **kwargs : Any
            Additional keyword arguments for the write operation.

        ---------------------------------------------------------------------------

        将 pandas DataFrame 写入 MySQL 数据库。

        参数
        ----------
        self : object
            类的实例。
        df_obj : pd.DataFrame
            要写入的 DataFrame。
        if_exists : Literal['fail', 'replace', 'append'], optional
            如果表已存在，如何处理。'fail'：引发 ValueError。
            'replace'：在插入新值之前删除表。'append'：将新值插入现有表。
            默认为 'append'。
        index : bool, optional
            是否将 DataFrame 索引写入为列，默认为 False。
        log : bool, optional
            是否记录写入操作，默认为 False。
        **kwargs : Any
            写入操作的额外关键字参数。

        ---------------------------------------------------------------------------
        """
        parameters = self.__parameters__(kwargs)
        engine = self.__engine__(**parameters)
        df_obj.to_sql(
            parameters['table'],
            con=engine,
            if_exists=if_exists,
            index=index,
            chunksize=320000
        )
        engine.dispose()
        if log:
            print(
                "Written DataFrame to <{schema}.{table}>: {count} records.".format(count=len(df_obj), **parameters)
            )
