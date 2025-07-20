# -*- coding: utf-8 -*-
"""
Created on Sat May 10 15:52:25 2025

@author: Porco Rosso
"""

from account.config import ACCOUNTS, PATH
from pathlib import Path
from typing import Any, Dict, List

class main():
    """
    ===========================================================================

    Manages account-related paths and operations.

    ---------------------------------------------------------------------------

    管理账户相关路径和操作。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self, 
        **kwargs: Any
    ):
        """
        ===========================================================================

        Initializes the main account manager with provided keyword arguments.

        Parameters
        ----------
        **kwargs : Any
            Keyword arguments to set as instance attributes.

        ---------------------------------------------------------------------------

        使用提供的关键字参数初始化主账户管理器。

        参数
        ----------
        **kwargs : Any
            要设置为实例属性的关键字参数。

        ---------------------------------------------------------------------------
        """
        [setattr(self, i, j) for i,j in kwargs.items()]
    
    @property
    def __order_path__(self) -> Path:
        """
        ===========================================================================

        Returns the Path object for the order directory.

        Returns
        -------
        Path
            The path to the order directory.

        ---------------------------------------------------------------------------

        返回订单目录的Path对象。

        返回
        -------
        Path
            订单目录的路径。

        ---------------------------------------------------------------------------
        """
        log_dir =  Path(self.account_path) / self.name / self.order_dir
        return log_dir
    
    @property
    def __settle_path__(self) -> Path:
        """
        ===========================================================================

        Returns the Path object for the settlement directory.

        Returns
        -------
        Path
            The path to the settlement directory.

        ---------------------------------------------------------------------------

        返回结算目录的Path对象。

        返回
        -------
        Path
            结算目录的路径。

        ---------------------------------------------------------------------------
        """
        log_dir =  Path(self.account_path) / self.name / self.settle_dir
        return log_dir

    @property
    def __test_path__(self) -> Path:
        """
        ===========================================================================

        Returns the Path object for the test directory.

        Returns
        -------
        Path
            The path to the test directory.

        ---------------------------------------------------------------------------

        返回测试目录的Path对象。

        返回
        -------
        Path
            测试目录的路径。

        ---------------------------------------------------------------------------
        """
        log_dir =  Path(self.account_path) / self.name / self.test_dir
        return log_dir
    
    @property    
    def __GET__(self) -> Any:
        """
        ===========================================================================

        Retrieves the data format attribute.

        Returns
        -------
        Any
            The value of the data_format attribute.

        ---------------------------------------------------------------------------

        检索数据格式属性。

        返回
        -------
        Any
            数据格式属性的值。

        ---------------------------------------------------------------------------
        """
        return getattr(self, self.data_format)

    def __account_create__(self):
        """
        ===========================================================================

        Creates the necessary account directories (order, settle, test).

        ---------------------------------------------------------------------------

        创建必要的账户目录（订单、结算、测试）。

        ---------------------------------------------------------------------------
        """
        self.__order_path__.mkdir(parents=True, exist_ok=True)
        self.__settle_path__.mkdir(parents=True, exist_ok=True)
        self.__test_path__.mkdir(parents=True, exist_ok=True)

    def __get_files_name__(
        self, 
        path: Path
    ) -> List[str]:
        """
        ===========================================================================

        Retrieves the names of files within a given directory.

        Parameters
        ----------
        path : Path
            The Path object of the directory.

        Returns
        -------
        List[str]
            A list of file names in the directory.

        ---------------------------------------------------------------------------

        检索给定目录中文件的名称。

        参数
        ----------
        path : Path
            目录的Path对象。

        返回
        -------
        List[str]
            目录中的文件名列表。

        ---------------------------------------------------------------------------
        """
        files = [f.name for f in path.iterdir() if f.is_file()]
        return files

    def __call__(
        self, 
        **kwargs: Any
    ):
        """
        ===========================================================================

        Allows updating instance attributes using keyword arguments.

        Parameters
        ----------
        **kwargs : Any
            Keyword arguments to set as instance attributes.

        ---------------------------------------------------------------------------

        允许使用关键字参数更新实例属性。

        参数
        ----------
        **kwargs : Any
            要设置为实例属性的关键字参数。

        ---------------------------------------------------------------------------
        """
        [setattr(self, i, j) for i,j in kwargs.items()]
