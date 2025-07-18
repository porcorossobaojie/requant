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

    Main class for handling announcement date table data from JoinQuant.

    This class extends the meta class to provide specific data processing
    and daily update functionalities for announcement date related tables.

    ---------------------------------------------------------------------------

    处理 JoinQuant 公告日期表数据的主类。

    此类扩展了元类，为公告日期相关表提供特定的数据处理和每日更新功能。

    ---------------------------------------------------------------------------
    """
    def __init__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Initializes the main class for announcement date table operations.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments passed to the superclass constructor.

        ---------------------------------------------------------------------------

        初始化公告日期表操作的主类。

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

        Processes the data pipeline for announcement date tables.

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

        处理公告日期表的数据管道。

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
        return df

    def daily(self, if_exists: Literal['append', 'replace'] = 'append') -> None:
        """
        ===========================================================================

        Performs daily updates for the announcement date table.

        This method handles the logic for appending or replacing data based on
        the `if_exists` parameter, ensuring the table is up-to-date.

        Parameters
        ----------
        if_exists : Literal['append', 'replace'], optional
            Determines how to handle existing data. 'append' adds new data,
            'replace' drops the table and recreates it before adding data.
            Defaults to 'append'.

        ---------------------------------------------------------------------------

        执行公告日期表的每日更新。

        此方法根据 `if_exists` 参数处理追加或替换数据的逻辑，确保表格是最新的。

        参数
        ----------
        if_exists : Literal['append', 'replace'], optional
            确定如何处理现有数据。'append' 添加新数据，'replace' 在添加数据前
            删除并重新创建表格。默认为 'append'。

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
















