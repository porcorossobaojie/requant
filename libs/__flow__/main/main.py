# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 23:33:58 2025

@author: Porco Rosso
"""

from typing import Dict, Any, List, Optional, Union
import pandas as pd

from libs.__flow__.config import FILTER, COLUMNS_INFO, DB_INFO
from libs.__flow__.base.main import __table_info__, __table_attr__
from libs.__flow__.meta.main import data_source
from local.login_info import JQ_LOGIN_INFO

STOCK: Dict[str, Any] = {}
INDEX: Dict[str, Any] = {}

_TABLE_INFO_DIC: Dict[str, List[str]] = __table_info__('dict')
_TABLE_ATTRS: Dict[str, Dict[str, Any]] = {i:__table_attr__(i, j) for i,j in _TABLE_INFO_DIC.items()}
_HELP: pd.DataFrame = __table_info__('DataFrame')

for i,j in _TABLE_ATTRS.items():
    if 'aindex' in i:
        INDEX[i] = data_source(**j)
    else:
        STOCK[i] = data_source(**j)
        
try:
    import jqdatasdk as jq
    jq.auth(**JQ_LOGIN_INFO)
    days = jq.get_trade_days('2005-01-01')
    days = pd.Index([pd.to_datetime(i) + pd.Timedelta(15, 'h') for i in days], name=COLUMNS_INFO.trade_dt)
    days = days[days < pd.Timestamp.today() - pd.Timedelta(4, 'h')]
    
except:
    print('net work is not avaiable.')
    days = INDEX['aindexeodprices']('s_dq_pctchange').index
trade_days: pd.DatetimeIndex = days[days > pd.to_datetime(FILTER.ann_start)]

class stock():
    """
    ===========================================================================

    Provides access to stock-related data and functionalities.

    ---------------------------------------------------------------------------

    提供股票相关数据和功能。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self, 
        data_init: Optional[str] = None
    ):
        """
        ===========================================================================

        Initializes the stock data access object.

        Parameters
        ----------
        data_init : Optional[str], optional
            Specifies how to initialize the data. Defaults to None.

        ---------------------------------------------------------------------------

        初始化股票数据访问对象。

        参数
        ----------
        data_init : Optional[str], optional
            指定如何初始化数据。默认为 None。

        ---------------------------------------------------------------------------
        """
        self.not_init_tables = ['ashareorder', 'ashareconnect', 'ashareindicator', 'ashareconcept', 'ashareeo1mprices']
        self.data_init(data_init)

    def data_init(
        self, 
        how: str = 'full'
    ):
        """
        ===========================================================================

        Initializes or re-initializes the stock data for all available tables.

        Parameters
        ----------
        how : str, optional
            The method for data initialization (e.g., 'full'). Defaults to 'full'.

        ---------------------------------------------------------------------------

        初始化或重新初始化所有可用表的股票数据。

        参数
        ----------
        how : str, optional
            数据初始化方法（例如，'full'）。默认为 'full'。

        ---------------------------------------------------------------------------
        """
        for i,j in STOCK.items():
            if j.table not in self.not_init_tables:
                try:
                    j.data_init(how)
                except:
                    pass
            setattr(self, i, j)
            
    @property
    def _help(self) -> pd.DataFrame:
        """
        ===========================================================================

        Returns a filtered DataFrame of help information related to stock tables.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing help information for stock-related tables.

        ---------------------------------------------------------------------------

        返回与股票表相关的帮助信息的过滤DataFrame。

        返回
        -------
        pd.DataFrame
            包含股票相关表帮助信息的DataFrame。

        ---------------------------------------------------------------------------
        """
        return _HELP[_HELP.TABLE_NAME.str.contains('ashare')]
    
    def help(
        self, 
        key: str
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Searches for help information based on a given keyword.

        Parameters
        ----------
        key : str
            The keyword to search for in the help information.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing filtered help information.

        ---------------------------------------------------------------------------

        根据给定关键字搜索帮助信息。

        参数
        ----------
        key : str
            在帮助信息中搜索的关键字。

        返回
        -------
        pd.DataFrame
            包含过滤后的帮助信息的DataFrame。

        ---------------------------------------------------------------------------
        """
        x = pd.concat([(i.str.contains(key) | i.str.contains(key.upper())) for j, i in self._help.items()], axis=1).any(axis=1)
        return self._help[x]

    def __call__(
        self, 
        keys: Union[str, List[str]], 
        end: Optional[Any] = None, 
        quarter_adj: bool = False, 
        quarter_diff: int = 1, 
        shift: int = 0, 
        **kwargs: Any
    ) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        ===========================================================================

        Retrieves data for specified keys from various stock tables.

        Parameters
        ----------
        keys : Union[str, List[str]]
            A single key or a list of keys (column names) to retrieve data for.
        end : Optional[Any], optional
            The end date for data retrieval. Defaults to None.
        quarter_adj : bool, optional
            Whether to adjust data by quarter. Defaults to False.
        quarter_diff : int, optional
            Quarter difference for adjustment. Defaults to 1.
        shift : int, optional
            Shift for data. Defaults to 0.
        **kwargs : Any
            Additional keyword arguments passed to the data source.

        Returns
        -------
        Union[pd.DataFrame, Dict[str, pd.DataFrame]]
            A DataFrame or a dictionary of DataFrames containing the requested data.

        Raises
        -------
        ValueError
            If duplicated or non-existent keys are provided.

        ---------------------------------------------------------------------------

        从各种股票表中检索指定键的数据。

        参数
        ----------
        keys : Union[str, List[str]]
            要检索数据的单个键或键（列名）列表。
        end : Optional[Any], optional
            数据检索的结束日期。默认为 None。
        quarter_adj : bool, optional
            是否按季度调整数据。默认为 False。
        quarter_diff : int, optional
            季度调整的季度差异。默认为 1。
        shift : int, optional
            数据偏移。默认为 0。
        **kwargs : Any
            传递给数据源的附加关键字参数。

        返回
        -------
        Union[pd.DataFrame, Dict[str, pd.DataFrame]]
            包含请求数据的DataFrame或DataFrame字典。

        引发
        -------
        ValueError
            如果提供了重复或不存在的键。

        ---------------------------------------------------------------------------
        """
        keys = [keys.upper()] if isinstance(keys, str) else [i.upper() for i in keys]
        tables = self._help
        tables = tables[tables[DB_INFO.columns_info].isin(keys)]        
        
        duplicated_keys = tables[DB_INFO.columns_info][tables[DB_INFO.columns_info].duplicated()].values
        if len(duplicated_keys):
            raise ValueError(f"duplicated value '{duplicated_keys}' for parameter 'keys'")
        not_exist_keys = list(set(keys) - set(tables[DB_INFO.columns_info].values))
        if len(not_exist_keys):
            raise ValueError(f"not exist value '{not_exist_keys}' for parameter 'keys'")
            
        load_info = tables.groupby(DB_INFO.table_info)[DB_INFO.columns_info].apply(list).to_dict()
        load_info = {i: getattr(self, i)(j, end, quarter_adj, quarter_diff, shift, **kwargs) for i,j in load_info.items()}
        if len(load_info) == 1:
            return list(load_info.values())[0]
        else:
            return load_info
        
    def letter_finance(
        self, 
        key: Union[str, List[str]], 
        quarter_adj: bool = False, 
        quarter_diff: int = 1, 
        shift: int = 0, 
        periods: int = 1, 
        min_periods: Optional[int] = None, 
        letter_info: bool = True, 
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Retrieves and processes letter finance data, with optional adjustments.

        Parameters
        ----------
        key : Union[str, List[str]]
            The key(s) for the finance data.
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
        letter_info : bool, optional
            Whether to include letter information. Defaults to True.
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        pd.DataFrame
            Processed letter finance data.

        ---------------------------------------------------------------------------

        检索和处理信函财务数据，并进行可选调整。

        参数
        ----------
        key : Union[str, List[str]]
            财务数据的键。
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
        letter_info : bool, optional
            是否包含信函信息。默认为 True。
        **kwargs : Any
            附加关键字参数。

        返回
        -------
        pd.DataFrame
            处理后的信函财务数据。

        ---------------------------------------------------------------------------
        """
        key = [key.upper()] if isinstance(key, str) else [i.upper() for i in key]
        tables = self._help
        tables = tables[tables[DB_INFO.columns_info].isin(key)]
        load_info = tables.groupby(DB_INFO.table_info)[DB_INFO.columns_info].apply(list).to_dict()
        df = [getattr(self, i).__finance_history__(j, periods + shift, trade_days) for i,j in load_info.items()][0]
        if letter_info:
            tables = self._help
            tables = tables[tables[DB_INFO.columns_info].isin([key[0] + 'LT'])]
            letter_info = tables.groupby(DB_INFO.table_info)[DB_INFO.columns_info].apply(list).to_dict()
            if len(letter_info):
                print('letter information is added.')
                letters = [getattr(self, i).__finance_history__(j, periods + shift, trade_days) for i,j in letter_info.items()][0]
                df = df.fillna(letters.reindex_like(df))
        df = [getattr(self, i).__finance_history_adj__(df, quarter_adj, quarter_diff, shift, periods, min_periods, **kwargs) for i in load_info.keys()][0]
        return df
    
    def stock_finance(
        self, 
        key: Union[str, List[str]], 
        quarter_adj: bool = False, 
        quarter_diff: int = 1, 
        shift: int = 0, 
        periods: int = 1, 
        min_periods: Optional[int] = None, 
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Retrieves and processes stock finance data, with optional adjustments.

        Parameters
        ----------
        key : Union[str, List[str]]
            The key(s) for the finance data.
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
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        pd.DataFrame
            Processed stock finance data.

        ---------------------------------------------------------------------------

        检索和处理股票财务数据，并进行可选调整。

        参数
        ----------
        key : Union[str, List[str]]
            财务数据的键。
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
        **kwargs : Any
            附加关键字参数。

        返回
        -------
        pd.DataFrame
            处理后的股票财务数据。

        ---------------------------------------------------------------------------
        """
        key = [key.upper()] if isinstance(key, str) else [i.upper() for i in key]
        tables = self._help
        tables = tables[tables[DB_INFO.columns_info].isin(key)]
        load_info = tables.groupby(DB_INFO.table_info)[DB_INFO.columns_info].apply(list).to_dict()
        df = [getattr(self, i).__get__(j) for i,j in load_info.items()][0].iloc[:, 0]
        df = [getattr(self, i).__finance__(df, quarter_adj, quarter_diff, shift, periods, min_periods, trade_days) for i in load_info.keys()][0]
        return df
    
    
    def is_st(
        self, 
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Checks if a stock is marked as ST (Special Treatment) or other status.

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        pd.DataFrame
            A DataFrame indicating the ST status of stocks.

        ---------------------------------------------------------------------------

        检查股票是否被标记为ST（特别处理）或其他状态。

        参数
        ----------
        **kwargs : Any
            附加关键字参数。

        返回
        -------
        pd.DataFrame
            指示股票ST状态的DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_is_st'):
            try:
                delattr(self.asharestatus, '_internal_data')
            except:
                pass
            df = self.asharestatus.__get__('PUBLIC_STATUS_ID', where=None)
            status = {301001:0, 301002:1, 301003:2, 301005:3}
            df = df[df.isin(status.keys())].dropna()
            df = df['PUBLIC_STATUS_ID'].replace(status)[~df.index.duplicated()].unstack(COLUMNS_INFO.code)
            x = df.reindex(pd.date_range(df.index.min(), trade_days.max(), name=COLUMNS_INFO.trade_dt)).ffill().reindex(trade_days).sort_index(axis=1)
            self._is_st = x
        x = self._is_st
        x = x[x < 3].loc[FILTER.trade_start:]
        return x
    
    def be_list(
        self, 
        limit: int = 1, 
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates the number of days a stock has been listed.

        Parameters
        ----------
        limit : int, optional
            The minimum number of listed days for filtering. Defaults to 1.
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        pd.DataFrame
            A DataFrame indicating if a stock has been listed for at least `limit` days.

        ---------------------------------------------------------------------------

        计算股票上市天数。

        参数
        ----------
        limit : int, optional
            过滤的最小上市天数。默认为 1。
        **kwargs : Any
            附加关键字参数。

        返回
        -------
        pd.DataFrame
            一个DataFrame，指示股票是否已上市至少 `limit` 天。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_be_list'):
            df = self(['S_INFO_LISTDATE', 'S_INFO_DELISTDATE'], **kwargs).set_index('S_INFO_DELISTDATE', append=True).iloc[:, 0].unstack().T
            df = df.bfill().reindex(pd.date_range(df.min().min(), trade_days.max(), name=COLUMNS_INFO.trade_dt)).bfill().ffill()
            df = ((df.sub(df.index, axis=0).astype('int64') / 8.64e13) * -1).round(0)
            df.index = df.index + pd.Timedelta(15, 'h')
            df = df[df > 0]
            x = (df > 0).loc[trade_days]
            x = x.cumsum() + df.loc[x.index[0]].fillna(0)
            self._be_list = x
        x = self._be_list
        df = (x >= limit).loc[FILTER.trade_start:]
        return df

class index():
    """
    ===========================================================================

    Provides access to index-related data and functionalities.

    ---------------------------------------------------------------------------

    提供指数相关数据和功能。

    ---------------------------------------------------------------------------
    """
    def __init__(self):
        """
        ===========================================================================

        Initializes the index data access object.

        ---------------------------------------------------------------------------

        初始化指数数据访问对象。

        ---------------------------------------------------------------------------
        """
        [setattr(self, i, j) for i,j in INDEX.items()]
        
    @property
    def _help(self) -> pd.DataFrame:
        """
        ===========================================================================

        Returns a filtered DataFrame of help information related to index tables.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing help information for index-related tables.

        ---------------------------------------------------------------------------

        返回与指数表相关的帮助信息的过滤DataFrame。

        返回
        -------
        pd.DataFrame
            包含指数相关表帮助信息的DataFrame。

        ---------------------------------------------------------------------------
        """
        return _HELP[_HELP.TABLE_NAME.str.contains('aindex')]
    
    def help(
        self, 
        key: str
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Searches for help information based on a given keyword for index tables.

        Parameters
        ----------
        key : str
            The keyword to search for in the help information.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing filtered help information for index tables.

        ---------------------------------------------------------------------------

        根据给定关键字搜索指数表的帮助信息。

        参数
        ----------
        key : str
            在帮助信息中搜索的关键字。

        返回
        -------
        pd.DataFrame
            包含过滤后的指数表帮助信息的DataFrame。

        ---------------------------------------------------------------------------
        """
        x = pd.concat([(i.str.contains(key) | i.str.contains(key.upper())) for j, i in self._help.items()], axis=1).any(axis=1)
        return stock._help[x]
    
    def __call__(
        self, 
        keys: Union[str, List[str]], 
        end: Optional[Any] = None, 
        **kwargs: Any
    ) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        ===========================================================================

        Retrieves data for specified keys from various index tables.

        Parameters
        ----------
        keys : Union[str, List[str]]
            A single key or a list of keys (column names) to retrieve data for.
        end : Optional[Any], optional
            The end date for data retrieval. Defaults to None.
        **kwargs : Any
            Additional keyword arguments passed to the data source.

        Returns
        -------
        Union[pd.DataFrame, Dict[str, pd.DataFrame]]
            A DataFrame or a dictionary of DataFrames containing the requested data.

        Raises
        -------
        ValueError
            If duplicated or non-existent keys are provided.

        ---------------------------------------------------------------------------

        从各种指数表中检索指定键的数据。

        参数
        ----------
        keys : Union[str, List[str]]
            要检索数据的单个键或键（列名）列表。
        end : Optional[Any], optional
            数据检索的结束日期。默认为 None。
        **kwargs : Any
            传递给数据源的附加关键字参数。

        返回
        -------
        Union[pd.DataFrame, Dict[str, pd.DataFrame]]
            包含请求数据的DataFrame或DataFrame字典。

        引发
        -------
        ValueError
            如果提供了重复或不存在的键。

        ---------------------------------------------------------------------------
        """
        keys = [keys.upper()] if isinstance(keys, str) else [i.upper() for i in keys]
        tables = self._help
        tables = tables[tables[DB_INFO.columns_info].isin(keys)]
        
        duplicated_keys = tables[DB_INFO.columns_info][tables[DB_INFO.columns_info].duplicated()].values
        if len(duplicated_keys):
            raise ValueError(f"duplicated value '{duplicated_keys}' for parameter 'keys'")
        not_exist_keys = list(set(keys) - set(tables[DB_INFO.columns_info].values))
        if len(not_exist_keys):
            raise ValueError(f"not exist value '{not_exist_keys}' for parameter 'keys'")
            
        load_info = tables.groupby(DB_INFO.table_info)[DB_INFO.columns_info].apply(list).to_dict()
        load_info = {i: getattr(self, i)(j, end, **kwargs) for i,j in load_info.items()}
        if len(load_info) == 1:
            return list(load_info.values())[0]
        else:
            return load_info
    
    def index_member(
        self, 
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Retrieves and processes index member data.

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing processed index member data.

        ---------------------------------------------------------------------------

        检索和处理指数成分数据。

        参数
        ----------
        **kwargs : Any
            附加关键字参数。

        返回
        -------
        pd.DataFrame
            包含处理后的指数成分数据的DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_index_member'):
            df = self.__call__(['S_INFO_IDXCODE', 'S_DQ_IDXWEIGHT'], **kwargs)
            df['S_DQ_IDXWEIGHT'] = df['S_DQ_IDXWEIGHT']
            df.index.names = [COLUMNS_INFO.trade_dt, COLUMNS_INFO.code]
            dic = {}
            for i,j in df.groupby('S_INFO_IDXCODE'):
                j = j['S_DQ_IDXWEIGHT'].unstack()
                j = j.tools.fillna(sorted(set(pd.date_range(FILTER.ann_start, pd.Timestamp.today())) | set(j.index)))
                dic[i] = j
            df = pd.concat(dic, axis=1)
            df = df.reindex(trade_days).loc[FILTER.trade_start:]
            self._index_member = df
        df = self._index_member
        return df
