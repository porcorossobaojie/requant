# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:18:57 2025

@author: Porco Rosso
"""

from typing import List, Type


class MySQL:
    TINYINT: str = 'TINYINT'
    SMALLINT: str = 'SMALLINT'
    INTEGER: str = 'INT'
    INT: str = 'INT'
    BIGINT: str = 'BIGINT'

    FLOAT: str = 'FLOAT'
    DOUBLE: str = 'DOUBLE'
    REAL: str = 'DOUBLE'

    DECIMAL: str = 'DECIMAL'
    NUMERIC: str = 'DECIMAL'

    BOOLEAN: str = 'BOOLEAN'
    BOOL: str = 'BOOLEAN'

    VARCHAR: str = 'VARCHAR'
    TEXT: str = 'TEXT'

    DATE: str = 'DATE'
    DATETIME: str = 'DATETIME'
    TIMESTAMP: str = 'DATETIME'

    UNDIFINED: str = 'VARCHAR(255)'

    MPS: List[str] = [INTEGER, FLOAT, REAL, DOUBLE, DECIMAL, VARCHAR]


class DuckDB:
    TINYINT: str = 'TINYINT'
    SMALLINT: str = 'SMALLINT'
    INTEGER: str = 'INT'
    INT: str = 'INT'
    BIGINT: str = 'BIGINT'

    FLOAT: str = 'FLOAT'
    DOUBLE: str = 'DOUBLE'
    REAL: str = 'DOUBLE'

    DECIMAL: str = 'DECIMAL'
    NUMERIC: str = 'DECIMAL'

    BOOLEAN: str = 'BOOLEAN'
    BOOL: str = 'BOOLEAN'

    VARCHAR: str = 'VARCHAR'
    TEXT: str = 'TEXT'

    DATE: str = 'DATE'
    DATETIME: str = 'DATETIME'
    TIMESTAMP: str = 'DATETIME'

    UNDIFINED: str = 'VARCHAR'

    MPS: List[str] = [DECIMAL]


class main:
    MySQL: Type[MySQL] = MySQL
    DuckDB: Type[DuckDB] = DuckDB

    def __init__(self, recommand: str) -> None:
        self.recommand = recommand

    def __call__(self, data_type: str) -> str:
        parts = data_type.split('(')
        base_type = parts[0].upper()
        class_obj = getattr(self, self.recommand)

        translated_type = getattr(class_obj, base_type, class_obj.UNDIFINED)

        if len(parts) > 1 and (translated_type in class_obj.MPS):
            return f"{translated_type}({parts[1]}"
        return translated_type