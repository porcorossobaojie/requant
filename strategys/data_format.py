# -*- coding: utf-8 -*-
"""
Created on Mon May 12 14:48:58 2025

@author: admin
"""
import re
import pandas as pd
import data_source
import flow
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

class meta:
    """
    ===========================================================================

    Base class for data format handling, providing common methods for code standardization and test data saving.

    ---------------------------------------------------------------------------

    数据格式处理的基类，提供代码标准化和测试数据保存的通用方法。

    ---------------------------------------------------------------------------
    """
    @classmethod
    def code_standard(
        cls, 
        obj: Union[pd.DataFrame, pd.Series, List[Any]], 
        how: Optional[str] = None
    ) -> Union[pd.DataFrame, pd.Series, List[str]]:
        """
        ===========================================================================

        Standardizes stock codes to a consistent 6-digit format, optionally converting to JQData format.

        Parameters
        ----------
        obj : Union[pd.DataFrame, pd.Series, List[Any]]
            The input object containing stock codes (DataFrame, Series, or list).
        how : Optional[str], optional
            If 'jq', converts codes to JQData format. Defaults to None.

        Returns
        -------
        Union[pd.DataFrame, pd.Series, List[str]]
            The object with standardized stock codes.

        ---------------------------------------------------------------------------

        将股票代码标准化为一致的6位格式，可选转换为JQData格式。

        参数
        ----------
        obj : Union[pd.DataFrame, pd.Series, List[Any]]
            包含股票代码的输入对象（DataFrame、Series或列表）。
        how : Optional[str], optional
            如果为 'jq'，则将代码转换为JQData格式。默认为 None。

        返回
        -------
        Union[pd.DataFrame, pd.Series, List[str]]
            具有标准化股票代码的对象。

        ---------------------------------------------------------------------------
        """
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            if flow.config.COLUMNS_INFO.code == obj.index.name:
                x = [''.join(re.findall(r'\d+', str(i))).zfill(6) for i in obj.index]
                if how =='jq':
                    x = data_source.joinquant.normalize_code(x)
                obj.index = pd.Index(x, name=obj.index.name)
            elif flow.config.COLUMNS_INFO.code == obj.columns.name:
                x = [''.join(re.findall(r'\d+', str(i))).zfill(6) for i in obj.columns]
                if how =='jq':
                    x = data_source.joinquant.normalize_code(x)
                obj.columns = pd.Index(x, name=obj.columns.name)
            return obj
        else:
            x = [''.join(re.findall(r'\d+', str(i))).zfill(6) for i in obj]
            if how =='jq':
                x = data_source.joinquant.normalize_code(x)
            return x
        
    @classmethod
    def test_save(
        cls, 
        test_obj: pd.DataFrame, 
        count: int, 
        path: Path
    ):
        """
        ===========================================================================

        Saves test data to a CSV file.

        Parameters
        ----------
        test_obj : pd.DataFrame
            The DataFrame containing test data.
        count : int
            A numerical identifier for the test file.
        path : Path
            The directory path where the file will be saved.

        ---------------------------------------------------------------------------

        将测试数据保存到CSV文件。

        参数
        ----------
        test_obj : pd.DataFrame
            包含测试数据的DataFrame。
        count : int
            测试文件的数字标识符。
        path : Path
            文件将保存到的目录路径。

        ---------------------------------------------------------------------------
        """
        name = f'{count}_stock_predict_{test_obj.columns[-2].date()}.csv'
        all_path = str(path / name)
        test_obj.to_csv(all_path, encoding='gbk')
                

