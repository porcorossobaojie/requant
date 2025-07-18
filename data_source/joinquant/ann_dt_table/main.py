# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 20:23:04 2025

@author: Porco Rosso

"""
from typing import Any, Literal

import pandas as pd

from data_source.joinquant.meta.main import main as meta


class main(meta):
    """
    ===========================================================================

    Main class for handling tables indexed by Announcement Date (ANN_DT).

    This class inherits from the base metadata handler and provides the logic
    for daily updates of financial tables that are keyed by the announcement
    date.

    ---------------------------------------------------------------------------

    用于处理按公告日期（ANN_DT）索引的表的主类。

    该类继承自基础元数据处理器，并提供了按公告日期为键的财务数据表
    的每日更新逻辑。

    ---------------------------------------------------------------------------
    """
    def __init__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Initializes the ANN_DT table handler.

        ---------------------------------------------------------------------------

        初始化 ANN_DT 表处理器。

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

        Executes the data processing pipeline.

        This method currently calls the parent class's pipeline directly.

        ---------------------------------------------------------------------------

        执行数据处理流程。

        此方法目前直接调用父类的处理流程。

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
            The processed DataFrame.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            处理后的 DataFrame。

        ---------------------------------------------------------------------------
        """
        df = super().pipeline(**kwargs)
        return df

    def daily(self, if_exists: Literal['append', 'replace'] = 'append') -> None:
        """
        ===========================================================================

        Performs daily updates for the specified table.

        It fetches and writes data incrementally based on the last available
        announcement date in the table.

        ---------------------------------------------------------------------------

        对指定的表执行每日更新。

        它根据表中最新的公告日期，增量获取并写入数据。

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
        if if_exists == 'replace':
            self.drop_table()

        if not self.table_exist():
            self.create_table()

        id_key = self.__find_max_of_exist_table__(self.id_key)
        df = self.pipeline(id_key=id_key)
        self.__write__(df, log=True)
        while len(df):
            id_key = df[self.id_key].max()
            df = self.pipeline(id_key=id_key)
            self.__write__(df, log=True)

'''
test:
    
    
from local.login_info import JQ_LOGIN_INFO
import jqdatasdk as jq
jq.auth (**JQ_LOGIN_INFO)
    
from data_source.joinquant.config import ANN_DT_TABLES as config
config = config()
self = main(**config.asharebalancesheet)
self.daily()
'''














