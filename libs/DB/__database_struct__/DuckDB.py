# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 13:25:09 2025

@author: Porco Rosso
"""
import inspect
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

import duckdb
import pandas as pd

from libs.DB.__data_type__.main import main as data_trans
from libs.DB.__database_struct__.meta import main as meta


class main(meta):
    """
    ===========================================================================

    Main class for DuckDB database operations.

    This class provides methods for interacting with a DuckDB database,
    including environment initialization, command execution, data reading,
    and table management.

    ---------------------------------------------------------------------------

    DuckDB 数据库操作的主类。

    此类提供与 DuckDB 数据库交互的方法，包括环境初始化、命令执行、数据读取和表管理。

    ---------------------------------------------------------------------------
    """
    __data_trans__ = data_trans('DuckDB')
    __internal_attrs__ = []

    def __init__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Initializes the DuckDB main class.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Keyword arguments to set internal attributes.

        ---------------------------------------------------------------------------

        初始化 DuckDB 主类。

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
        parameters = self.__parameters__()
        with self.__engine__(**parameters) as con:
            con.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')

    def __engine__(self, **kwargs: Any) -> duckdb.DuckDBPyConnection:
        """
        ===========================================================================

        Establishes a connection to the DuckDB database.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Keyword arguments for database connection parameters.

        Returns
        -------
        duckdb.DuckDBPyConnection
            A DuckDB database connection object.

        ---------------------------------------------------------------------------

        建立与 DuckDB 数据库的连接。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            数据库连接参数的关键字参数。

        返回
        -------
        duckdb.DuckDBPyConnection
            一个 DuckDB 数据库连接对象。

        ---------------------------------------------------------------------------
        """
        parameters = self.__parameters__(kwargs)
        database = "{path}/{database}.duckdb".format(**parameters)
        x = duckdb.connect(database=database)
        return x

    def __command__(self, command: str, **kwargs: Any) -> pd.DataFrame:
        """
        ===========================================================================

        Executes a SQL command on the DuckDB database.

        Parameters
        ----------
        self : object
            The instance of the class.
        command : str
            The SQL command to execute.
        **kwargs : Any
            Additional keyword arguments for the engine.

        Returns
        -------
        pd.DataFrame
            The result of the command as a pandas DataFrame.

        ---------------------------------------------------------------------------

        在 DuckDB 数据库上执行 SQL 命令。

        参数
        ----------
        self : object
            类的实例。
        command : str
            要执行的 SQL 命令。
        **kwargs : Any
            引擎的额外关键字参数。

        返回
        -------
        pd.DataFrame
            命令执行结果的 pandas DataFrame。

        ---------------------------------------------------------------------------
        """
        with self.__engine__(**kwargs) as engine:
            x = engine.execute(command).fetchdf()
            return x
    
    def __columns_connect__(
        self,
        columns_obj: Optional[Union[str, List[str], Dict[str, Any]]],
        type_position: Optional[int] = None,
        comment_position: Optional[int] = None
    ) -> Union[str, Tuple[str, Dict[str, str]]]:
        """
        ===========================================================================

        Connects and formats column information for DuckDB.

        This method takes a column object and formats it into a string suitable
        for SQL queries or a tuple containing column definitions and comments.

        Parameters
        ----------
        self : object
            The instance of the class.
        columns_obj : Optional[Union[str, List[str], Dict[str, Any]]]
            Column object. Can be:
            - None: Returns '*' for selecting all columns.
            - str: Returns the string as is.
            - list: Joins the list elements with ', ' for column selection.
            - dict: Formats dictionary keys and values into column definitions
              with types and comments.
        type_position : Optional[int], optional
            For dictionary `columns_obj`, the index of the type within the value list, by default None.
        comment_position : Optional[int], optional
            For dictionary `columns_obj`, the index of the comment within the value list, by default None.

        Returns
        -------
        Union[str, Tuple[str, Dict[str, str]]]
            Formatted column information. Returns a string if `columns_obj` is
            None, str, or list. Returns a tuple of (column_definitions_string, comments_dictionary)
            if `columns_obj` is a dictionary.

        ---------------------------------------------------------------------------

        连接并格式化 DuckDB 的列信息。

        此方法接受一个列对象，并将其格式化为适合 SQL 查询的字符串，
        或包含列定义和注释的元组。

        参数
        ----------
        self : object
            类的实例。
        columns_obj : Optional[Union[str, List[str], Dict[str, Any]]]
            列对象。可以是：
            - None：返回 '*' 以选择所有列。
            - str：直接返回字符串。
            - list：将列表元素用 ', ' 连接起来以供列选择。
            - dict：将字典的键和值格式化为包含类型和注释的列定义。
        type_position : Optional[int], optional
            对于字典 `columns_obj`，值列表中类型所在的索引，默认为 None。
        comment_position : Optional[int], optional
            对于字典 `columns_obj`，值列表中注释所在的索引，默认为 None。

        返回
        -------
        Union[str, Tuple[str, Dict[str, str]]]
            格式化的列信息。如果 `columns_obj` 为 None、str 或 list，则返回字符串。
            如果 `columns_obj` 为字典，则返回 (列定义字符串, 注释字典) 的元组。

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

        Reads data from the DuckDB database.

        Parameters
        ----------
        self : object
            The instance of the class.
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

        从 DuckDB 数据库读取数据。

        参数
        ----------
        self : object
            类的实例。
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

        Retrieves schema information from the DuckDB database.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Additional keyword arguments for schema information retrieval.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing schema information.

        ---------------------------------------------------------------------------

        从 DuckDB 数据库检索模式信息。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            用于检索模式信息的额外关键字参数。

        返回
        -------
        pd.DataFrame
            包含模式信息的 pandas DataFrame。

        ---------------------------------------------------------------------------
        """
        info_params = {
            'schema': 'INFORMATION_SCHEMA',
            'table': 'COLUMNS',
            'columns': '*'
        }
        parameters = self.__parameters__(info_params, kwargs)
        df = self.__read__(**parameters)
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
        self : object
            The instance of the class.
        schema : Optional[str], optional
            The schema name, by default None.
        table : Optional[str], optional
            The table name, by default None.
        schema_column : str, optional
            The column name for schema in the information schema, by default 'table_schema'.
        table_column : str, optional
            The column name for table in the information schema, by default 'table_name'.
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        bool
            True if the table exists, False otherwise.

        ---------------------------------------------------------------------------

        检查指定模式中是否存在表。

        参数
        ----------
        self : object
            类的实例。
        schema : Optional[str], optional
            模式名称，默认为 None。
        table : Optional[str], optional
            表名称，默认为 None。
        schema_column : str, optional
            信息模式中模式的列名，默认为 'table_schema'。
        table_column : str, optional
            信息模式中表的列名，默认为 'table_name'。
        **kwargs : Any
            额外的关键字参数。

        返回
        -------
        bool
            如果表存在则为 True，否则为 False。

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

        Drops a table from the DuckDB database.

        Parameters
        ----------
        self : object
            The instance of the class.
        log : bool, optional
            Whether to log the SQL command, by default False.
        **kwargs : Any
            Additional keyword arguments for table dropping.

        ---------------------------------------------------------------------------

        从 DuckDB 数据库中删除表。

        参数
        ----------
        self : object
            类的实例。
        log : bool, optional
            是否记录 SQL 命令，默认为 False。
        **kwargs : Any
            用于删除表的额外关键字参数。

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
        """
        ===========================================================================

        Creates a table in the DuckDB database.

        Parameters
        ----------
        self : object
            The instance of the class.
        log : bool, optional
            Whether to log the SQL command, by default False.
        **kwargs : Any
            Additional keyword arguments for table creation.

        ---------------------------------------------------------------------------

        在 DuckDB 数据库中创建表。

        参数
        ----------
        self : object
            类的实例。
        log : bool, optional
            是否记录 SQL 命令，默认为 False。
        **kwargs : Any
            用于创建表的额外关键字参数。

        ---------------------------------------------------------------------------
        """
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
        """
        ===========================================================================

        Writes a pandas DataFrame to the DuckDB database.

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

        将 pandas DataFrame 写入 DuckDB 数据库。

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