class tonghua(meta):
    """
    ===========================================================================

    Handles data formatting specific to the 'tonghua' system.

    ---------------------------------------------------------------------------

    处理'tonghua'系统特有的数据格式。

    ---------------------------------------------------------------------------
    """
    order_rename: Dict[str, str] = {flow.config.COLUMNS_INFO.code:'证券代码', 'share':'成份数量'}
    order_columns: List[str] = ['证券代码','成份数量'] #'资金比例%']
    settle_rename: Dict[str, str] = {'证券代码': flow.config.COLUMNS_INFO.code}
    settle_columns: List[str] = ['证券代码', '股票余额', '持仓数量', '成份数量', '当前数量']
    
    @classmethod
    def order_standard(
        cls, 
        df: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """
        ===========================================================================

        Standardizes an order DataFrame for the 'tonghua' system.

        Parameters
        ----------
        df : pd.DataFrame
            The input order DataFrame.

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary containing standardized buy, sell, and detail order DataFrames.

        ---------------------------------------------------------------------------

        为'tonghua'系统标准化订单DataFrame。

        参数
        ----------
        df : pd.DataFrame
            输入订单DataFrame。

        返回
        -------
        Dict[str, pd.DataFrame]
            包含标准化买入、卖出和详细订单DataFrames的字典。

        ---------------------------------------------------------------------------
        """
        x = cls.code_standard(df).reset_index().rename(cls.order_rename, axis=1).reindex(cls.order_columns, axis=1)
        buy = x[(x.iloc[:, 1:] > 0).any(axis=1)]
        sell = x[(x.iloc[:, 1:] < 0).any(axis=1)]
        sell.iloc[:, 1] = sell.iloc[:, 1].abs()
        x = {f'buy_{df.columns[-1].date()}.csv':buy.astype(int), f'sell_{df.columns[-1].date()}.csv':sell.astype(int), f'detail_{df.columns[-1].date()}.csv': df.reset_index()}
        return x
    
    @classmethod
    def order_save(
        cls, 
        standarded_order: Dict[str, pd.DataFrame], 
        path: Path
    ):
        """
        ===========================================================================

        Saves standardized order DataFrames to CSV files.

        Parameters
        ----------
        standarded_order : Dict[str, pd.DataFrame]
            A dictionary of standardized order DataFrames.
        path : Path
            The directory path where the files will be saved.

        ---------------------------------------------------------------------------

        将标准化订单DataFrame保存到CSV文件。

        参数
        ----------
        standarded_order : Dict[str, pd.DataFrame]
            标准化订单DataFrames的字典。
        path : Path
            文件将保存到的目录路径。

        ---------------------------------------------------------------------------
        """
        for i,j in standarded_order.items():
            j.to_csv(str(path / i), index=False)
            
    @classmethod
    def settle_load(
        cls, 
        path: Path, 
        file_name: str
    ) -> pd.Series:
        """
        ===========================================================================

        Loads settlement data from a CSV file for the 'tonghua' system.

        Parameters
        ----------
        path : Path
            The directory path where the settlement file is located.
        file_name : str
            The name of the settlement file.

        Returns
        -------
        pd.Series
            A Series containing the loaded and standardized settlement data.

        ---------------------------------------------------------------------------

        为'tonghua'系统从CSV文件加载结算数据。

        参数
        ----------
        path : Path
            结算文件所在的目录路径。
        file_name : str
            结算文件的名称。

        返回
        -------
        pd.Series
            包含加载和标准化结算数据的Series。

        ---------------------------------------------------------------------------
        """
        all_file_name = str(path / file_name)
        date = pd.to_datetime(pd.to_datetime(file_name.split('.')[0]).date()) + pd.Timedelta(15, 'h')
        try:
            df = (pd.read_csv(all_file_name, encoding='gbk', sep='\t')
                  .reindex(cls.settle_columns, axis=1).rename(cls.settle_rename, axis=1).dropna(how='all', axis=1)
                  .set_index(flow.config.COLUMNS_INFO.code).iloc[:, 0].rename(date))
        except:
            df = (pd.read_csv(all_file_name, encoding='gbk')
                  .reindex(cls.settle_columns, axis=1).rename(cls.settle_rename, axis=1).dropna(how='all', axis=1)
                  .set_index(flow.config.COLUMNS_INFO.code).iloc[:, 0].rename(date))
            
        if df.index[-1] == 'cash':
            cash = df.iloc[-1]
            df = df.iloc[:-1]
        else:
            cash = 0
        df = cls.code_standard(df, how='jq')
        df = pd.to_Series(df, cash=cash, state='settle', unit='share', is_adj=False)
        return df
    
class main():
    """
    ===========================================================================

    Main class for managing different data format handlers.

    ---------------------------------------------------------------------------

    管理不同数据格式处理程序的主类。

    ---------------------------------------------------------------------------
    """
    tonghua: tonghua = tonghua
