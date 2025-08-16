# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:52:23 2025

@author: Porco Rosso

"""

from local.login_info import SOURCE
from libs import __DUCKDB_STATSMETHOD__, __MYSQL_STATSMETHOD__

from libs.__flow__.config import DB_INFO, COLUMNS_INFO, FILTER
from libs.utils.functions import filter_parent_class_attrs

def __source__(source=SOURCE):
    if source == 'DuckDB':
        return __DUCKDB_STATSMETHOD__
    else:
        return __MYSQL_STATSMETHOD__


def __table_info__(how: str = 'DataFrame'):
    df = __source__()().__schema_info__(
        where="{schema_info} = '{schema}'".format(
            schema_info=DB_INFO.schema_info, 
            schema=__source__().schema
        )
    )
    df.columns = df.columns.str.upper()
    df = df[~( 
              (df[DB_INFO.table_info].str.contains('ashareindicator') &
               df[DB_INFO.columns_info].isin(['OPERATING_PROFIT']))
               |
              (df[DB_INFO.table_info].str.contains('ashareincome') &
               df[DB_INFO.columns_info].isin(['EPS']))
              | df[DB_INFO.table_info].str.contains('ashareperformance_lt')
              |(df[DB_INFO.table_info].str.contains('asharecashflow') &
               df[DB_INFO.columns_info].isin(['NET_PROFIT']))
            )]
    if how == 'DataFrame':
        df = df.loc[:, df.columns.isin(filter_parent_class_attrs(DB_INFO).values())]
    elif how == 'dict':
        df = df.groupby(DB_INFO.table_info)[DB_INFO.columns_info].apply(list).to_dict()
    else:
        raise ValueError(
            f"Invalid value '{how}' for parameter 'how'. Valid values are: {', '.join(['DataFrame', 'dict'])}"
        )
    return df

def __table_attr__(key, value):
    class_attributes = (filter_parent_class_attrs(COLUMNS_INFO) 
                        | filter_parent_class_attrs((FILTER)) 
                        | {'table':key, 'columns': list(set(value) - set(COLUMNS_INFO.drop_columns))})
    return class_attributes
