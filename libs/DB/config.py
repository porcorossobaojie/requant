# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:37:50 2025

@author: admin
"""

from typing import Any, Dict, Type
from local.login_info import DB_LOGIN_INFO


class MySQL(DB_LOGIN_INFO.MySQL):
    mysql_connect: str = 'mysql+pymysql://'
    charset: str = 'utf8mb4'
    collate: str = 'utf8mb4_general_ci'
    chunksize: int = 64000000
    host: str = '127.0.0.1'
    port: int = 3306
    schema = 'jq_data'

    @classmethod
    def __URL__(
        cls,
        schema: str,
        **kwargs: Dict[str, Any]
    ) -> str:
        return (
            "{mysql_connect}{user}:{password}@{host}:{port}/{schema}?charset={charset}"
        ).format(schema=schema, **kwargs)




class DuckDB(DB_LOGIN_INFO.DuckDB):
    path: str = 'e:/programdata/DuckDB'
    database: str = 'Local'
    schema = 'jq_data'