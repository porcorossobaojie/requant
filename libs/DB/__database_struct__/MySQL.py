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
    __data_trans__ = data_trans('MySQL')
    __internal_attrs__ = []
    
    def __init__(self, **kwargs: Any) -> None:
        self.__internal_attrs__ = list(set(self.__internal_attrs__) | set(kwargs.keys()))
        [setattr(self, i, j) for i, j in kwargs.items()]

    def __env_init__(self, schema: Optional[str] = None) -> None:
        schema = self.schema if schema is None else schema
        self.__command__(f'CREATE SCHEMA IF NOT EXISTS {schema}')

    def __engine__(
        self,
        schema: str,
        **kwargs: Any
    ) -> Engine:
        parameters = self.__parameters__(kwargs)
        connection_string = self.__URL__(schema, **parameters)
        engine = create_engine(connection_string)
        return engine

    def __command__(self, command: str, **kwargs: Any) -> Tuple:
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
                x[i] = [self.__data_trans__(j[type_position].upper()),
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
