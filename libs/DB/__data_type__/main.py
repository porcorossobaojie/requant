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
    """
    ===========================================================================

    Main class for data type translation.

    This class provides methods to translate generic data types to
    database-specific data types (MySQL or DuckDB).

    ---------------------------------------------------------------------------

    数据类型转换的主类。

    此类提供将通用数据类型转换为特定数据库数据类型（MySQL 或 DuckDB）的方法。

    ---------------------------------------------------------------------------
    """
    MySQL: Type[MySQL] = MySQL
    DuckDB: Type[DuckDB] = DuckDB

    def __init__(self, recommand: str) -> None:
        """
        ===========================================================================

        Initializes the data type translation class.

        Parameters
        ----------
        self : object
            The instance of the class.
        recommand : str
            The database type to recommend (e.g., 'MySQL' or 'DuckDB').

        ---------------------------------------------------------------------------

        初始化数据类型转换类。

        参数
        ----------
        self : object
            类的实例。
        recommand : str
            要推荐的数据库类型（例如，'MySQL' 或 'DuckDB'）。

        ---------------------------------------------------------------------------
        """
        self.recommand = recommand

    def __call__(self, data_type: str) -> str:
        """
        ===========================================================================

        Translates a generic data type string to a database-specific data type.

        Parameters
        ----------
        self : object
            The instance of the class.
        data_type : str
            The generic data type string (e.g., 'INT', 'VARCHAR(255)').

        Returns
        -------
        str
            The translated database-specific data type string.

        ---------------------------------------------------------------------------

        将通用数据类型字符串转换为特定数据库的数据类型。

        参数
        ----------
        self : object
            类的实例。
        data_type : str
            通用数据类型字符串（例如，'INT'，'VARCHAR(255)'）。

        返回
        -------
        str
            转换后的特定数据库数据类型字符串。

        ---------------------------------------------------------------------------
        """
        parts = data_type.split('(')
        base_type = parts[0].upper()
        class_obj = getattr(self, self.recommand)

        translated_type = getattr(
            class_obj, base_type, class_obj.UNDIFINED
        )

        if len(parts) > 1 and (translated_type in class_obj.MPS):
            return f"{translated_type}({parts[1]}"
        return translated_type