# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 09:26:48 2025

@author: Porco Rosso

"""
from typing import Any, Dict, List, Union

import jqdatasdk as jq
import numpy as np
import pandas as pd

from data_source.config import DATABASE as META_DATABASE
from data_source.joinquant.config import DATABASE, FILTER
from libs import __DB_CLASS__
from libs.utils.functions import filter_class_attrs, merge_dicts


class main(__DB_CLASS__, META_DATABASE):
    """
    ===========================================================================

    The main class for handling metadata from JoinQuant.

    This class is responsible for fetching, standardizing, and managing metadata
    related to stocks, trade days, and other market information. It serves as a
    base class for more specific data source handlers.

    ---------------------------------------------------------------------------

    用于处理聚宽元数据的主类。

    该类负责获取、标准化和管理与股票、交易日及其他市场信息相关的元数据。
    它作为更具体数据源处理器的基类。

    ---------------------------------------------------------------------------
    """

    source = META_DATABASE.source

    def __init__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Initializes the main metadata handler class.

        It merges configuration parameters from various sources and initializes
        the parent database class.

        ---------------------------------------------------------------------------

        初始化元数据处理器主类。

        它合并来自不同来源的配置参数，并初始化父数据库类。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments that will be passed to the parent class
            and used for configuration.

        ---------------------------------------------------------------------------

        参数
        ----------
        **kwargs : Any
            将被传递给父类并用于配置的任意关键字参数。

        ---------------------------------------------------------------------------
        """
        parameters = (
            filter_class_attrs(DATABASE) | kwargs | filter_class_attrs(FILTER)
            )
        super().__init__(**parameters)
        self.__env_init__()
        self._stock = jq.get_all_securities('stock', date=None).index.tolist()
        trade_days = pd.to_datetime(jq.get_trade_days('2005-01-01')) + DATABASE.time_bias
        self._trade_days = trade_days[trade_days <= pd.Timestamp.today() - pd.Timedelta(5, 'h')]


    @property
    def columns(self) -> Dict:
        """
        ===========================================================================

        Generates a dictionary of column information for the database table.

        It processes the `columns_information` attribute to create a standardized
        dictionary mapping column names to their data types and properties.

        ---------------------------------------------------------------------------

        为数据库表生成列信息的字典。

        它处理 `columns_information` 属性，以创建一个将列名映射到其数据类型
        和属性的标准化字典。

        ---------------------------------------------------------------------------

        Returns
        -------
        Dict
            A dictionary where keys are uppercase column names and values are their
            properties (e.g., data type).

        ---------------------------------------------------------------------------

        返回
        -------
        Dict
            一个字典，其中键是转换成大写的列名，值是它们的属性（例如，数据类型）。

        ---------------------------------------------------------------------------
        """
        if isinstance(self.columns_information, dict):
            x = merge_dicts(*list(self.columns_information.values()))
        else:
            x = jq.get_table_info(self.columns_information)
            x.iloc[:, 0] = x.iloc[:, 0].replace(self.columns_replace).str.upper()
            x.iloc[:, 2] = x.iloc[:, 2].replace({'date': 'datetime', 'DATE': 'datetime'})
            x = x.set_index(x.columns[0]).iloc[:, [1, 0]].T.to_dict('list')
        return x

    def __columns_rename__(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ===========================================================================

        Renames and filters the columns of a DataFrame.

        This method renames columns based on predefined mappings and filters them
        to keep only the columns specified in the `self.columns` property.

        ---------------------------------------------------------------------------

        重命名并筛选 DataFrame 的列。

        此方法根据预定义的映射重命名列，并进行筛选，只保留 `self.columns`
        属性中指定的列。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame whose columns need to be renamed.

        ---------------------------------------------------------------------------

        参数
        ----------
        df : pd.DataFrame
            需要重命名列的输入 DataFrame。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            A DataFrame with renamed, uppercased, and filtered columns.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            一个列经过重命名、大写转换和筛选的 DataFrame。

        ---------------------------------------------------------------------------
        """
        if isinstance(self.columns_information, dict):
            rename_dic = {i: list(j.keys())[0] for i, j in self.columns_information.items()}
        else:
            rename_dic = self.columns_replace
        df = df.reset_index().rename(rename_dic, axis=1)
        # it may be multi index here(individual_table.ashareindustrys)
        # and it is impossible to reanme from 2-dim multi-index object to 1-dim index
        # so it fix the problem here
        if df.columns.nlevels > 1:
            df.columns = [rename_dic.get(col, col) for col in df.columns]
        df.columns = df.columns.str.upper()
        df = df.loc[:, df.columns.isin(list(self.columns.keys()))]
        return df

    def __get_data_from_jq_remote__(self, **kwargs: Any) -> pd.DataFrame:
        """
        ===========================================================================

        Fetches data from the JoinQuant remote API.

        It executes a command stored in `self.jq_command` to retrieve data.

        ---------------------------------------------------------------------------

        从聚宽远程 API 获取数据。

        它执行存储在 `self.jq_command` 中的命令来检索数据。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        **kwargs : Any
            Keyword arguments to be formatted into the `jq_command` string.

        ---------------------------------------------------------------------------

        参数
        ----------
        **kwargs : Any
            用于格式化 `jq_command` 字符串的关键字参数。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the data fetched from JoinQuant.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            一个包含从聚宽获取的数据的 DataFrame。

        ---------------------------------------------------------------------------
        """
        df = eval(self.jq_command.format(**kwargs))
        return df

    def __data_standard__(self, df: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
        """
        ===========================================================================

        Standardizes the fetched data.

        This method performs several standardization steps, including renaming
        columns, converting date columns to datetime objects, and handling
        infinite values.

        ---------------------------------------------------------------------------

        标准化获取的数据。

        此方法执行多个标准化步骤，包括重命名列、将日期列转换为 datetime 对象
        以及处理无穷大值。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        df : pd.DataFrame
            The raw DataFrame to be standardized.
        **kwargs : Any
            Additional keyword arguments, may contain 'date' for filling
            missing date values.

        ---------------------------------------------------------------------------

        参数
        ----------
        df : pd.DataFrame
            需要被标准化的原始 DataFrame。
        **kwargs : Any
            额外的关键字参数，可能包含用于填充缺失日期值的 'date'。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            The standardized DataFrame.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            标准化后的 DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.__columns_rename__(df)
        for i in [self.ann_dt, self.trade_dt]:
            if i in df.columns:
                df[i] = pd.to_datetime(df[i]) + self.time_bias
            if (i not in df.columns) and i in self.columns.keys():
                try:
                    df[i] = pd.to_datetime(kwargs['date']) + self.time_bias
                except KeyError:
                    pass
        df = df.replace({np.inf: np.nan, -np.inf: np.nan})
        return df

    def pipeline(self, **kwargs: Any) -> pd.DataFrame:
        """
        ===========================================================================

        The main data processing pipeline.

        It orchestrates the process of fetching data from the remote source and
        then standardizing it.

        ---------------------------------------------------------------------------

        主数据处理流程。

        它协调从远程源获取数据然后进行标准化的整个过程。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        **kwargs : Any
            Keyword arguments passed to the fetching and standardization methods.

        ---------------------------------------------------------------------------

        参数
        ----------
        **kwargs : Any
            传递给数据获取和标准化方法的关键字参数。

        ---------------------------------------------------------------------------

        Returns
        -------
        pd.DataFrame
            The final, processed DataFrame.

        ---------------------------------------------------------------------------

        返回
        -------
        pd.DataFrame
            最终处理完成的 DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.__get_data_from_jq_remote__(**kwargs)
        df = self.__data_standard__(df, **kwargs)
        return df

    def __find_max_of_exist_table__(
        self, columns: str, **kwargs: Any
        ) -> Union[int, float, pd.Timestamp]:
        """
        ===========================================================================

        Finds the maximum value of a column in an existing table.

        This is typically used to determine the starting point for incremental
        data updates.

        ---------------------------------------------------------------------------

        在现有表中查找某一列的最大值。

        这通常用于确定增量数据更新的起始点。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        columns : str
            The name of the column to find the maximum value of.
        **kwargs : Any
            Additional keyword arguments passed to the read method.

        ---------------------------------------------------------------------------

        参数
        ----------
        columns : str
            需要查找最大值的列名。
        **kwargs : Any
            传递给读取方法的额外关键字参数。

        ---------------------------------------------------------------------------

        Returns
        -------
        Union[int, float, pd.Timestamp]
            The maximum value found in the column, or a default start value if
            the table or value does not exist.

        ---------------------------------------------------------------------------

        返回
        -------
        Union[int, float, pd.Timestamp]
            在列中找到的最大值，如果表或值不存在，则返回默认起始值。

        ---------------------------------------------------------------------------
        """
        id_key = None
        if self.table_exist():
            id_key = self.__read__(columns=f'MAX({columns})', show_time=False, **kwargs).iloc[0, 0]
            id_key = None if pd.isnull(id_key) else id_key

        if id_key is None:
            if 'DATE' in self.columns.get(columns, ['None'])[0].upper():
                id_key = self.trade_start
            else:
                id_key = 0
        return id_key

    def create_table(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Creates a database table based on the class's configuration.

        It prepares the necessary parameters, such as column definitions and
        partitioning keys, and then calls the parent class's method to
        execute the table creation.

        ---------------------------------------------------------------------------

        根据类的配置创建数据库表。

        它准备必要的参数，如列定义和分区键，然后调用父类的方法来执行
        表的创建。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments to customize table creation.

        ---------------------------------------------------------------------------

        参数
        ----------
        **kwargs : Any
            用于自定义表创建的额外关键字参数。

        ---------------------------------------------------------------------------
        """
        parameters = {'columns': self.columns, 'log': True}
        if self.source == 'MySQL':
            keys = (
                self.ann_dt
                if self.trade_dt not in self.columns.keys()
                else self.trade_dt
                )
            partition = None if keys != self.trade_dt else {self.trade_dt: self.partition}
            parameters = (
                self.__parameters__()
                | {'keys': keys, 'partition': partition}
                | {'columns': self.columns, 'log': True}
                | kwargs
                )
        else:
            parameters = self.__parameters__(parameters, kwargs)

        super().create_table(**parameters)

    def drop_table(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Drops the database table.

        ---------------------------------------------------------------------------

        删除数据库表。

        ---------------------------------------------------------------------------

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments passed to the parent's drop_table method.

        ---------------------------------------------------------------------------

        参数
        ----------
        **kwargs : Any
            传递给父类的 drop_table 方法的额外关键字参数。

        ---------------------------------------------------------------------------
        """
        parameters = self.__parameters__({'log': True}, kwargs)
        super().drop_table(**parameters)