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

    Main class for handling tables indexed by Trade Date (TRADE_DT).

    This class inherits from the base metadata handler and provides the logic
    for daily updates of market data tables that are keyed by the trade date.
    It includes special handling for price adjustments and weight calculations.

    ---------------------------------------------------------------------------

    用于处理按交易日期（TRADE_DT）索引的表的主类。

    该类继承自基础元数据处理器，并提供了按交易日期为键的市场数据表
    的每日更新逻辑。它包含了对价格调整和权重计算的特殊处理。

    ---------------------------------------------------------------------------
    """
    def __init__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Initializes the TRADE_DT table handler.

        ---------------------------------------------------------------------------

        初始化 TRADE_DT 表处理器。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments passed to the parent class.

        ---------------------------------------------------------------------------

        参数
        ----------
        **kwargs : Any
            传递给父类的任意关键字参数。

        ---------------------------------------------------------------------------
        """
        super().__init__(**kwargs)

    def pipeline(self, **kwargs: Any) -> pd.DataFrame:
        """
        ===========================================================================

        Executes the data processing pipeline with special adjustments.

        This method calls the parent pipeline and then performs specific fixes:
        1. Calculates the percentage change (return) using adjusted prices first.
        2. Adjusts index weights from a scale of 100 to 1.
        3. Filters out rows with a high number of null values.

        ---------------------------------------------------------------------------

        执行带有特殊调整的数据处理流程。

        此方法调用父级流程，然后执行特定的修正：
        1. 优先使用调整后价格计算百分比变化（收益率）。
        2. 将指数权重从 100 的标度调整为 1。
        3. 过滤掉具有大量空值的行。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        **kwargs : Any
            Keyword arguments passed to the parent's pipeline method.

        ---------------------------------------------------------------------------

        参数
        ----------
        **kwargs : Any
            传递给父类 pipeline 方法的关键字参数。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            The processed and adjusted DataFrame.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            经过处理和调整的 DataFrame。

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

        Performs daily updates for the specified table.

        It fetches and writes data incrementally based on the last available
        trade date. It has special logic for handling full replacements for
        certain tables like 'asharelisting' and setting specific start dates
        for others like 'ashareconcept'.

        ---------------------------------------------------------------------------

        对指定的表执行每日更新。

        它根据表中最新的交易日期增量获取并写入数据。它包含特殊逻辑，
        用于处理特定表（如 'asharelisting'）的完全替换，并为其他表
        （如 'ashareconcept'）设置特定的起始日期。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        if_exists : Literal['append', 'replace'], default 'append'
            Specifies the behavior if the table already exists.
            - 'append': Adds new data to the existing table.
            - 'replace': Drops and recreates the table before writing data.

        ---------------------------------------------------------------------------

        参数
        ----------
        if_exists : Literal['append', 'replace'], 默认为 'append'
            指定当表已存在时的行为。
            - 'append': 将新数据追加到现有表中。
            - 'replace': 在写入数据前，删除并重新创建表。

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


'''
test:
config = config()

self = main(**config.asharelisting)
self.daily()
'''