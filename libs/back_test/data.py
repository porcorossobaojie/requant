# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 17:12:42 2025

@author: Porco Rosso
"""

import pandas as pd
import numpy as np
from libs.utils import functions as tools
import flow

from libs.back_test.config import DATA_INFO, TRADE_INFO
META_ATTRS = tools.filter_class_attrs(DATA_INFO) | tools.filter_class_attrs(TRADE_INFO)

class __data__():
    """
    ===========================================================================

    Manages the underlying market data for the backtesting framework.
    It loads EOD prices, processes trade status, and determines buyable/sellable flags.
    Serves as the central DATA_SOURCE for the backtesting engine.

    ---------------------------------------------------------------------------


    管理回测框架的底层市场数据。
    它加载日末价格，处理交易状态，并确定可买/可卖标志。
    作为回测引擎的中央数据源。

    ---------------------------------------------------------------------------
    """
    
    def __init__(self, **kwargs):
        """
        ===========================================================================

        Initializes the data source by loading market data and setting up trading parameters.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments to override default data or trade info attributes.

        Examples
        --------
        >>> # Initialize with a custom buy limit
        >>> data_source = __data__(buy_limit=0.01)

        ---------------------------------------------------------------------------


        通过加载市场数据和设置交易参数来初始化数据源。

        参数
        ----------
        **kwargs : Any
            用于覆盖默认数据或交易信息属性的任意关键字参数。

        示例
        --------
        >>> # 使用自定义买入限制进行初始化
        >>> data_source = __data__(buy_limit=0.01)

        ---------------------------------------------------------------------------
        """
        flow.stock.ashareeodprices.data_init('full')
        self._internal_data = flow.stock.ashareeodprices._internal_data
        
        self._internal_attributes = META_ATTRS.copy()
        parameters = self._internal_attributes.copy()
        parameters.update({'_' + i : j  for i,j in kwargs.items()})
        [setattr(self, i, j) for i,j in parameters.items()]
        self.__not_st_init__()
        self.__buyable_init__()
        self.__sellable_init__()
        self.trade_days = flow.trade_days()
        
    def __not_st_init__(self):
        """
        ===========================================================================

        Initializes the 'NOT_ST' filter based on the _not_st attribute.
        This filter identifies stocks that are not under Special Treatment (ST).

        Examples
        --------
        >>> # This method is called internally during initialization.
        >>> pass

        ---------------------------------------------------------------------------


        根据 _not_st 属性初始化 'NOT_ST' 过滤器。
        此过滤器用于识别非ST（特别处理）的股票。

        示例
        --------
        >>> # 此方法在初始化期间内部调用。
        >>> pass

        ---------------------------------------------------------------------------
        """
        self._internal_data[self._st_filter] = (flow.is_st() < self._not_st).stack()
    @property
    def not_st(self):
        """
        ===========================================================================

        Gets the current 'not_st' filter value.
        If the filter column is not in internal data, it will be initialized.

        Returns
        -------
        int
            The value representing the 'not_st' filter.

        Examples
        --------
        >>> data_source = __data__()
        >>> not_st_value = data_source.not_st
        >>> print(not_st_value)
        1

        ---------------------------------------------------------------------------


        获取当前的 'not_st' 过滤器值。
        如果内部数据中不存在该过滤器列，则会进行初始化。

        返回
        -------
        int
            表示 'not_st' 过滤器值。

        示例
        --------
        >>> data_source = __data__()
        >>> not_st_value = data_source.not_st
        >>> print(not_st_value)
        1

        ---------------------------------------------------------------------------
        """
        if self._st_filter not in self._internal_data.columns:
            self.__not_st_init__()
        return self._not_st
    @not_st.setter
    def not_st(self, v: int):
        """
        ===========================================================================

        Sets the 'not_st' filter value and re-initializes the filter.

        Parameters
        ----------
        v : int
            The new value for the 'not_st' filter.

        Examples
        --------
        >>> data_source = __data__()
        >>> data_source.not_st = 0

        ---------------------------------------------------------------------------


        设置 'not_st' 过滤器值并重新初始化过滤器。

        参数
        ----------
        v : int
            'not_st' 过滤器的新值。

        示例
        --------
        >>> data_source = __data__()
        >>> data_source.not_st = 0

        ---------------------------------------------------------------------------
        """
        self._not_st = v
        self.__not_st_init__()
        
    def __buyable_init__(self):
        """
        ===========================================================================

        Initializes the 'BUYABLE' flag based on the _buy_limit and _trade_price attributes.
        Determines if a stock is buyable based on its high limit and trade price.

        Examples
        --------
        >>> # This method is called internally during initialization.
        >>> pass

        ---------------------------------------------------------------------------


        根据 _buy_limit 和 _trade_price 属性初始化 'BUYABLE' 标志。
        根据股票的涨停价和交易价格判断是否可买。

        示例
        --------
        >>> # 此方法在初始化期间内部调用。
        >>> pass

        ---------------------------------------------------------------------------
        """
        self._internal_data[self._buyable] = ~((self._internal_data[self._high_limit] / self._internal_data[self._trade_price]  - 1) < self._buy_limit)
    @property
    def buy_limit(self):
        """
        ===========================================================================

        Gets the current buy limit percentage.

        Returns
        -------
        float
            The buy limit percentage.

        Examples
        --------
        >>> data_source = __data__()
        >>> buy_limit = data_source.buy_limit
        >>> print(buy_limit)
        0.005

        ---------------------------------------------------------------------------


        获取当前买入限制百分比。

        返回
        -------
        float
            买入限制百分比。

        示例
        --------
        >>> data_source = __data__()
        >>> buy_limit = data_source.buy_limit
        >>> print(buy_limit)
        0.005

        ---------------------------------------------------------------------------
        """
        return self._buy_limit
    @buy_limit.setter
    def buy_limit(self, v: float):
        """
        ===========================================================================

        Sets the buy limit percentage and re-initializes the 'BUYABLE' flag.

        Parameters
        ----------
        v : float
            The new buy limit percentage.

        Examples
        --------
        >>> data_source = __data__()
        >>> data_source.buy_limit = 0.01

        ---------------------------------------------------------------------------


        设置买入限制百分比并重新初始化 'BUYABLE' 标志。

        参数
        ----------
        v : float
            新的买入限制百分比。

        示例
        --------
        >>> data_source = __data__()
        >>> data_source.buy_limit = 0.01

        ---------------------------------------------------------------------------
        """
        self._buy_limit = v
        self.__buyable_init__()
        
    def __sellable_init__(self):
        """
        ===========================================================================

        Initializes the 'SELLABLE' flag based on the _sell_limit and _trade_price attributes.
        Determines if a stock is sellable based on its low limit and trade price.

        Examples
        --------
        >>> # This method is called internally during initialization.
        >>> pass

        ---------------------------------------------------------------------------


        根据 _sell_limit 和 _trade_price 属性初始化 'SELLABLE' 标志。
        根据股票的跌停价和交易价格判断是否可卖。

        示例
        --------
        >>> # 此方法在初始化期间内部调用。
        >>> pass

        ---------------------------------------------------------------------------
        """
        self._internal_data[self._sellable] = ~((1 - self._internal_data[self._low_limit] / self._internal_data[self._trade_price]) < self._sell_limit)
    @property
    def sell_limit(self):
        """
        ===========================================================================

        Gets the current sell limit percentage.

        Returns
        -------
        float
            The sell limit percentage.

        Examples
        --------
        >>> data_source = __data__()
        >>> sell_limit = data_source.sell_limit
        >>> print(sell_limit)
        0.005

        ---------------------------------------------------------------------------


        获取当前卖出限制百分比。

        返回
        -------
        float
            卖出限制百分比。

        示例
        --------
        >>> data_source = __data__()
        >>> sell_limit = data_source.sell_limit
        >>> print(sell_limit)
        0.005

        ---------------------------------------------------------------------------
        """
        return self._sell_limit
    @sell_limit.setter
    def sell_limit(self, v: float):
        """
        ===========================================================================

        Sets the sell limit percentage and re-initializes the 'SELLABLE' flag.

        Parameters
        ----------
        v : float
            The new sell limit percentage.

        Examples
        --------
        >>> data_source = __data__()
        >>> data_source.sell_limit = 0.01

        ---------------------------------------------------------------------------


        设置卖出限制百分比并重新初始化 'SELLABLE' 标志。

        参数
        ----------
        v : float
            新的卖出限制百分比。

        示例
        --------
        >>> data_source = __data__()
        >>> data_source.sell_limit = 0.01

        ---------------------------------------------------------------------------
        """
        self._sell_limit = v
        self.__sellable_init__()

    @property
    def trade_cost(self):
        """
        ===========================================================================

        Gets the current transaction cost percentage.

        Returns
        -------
        float
            The transaction cost percentage.

        Examples
        --------
        >>> data_source = __data__()
        >>> cost = data_source.trade_cost
        >>> print(cost)
        0.0005

        ---------------------------------------------------------------------------


        获取当前交易成本百分比。

        返回
        -------
        float
            交易成本百分比。

        示例
        --------
        >>> data_source = __data__()
        >>> cost = data_source.trade_cost
        >>> print(cost)
        0.0005

        ---------------------------------------------------------------------------
        """
        return self._trade_cost
    @trade_cost.setter
    def trade_cost(self, v: float):
        """
        ===========================================================================

        Sets the transaction cost percentage.

        Parameters
        ----------
        v : float
            The new transaction cost percentage.

        Examples
        --------
        >>> data_source = __data__()
        >>> data_source.trade_cost = 0.001

        ---------------------------------------------------------------------------


        设置交易成本百分比。

        参数
        ----------
        v : float
            新的交易成本百分比。

        示例
        --------
        >>> data_source = __data__()
        >>> data_source.trade_cost = 0.001

        ---------------------------------------------------------------------------
        """
        self._trade_cost = v
