# -*- coding: utf-8 -*-
"""
Created on Mon May 12 22:08:09 2025

@author: Porco Rosso
"""

from account import meta_account, ACCOUNTS, PATH
from strategys.data_format import main as data_format_meta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import pandas as pd

class main(meta_account, data_format_meta):
    """
    ===========================================================================

    Manages account-related operations, including code standardization, order processing, and data saving.

    ---------------------------------------------------------------------------

    管理账户相关操作，包括代码标准化、订单处理和数据保存。

    ---------------------------------------------------------------------------
    """
    
    def code_standard(
        self, 
        obj: Any, 
        how: Optional[str] = None
    ) -> Any:
        """
        ===========================================================================

        Standardizes stock codes using the configured data format.

        Parameters
        ----------
        obj : Any
            The object containing stock codes to be standardized.
        how : Optional[str], optional
            Method for standardization. Defaults to None.

        Returns
        -------
        Any
            The standardized stock codes.

        ---------------------------------------------------------------------------

        使用配置的数据格式标准化股票代码。

        参数
        ----------
        obj : Any
            包含要标准化股票代码的对象。
        how : Optional[str], optional
            标准化方法。默认为 None。

        返回
        -------
        Any
            标准化后的股票代码。

        ---------------------------------------------------------------------------
        """
        x = self.__GET__.code_standard(obj, how)
        return x
        
    def order_standard(
        self, 
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Standardizes order DataFrame using the configured data format.

        Parameters
        ----------
        df : pd.DataFrame
            The input order DataFrame.

        Returns
        -------
        pd.DataFrame
            The standardized order DataFrame.

        ---------------------------------------------------------------------------

        使用配置的数据格式标准化订单DataFrame。

        参数
        ----------
        df : pd.DataFrame
            输入订单DataFrame。

        返回
        -------
        pd.DataFrame
            标准化后的订单DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self.__GET__.order_standard(df)
        return x
    
    def order_save(
        self, 
        standarded_order: pd.DataFrame
    ):
        """
        ===========================================================================

        Saves the standardized order DataFrame to the order path.

        Parameters
        ----------
        standarded_order : pd.DataFrame
            The standardized order DataFrame to save.

        ---------------------------------------------------------------------------

        将标准化订单DataFrame保存到订单路径。

        参数
        ----------
        standarded_order : pd.DataFrame
            要保存的标准化订单DataFrame。

        ---------------------------------------------------------------------------
        """
        self.__GET__.order_save(standarded_order, self.__order_path__)
    
    def settle_load(
        self, 
        file_name: str
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Loads settlement data from a specified file.

        Parameters
        ----------
        file_name : str
            The name of the file to load settlement data from.

        Returns
        -------
        pd.DataFrame
            The loaded settlement DataFrame.

        ---------------------------------------------------------------------------

        从指定文件加载结算数据。

        参数
        ----------
        file_name : str
            要加载结算数据的文件名。

        返回
        -------
        pd.DataFrame
            加载的结算DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.__GET__.settle_load(self.__settle_path__, file_name)
        return df
    
    def test_save(
        self, 
        test_obj: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Saves test data to the test path.

        Parameters
        ----------
        test_obj : Any
            The test object to save.

        Returns
        -------
        pd.DataFrame
            The saved test DataFrame.

        ---------------------------------------------------------------------------

        将测试数据保存到测试路径。

        参数
        ----------
        test_obj : Any
            要保存的测试对象。

        返回
        -------
        pd.DataFrame
            保存的测试DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.__GET__.test_save(test_obj, self.count, self.__test_path__)
        return df
    
    def last_settle(
        self, 
        how: int = -1
    ) -> Optional[pd.DataFrame]:
        """
        ===========================================================================

        Loads the last settlement file.

        Parameters
        ----------
        how : int, optional
            Index of the settlement file to load from the sorted list of files. Defaults to -1 (last file).

        Returns
        -------
        Optional[pd.DataFrame]
            The last settlement DataFrame, or None if no files exist.

        ---------------------------------------------------------------------------

        加载最后一个结算文件。

        参数
        ----------
        how : int, optional
            从排序的文件列表中加载的结算文件索引。默认为 -1（最后一个文件）。

        返回
        -------
        Optional[pd.DataFrame]
            最后一个结算DataFrame，如果不存在文件则为 None。

        ---------------------------------------------------------------------------
        """
        file_name = sorted(self.__get_files_name__(self.__settle_path__))
        if len(file_name):
            df = self.settle_load(file_name[how])
            return df
        else:
            return None
