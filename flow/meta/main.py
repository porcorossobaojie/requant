# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 23:16:33 2025

@author: Porco Rosso
"""

from flow.config import COLUMNS_INFO
from flow.base.main import __source__
import pandas as pd
from typing import Any, List, Optional, Union, Tuple

from libs.DB import config as meta_config
from libs.utils.functions import filter_parent_class_attrs as __filter_class_attrs__


class data_source(__source__(), COLUMNS_INFO):
    """
    ===========================================================================

    A class for managing and accessing financial data from a SQL database.
    It extends both the SQL login capabilities and database configuration.

    ---------------------------------------------------------------------------

    一个用于管理和访问SQL数据库中财务数据的类。
    它扩展了SQL登录功能和数据库配置。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self, 
        **kwargs: Any
    ):
        """
        ===========================================================================

        Initializes the data_source object with database connection parameters.

        Parameters
        ----------
        **kwargs : Any
            Keyword arguments for database connection and table configuration.

        ---------------------------------------------------------------------------

        使用数据库连接参数初始化data_source对象。

        参数
        ----------
        **kwargs : Any
            数据库连接和表配置的关键字参数。

        ---------------------------------------------------------------------------
        """
        super().__init__(**kwargs)
        
    @property    
    def index_keys(self) -> List[str]:
        """
        ===========================================================================

        Determines the primary index keys for the data based on database configuration.

        Returns
        -------
        List[str]
            A list of column names to be used as index keys.

        ---------------------------------------------------------------------------

        根据数据库配置确定数据的主索引键。

        返回
        -------
        List[str]
            用作索引键的列名列表。

        ---------------------------------------------------------------------------
        """
        keys = (([self.ann_dt, self.report_period] 
                if self.trade_dt not in self.columns else [self.trade_dt]) 
                + [self.code])
        return keys
        
    @property
    def filter_key(self) -> str:
        """
        ===========================================================================

        Returns the primary key used for filtering data.

        Returns
        -------
        str
            The column name used as the filter key.

        ---------------------------------------------------------------------------

        返回用于过滤数据的主键。

        返回
        -------
        str
            用作过滤键的列名。

        ---------------------------------------------------------------------------
        """
        return self.index_keys[0]

    def __standard_columns__(
        self, 
        columns: Union[str, List[str]]
    ) -> List[str]:
        """
        ===========================================================================

        Standardizes column names to uppercase and checks for existence in the table.

        Parameters
        ----------
        columns : Union[str, List[str]]
            A single column name or a list of column names to standardize.

        Returns
        -------
        List[str]
            A list of standardized (uppercase) column names.

        Raises
        -------
        ValueError
            If any of the provided column names do not exist in the table.

        ---------------------------------------------------------------------------

        将列名标准化为大写并检查其在表中是否存在。

        参数
        ----------
        columns : Union[str, List[str]]
            要标准化的单个列名或列名列表。

        返回
        -------
        List[str]
            标准化（大写）列名列表。

        引发
        -------
        ValueError
            如果提供的任何列名在表中不存在。

        ---------------------------------------------------------------------------
        """
        columns = [columns.upper()] if isinstance(columns, str) else [i.upper() for i in columns]
        not_have_columns = [i for i in columns if i not in self.columns]
        if not len(not_have_columns):
            return columns
        else:
            raise ValueError(f"Invalid value '{not_have_columns}' for parameter 'columns'. Valid values are: {self.columns}")
    
    def __read_from_db__(
        self, 
        columns: List[str], 
        **kwargs: Any
    ):
        """
        ===========================================================================

        Reads data from the SQL database and stores it internally.

        Parameters
        ----------
        columns : List[str]
            A list of column names to read from the database.
        **kwargs : Any
            Additional keyword arguments for the SQL read operation.

        ---------------------------------------------------------------------------

        从SQL数据库读取数据并内部存储。

        参数
        ----------
        columns : List[str]
            要从数据库读取的列名列表。
        **kwargs : Any
            SQL读取操作的附加关键字参数。

        ---------------------------------------------------------------------------
        """
        start = self.trade_start if self.filter_key == self.trade_dt else self.ann_start        
        if not hasattr(self, '_internal_data'):
            keys = [i for i in self.index_keys if i in self.columns]
            try:
                df = self.__read__(columns=keys + columns, where=kwargs.get('where', f"{self.filter_key} >= '{start}'"), show_time=True, **kwargs)
            except:
                df = self.__read__(columns=keys + columns, show_time=True, **kwargs)
                print(f"WARNING: UNSTANDARD LOADING ON DATA SOURCE <{self.table}>")
            if len(keys):
                df = df.set_index(keys)
            setattr(self, '_internal_data', df)
        else:
            columns = [i for i in columns if i not in self._internal_data.columns]
            if len(columns):
                try:
                    df = self.__read__(columns=columns, where=kwargs.get('where', f"{self.filter_key} >= '{start}'"))
                except:
                    df = self.__read__(columns=columns)
                    print(f"WARNING: UNSTANDARD LOADING ON DATA SOURCE <{self.table}>")
                self._internal_data[columns] = df.values
            
        if self.filter_key == self.trade_dt:
            try:
                [setattr(self, i, self._internal_data[i].unstack(self.filter_key).T.sort_index())  for i in columns]
            except:
                pass

    def __get__(
        self, 
        columns: Union[str, List[str]], 
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Retrieves specified columns from the internal data or loads them from SQL.

        Parameters
        ----------
        columns : Union[str, List[str]]
            A single column name or a list of column names to retrieve.
        **kwargs : Any
            Additional keyword arguments for the SQL read operation.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the requested columns.

        ---------------------------------------------------------------------------

        从内部数据中检索指定列或从SQL加载它们。

        参数
        ----------
        columns : Union[str, List[str]]
            要检索的单个列名或列名列表。
        **kwargs : Any
            SQL读取操作的附加关键字参数。

        返回
        -------
        pd.DataFrame
            包含请求列的DataFrame。

        ---------------------------------------------------------------------------
        """
        columns = self.__standard_columns__(columns)
        self.__read_from_db__(columns, **kwargs)
        
        if self.filter_key == self.trade_dt:
            if (len(columns) - 1):
                try:
                    df = pd.concat({i: getattr(self, i) for i in columns}, axis=1)
                    df.columns.names = ['VALUE'] + list(df.columns.names)[1:]
                except:
                    df = getattr(self, '_internal_data')[columns]
            else:
                try:
                    df = getattr(self, columns[0])
                except:
                    df = getattr(self, '_internal_data')[columns]
        else:
            df = getattr(self, '_internal_data')[columns]
        
        return df
    
    
    def __data_init__(
        self, 
        how: Optional[str] = None, 
        **kwargs: Any
    ):
        """
        ===========================================================================

        Initializes the internal data based on the specified method.

        Parameters
        ----------
        how : Optional[str], optional
            The initialization method: 'auto', 'full', or 'min'. Defaults to None.
        **kwargs : Any
            Additional keyword arguments for data loading.

        Raises
        -------
        ValueError
            If an invalid initialization method is provided.

        ---------------------------------------------------------------------------

        根据指定方法初始化内部数据。

        参数
        ----------
        how : Optional[str], optional
            初始化方法：'auto'、'full' 或 'min'。默认为 None。
        **kwargs : Any
            数据加载的附加关键字参数。

        引发
        -------
        ValueError
            如果提供了无效的初始化方法。

        ---------------------------------------------------------------------------
        """
        how = ('auto' if self.filter_key == self.trade_dt else 'full') if how is None else how
        if how == 'auto':
            if self.table:
                self.__read_from_db__([], **kwargs)
        elif how == 'full':
            self.__read_from_db__([i for i in self.columns if i not in self.index_keys], **kwargs)
        elif how == 'min' :
            pass
        else:
            raise ValueError(f"Invalid value '{how}' for parameter 'how'. Valid values are: {', '.join(['auto', 'full', 'min'])}")
            
    def data_init(
        self, 
        how: Optional[str] = None
    ):
        """
        ===========================================================================

        Public method to initialize the data.

        Parameters
        ----------
        how : Optional[str], optional
            The initialization method. Defaults to None.

        ---------------------------------------------------------------------------

        初始化数据的公共方法。

        参数
        ----------
        how : Optional[str], optional
            初始化方法。默认为 None。

        ---------------------------------------------------------------------------
        """
        return self.__data_init__(how)
        
            
    def __call__(
        self, 
        columns: Union[str, List[str]], 
        end: Optional[Any] = None, 
        quarter_adj: bool = False, 
        quarter_diff: int = 1, 
        shift: int = 0, 
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Retrieves and processes data for specified columns, with optional adjustments.

        Parameters
        ----------
        columns : Union[str, List[str]]
            A single column name or a list of column names to retrieve.
        end : Optional[Any], optional
            The end date for data retrieval. Defaults to None.
        quarter_adj : bool, optional
            Whether to adjust data by quarter. Defaults to False.
        quarter_diff : int, optional
            Quarter difference for adjustment. Defaults to 1.
        shift : int, optional
            Shift for data. Defaults to 0.
        **kwargs : Any
            Additional keyword arguments for data retrieval.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the processed data.

        ---------------------------------------------------------------------------

        检索和处理指定列的数据，并进行可选调整。

        参数
        ----------
        columns : Union[str, List[str]]
            要检索的单个列名或列名列表。
        end : Optional[Any], optional
            数据检索的结束日期。默认为 None。
        quarter_adj : bool, optional
            是否按季度调整数据。默认为 False。
        quarter_diff : int, optional
            季度调整的季度差异。默认为 1。
        shift : int, optional
            数据偏移。默认为 0。
        **kwargs : Any
            数据检索的附加关键字参数。

        返回
        -------
        pd.DataFrame
            包含处理后的数据的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.__get__(columns, **kwargs)
        if end is not None:
            df = df[df.index.get_level_values(self.filter_key) <= end]
        if self.ann_dt in df.index.names:
            df.index = df.index.droplevel(self.ann_dt)
            df = df.iloc[:, 0] if df.shape[1] == 1 else df
            try:
                df = df.unstack()
                filter_end = pd.Timestamp.today() if end is None else end
                df = df.reindex(pd.date_range(df.index.min(), filter_end, freq='QE', name=df.index.name))
                df = df.sort_index(axis=1).sort_index()
                if quarter_adj:
                    df = self.__finance_quarter_adjust__(df, quarter_adj, quarter_diff)
                if shift:
                    df = self.__finance_shift__(df, shift)
            except:
                pass
        return df

    
    def __finance_shift__(
        self, 
        df: pd.DataFrame, 
        n: int
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Shifts DataFrame columns if their last value is NaN, up to `n` times.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame to shift.
        n : int
            The maximum number of shifts to perform.

        Returns
        -------
        pd.DataFrame
            The DataFrame with columns conditionally shifted.

        ---------------------------------------------------------------------------

        如果DataFrame列的最后一个值为NaN，则有条件地移动该列，最多移动 `n` 次。

        参数
        ----------
        df : pd.DataFrame
            要移动的输入DataFrame。
        n : int
            要执行的最大移动次数。

        返回
        -------
        pd.DataFrame
            列有条件移动的DataFrame。

        ---------------------------------------------------------------------------
        """
        bools = df.iloc[-1].isnull()
        while n > 0 and bools.any():
            n -= 1
            df.loc[:, bools] = df.loc[:, bools].shift()
            bools = df.iloc[-1].isnull()
        return df
    
    def __finance_quarter_adjust__(
        self, 
        df: pd.DataFrame, 
        month: int, 
        quarter_diff: int
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Adjusts financial data by quarter, specifically for a given month.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame with financial data.
        month : int
            The month to use for quarter adjustment (e.g., 3 for Q1, 6 for Q2).
        quarter_diff : int
            The quarter difference for adjustment.

        Returns
        -------
        pd.DataFrame
            The DataFrame with quarter-adjusted financial data.

        ---------------------------------------------------------------------------

        按季度调整财务数据，特别是针对给定月份。

        参数
        ----------
        df : pd.DataFrame
            包含财务数据的输入DataFrame。
        month : int
            用于季度调整的月份（例如，Q1为3，Q2为6）。
        quarter_diff : int
            季度调整的季度差异。

        返回
        -------
        pd.DataFrame
            经过季度调整的财务数据DataFrame。

        ---------------------------------------------------------------------------
        """
        if self.report_period in df.index.names:
            day = 31 if month in [1,3,5,7,8,10,12] else (30 if month in [4, 6, 9, 11] else 28)
            index = df.index.get_level_values(self.report_period)
            tmp = df[(index.month == month) & (index.day == day)]
            df = df.diff(quarter_diff)
            df.loc[tmp.index] = tmp
        return df
    
    def __finance_history__(
        self, 
        column: str, 
        periods: int, 
        trade_dt: pd.DatetimeIndex
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Retrieves and processes historical financial data for a given column.

        Parameters
        ----------
        column : str
            The column name for which to retrieve historical data.
        periods : int
            The number of historical periods to retrieve.
        trade_dt : pd.DatetimeIndex
            A DatetimeIndex representing valid trading days.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the processed historical financial data.

        ---------------------------------------------------------------------------

        检索和处理给定列的历史财务数据。

        参数
        ----------
        column : str
            要检索历史数据的列名。
        periods : int
            要检索的历史周期数。
        trade_dt : pd.DatetimeIndex
            表示有效交易日的DatetimeIndex。

        返回
        -------
        pd.DataFrame
            包含处理后的历史财务数据的DataFrame。

        ---------------------------------------------------------------------------
        """
        df = self.__get__(column).iloc[:, 0]
        trade_dt = pd.Index(trade_dt, name=self.ann_dt)
        nature_dt = pd.date_range(trade_dt.min(), trade_dt.max())
        total_report_periods = pd.date_range(pd.Timestamp('2000-01-01'), pd.Timestamp.today(), freq='Q')
        
        df = df.unstack(self.ann_dt).T
        limit = pd.date_range('2000-12-31', periods=periods + 1, freq='q')
        limit = int((limit.max() - limit.min()).days)
        df = df.reindex(nature_dt).ffill(limit = limit).reindex(trade_dt)
        df = df.loc[self.ann_start:].stack(self.report_period)
        df = df[df.index.get_level_values(self.ann_dt) > df.index.get_level_values(self.report_period)]
        def fun(df: pd.DataFrame) -> pd.DataFrame:
            date = df.index.get_level_values(self.ann_dt)[0]
            needed = total_report_periods[total_report_periods <= date][-1 * (periods):]
            df.index = df.index.get_level_values(self.report_period)
            if not needed.isin(df.index).all():
                df = df.reindex(needed)
            return df
        df = df.groupby(self.ann_dt).apply(lambda x: fun(x))
        return df

    def __finance_history_adj__(
        self, 
        df: pd.DataFrame, 
        quarter_adj: Union[bool, int], 
        quarter_diff: int, 
        shift: int, 
        periods: int, 
        min_periods: Optional[int]
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Adjusts historical financial data based on quarter and applies shifting.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame with historical financial data.
        quarter_adj : Union[bool, int]
            If True or an integer (month), adjusts data by quarter. If an integer, specifies the month.
        quarter_diff : int
            The quarter difference for adjustment.
        shift : int
            The number of shifts to apply.
        periods : int
            The number of periods to keep after shifting.
        min_periods : Optional[int]
            Minimum number of non-null periods required per row.

        Returns
        -------
        pd.DataFrame
            The adjusted historical financial data.

        ---------------------------------------------------------------------------

        根据季度调整历史财务数据并应用移动。

        参数
        ----------
        df : pd.DataFrame
            包含历史财务数据的输入DataFrame。
        quarter_adj : Union[bool, int]
            如果为 True 或整数（月份），则按季度调整数据。如果为整数，则指定月份。
        quarter_diff : int
            季度调整的季度差异。
        shift : int
            要应用的移动次数。
        periods : int
            移动后要保留的周期数。
        min_periods : Optional[int]
            每行所需的非空最小周期数。

        返回
        -------
        pd.DataFrame
            调整后的历史财务数据。

        ---------------------------------------------------------------------------
        """
        if quarter_adj:
            tmp = df[(df.index.get_level_values(self.report_period).month == quarter_adj)]
            df = df.groupby(self.ann_dt).diff(quarter_diff)
            df.loc[tmp.index] = tmp
        
        def period(df: pd.DataFrame) -> pd.DataFrame:
            df.index = range(-df.shape[0], 0)
            df.index.name = self.report_period
            return df
        df = df.groupby(self.ann_dt).apply(lambda x: period(x))    
        df = df.unstack(self.ann_dt).dropna(how='all', axis=1).T
        
        bools = df.iloc[:, -1].isnull()
        while shift and bools.any():
            shift -= 1
            df.loc[bools] =  df.loc[bools].shift(axis=1)
            bools = df.iloc[:, -1].isnull()
        df = df.iloc[:, -periods:]
        
        if min_periods is not None:
            df = df[df.notnull().sum(axis=1) >= min_periods]
        df.index.names = [self.code, self.trade_dt]
        if df.shape[1] == 1:
            df = df.iloc[:, 0].unstack(self.code)
        else:
            df = df.unstack(self.trade_dt).T
            df.index = df.index.reorder_levels([self.trade_dt, self.report_period])
        
        df = df.sort_index().sort_index(axis=1)
        return df

    def __finance__(
        self, 
        df: pd.Series, 
        quarter_adj: bool = False, 
        quarter_diff: int = 1, 
        shift: int = 0, 
        periods: int = 1, 
        min_periods: Optional[int] = None, 
        trade_days: Optional[pd.DatetimeIndex] = None
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Processes financial data, handling quarter adjustments, shifting, and period filtering.

        Parameters
        ----------
        df : pd.Series
            The input Series of financial data.
        quarter_adj : bool, optional
            Whether to adjust data by quarter. Defaults to False.
        quarter_diff : int, optional
            Quarter difference for adjustment. Defaults to 1.
        shift : int, optional
            Shift for data. Defaults to 0.
        periods : int, optional
            Number of periods for historical data. Defaults to 1.
        min_periods : Optional[int], optional
            Minimum number of periods required. Defaults to None.
        trade_days : Optional[pd.DatetimeIndex], optional
            A DatetimeIndex representing valid trading days. Defaults to None.

        Returns
        -------
        pd.DataFrame
            The processed financial data as a DataFrame.

        ---------------------------------------------------------------------------

        处理财务数据，处理季度调整、移动和周期过滤。

        参数
        ----------
        df : pd.Series
            财务数据的输入Series。
        quarter_adj : bool, optional
            是否按季度调整数据。默认为 False。
        quarter_diff : int, optional
            季度调整的季度差异。默认为 1。
        shift : int, optional
            数据偏移。默认为 0。
        periods : int, optional
            历史数据的周期数。默认为 1。
        min_periods : Optional[int], optional
            所需的最小周期数。默认为 None。
        trade_days : Optional[pd.DatetimeIndex], optional
            表示有效交易日的DatetimeIndex。默认为 None。

        返回
        -------
        pd.DataFrame
            处理后的财务数据作为DataFrame。

        ---------------------------------------------------------------------------
        """
        total_report_periods = pd.date_range(pd.Timestamp('2000-01-01'), pd.Timestamp.today(), freq='Q')
        total_nature_days = pd.date_range(self.trade_start, pd.Timestamp.today(), freq='d')

        def report_periods_check(check_df: pd.DataFrame, date: pd.Timestamp) -> Tuple[pd.DataFrame, pd.DataFrame]:
            needed = total_report_periods[total_report_periods <= date][-1 * (shift+periods):]
            if not needed.isin(check_df.index).all():
                check_df = check_df.reindex(needed)
            obj = check_df.copy(deep=False)
            obj.index = range(-1*obj.shape[0], 0)
            return check_df, obj
        
            
        df = df.sort_index()
        
        if quarter_adj:
            tmp = df[(df.index.get_level_values(self.report_period).month == quarter_adj)]
            df = pd.merge(df.reset_index(), df.reset_index(self.ann_dt)[df.name].unstack().diff().unstack().to_frame(0), on=[self.report_period, self.code], how='left').set_index([self.ann_dt, self.report_period, self.code])[0]
            df.loc[tmp.index] = tmp
        
        meta_df, unmerged = df.loc[:self.trade_start], df.loc[self.trade_start:].unstack(self.code)
        meta_df.index = meta_df.index.droplevel(self.ann_dt)
        meta_df = meta_df.unstack(self.code).reindex(df.index.get_level_values(self.code).unique(), axis=1).sort_index(axis=1)
        meta_df, check_df = report_periods_check(meta_df, self.trade_start)

        dic = {}
        dic[pd.to_datetime(self.trade_start)] = check_df
        for i in total_nature_days:
            if i not in unmerged.index:
                meta_df, dic[i] = report_periods_check(meta_df, i)
            else:
                merger = unmerged.loc[i]
                unmerged = unmerged.iloc[merger.shape[0]:]
                if not merger.index.isin(meta_df.index).all():
                    meta_df = meta_df.reindex(meta_df.index.union(merger.index).sort_values())
                meta_df = meta_df.fillna(merger)
                meta_df, dic[i] = report_periods_check(meta_df, i)
        dic = {i: j for i,j in dic.items() if i in trade_days}
        dic = pd.concat(dic, axis=1).T
        dic.index.names = [self.trade_dt, self.code]
        dic.columns.names = [self.report_period]
        bools = dic.iloc[:, -1].isnull()
        while shift and bools.any():
            shift -= 1
            dic.loc[bools] =  dic.loc[bools].shift(axis=1)
            bools = dic.iloc[:, -1].isnull()
        dic = dic.iloc[:, -periods:]
        
        if min_periods is not None:
            dic = dic[dic.notnull().sum(axis=1) >= min_periods]
        if dic.shape[1] == 1:
            dic = dic.iloc[:, 0].unstack(self.code)
        else:
            dic = dic.unstack(self.trade_dt).T
            dic.index = dic.index.reorder_levels([self.trade_dt, self.report_period])
        dic = dic.sort_index().sort_index(axis=1)
        return dic
