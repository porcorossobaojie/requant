# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 13:25:09 2025

@author: Porco Rosso
"""
import inspect
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple

import duckdb
import pandas as pd

from libs.DB.__data_type__.main import main as data_trans
from libs.DB.__database_struct__.meta import main as meta
from libs.DB.config import DuckDB as config
from libs.utils.functions import filter_class_attrs


class main(meta, config):
    __data_trans__ = data_trans('DuckDB')
    __internal_attrs__ = list(filter_class_attrs(config).keys())

    def __init__(self, **kwargs: Any) -> None:
        self.__internal_attrs__ = list(
            set(self.__internal_attrs__) | set(kwargs.keys())
        )
        [setattr(self, i, j) for i, j in kwargs.items()]

    def __env_init__(self, schema: Optional[str] = None) -> None:
        schema = self.schema if schema is None else schema
        parameters = self.__parameters__()
        with self.__engine__(**parameters) as con:
            con.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')

    def __engine__(self, **kwargs: Any) -> duckdb.DuckDBPyConnection:
        parameters = self.__parameters__(kwargs)
        database = "{path}/{database}.duckdb".format(**parameters)
        x = duckdb.connect(database=database)
        return x

    def __command__(self, command: str, **kwargs: Any) -> pd.DataFrame:
        with self.__engine__(**kwargs) as engine:
            x = engine.execute(command).fetchdf()
            return x
    
    def __columns_connect__(
        self,
        columns_obj,
        type_position=None,
        comment_position=None
    ):
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
                    self.__data_trans__(j[type_position].upper()), '' if len(j) == 1 else j[comment_position]
                ]
            x = (
                ', \n'.join([f'{i} {j[0]} DEFAULT NULL' for i, j in x.items()]),
                {i: j[1] for i, j in x.items()}
            )
        return x

    def __read__(
        self,
        log: bool = False,
        show_time: bool = False,
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Core function for loading data from MySQL server.

        Parameters
        ----------
        chunksize : int, optional
            The number of rows to include in each chunk. Defaults to None.
        log : bool, optional
            Whether to print the SQL command. Defaults to False.
        show_time : bool, optional
            Whether to display the execution time. Defaults to False.
        **kwargs : Any
            Any parameters using temporary for create engine

        Returns
        -------
        DataFrame : pd.DataFrame
            A DataFrame containing the loaded data.

        ---------------------------------------------------------------------------

        从MySQL服务器加载数据的核心函数。

        参数
        ----------
        chunksize : int, optional
            每个块中包含的行数。默认为 None。
        log : bool, optional
            是否打印SQL命令。默认为 False。
        show_time : bool, optional
            是否显示执行时间。默认为 False。
        **kwargs : Any
            用于临时创建引擎的任何参数

        返回
        -------
        DataFrame : pd.DataFrame
            包含加载数据的DataFrame。

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

            command = 'SELECT {columns} FROM {schema}.{table}'.format(
                **parameters
            )
            if parameters.get('where', None) is not None:
                where_clause = parameters['where'].replace('"', "'")
                command = f"{command} WHERE {where_clause}"

            if log:
                print(command)
            x = self.__command__(command, read_only=True, **parameters)
            return x
        return wraps_function()

    def __schema_info__(self, **kwargs: Any ) -> pd.DataFrame:
        """
        ===========================================================================

        Retrieves schema information from the INFORMATION_SCHEMA.

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the schema information.

        ---------------------------------------------------------------------------

        从 INFORMATION_SCHEMA 中检索 schema 信息。

        参数
        ----------
        **kwargs : Any
            附加关键字参数。

        返回
        -------
        pd.DataFrame
            包含模式信息的DataFrame。

        ---------------------------------------------------------------------------
        """
        info_params = {
            'schema': 'INFORMATION_SCHEMA',
            'table': 'COLUMNS',
            'columns': '*'
        }
        parameters = self.__parameters__(info_params, kwargs)
        command = 'select * from information_schema.{table}'.format(
            **parameters
        )
        df = self.__command__(command, **parameters)
        return df

    def __table_exist__(
        self,
        schema: Optional[str] = None,
        table: Optional[str] = None,
        schema_column: str = 'table_schema',
        table_column: str = 'table_name',
        **kwargs: Any
    ) -> bool:
        """
        ===========================================================================

        Checks if a table exists in the specified schema.

        Parameters
        ----------
        schema : str, optional
            The schema name. Defaults to the instance's schema.
        table : str, optional
            The table name. Defaults to the instance's table.
        schema_column : str, optional
            The column name for the schema in the information table. Defaults to 'TABLE_SCHEMA'.
        table_column : str, optional
            The column name for the table in the information table. Defaults to 'TABLE_NAME'.

        Returns
        -------
        bool
            True if the table exists, False otherwise.

        ---------------------------------------------------------------------------

        检查指定的 schema 中是否存在某个表。

        参数
        ----------
        schema : str, optional
            模式名称。默认为实例的模式。
        table : str, optional
            表名。默认为实例的表。
        schema_column : str, optional
            信息表中模式的列名。默认为 'TABLE_SCHEMA'。
        table_column : str, optional
            信息表中表的列名。默认为 'TABLE_NAME'。

        返回
        -------
        bool
            如果表存在，则为 True，否则为 False。

        ---------------------------------------------------------------------------
        """
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
        """
        ===========================================================================

        Executes a 'DROP TABLE' SQL command.

        Parameters
        ----------
        log : bool, optional
            Whether to print the SQL command. Defaults to False.
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        执行 'DROP TABLE' SQL 命令。

        参数
        ----------
        log : bool, optional
            是否打印SQL命令。默认为 False。
        **kwargs : Any
            附加关键字参数。

        ---------------------------------------------------------------------------
        """
        parameters = self.__parameters__(kwargs)
        sql_command = 'DROP TABLE IF EXISTS {schema}.{table}'.format(
            **parameters
        )
        self.__command__(sql_command, **kwargs)
        if log:
            print(sql_command)

    def __create_table__(self, log: bool = False, **kwargs: Any) -> None:
        args = inspect.getargvalues(inspect.currentframe())
        args = {i: args.locals[i] for i in args.args if i != 'self'}
        parameters = self.__parameters__(args, kwargs)

        command = 'CREATE TABLE IF NOT EXISTS {schema}.{table} (\n'.format(**parameters)

        columns = self.__columns_connect__(parameters.get('columns', {}))
        if isinstance(columns, tuple):
            columns_str, comments_dict = columns
            command = command + columns_str + '\n);'
            comment_commands = [
                "COMMENT ON COLUMN {schema}.{table}.{i} IS '{j}';".format(
                    i=i, j=j, **parameters
                ) for i, j in comments_dict.items()
            ]
            command_list = [
                'BEGIN TRANSACTION;',
                command,
                *comment_commands,
                'COMMIT;'
            ]
            full_command = '\n'.join(command_list)
            self.__command__(full_command)
            if log:
                print(full_command)
        else:
            command = command + columns + '\n);'
            self.__command__(command)
            if log:
                print(command)

    def __write__(
        self,
        df_obj: pd.DataFrame,
        if_exists: Literal['fail', 'replace', 'append'] = 'append',
        index: bool = False,
        log: bool = False,
        **kwargs: Any
    ) -> None:
        if index:
            df_obj = df_obj.reset_index()

        parameters = self.__parameters__(kwargs)
        table_exist = self.__table_exist__(**parameters)
        
        with self.__engine__(**parameters) as con:
            con.register('df_obj', df_obj)
    
            insert_statement = (
                "INSERT INTO {database}.{schema}.{table} BY NAME SELECT * FROM df_obj"
            ).format(**parameters)
            create_statement = (
                "CREATE OR REPLACE TABLE {database}.{schema}.{table} AS SELECT * FROM df_obj"
            ).format(**parameters)
    
            if table_exist:
                if if_exists == 'replace':
                    self.__drop_table__(**parameters)
                    try:
                        self.__create_table__(**parameters)
                        con.execute(insert_statement)
                    except Exception:
                        print('Function: __create_table__ Failed. \nCreate table automatic.')
                        con.execute(create_statement)
    
                elif if_exists == 'append':
                    con.execute(insert_statement)
                elif if_exists == 'fail':
                    raise ValueError('Table already existed.')
                else:
                    raise ValueError("if_exists must be in ['fail', 'replace', 'append']")
            else:
                try:
                    self.__create_table__(**parameters)
                    con.execute(insert_statement)
                except Exception:
                    print('Function: __create_table__ Failed. \nCreate table automatic.')
                    con.execute(create_statement)
    
            con.close()
        if log:
            print("Written DataFrame to <{schema}.{table}>: {count} records.".format(count=len(df_obj), **parameters))
