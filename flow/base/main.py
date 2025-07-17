# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:52:23 2025

@author: Porco Rosso

"""

from libs import db
from flow.config import DB_INFO, DATABASE, FILTER
from libs.utils.functions import filter_class_attrs

def __table_info__(how: str = 'DataFrame'):
    df = db.schema_info(
        where="{schema_info} = '{schema}'".format(
            schema_info=DB_INFO.schema_info, 
            schema=DATABASE.schema
        )
    )
    df.columns = df.columns.str.upper()
    df = df[~( 
              (df[DB_INFO.table_info].str.contains('ashareindicator') &
               df[DB_INFO.columns_info].isin(['OPERATING_PROFIT']))
               |
              (df[DB_INFO.table_info].str.contains('ashareincome') &
               df[DB_INFO.columns_info].isin(['EPS']))
            )]
    if how == 'DataFrame':
        df = df.loc[:, df.columns.isin(filter_class_attrs(DB_INFO).values())]
    elif how == 'dict':
        df = df.groupby(DB_INFO.table_info)[DB_INFO.columns_info].apply(list).to_dict()
    else:
        raise ValueError(
            f"Invalid value '{how}' for parameter 'how'. Valid values are: {', '.join(['DataFrame', 'dict'])}"
        )
    return df

def __table_attr__(key, value):
    class_attributes = filter_class_attrs(DATABASE) | filter_class_attrs((FILTER)) | {'table':key, 'columns': list(set(value) - set(DATABASE.drop_columns))}
    return class_attributes
