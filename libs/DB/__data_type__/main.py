# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:18:57 2025

@author: Porco Rosso
"""

from typing import List, Type


class MySQL:
    """
    ===========================================================================

    MySQL Data Type Mappings.

    ---------------------------------------------------------------------------

    MySQL 数据类型映射。

    ---------------------------------------------------------------------------
    """
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
    """
    ===========================================================================

    DuckDB Data Type Mappings.

    ---------------------------------------------------------------------------

    DuckDB 数据类型映射。

    ---------------------------------------------------------------------------
    """
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
    """
    ===========================================================================

    Main class for data type translation.

    ---------------------------------------------------------------------------

    用于数据类型转换的主类。

    ---------------------------------------------------------------------------
    """
    MySQL: Type[MySQL] = MySQL
    DuckDB: Type[DuckDB] = DuckDB

    def __init__(self, recommand: str) -> None:
        """
        ===========================================================================

        Initializes the data type translator.

        Parameters
        ----------
        recommand : str
            The recommended database dialect ('MySQL' or 'DuckDB').

        ---------------------------------------------------------------------------

        初始化数据类型转换器。

        参数
        ----------
        recommand : str
            推荐的数据库方言（'MySQL' 或 'DuckDB'）。

        ---------------------------------------------------------------------------
        """
        self.recommand = recommand

    def __call__(self, data_type: str) -> str:
        """
        ===========================================================================

        Translates a generic data type to the specific dialect.

        Parameters
        ----------
        data_type : str
            The generic data type string (e.g., 'VARCHAR(100)').

        Returns
        -------
        str
            The translated data type string for the recommended dialect.

        ---------------------------------------------------------------------------

        将通用数据类型转换为特定的方言。

        参数
        ----------
        data_type : str
            通用数据类型字符串（例如，'VARCHAR(100)'）。

        返回
        -------
        str
            转换后的推荐方言的数据类型字符串。

        ---------------------------------------------------------------------------
        """
        parts = data_type.split('(')
        base_type = parts[0].upper()
        class_obj = getattr(self, self.recommand)

        translated_type = getattr(class_obj, base_type, class_obj.UNDIFINED)

        if len(parts) > 1 and (translated_type in class_obj.MPS):
            return f"{translated_type}({parts[1]}"
        return translated_type
