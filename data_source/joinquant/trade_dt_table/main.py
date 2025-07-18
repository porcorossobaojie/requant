# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 20:23:04 2025

@author: Porco Rosso

"""
from typing import Any, Literal

import jqdatasdk as jq
import pandas as pd

from data_source.joinquant.config import TRADE_DT_TABLES as config
from data_source.joinquant.meta.main import main as meta


class main(meta):
    """
    ===========================================================================

    Main class for handling trade date table data from JoinQuant.

    This class extends the meta class to provide specific data processing
    and daily update functionalities for trade date related tables.

    ---------------------------------------------------------------------------

    处理 JoinQuant 交易日期表数据的主类。

    此类扩展了元类，为交易日期相关表提供特定的数据处理和每日更新功能。

    ---------------------------------------------------------------------------
    """
    def __init__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Initializes the main class for trade date table operations.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments passed to the superclass constructor.

        ---------------------------------------------------------------------------

        初始化交易日期表操作的主类。

        参数
        ----------
        **kwargs : Any
            传递给超类构造函数的任意关键字参数。

        ---------------------------------------------------------------------------
        """
        super().__init__(**kwargs)

    def pipeline(self, **kwargs: Any) -> pd.DataFrame:
        """
        ===========================================================================

        Processes the data pipeline for trade date tables.

        This method applies specific transformations and filters to the DataFrame
        obtained from the superclass pipeline.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments passed to the superclass pipeline.

        Returns
        -------
        pd.DataFrame
            The processed DataFrame.

        ---------------------------------------------------------------------------

        处理交易日期表的数据管道。

        此方法对从超类管道获取的 DataFrame 应用特定的转换和过滤。

        参数
        ----------
        **kwargs : Any
            传递给超类管道的任意关键字参数。

        返回
        -------
        pd.DataFrame
            处理后的 DataFrame。

        ---------------------------------------------------------------------------
        """
        df = super().pipeline(**kwargs)

        # special fix:
        # 1. construct returns of portfolio by calculated with close price(first use adj price if have)
        # 2. adjust weight total from 100 to 1
        pct_key = 'S_DQ_PCTCHANGE'
        weight_key = 'S_DQ_IDXWEIGHT'
        if pct_key in self.columns.keys():
            try:
                df[pct_key] = df['S_DQ_CLOSE_ADJ'] / df['S_DQ_PRECLOSE_ADJ'] - 1
            except Exception:
                df[pct_key] = df['S_DQ_CLOSE'] / df['S_DQ_PRECLOSE'] - 1
        if weight_key in self.columns.keys():
            df[weight_key] = df[weight_key] / 100

        df = df[df.notnull().sum(axis=1) > df.shape[1] * 0.6]
        return df

    def daily(self, if_exists: Literal['append', 'replace'] = 'append') -> None:
        """
        ===========================================================================

        Performs daily updates for the trade date table.

        This method handles the logic for appending or replacing data based on
        the `if_exists` parameter, ensuring the table is up-to-date.

        Parameters
        ----------
        if_exists : Literal['append', 'replace'], optional
            Determines how to handle existing data. 'append' adds new data,
            'replace' drops the table and recreates it before adding data.
            Defaults to 'append'.

        ---------------------------------------------------------------------------

        执行交易日期表的每日更新。

        此方法根据 `if_exists` 参数处理追加或替换数据的逻辑，确保表格是最新的。

        参数
        ----------
        if_exists : Literal['append', 'replace'], optional
            确定如何处理现有数据。'append' 添加新数据，'replace' 在添加数据前
            删除并重新创建表格。默认为 'append'。

        ---------------------------------------------------------------------------
        """
        if self.table == 'asharelisting':  # this table inform the on list time for each stock, which will replace every day
            if_exists = 'replace'

        if if_exists == 'replace':
            self.drop_table()

        if not self.table_exist():
            self.create_table()

        id_key = self.__find_max_of_exist_table__(self.trade_dt)
        if self.table == 'ashareconcept':  # this table inform the ’题材‘ and '概念' for which not have data at 2010, the earlest data appeared at 2015
            id_key = max(pd.to_datetime('2015-01-01 15:00'), id_key)
        days = self._trade_days.copy()
        days = days[days > id_key]
        if self.table == 'asharelisting' and len(days):
            days = days[-1:]

        for i in days:
            if jq.get_query_count()['spare'] <= 5000000:
                break
            df = self.pipeline(date=f'{i.date()}')
            print(i)
            self.__write__(df, log=True)


