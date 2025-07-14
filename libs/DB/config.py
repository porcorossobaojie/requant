# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:37:50 2025

@author: admin
"""

class MySQL:
    mysql_connect = 'mysql+pymysql://'
    charset = 'utf8mb4'
    collate = 'utf8mb4_general_ci'
    chunksize = 64000000
    host = '127.0.0.1'
    port = 3306    

    user = str
    password = str
    
    @classmethod
    def __URL__(cls, schema, **kwargs):
        text = (
                "{mysql_connect}{user}:{password}@{host}:{port}/{}?charset={charset}"
        ).format(
                schema, 
                **kwargs
        )
        return text

    @classmethod
    def __env_init__(cls, *args, **kwargs):
        pass
    
class DuckDB:
    path = 'e:/programdata/DuckDB'
    database = 'Local'    

    @classmethod
    def __env_init__(cls, *args, **kwargs):
        pass
    
DB_RECOMMAND_SOURCE = 'DuckDB'