# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 09:26:48 2025

@author: Porco Rosso

"""
import numpy as np
import pandas as pd
import jqdatasdk as jq
from typing import Any, Dict, List, Union

from data_source.joinquant.config import TABLE_INFO_AND_PUBLIC_KEYS, FILTER
from libs import db
from libs.DB import config
from libs.utils.functions import filter_class_attrs, merge_dicts
from local.login_info import SOURCE


class main(db.__DB_CLASS_DIC__[SOURCE], TABLE_INFO_AND_PUBLIC_KEYS, FILTER, getattr(config, SOURCE)):
    """
    ===========================================================================

    Main class for JoinQuant metadata operations.

    This class serves as a base for other JoinQuant data source classes,
    providing common functionalities for data retrieval, standardization,
    and database interaction.

    ---------------------------------------------------------------------------

    JoinQuant 元数据操作的主类。

    此类作为其他 JoinQuant 数据源类的基础，提供数据检索、标准化和数据库交互的
    通用功能。

    ---------------------------------------------------------------------------
    """
    def __init__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Initializes the main class for JoinQuant metadata operations.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments.

        ---------------------------------------------------------------------------

        初始化 JoinQuant 元数据操作的主类。

        参数
        ----------
        **kwargs : Any
            任意关键字参数。

        ---------------------------------------------------------------------------
        """
        self.source = SOURCE
        super().__init__(**kwargs)
        self.__env_init__()
        self._stock = jq.get_all_securities('stock', date=None).index.tolist()
        trade_days = pd.to_datetime(jq.get_trade_days('2005-01-01')) + self.time_bias
        self._trade_days = trade_days[trade_days <= pd.Timestamp.today() - pd.Timedelta(4, 'h')]
    
    @property
    def columns(self) -> Dict:
        """
        ===========================================================================

        Returns the column information for the current table.

        This property dynamically retrieves and formats column metadata,
        including renaming and type mapping.

        Returns
        -------
        Dict
            A dictionary where keys are column names and values are their types.

        ---------------------------------------------------------------------------

        返回当前表的列信息。

        此属性动态检索和格式化列元数据，包括重命名和类型映射。

        返回
        -------
        Dict
            一个字典，其中键是列名，值是其类型。

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

        Renames columns of the input DataFrame based on predefined mappings.

        This internal method handles column renaming and ensures consistency
        across different data sources, including handling multi-level columns.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame whose columns need to be renamed.

        Returns
        -------
        pd.DataFrame
            The DataFrame with renamed columns.

        ---------------------------------------------------------------------------

        根据预定义的映射重命名输入 DataFrame 的列。

        此内部方法处理列重命名并确保不同数据源之间的一致性，包括处理多级列。

        参数
        ----------
        df : pd.DataFrame
            需要重命名列的 DataFrame。

        返回
        -------
        pd.DataFrame
            列已重命名的 DataFrame。

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

        Retrieves data from the JoinQuant remote API.

        This internal method executes the predefined JQ command to fetch raw data.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments to be formatted into the JQ command.

        Returns
        -------
        pd.DataFrame
            The raw DataFrame retrieved from the JoinQuant API.

        ---------------------------------------------------------------------------

        从 JoinQuant 远程 API 获取数据。

        此内部方法执行预定义的 JQ 命令以获取原始数据。

        参数
        ----------
        **kwargs : Any
            要格式化到 JQ 命令中的任意关键字参数。

        返回
        -------
        pd.DataFrame
            从 JoinQuant API 获取的原始 DataFrame。

        ---------------------------------------------------------------------------
        """
        df = eval(self.jq_command.format(**kwargs))
        return df

    def __data_standard__(self, df: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
        """
        ===========================================================================

        Standardizes the input DataFrame by renaming columns and converting date columns.

        This internal method ensures data consistency and handles common data issues
        like infinite values.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame to be standardized.
        **kwargs : Any
            Arbitrary keyword arguments, potentially containing date information.

        Returns
        -------
        pd.DataFrame
            The standardized DataFrame.

        ---------------------------------------------------------------------------

        通过重命名列和转换日期列来标准化输入 DataFrame。

        此内部方法确保数据一致性并处理常见的日期问题，例如无限值。

        参数
        ----------
        df : pd.DataFrame
            要标准化的 DataFrame。
        **kwargs : Any
            任意关键字参数，可能包含日期信息。

        返回
        -------
        pd.DataFrame
            标准化的 DataFrame。

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

        Executes the data pipeline for fetching and standardizing data.

        This method orchestrates the retrieval of raw data from JoinQuant
        and its subsequent standardization.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments passed to data retrieval and standardization methods.

        Returns
        -------
        pd.DataFrame
            The processed and standardized DataFrame.

        ---------------------------------------------------------------------------

        执行数据管道以获取和标准化数据。

        此方法协调从 JoinQuant 检索原始数据及其后续标准化。

        参数
        ----------
        **kwargs : Any
            传递给数据检索和标准化方法的任意关键字参数。

        返回
        -------
        pd.DataFrame
            处理和标准化后的 DataFrame。

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

        Finds the maximum value of a specified column in an existing table.

        This internal method is used to determine the starting point for fetching
        new data, ensuring data continuity.

        Parameters
        ----------
        columns : str
            The name of the column to find the maximum value from.
        **kwargs : Any
            Arbitrary keyword arguments passed to the internal read method.

        Returns
        -------
        Union[int, float, pd.Timestamp]
            The maximum value of the column, or a default value (trade_start or 0)
            if the table is empty or the column is not found.

        ---------------------------------------------------------------------------

        查找现有表中指定列的最大值。

        此内部方法用于确定获取新数据的起始点，确保数据连续性。

        参数
        ----------
        columns : str
            要查找最大值的列名。
        **kwargs : Any
            传递给内部读取方法的任意关键字参数。

        返回
        -------
        Union[int, float, pd.Timestamp]
            列的最大值，如果表为空或未找到列，则返回默认值（trade_start 或 0）。

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

        Creates a new table in the database based on the defined schema.

        This method constructs the table creation parameters and calls the
        superclass method to execute the table creation.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments to customize table creation.

        ---------------------------------------------------------------------------

        在数据库中根据定义的模式创建新表。

        此方法构造表创建参数并调用超类方法来执行表创建。

        参数
        ----------
        **kwargs : Any
            用于自定义表创建的任意关键字参数。

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

        super().__create_table__(**parameters)

    def drop_table(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Drops the current table from the database.

        This method constructs the table dropping parameters and calls the
        superclass method to execute the table deletion.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments to customize table dropping.

        ---------------------------------------------------------------------------

        从数据库中删除当前表。

        此方法构造表删除参数并调用超类方法来执行表删除。

        参数
        ----------
        **kwargs : Any
            用于自定义表删除的任意关键字参数。

        ---------------------------------------------------------------------------
        """
        parameters = self.__parameters__({'log': True}, kwargs)
        super().__drop_table__(**parameters)
        
    def table_exist(self):
        """
        ===========================================================================

        Checks if the current table exists in the database.

        Returns
        -------
        bool
            True if the table exists, False otherwise.

        ---------------------------------------------------------------------------

        检查当前表是否存在于数据库中。

        返回
        -------
        bool
            如果表存在则为 True，否则为 False。

        ---------------------------------------------------------------------------
        """
        return super().__table_exist__()
        
        
'''        
from local.login_info import JQ_LOGIN_INFO
import jqdatasdk as jq
jq.auth (**JQ_LOGIN_INFO)
    
from data_source.joinquant.config import ANN_DT_TABLES as config
config = config()
self = main(**config.asharebalancesheet)
self.daily()
        
 '''       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        