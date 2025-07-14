# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:37:50 2025

@author: admin
"""

from typing import Any, Dict, Type


class MySQL:
    """
    ===========================================================================

    Configuration class for MySQL database connections.

    ---------------------------------------------------------------------------

    用于MySQL数据库连接的配置类。

    ---------------------------------------------------------------------------
    """
    mysql_connect: str = 'mysql+pymysql://'
    charset: str = 'utf8mb4'
    collate: str = 'utf8mb4_general_ci'
    chunksize: int = 64000000
    host: str = '127.0.0.1'
    port: int = 3306

    user: Type[str] = str
    password: Type[str] = str

    @classmethod
    def __URL__(
        cls,
        schema: str,
        **kwargs: Dict[str, Any]
    ) -> str:
        """
        ===========================================================================

        Constructs the database connection URL.

        Parameters
        ----------
        schema : str
            The database schema name.
        **kwargs : Dict[str, Any]
            Connection parameters.

        Returns
        -------
        str
            The full connection URL string.

        ---------------------------------------------------------------------------

        构建数据库连接URL。

        参数
        ----------
        schema : str
            数据库模式名称。
        **kwargs : Dict[str, Any]
            连接参数。

        返回
        -------
        str
            完整的连接URL字符串。

        ---------------------------------------------------------------------------
        """
        return (
            "{mysql_connect}{user}:{password}@{host}:{port}/{schema}?charset={charset}"
        ).format(schema=schema, **kwargs)

    @classmethod
    def __env_init__(cls, *args: Any, **kwargs: Any) -> None:
        pass


class DuckDB:
    """
    ===========================================================================

    Configuration class for DuckDB connections.

    ---------------------------------------------------------------------------

    用于DuckDB连接的配置类。

    ---------------------------------------------------------------------------
    """
    path: str = 'e:/programdata/DuckDB'
    database: str = 'Local'

    @classmethod
    def __env_init__(cls, *args: Any, **kwargs: Any) -> None:
        pass


DB_RECOMMAND_SOURCE: str = 'DuckDB'
