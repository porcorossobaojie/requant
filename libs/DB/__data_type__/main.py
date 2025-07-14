# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:18:57 2025

@author: Porco Rosso
"""

class MySQL:
    TINYINT = 'TINYINT'         # 1 字节有符号整数
    SMALLINT = 'SMALLINT'       # 2 字节有符号整数
    INTEGER = 'INT'             # 4 字节有符号整数
    INT  = 'INT'               # 4 字节有符号整数
    BIGINT = 'BIGINT'           # 8 字节有符号整数
    
    FLOAT = 'FLOAT'    
    DOUBLE = 'DOUBLE'
    REAL = 'DOUBLE'
    
    DECIMAL = 'DECIMAL'
    NUMERIC = 'DECIMAL'
    
    BOOLEAN  = 'BOOLEAN'
    BOOL = 'BOOLEAN'
    
    VARCHAR = 'VARCHAR'
    TEXT = 'TEXT'
    
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    TIMESTAMP = 'DATETIME'
    
    UNDIFINED = 'VARCHAR(255)'
    
    MPS = [INT, INTEGER, FLOAT, REAL, DOUBLE, DECIMAL, VARCHAR]
    
    
class DuckDB:
    TINYINT = 'TINYINT'         
    SMALLINT = 'SMALLINT'       
    INTEGER = 'INT'             
    INT  = 'INT'               
    BIGINT = 'BIGINT'          
    
    FLOAT = 'FLOAT'    
    DOUBLE = 'DOUBLE'
    REAL = 'DOUBLE'
    
    DECIMAL = 'DECIMAL'
    NUMERIC = 'DECIMAL'
    
    BOOLEAN  = 'BOOLEAN'
    BOOL = 'BOOLEAN'
    
    VARCHAR = 'VARCHAR'
    TEXT = 'TEXT'
    
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    TIMESTAMP = 'DATETIME'
    
    UNDIFINED = 'VARCHAR'
    
    MPS = [REAL, DECIMAL]
    
class main():
    MySQL = MySQL
    DuckDB = DuckDB
    
    def __init__(self, recommand):
        self.recommand = recommand
        
    def __call__(self, data_type):
        x = data_type.split('(')
        class_obj = getattr(self, self.recommand)
        x1 = getattr(class_obj, x[0], class_obj.UNDIFINED)
        if len(x) > 1 and x1 in class_obj.MPS:
            x1 = f"{x1}({x[1]}"
        return x1
            
            
    
    
    
    
    
    
    
    
    