# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:37:50 2025

@author: admin
"""

from typing import Any, Dict, Type
from local.login_info import DB_LOGIN_INFO


class MySQL(DB_LOGIN_INFO.MySQL):
    """
    ===========================================================================

    Configuration class for MySQL database connection.

    This class holds static configuration values and methods for connecting to a MySQL database.

    ---------------------------------------------------------------------------

    MySQL 数据库连接的配置类。

    此类包含用于连接 MySQL 数据库的静态配置值和方法。

    ---------------------------------------------------------------------------
    """
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
        """
        ===========================================================================

        Constructs the MySQL connection URL.

        Parameters
        ----------
        cls : type
            The class itself.
        schema : str
            The database schema to connect to.
        **kwargs : Dict[str, Any]
            Additional keyword arguments for connection parameters (e.g., user, password, host, port, charset).

        Returns
        -------
        str
            The constructed MySQL connection URL.

        ---------------------------------------------------------------------------

        构建 MySQL 连接 URL。

        参数
        ----------
        cls : type
            类本身。
        schema : str
            要连接的数据库模式。
        **kwargs : Dict[str, Any]
            连接参数的额外关键字参数（例如，user, password, host, port, charset）。

        返回
        -------
        str
            构建的 MySQL 连接 URL。

        ---------------------------------------------------------------------------
        """
        return (
            "{mysql_connect}{user}:{password}@{host}:{port}/{schema}?charset={charset}"
        ).format(schema=schema, **kwargs)


class DuckDB(DB_LOGIN_INFO.DuckDB):
    """
    ===========================================================================

    Configuration class for DuckDB database connection.

    This class holds static configuration values for connecting to a DuckDB database.

    ---------------------------------------------------------------------------

    DuckDB 数据库连接的配置类。

    此类包含用于连接 DuckDB 数据库的静态配置值。

    ---------------------------------------------------------------------------
    """
    path: str = 'e:/programdata/DuckDB'
    database: str = 'Local'
    schema = 'jq_data'