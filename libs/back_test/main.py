# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 12:57:46 2025

@author: Porco Rosso
"""

from libs.back_test.data import __data__        
DATA_SOURCE = __data__()

from pandas import DataFrame as meta_DataFrame
from pandas import Series as meta_Series
import pandas as pd
import numpy as np
from typing import Union, List, Dict, Any, Optional, Tuple, Callable
from libs.utils import functions as tools


from libs.back_test.config import SERIES_ATTRIBUTES, TRADE_INFO
META_ATTRS = tools.filter_class_attrs(SERIES_ATTRIBUTES)
TRADE_INFO_ATTRS = tools.filter_class_attrs(TRADE_INFO)
            
class Series(meta_Series):
    """
    ===========================================================================

    A custom pandas Series designed for portfolio management in the backtesting framework.
    It extends standard Series with custom attributes and methods for unit conversion,
    portfolio information, and integration with trading rules.

    ---------------------------------------------------------------------------


    一个自定义的 pandas Series，专为回测框架中的投资组合管理而设计。
    它扩展了标准 Series，增加了用于单位转换、投资组合信息和交易规则集成的自定义属性和方法。

    ---------------------------------------------------------------------------
    """
    _internal_names = meta_Series._internal_names + []
    _internal_names_set = set(_internal_names)
    _metadata = meta_Series._metadata  + list(META_ATTRS.keys())

    @property
    def _constructor(self):
        return Series

    @property
    def _constructor_sliced(self):
        return Series    
    
    def __init__(self,
        data=None,
        index=None,
        dtype=None,
        name=None,
        copy=False,
        fastpath=False,
        **kwargs
    ):
        """
        ===========================================================================

        Initializes the custom Series object.

        Parameters
        ----------
        data : array-like, Iterable, dict, or Scalar, optional
            Data to be stored in the Series. Defaults to None.
        index : array-like or Index, optional
            Index for the Series. Defaults to None.
        dtype : numpy.dtype or ExtensionDtype, optional
            Data type for the Series. Defaults to None.
        name : str, optional
            Name for the Series. Defaults to None.
        copy : bool, optional
            Copy data if True. Defaults to False.
        fastpath : bool, optional
            Internal optimization. Defaults to False.
        **kwargs : Any
            Additional keyword arguments to set custom attributes like unit, state, cash, is_adj.

        ---------------------------------------------------------------------------


        初始化自定义 Series 对象。

        参数
        ----------
        data : array-like, Iterable, dict, or Scalar, optional
            要存储在 Series 中的数据。默认为 None。
        index : array-like or Index, optional
            Series 的索引。默认为 None。
        dtype : numpy.dtype or ExtensionDtype, optional
            Series 的数据类型。默认为 None。
        name : str, optional
            Series 的名称。默认为 None。
        copy : bool, optional
            如果为 True，则复制数据。默认为 False。
        fastpath : bool, optional
            内部优化。默认为 False。
        **kwargs : Any
            用于设置自定义属性（如 unit, state, cash, is_adj）的额外关键字参数。

        ---------------------------------------------------------------------------
        """
        params = META_ATTRS.copy()
        params.update({'_' + i: j for i,j in kwargs.items()})
        [setattr(self, i, j) for i,j in params.items()]
        self.__setup_property__()
        super().__init__(data, index, dtype, name, copy, fastpath)
        
    def __repr__(self) -> str:
        """
        ===========================================================================

        Returns a string representation of the Series, including custom attributes.

        Returns
        -------
        str
            String representation of the Series.

        ---------------------------------------------------------------------------


        返回 Series 的字符串表示，包括自定义属性。

        返回
        -------
        str
            Series 的字符串表示。

        ---------------------------------------------------------------------------
        """
        x = super().__repr__()
        x = x + '\nstate: %s, unit: %s, \ncount: %s, cash: %s, \nis_adj: %s' %(self.state, self.unit, len(self), round(self.cash, 3), self.is_adj)
        return x
    
    def __setup_property__(self):
        """
        ===========================================================================

        Sets up dynamic properties for trade information (e.g., buy_limit, sell_limit, trade_cost)
        from the global DATA_SOURCE object.

        ---------------------------------------------------------------------------


        从全局 DATA_SOURCE 对象设置交易信息（例如，买入限制、卖出限制、交易成本）的动态属性。

        ---------------------------------------------------------------------------
        """
        for key in TRADE_INFO_ATTRS:
            setattr(
                self.__class__, 
                key[1:], 
                property(
                    self.__create_property_getter__(key[1:]), 
                    self.__create_property_setter__(key[1:])
                )
            )
    
    def __create_property_getter__(self, key: str):
        """
        ===========================================================================

        Creates a getter function for dynamic properties linked to DATA_SOURCE.

        Parameters
        ----------
        key : str
            The attribute key to get from DATA_SOURCE.

        Returns
        -------
        callable
            A getter function.

        ---------------------------------------------------------------------------


        为链接到 DATA_SOURCE 的动态属性创建 getter 函数。

        参数
        ----------
        key : str
            要从 DATA_SOURCE 获取的属性键。

        返回
        -------
        callable
            一个 getter 函数。

        ---------------------------------------------------------------------------
        """
        def getter(self):
            return getattr(DATA_SOURCE, key)
        return getter
    
    def __create_property_setter__(self, key: str):
        """
        ===========================================================================

        Creates a setter function for dynamic properties linked to DATA_SOURCE.
        When a property is set, it updates DATA_SOURCE and reloads internal data.

        Parameters
        ----------
        key : str
            The attribute key to set in DATA_SOURCE.

        Returns
        -------
        callable
            A setter function.

        ---------------------------------------------------------------------------


        为链接到 DATA_SOURCE 的动态属性创建 setter 函数。
        设置属性时，它会更新 DATA_SOURCE 并重新加载内部数据。

        参数
        ----------
        key : str
            要在 DATA_SOURCE 中设置的属性键。

        返回
        -------
        callable
            一个 setter 函数。

        ---------------------------------------------------------------------------
        """
        def setter(self, value):
           setattr(DATA_SOURCE, key, value)
           # because of the values of BUYABLE/SELLABLE/NOT_ST columns in DATA_SOURCE._internal_data is UPDATED by limit CHANGING, 
           # Series need RELOAD data from DATA_SOURCE even trade_dt UNCHANGE
           self.__internal_data_update__(self.trade_dt) 
        return setter
        
    def __internal_data_update__(self, trade_dt: pd.Timestamp):
        """
        ===========================================================================

        Updates the internal market data for the current trading date.

        Parameters
        ----------
        trade_dt : pd.Timestamp
            The trading date to update the internal data for.

        Raises
        -------
        ValueError
            If unable to set the _internal_data attribute.

        ---------------------------------------------------------------------------


        更新当前交易日期的内部市场数据。

        参数
        ----------
        trade_dt : pd.Timestamp
            要更新内部数据的交易日期。

        引发
        -------
        ValueError
            如果无法设置 _internal_data 属性。

        ---------------------------------------------------------------------------
        """
        try:
            df = DATA_SOURCE._internal_data.loc[pd.to_datetime(trade_dt)]
            setattr(self, '_internal_data', df)
            setattr(self, '_internal_data_date', pd.to_datetime(trade_dt))
        except:
            raise ValueError("Fail to set attribute: <_internal_data>")
        
    @property
    def internal_data(self) -> pd.DataFrame:
        """
        ===========================================================================

        Gets the internal market data for the current trading date.
        If the data is not loaded or outdated, it will be updated.

        Returns
        -------
        pd.DataFrame
            The internal market data for the current trading date.

        ---------------------------------------------------------------------------


        获取当前交易日期的内部市场数据。
        如果数据未加载或已过期，则会进行更新。

        返回
        -------
        pd.DataFrame
            当前交易日期的内部市场数据。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_internal_data') or (self._internal_data_date != self.trade_dt):
            self.__internal_data_update__(self.trade_dt)
        return self._internal_data
    
    @property
    def name(self) -> pd.Timestamp:
        """
        ===========================================================================

        Gets the name of the Series, which represents the trading date.

        Returns
        -------
        pd.Timestamp
            The trading date of the Series.

        ---------------------------------------------------------------------------


        获取 Series 的名称，表示交易日期。

        返回
        -------
        pd.Timestamp
            Series 的交易日期。

        ---------------------------------------------------------------------------
        """
        return self._name
    @name.setter
    def name(self, trade_dt: pd.Timestamp):
        """
        ===========================================================================

        Sets the name of the Series, which represents the trading date.

        Parameters
        ----------
        trade_dt : pd.Timestamp
            The trading date to set for the Series.

        ---------------------------------------------------------------------------


        设置 Series 的名称，表示交易日期。

        参数
        ----------
        trade_dt : pd.Timestamp
            要为 Series 设置的交易日期。

        ---------------------------------------------------------------------------
        """
        self._name = pd.to_datetime(trade_dt)
        
    @property
    def trade_dt(self) -> pd.Timestamp:
        """
        ===========================================================================

        Gets the current trading date of the Series.

        Returns
        -------
        pd.Timestamp
            The current trading date.

        ---------------------------------------------------------------------------


        获取 Series 的当前交易日期。

        返回
        -------
        pd.Timestamp
            当前交易日期。

        ---------------------------------------------------------------------------
        """
        return self.name
    @trade_dt.setter
    def trade_dt(self, trade_dt: pd.Timestamp):
        """
        ===========================================================================

        Sets the trading date of the Series.
        Handles adjustment of share counts if unit is 'share' and is_adj is False.

        Parameters
        ----------
        trade_dt : pd.Timestamp
            The new trading date to set.

        ---------------------------------------------------------------------------


        设置 Series 的交易日期。
        如果单位是 'share' 且 is_adj 为 False，则处理股票数量的调整。

        参数
        ----------
        trade_dt : pd.Timestamp
            要设置的新交易日期。

        ---------------------------------------------------------------------------
        """
        trade_dt = pd.to_datetime(trade_dt)
        # BE CAREFUL:
        # when trade_dt is changing and Series.unit = "share" and Series.is_adj = "False", it makes error because of the post_factor,
        # so we need to adjust share count with post_factor's pctchange between these two days.
        if (self.unit == 'share') and (self.is_adj == False) and self.trade_dt is not None:
            post_adj = (DATA_SOURCE._internal_data.loc[trade_dt][DATA_SOURCE._adj_factor] / self.internal_data[DATA_SOURCE._adj_factor])[self.index]
            self.values[:] = self.values * post_adj
            self.name = trade_dt
        elif self.trade_dt is None:
            self.name = trade_dt
            self.__internal_data_update__(trade_dt)
        else:
            self.name = trade_dt
        
    @property
    def unit(self) -> str:
        """
        ===========================================================================

        Gets the current unit of the Series (e.g., 'assets', 'weight', 'share').

        Returns
        -------
        str
            The current unit.

        ---------------------------------------------------------------------------


        获取 Series 的当前单位（例如，'assets'、'weight'、'share'）。

        返回
        -------
        str
            当前单位。

        ---------------------------------------------------------------------------
        """
        return self._unit
    @unit.setter
    def unit(self, v: str):
        """
        ===========================================================================

        Sets the unit of the Series.

        Parameters
        ----------
        v : str
            The new unit. Must be one of the defined _unit_types.

        Raises
        -------
        ValueError
            If the provided unit is not valid.

        ---------------------------------------------------------------------------


        设置 Series 的单位。

        参数
        ----------
        v : str
            新单位。必须是定义的 _unit_types 之一。

        引发
        -------
        ValueError
            如果提供的单位无效。

        ---------------------------------------------------------------------------
        """
        if v not in self._unit_types:
            raise ValueError(f"unit must be one of {self._unit_types}")
        self._unit = v
    
    @property
    def cash(self) -> float:
        """
        ===========================================================================

        Gets the current cash amount associated with the Series.

        Returns
        -------
        float
            The current cash amount.

        ---------------------------------------------------------------------------


        获取与 Series 关联的当前现金金额。

        返回
        -------
        float
            当前现金金额。

        ---------------------------------------------------------------------------
        """
        return self._cash
    @cash.setter
    def cash(self, v: float):
        """
        ===========================================================================

        Sets the cash amount associated with the Series.

        Parameters
        ----------
        v : float
            The new cash amount.

        ---------------------------------------------------------------------------


        设置与 Series 关联的现金金额。

        参数
        ----------
        v : float
            新的现金金额。

        ---------------------------------------------------------------------------
        """
        self._cash = v
        
    @property
    def state(self) -> str:
        """
        ===========================================================================

        Gets the current state of the Series (e.g., 'order', 'trade', 'settle').

        Returns
        -------
        str
            The current state.

        ---------------------------------------------------------------------------


        获取 Series 的当前状态（例如，'order'、'trade'、'settle'）。

        返回
        -------
        str
            当前状态。

        ---------------------------------------------------------------------------
        """
        return self._state
    @state.setter
    def state(self, v: str):
        """
        ===========================================================================

        Sets the state of the Series.
        Adjusts cash based on the new state (e.g., sets cash to 0 for 'order', or negative sum of assets for 'trade').

        Parameters
        ----------
        v : str
            The new state. Must be one of the valid price-related states from DATA_SOURCE.

        Raises
        -------
        ValueError
            If the provided state is not valid.

        ---------------------------------------------------------------------------


        设置 Series 的状态。
        根据新状态调整现金（例如，'order' 状态现金设置为 0，'trade' 状态现金设置为资产总和的负值）。

        参数
        ----------
        v : str
            新状态。必须是 DATA_SOURCE 中有效的与价格相关的状态之一。

        引发
        -------
        ValueError
            如果提供的状态无效。

        ---------------------------------------------------------------------------
        """
        state_values = [i.split('_')[1] for i in DATA_SOURCE._internal_attributes.keys() if 'price' in i]
        if v not in state_values:
            raise ValueError(f"unit must be one of {state_values}")
        self._state = v
        if v == 'order':
            self.cash = 0
        elif v == 'trade':
            self.cash = self.to('assets').sum() * -1
        
    @property
    def is_adj(self) -> bool:
        """
        ===========================================================================

        Gets the current adjustment status of the Series (True if prices are adjusted).

        Returns
        -------
        bool
            True if prices are adjusted, False otherwise.

        ---------------------------------------------------------------------------


        获取 Series 的当前复权状态（如果价格已复权则为 True）。

        返回
        -------
        bool
            如果价格已复权则为 True，否则为 False。

        ---------------------------------------------------------------------------
        """
        return self._is_adj
    @is_adj.setter
    def is_adj(self, v: bool):
        """
        ===========================================================================

        Sets the adjustment status of the Series.
        A warning is printed if changing is_adj when unit is 'share', as it may affect total assets.

        Parameters
        ----------
        v : bool
            The new adjustment status.

        ---------------------------------------------------------------------------


        设置 Series 的复权状态。
        如果单位是 'share' 时更改 is_adj，会打印警告，因为它可能会影响总资产。

        参数
        ----------
        v : bool
            新的复权状态。

        ---------------------------------------------------------------------------
        """
        if (self.unit == 'share') and (self._is_adj != v):
            print("the echange of Series.is_adj may occoured portfolio's total assetS")
        # WARING:
        # when Series.unit = "share", changing Series.is_adj will make the total assets of portfolio not equal bewteen unchange/change
        # but it is useful if you REAL want to change Series.is_adj and KNOW what it will occoured.
        # So if you want to keep portfolio's total assets not change, please use Series.to("share") instead of simple set Series.is_adj.
        self._is_adj = v
    
    def __weight_to_assets__(self, assets: float, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Converts the Series from 'weight' unit to 'assets' unit.

        Parameters
        ----------
        assets : float
            The total asset value to scale the weights to.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series converted to 'assets' unit.

        ---------------------------------------------------------------------------


        将 Series 从 'weight' 单位转换为 'assets' 单位。

        参数
        ----------
        assets : float
            用于缩放权重的总资产价值。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            转换为 'assets' 单位的 Series。

        ---------------------------------------------------------------------------
        """
        obj = self.copy() if copy else self
        obj = obj / obj.sum() * assets
        obj.unit = 'assets'
        return obj
    
    def __weight_to_share__(self, assets: float, is_adj: bool = None, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Converts the Series from 'weight' unit to 'share' unit.

        Parameters
        ----------
        assets : float
            The total asset value to scale the weights to.
        is_adj : bool, optional
            Whether to use adjusted prices for conversion. Defaults to current Series.is_adj.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series converted to 'share' unit.

        ---------------------------------------------------------------------------


        将 Series 从 'weight' 单位转换为 'share' 单位。

        参数
        ----------
        assets : float
            用于缩放权重的总资产价值。
        is_adj : bool, optional
            是否使用复权价格进行转换。默认为当前 Series.is_adj。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            转换为 'share' 单位的 Series。

        ---------------------------------------------------------------------------
        """
        is_adj = self.is_adj if is_adj is None else is_adj
        obj = self.__weight_to_assets__(assets, copy)
        obj.is_adj = is_adj
        obj = (obj / obj.price())
        obj.unit = 'share'
        return obj
    
    def __weight_to_weight__(self, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Normalizes the Series to 'weight' unit (sum to 1).

        Parameters
        ----------
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series normalized to 'weight' unit.

        ---------------------------------------------------------------------------


        将 Series 归一化为 'weight' 单位（总和为 1）。

        参数
        ----------
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            归一化为 'weight' 单位的 Series。

        ---------------------------------------------------------------------------
        """
        obj = self.copy() if copy else self
        obj = obj / obj.sum()
        return obj
        
    def __assets_to_assets__(self, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Returns the Series in 'assets' unit (no conversion needed).

        Parameters
        ----------
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series in 'assets' unit.

        ---------------------------------------------------------------------------


        返回 'assets' 单位的 Series（无需转换）。

        参数
        ----------
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            'assets' 单位的 Series。

        ---------------------------------------------------------------------------
        """
        obj = self.copy() if copy else self
        return obj
    
    def __assets_to_share__(self, is_adj: bool = None, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Converts the Series from 'assets' unit to 'share' unit.

        Parameters
        ----------
        is_adj : bool, optional
            Whether to use adjusted prices for conversion. Defaults to current Series.is_adj.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series converted to 'share' unit.

        ---------------------------------------------------------------------------


        将 Series 从 'assets' 单位转换为 'share' 单位。

        参数
        ----------
        is_adj : bool, optional
            是否使用复权价格进行转换。默认为当前 Series.is_adj。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            转换为 'share' 单位的 Series。

        ---------------------------------------------------------------------------
        """
        is_adj = self.is_adj if is_adj is None else is_adj
        obj = self.copy() if copy else self
        obj.is_adj = is_adj
        obj = (obj / obj.price())
        obj.unit = 'share'
        return obj
    
    def __assets_to_weight__(self, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Converts the Series from 'assets' unit to 'weight' unit.

        Parameters
        ----------
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series converted to 'weight' unit.

        ---------------------------------------------------------------------------


        将 Series 从 'assets' 单位转换为 'weight' 单位。

        参数
        ----------
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            转换为 'weight' 单位的 Series。

        ---------------------------------------------------------------------------
        """
        obj = self.copy() if copy else self
        obj = obj / obj.sum()
        obj.unit = 'weight'
        return obj

    def __share_to_assets__(self, is_adj: bool = None, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Converts the Series from 'share' unit to 'assets' unit.

        Parameters
        ----------
        is_adj : bool, optional
            Whether to use adjusted prices for conversion. Defaults to current Series.is_adj.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series converted to 'assets' unit.

        ---------------------------------------------------------------------------


        将 Series 从 'share' 单位转换为 'assets' 单位。

        参数
        ----------
        is_adj : bool, optional
            是否使用复权价格进行转换。默认为当前 Series.is_adj。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            转换为 'assets' 单位的 Series。

        ---------------------------------------------------------------------------
        """
        is_adj = self.is_adj if is_adj is None else is_adj
        obj = self.copy() if copy else self
        obj.is_adj = is_adj
        obj = obj * obj.price()
        obj.unit = 'assets'
        return obj
    
    def __share_to_share__(self, is_adj: bool = None, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Converts the Series from 'share' unit to 'share' unit, potentially changing adjustment status.

        Parameters
        ----------
        is_adj : bool, optional
            Whether to use adjusted prices for conversion. Defaults to current Series.is_adj.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series converted to 'share' unit with potentially new adjustment status.

        ---------------------------------------------------------------------------


        将 Series 从 'share' 单位转换为 'share' 单位，可能会更改复权状态。

        参数
        ----------
        is_adj : bool, optional
            是否使用复权价格进行转换。默认为当前 Series.is_adj。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            转换为 'share' 单位的 Series，可能具有新的复权状态。

        ---------------------------------------------------------------------------
        """
        if is_adj is not None and is_adj != self.is_adj:
            obj = self.__share_to_assets__(None, copy)
            obj = obj.__assets_to_share__(is_adj, False)
            # for not print the warning in Series.is_adj changing
            obj._is_adj = is_adj
        else:
            obj = self.copy() if copy else self
        return obj
            
    def __share_to_weight__(self, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Converts the Series from 'share' unit to 'weight' unit.

        Parameters
        ----------
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments (not used in this method).

        Returns
        -------
        Series
            The Series converted to 'weight' unit.

        ---------------------------------------------------------------------------


        将 Series 从 'share' 单位转换为 'weight' 单位。

        参数
        ----------
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            其他关键字参数（此方法中未使用）。

        返回
        -------
        Series
            转换为 'weight' 单位的 Series。

        ---------------------------------------------------------------------------
        """
        obj = self.copy() if copy else self
        obj = obj * obj.price()
        obj = obj / obj.sum()
        obj.unit = 'weight'
        return obj
    
    def to(self, unit: str=None, state: str = None, copy: bool = True, **kwargs) -> 'Series':
        """
        ===========================================================================

        Converts the Series to a specified unit and optionally sets its state.

        Parameters
        ----------
        unit : str
            The target unit (e.g., 'assets', 'weight', 'share').
        state : str, optional
            The target state (e.g., 'order', 'trade', 'settle'). Defaults to None.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.
        **kwargs : Any
            Additional keyword arguments passed to the specific conversion method.

        Returns
        -------
        Series
            The Series converted to the target unit and state.

        ---------------------------------------------------------------------------


        将 Series 转换为指定单位，并可选地设置其状态。

        参数
        ----------
        unit : str
            目标单位（例如，'assets'、'weight'、'share'）。
        state : str, optional
            目标状态（例如，'order'、'trade'、'settle'）。默认为 None。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。
        **kwargs : Any
            传递给特定转换方法的其他关键字参数。

        返回
        -------
        Series
            转换为目标单位和状态的 Series。

        ---------------------------------------------------------------------------
        """
        unit = self.unit if unit is None else unit
        key = f'__{self.unit}_to_{unit}__'
        obj = getattr(self, key)(copy=copy, **kwargs)
        if state is not None:
            obj.state = state
        return obj

    def __obj_adjust__(self, Series_obj: 'meta_Series') -> 'Series':
        """
        ===========================================================================

        Adjusts another Series-like object to match the unit and adjustment status of this Series.

        Parameters
        ----------
        Series_obj : meta_Series
            The Series-like object to adjust.

        Returns
        -------
        Series
            The adjusted Series object.

        ---------------------------------------------------------------------------


        调整另一个类似 Series 的对象，以匹配此 Series 的单位和复权状态。

        参数
        ----------
        Series_obj : meta_Series
            要调整的类似 Series 的对象。

        返回
        -------
        Series
            调整后的 Series 对象。

        ---------------------------------------------------------------------------
        """
        # For ensure the Series and calcuated object(Series object or Pandas.Series) with SAME object's attributes in unit, is_adj,
        # we need exchange the second object as same as the first in thest attributes.
        if isinstance(Series_obj, self.__class__):
            obj = Series_obj.to(unit=self.unit, is_adj=self.is_adj)
        else:
            obj = Series(Series_obj, unit=self.unit, state=self.state, cash=0, is_adj=self.is_adj)
        return obj
        
    def __add__(self, other: 'meta_Series') -> 'Series':
        """
        ===========================================================================

        Overloads the addition operator for Series objects.
        Handles alignment of indices and adjusts the other Series to match unit and adjustment status.

        Parameters
        ----------
        other : meta_Series
            The other Series object to add.

        Returns
        -------
        Series
            A new Series representing the sum.

        ---------------------------------------------------------------------------


        重载 Series 对象的加法运算符。
        处理索引对齐，并调整另一个 Series 以匹配单位和复权状态。

        参数
        ----------
        other : meta_Series
            要相加的另一个 Series 对象。

        返回
        -------
        Series
            表示和的新 Series。

        ---------------------------------------------------------------------------
        """
        if isinstance(other, meta_Series):
            index = self.index.union(other.index)
            self = self.reindex(index, fill_value=0)
            other = other.reindex(index, fill_value=0)
            try:
                other = self.__obj_adjust__(other)
            except:
                pass
            x = super().__add__(other)
            x.cash = x.cash + getattr(other, 'cash', 0)
            x.trade_dt = max(self.trade_dt, other.name)
        else:
            x = super().__add__(other)
        x = x[x != 0]
        return x
    
    def __radd__(self, other: 'meta_Series') -> 'Series':
        """
        ===========================================================================

        Overloads the reverse addition operator for Series objects.

        Parameters
        ----------
        other : meta_Series
            The other Series object to add.

        Returns
        -------
        Series
            A new Series representing the sum.

        ---------------------------------------------------------------------------


        重载 Series 对象的反向加法运算符。

        参数
        ----------
        other : meta_Series
            要相加的另一个 Series 对象。

        返回
        -------
        Series
            表示和的新 Series。

        ---------------------------------------------------------------------------
        """
        return self.__add__(other)
    
    def __sub__(self, other: 'meta_Series') -> 'Series':
        """
        ===========================================================================

        Overloads the subtraction operator for Series objects.
        Handles alignment of indices and adjusts the other Series to match unit and adjustment status.

        Parameters
        ----------
        other : meta_Series
            The other Series object to subtract.

        Returns
        -------
        Series
            A new Series representing the difference.

        ---------------------------------------------------------------------------


        重载 Series 对象的减法运算符。
        处理索引对齐，并调整另一个 Series 以匹配单位和复权状态。

        参数
        ----------
        other : meta_Series
            要相减的另一个 Series 对象。

        返回
        -------
        Series
            表示差的新 Series。

        ---------------------------------------------------------------------------
        """
        if isinstance(other, meta_Series):
            index = self.index.union(other.index)
            self = self.reindex(index, fill_value=0)
            other = other.reindex(index, fill_value=0)
            try:
                other = self.__obj_adjust__(other)
            except:
                pass
            x = super().__sub__(other)
            x.cash = x.cash + getattr(other, 'cash', 0)
            x.trade_dt = max(self.trade_dt, other.name)
        else:
            x = super().__sub__(other)
        x = x[x != 0]
        return x
    
    def __rsub__(self, other: 'meta_Series') -> 'Series':
        """
        ===========================================================================

        Overloads the reverse subtraction operator for Series objects.

        Parameters
        ----------
        other : meta_Series
            The other Series object.

        Returns
        -------
        Series
            A new Series representing the difference.

        ---------------------------------------------------------------------------


        重载 Series 对象的反向减法运算符。

        参数
        ----------
        other : meta_Series
            另一个 Series 对象。

        返回
        -------
        Series
            表示差的新 Series。

        ---------------------------------------------------------------------------
        """
        return self.__sub__(other)
    
    def __mul__(self, others: [int, float, np.number, 'meta_Series']) -> 'Series':
        """
        ===========================================================================

        Overloads the multiplication operator for Series objects.
        Handles scalar multiplication and element-wise multiplication with another Series.

        Parameters
        ----------
        others : int, float, numpy.number, or meta_Series
            The scalar or Series to multiply by.

        Returns
        -------
        Series
            A new Series representing the product.

        ---------------------------------------------------------------------------


        重载 Series 对象的乘法运算符。
        处理标量乘法和与另一个 Series 的元素级乘法。

        参数
        ----------
        others : int, float, numpy.number, or meta_Series
            要相乘的标量或 Series。

        返回
        -------
        Series
            表示乘积的新 Series。

        ---------------------------------------------------------------------------
        """
        if isinstance(others, (int, float, np.number)):
            x = super().__mul__(others)
            x.cash = x.cash * others
        else:
            x = super().__mul__(others)
        x.trade_dt = self.trade_dt
        x = x[x != 0]
        return x
    
    def __truediv__(self, others: [int, float, np.number, 'meta_Series']) -> 'Series':
        """
        ===========================================================================

        Overloads the true division operator for Series objects.
        Handles scalar division and element-wise division with another Series.

        Parameters
        ----------
        others : int, float, numpy.number, or meta_Series
            The scalar or Series to divide by.

        Returns
        -------
        Series
            A new Series representing the quotient.

        ---------------------------------------------------------------------------


        重载 Series 对象的真除法运算符。
        处理标量除法和与另一个 Series 的元素级除法。

        参数
        ----------
        others : int, float, numpy.number, or meta_Series
            要相除的标量或 Series。

        返回
        -------
        Series
            表示商的新 Series。

        ---------------------------------------------------------------------------
        """
        if isinstance(others, (int, float, np.number)):
            x = super().__truediv__(others)
            x.cash = x.cash / others
        else:
            x = super().__truediv__(others)
        x.trade_dt = self.trade_dt
        x = x[x != 0]
        return x

    def d_shift(self, trade_dt: int = 1, copy: bool = True) -> 'Series':
        """
        ===========================================================================

        Shifts the trading date of the Series by a specified number of days.

        Parameters
        ----------
        trade_dt : int, optional
            The number of days to shift. Positive for future, negative for past. Defaults to 1.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.

        Returns
        -------
        Series
            The Series with the shifted trading date.

        ---------------------------------------------------------------------------


        将 Series 的交易日期移动指定的天数。

        参数
        ----------
        trade_dt : int, optional
            移动的天数。正数表示未来，负数表示过去。默认为 1。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。

        返回
        -------
        Series
            交易日期已移动的 Series。

        ---------------------------------------------------------------------------
        """
        day = DATA_SOURCE.trade_days.get_loc(self.trade_dt) + trade_dt
        day = DATA_SOURCE.trade_days[day]
        if copy:
            obj = self.copy()
            obj.trade_dt = day
            return obj
        else:
            self.trade_dt = day

    def price(self, is_adj: bool = None, all_price: bool = False) -> 'pd.Series':
        """
        ===========================================================================

        Retrieves the price data for the current state of the Series.

        Parameters
        ----------
        is_adj : bool, optional
            Whether to retrieve adjusted prices. Defaults to current Series.is_adj.
        all_price : bool, optional
            If True, returns all available prices for the current trade_dt.
            If False, returns prices only for the Series' index. Defaults to False.

        Returns
        -------
        pd.Series
            A pandas Series containing the price data.

        ---------------------------------------------------------------------------


        检索 Series 当前状态的价格数据。

        参数
        ----------
        is_adj : bool, optional
            是否检索复权价格。默认为当前 Series.is_adj。
        all_price : bool, optional
            如果为 True，则返回当前 trade_dt 的所有可用价格。
            如果为 False，则仅返回 Series 索引的价格。默认为 False。

        返回
        -------
        pd.Series
            包含价格数据的 pandas Series。

        ---------------------------------------------------------------------------
        """
        key = DATA_SOURCE._internal_attributes[f'_{self.state}_price']
        is_adj = self.is_adj if is_adj is None else is_adj
        key = key + (DATA_SOURCE._internal_attributes['_adj_label'] if is_adj else '')
        df = self.internal_data[key]
        df.trade_dt = self.trade_dt
        if not all_price:
            return df.reindex(self.index)
        else:
            return df
        
    def total_assets(self, cash: bool = True) -> float:
        """
        ===========================================================================

        Calculates the total assets of the portfolio represented by the Series.

        Parameters
        ----------
        cash : bool, optional
            Whether to include cash in the total assets calculation. Defaults to True.

        Returns
        -------
        float
            The total assets value.

        ---------------------------------------------------------------------------


        计算 Series 所代表投资组合的总资产。

        参数
        ----------
        cash : bool, optional
            计算总资产时是否包含现金。默认为 True。

        返回
        -------
        float
            总资产价值。

        ---------------------------------------------------------------------------
        """
        x = self.to('assets').sum() + self.cash if cash else 0
        return x
    
    def cost(self) -> 'Series':
        """
        ===========================================================================

        Calculates the transaction cost for the portfolio represented by the Series.

        Returns
        -------
        Series
            A Series representing the transaction costs for each position.

        ---------------------------------------------------------------------------


        计算 Series 所代表投资组合的交易成本。

        返回
        -------
        Series
            表示每个头寸交易成本的 Series。

        ---------------------------------------------------------------------------
        """
        x = self.to('assets').abs() * self.trade_cost * -1
        return x
    
    def order_standard(self, d_shift: int = 0, is_adj: bool = False, copy: bool = True) -> 'Series':
        """
        ===========================================================================

        Prepares an order portfolio by shifting the trading date and converting to share units.

        Parameters
        ----------
        d_shift : int, optional
            Number of days to shift the trading date. Defaults to 0.
        is_adj : bool, optional
            Whether to use adjusted prices for conversion to shares. Defaults to False.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.

        Returns
        -------
        Series
            The prepared order portfolio in 'share' unit.

        ---------------------------------------------------------------------------


        通过移动交易日期并转换为股票数量单位来准备订单投资组合。

        参数
        ----------
        d_shift : int, optional
            移动交易日期的天数。默认为 0。
        is_adj : bool, optional
            转换为股票数量时是否使用复权价格。默认为 False。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。

        返回
        -------
        Series
            以 'share' 单位表示的准备好的订单投资组合。

        ---------------------------------------------------------------------------
        """
        obj = self.copy() if copy else self
        obj.state = 'order'
        obj.d_shift(d_shift, copy=False)
        obj = obj.to('share', is_adj=is_adj)

        return obj
        
    def tradeable_standard(self, d_shift: int = 0, cost: bool = True, copy: bool = True) -> 'Series':
        """
        ===========================================================================

        Filters the portfolio based on trading status, buy/sell limits, and ST status.
        Adjusts cash for trade fees if `cost` is True.

        Parameters
        ----------
        d_shift : int, optional
            Number of days to shift the trading date. Defaults to 0.
        cost : bool, optional
            Whether to adjust cash for trade fees. Defaults to True.
        copy : bool, optional
            Whether to return a copy or modify in place. Defaults to True.

        Returns
        -------
        Series
            The tradeable portion of the portfolio.

        ---------------------------------------------------------------------------


        根据交易状态、买入/卖出限制和 ST 状态筛选投资组合。
        如果 `cost` 为 True，则调整现金以支付交易费用。

        参数
        ----------
        d_shift : int, optional
            移动交易日期的天数。默认为 0。
        cost : bool, optional
            是否调整现金以支付交易费用。默认为 True。
        copy : bool, optional
            是否返回副本或就地修改。默认为 True。

        返回
        -------
        Series
            投资组合中可交易的部分。

        ---------------------------------------------------------------------------
        """
        obj = self.copy() if copy else self
        df = obj.internal_data.reindex(obj.index)
        obj.d_shift(d_shift, copy=False)
        df = obj.internal_data.reindex(obj.index)
        tradeable = (((obj > 0) & df[DATA_SOURCE._buyable]) | ((obj < 0) & df[DATA_SOURCE._sellable])) & (df[DATA_SOURCE._trade_status] == 0)
        obj = obj[tradeable]
        obj.state = 'trade'
        obj.cash = obj.cash + (obj.to('assets').abs().sum() * self.trade_cost * -1 if cost else 0)
        return obj

class link():
    """
    ===========================================================================

    Simulates a single day's trading and settlement process within the backtesting framework.
    It calculates actual trades, new settlement portfolios, and remaining orders.

    ---------------------------------------------------------------------------


    在回测框架中模拟单日交易和结算过程。
    它计算实际交易、新的结算投资组合和剩余订单。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self,
        settle_portfolio_T0: 'Series',
        order_portfolio_T0: 'Series',
        hope_portfolio_T1: 'Series',
        init_assets: float = None,
        is_adj: bool = True
    ):
        """
        ===========================================================================

        Initializes the link object for a single day's simulation.

        Parameters
        ----------
        settle_portfolio_T0 : Series
            The settlement portfolio from the previous day (T0).
        order_portfolio_T0 : Series
            The order portfolio from the previous day (T0).
        hope_portfolio_T1 : Series
            The desired (hope) portfolio for the current day (T1).
        init_assets : float, optional
            Initial assets for the very first day of backtest. Defaults to None.
        is_adj : bool, optional
            Whether prices are adjusted. Defaults to True.

        ---------------------------------------------------------------------------


        初始化用于单日模拟的 link 对象。

        参数
        ----------
        settle_portfolio_T0 : Series
            前一日（T0）的结算投资组合。
        order_portfolio_T0 : Series
            前一日（T0）的订单投资组合。
        hope_portfolio_T1 : Series
            当前日（T1）的期望（目标）投资组合。
        init_assets : float, optional
            回测第一天的初始资产。默认为 None。
        is_adj : bool, optional
            价格是否复权。默认为 True。

        ---------------------------------------------------------------------------
        """
        self._settle_portfolio_T0 = settle_portfolio_T0
        self._order_portfolio_T0 = order_portfolio_T0
        self._hope_portfolio_T1 = hope_portfolio_T1
        self._init_assets = init_assets
        self.is_adj = is_adj
        
    @property
    def settle_T0(self) -> 'Series':
        """
        ===========================================================================

        Gets the settlement portfolio for the previous day (T0).
        Initializes if not already set.

        Returns
        -------
        Series
            The settlement portfolio at T0.

        ---------------------------------------------------------------------------


        获取前一日（T0）的结算投资组合。
        如果尚未设置，则进行初始化。

        返回
        -------
        Series
            T0 时的结算投资组合。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_settle_T0'):
            if self._settle_portfolio_T0 is None:
                self._settle_T0 = Series(name=self._hope_portfolio_T1.trade_dt, unit='share', state='settle', cash=self._init_assets).d_shift(-1, copy=True)
            else:
                self._settle_T0 = self._settle_portfolio_T0.to('share', state='settle', is_adj=self.is_adj)
        return self._settle_T0
    
    @property
    def order_T0(self) -> 'Series':
        """
        ===========================================================================

        Gets the order portfolio for the previous day (T0).
        Initializes if not already set.

        Returns
        -------
        Series
            The order portfolio at T0.

        ---------------------------------------------------------------------------


        获取前一日（T0）的订单投资组合。
        如果尚未设置，则进行初始化。

        返回
        -------
        Series
            T0 时的订单投资组合。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_order_T0'):
            if self._order_portfolio_T0 is None:
                self._order_T0 = Series(name=self._hope_portfolio_T1.trade_dt, state='order', unit='share').d_shift(-1, copy=True)
            else:
                self._order_T0 = self._order_portfolio_T0.to('share', state='order', is_adj=self.is_adj)
        return self._order_T0
    
    @property
    def trade_T1(self) -> 'Series':
        """
        ===========================================================================

        Calculates the tradeable portfolio for the current day (T1).

        Returns
        -------
        Series
            The tradeable portfolio at T1.

        ---------------------------------------------------------------------------


        计算当前日（T1）的可交易投资组合。

        返回
        -------
        Series
            T1 时的可交易投资组合。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_trade_T1'):
            self._trade_T1 = self.order_T0.tradeable_standard(d_shift=1)
        return self._trade_T1
    
    @property
    def settle_T1(self) -> 'Series':
        """
        ===========================================================================

        Calculates the settlement portfolio for the current day (T1).
        This is the previous day's settlement adjusted by the current day's trades.

        Returns
        -------
        Series
            The settlement portfolio at T1.

        ---------------------------------------------------------------------------


        计算当前日（T1）的结算投资组合。
        这是前一日的结算投资组合根据当日交易调整后的结果。

        返回
        -------
        Series
            T1 时的结算投资组合。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_settle_T1'):
            self._settle_T1 = self.settle_T0.d_shift(1, copy=True) + self.trade_T1 # left state = "settle" that is no need to adjust
        return self._settle_T1
    
    @property
    def hope_T1(self) -> 'Series':
        """
        ===========================================================================

        Gets the desired (hope) portfolio for the current day (T1), scaled to total assets.

        Returns
        -------
        Series
            The scaled desired portfolio at T1.

        ---------------------------------------------------------------------------


        获取当前日（T1）的期望（目标）投资组合，并按总资产进行缩放。

        返回
        -------
        Series
            T1 时缩放后的期望投资组合。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_hope_T1'):
            self._hope_T1 = self._hope_portfolio_T1.to('share', assets=self.settle_T1.total_assets())
        return self._hope_T1
    
    @property
    def order_T1(self) -> 'Series':
        """
        ===========================================================================

        Calculates the remaining order portfolio for the current day (T1).
        This is the difference between the desired portfolio and the settled portfolio.

        Returns
        -------
        Series
            The remaining order portfolio at T1.

        ---------------------------------------------------------------------------


        计算当前日（T1）的剩余订单投资组合。
        这是期望投资组合与已结算投资组合之间的差额。

        返回
        -------
        Series
            T1 时的剩余订单投资组合。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_order_T1'):
            self._order_T1 = self.hope_T1 - self.settle_T1
        return self._order_T1
    
    @property
    def cost(self) -> float:
        """
        ===========================================================================

        Calculates the total transaction cost for the current day's trades.

        Returns
        -------
        float
            The total transaction cost.

        ---------------------------------------------------------------------------


        计算当日交易的总交易成本。

        返回
        -------
        float
            总交易成本。

        ---------------------------------------------------------------------------
        """
        return self.trade_T1.cost().sum()
    
    @property
    def cost_pct(self) -> float:
        """
        ===========================================================================

        Calculates the transaction cost as a percentage of the previous day's total assets.

        Returns
        -------
        float
            The transaction cost percentage.

        ---------------------------------------------------------------------------


        计算交易成本占前一日总资产的百分比。

        返回
        -------
        float
            交易成本百分比。

        ---------------------------------------------------------------------------
        """
        return self.cost / self.settle_T0.total_assets()
    
    @property
    def turnover(self) -> float:
        """
        ===========================================================================

        Calculates the turnover for the current day's trades.

        Returns
        -------
        float
            The turnover value.

        ---------------------------------------------------------------------------


        计算当日交易的换手率。

        返回
        -------
        float
            换手率值。

        ---------------------------------------------------------------------------
        """
        return self.trade_T1.to('assets').abs().sum() / self.settle_T0.total_assets()
    
    @property
    def trade_difference(self) -> pd.DataFrame:
        """
        ===========================================================================

        Provides a DataFrame showing the difference between ordered and actual trades.

        Returns
        -------
        pd.DataFrame
            A DataFrame detailing trade differences.

        ---------------------------------------------------------------------------


        提供一个 DataFrame，显示订单与实际交易之间的差异。

        返回
        -------
        pd.DataFrame
            详细说明交易差异的 DataFrame。

        ---------------------------------------------------------------------------
        """
        df = pd.concat({'order':self.order_T0, 'trade':self.trade_T1, 'difference':self.trade_T1 - self.order_T0}, axis=1)
        df = pd.concat([df, self.trade_T1.internal_data.loc[df.index]], axis=1)
        return df
    
    @property
    def total_assets(self) -> float:
        """
        ===========================================================================

        Calculates the total assets of the settlement portfolio at T1.

        Returns
        -------
        float
            The total assets at T1.

        ---------------------------------------------------------------------------


        计算 T1 时结算投资组合的总资产。

        返回
        -------
        float
            T1 时的总资产。

        ---------------------------------------------------------------------------
        """
        return self.settle_T1.total_assets()
    
    @property
    def returns(self) -> float:
        """
        ===========================================================================

        Calculates the effective returns for the current day.

        Returns
        -------
        float
            The effective returns.

        ---------------------------------------------------------------------------


        计算当日的有效收益。

        返回
        -------
        float
            有效收益。

        ---------------------------------------------------------------------------
        """
        return self.settle_T1.total_assets() / self.settle_T0.total_assets() - 1
    
    @property
    def theoretical_returns(self) -> float:
        """
        ===========================================================================

        Calculates the theoretical returns for the current day.

        Returns
        -------
        float
            The theoretical returns.

        ---------------------------------------------------------------------------


        计算当日的理论收益。

        返回
        -------
        float
            理论收益。

        ---------------------------------------------------------------------------
        """
        return ((self.order_T0 + self.settle_T0).d_shift(1, copy=True).total_assets() - self.order_T0.total_assets())/ self.settle_T0.total_assets() - 1
        
    
    def __call__(self) -> dict:
        """
        ===========================================================================

        Returns the updated settlement and order portfolios for the next day's simulation.

        Returns
        -------
        dict
            A dictionary containing 'settle_portfolio_T0' and 'order_portfolio_T0'.

        ---------------------------------------------------------------------------


        返回更新后的结算和订单投资组合，用于下一天的模拟。

        返回
        -------
        dict
            包含 'settle_portfolio_T0' 和 'order_portfolio_T0' 的字典。

        ---------------------------------------------------------------------------
        """
        dic = {'settle_portfolio_T0':self.settle_T1, 'order_portfolio_T0':self.order_T1}
        return dic
    
class DataFrame(meta_DataFrame):
    """
    ===========================================================================

    A custom pandas DataFrame that includes a `chain()` method to initiate backtesting simulations.

    ---------------------------------------------------------------------------


    一个自定义的 pandas DataFrame，包含 `chain()` 方法以启动回测模拟。

    ---------------------------------------------------------------------------
    """
    _internal_names = meta_DataFrame._internal_names + []
    _internal_names_set = set(_internal_names)
    _metadata = meta_DataFrame._metadata
    
    @property
    def _constructor(self):
        return DataFrame
    
    @property
    def _constructor_sliced(self):
        return Series
    
    def chain(self, init_assets: float = 10000, is_adj: bool = True, report_freq: str = 'month') -> 'chain':
        """
        ===========================================================================

        Initiates a backtesting simulation by creating and running a `chain` object.

        Parameters
        ----------
        init_assets : float, optional
            Initial assets for the backtest. Defaults to 10000.
        is_adj : bool, optional
            Whether prices are adjusted during the backtest. Defaults to True.
        report_freq : str, optional
            Frequency for reporting progress (e.g., 'month'). Defaults to 'month'.

        Returns
        -------
        chain
            The initialized and run chain object.

        ---------------------------------------------------------------------------


        通过创建并运行 `chain` 对象来启动回测模拟。

        参数
        ----------
        init_assets : float, optional
            回测的初始资产。默认为 10000。
        is_adj : bool, optional
            回测期间价格是否复权。默认为 True。
        report_freq : str, optional
            报告进度的频率（例如，'month'）。默认为 'month'。

        返回
        -------
        chain
            已初始化并运行的 chain 对象。

        ---------------------------------------------------------------------------
        """
        x = chain(self, init_assets, is_adj, report_freq)
        x()
        return x
    
    
class chain:
    """
    ===========================================================================

    Orchestrates the backtesting simulation over a period.
    It iterates through daily target portfolios and uses the `link` class
    to simulate day-by-day trading, settlement, and portfolio updates.

    ---------------------------------------------------------------------------


    协调一段时间内的回测模拟。
    它遍历每日目标投资组合，并使用 `link` 类模拟逐日交易、结算和投资组合更新。

    ---------------------------------------------------------------------------
    """
    def __init__(
        self,
        DataFrame_obj: 'pd.DataFrame',
        init_assets: float = 10000,
        is_adj: bool = True,
        report_freq: str = 'month'
    ):
        """
        ===========================================================================

        Initializes the chain object for backtesting.

        Parameters
        ----------
        DataFrame_obj : pd.DataFrame
            A DataFrame of daily target portfolios.
        init_assets : float, optional
            Initial assets for the backtest. Defaults to 10000.
        is_adj : bool, optional
            Whether prices are adjusted during the backtest. Defaults to True.
        report_freq : str, optional
            Frequency for reporting progress (e.g., 'month'). Defaults to 'month'.

        ---------------------------------------------------------------------------


        初始化用于回测的 chain 对象。

        参数
        ----------
        DataFrame_obj : pd.DataFrame
            每日目标投资组合的 DataFrame。
        init_assets : float, optional
            回测的初始资产。默认为 10000。
        is_adj : bool, optional
            回测期间价格是否复权。默认为 True。
        report_freq : str, optional
            报告进度的频率（例如，'month'）。默认为 'month'。

        ---------------------------------------------------------------------------
        """
        self._data = DataFrame_obj
        self._init_assets = 10000
        self._is_adj = is_adj
        self.report_freq = report_freq
        
    def __call__(self):
        """
        ===========================================================================

        Executes the backtesting simulation day by day.
        It iterates through the target portfolios and uses the `link` class
        to simulate trading and update portfolios.

        ---------------------------------------------------------------------------


        逐日执行回测模拟。
        它遍历目标投资组合，并使用 `link` 类模拟交易和更新投资组合。

        ---------------------------------------------------------------------------
        """
        link_obj = None
        dic = {}
        for i,j in self._data.iterrows():
            try:
                if link_obj is None:
                    link_obj = link(None, None, hope_portfolio_T1=j, init_assets=self._init_assets)
                else:
                    link_obj = link(**link_obj(), hope_portfolio_T1=j)
                dic[i] = link_obj
                if ((getattr(link_obj.settle_T1.trade_dt, self.report_freq) != getattr(DATA_SOURCE.trade_days[DATA_SOURCE.trade_days.get_loc(link_obj.settle_T1.trade_dt) + 1], self.report_freq))
                    or
                    (i == self._data.index[-1]) ):
                    print(i.date(), round(link_obj.total_assets, 3))
            except:
                pass
        self.genertor_link = dic
    
    def __check_link__(self):
        """
        ===========================================================================

        Checks if the backtesting simulation has been run.
        If not, it calls the `__call__` method to run it.

        ---------------------------------------------------------------------------


        检查回测模拟是否已运行。
        如果未运行，则调用 `__call__` 方法来运行它。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, 'genertor_link'):
            self.__call__()
    
    def total_assets(self) -> pd.Series:
        """
        ===========================================================================

        Retrieves the total assets for each day of the backtest.

        Returns
        -------
        pd.Series
            A pandas Series containing total assets over time.

        ---------------------------------------------------------------------------


        检索回测期间每天的总资产。

        返回
        -------
        pd.Series
            包含随时间变化的总资产的 pandas Series。

        ---------------------------------------------------------------------------
        """
        self.__check_link__()
        if not hasattr(self, '_total_assets'):
            df = pd.Series({i:j.settle_T1.total_assets() for i,j in self.genertor_link.items()}, name='TOTAL_ASSETS')
            self._total_assets = df
        return self._total_assets
    
    def theoretical_returns(self) -> pd.Series:
        """
        ===========================================================================

        Retrieves the theoretical returns for each day of the backtest.

        Returns
        -------
        pd.Series
            A pandas Series containing theoretical returns over time.

        ---------------------------------------------------------------------------


        检索回测期间每天的理论收益。

        返回
        -------
        pd.Series
            包含随时间变化的理论收益的 pandas Series。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_theoretical_returns'):
            df = pd.Series({i:j.theoretical_returns for i,j in self.genertor_link.items()}, name='THEORETICAL')
            self._theoretical_returns = df
        return self._theoretical_returns
    
    def effective_returns(self) -> pd.Series:
        """
        ===========================================================================

        Retrieves the effective returns for each day of the backtest.

        Returns
        -------
        pd.Series
            A pandas Series containing effective returns over time.

        ---------------------------------------------------------------------------


        检索回测期间每天的有效收益。

        返回
        -------
        pd.Series
            包含随时间变化的有效收益的 pandas Series。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_returns'):
            df = pd.Series({i:j.returns for i,j in self.genertor_link.items()}, name='EFFECTIVE')
            self._returns = df
        return self._returns
        
    def turnover(self) -> pd.Series:
        """
        ===========================================================================

        Retrieves the turnover for each day of the backtest.

        Returns
        -------
        pd.Series
            A pandas Series containing turnover values over time.

        ---------------------------------------------------------------------------


        检索回测期间每天的换手率。

        返回
        -------
        pd.Series
            包含随时间变化的换手率值的 pandas Series。

        ---------------------------------------------------------------------------
        """
        if not hasattr(self, '_turnover'):
            df = pd.Series({i:j.turnover for i,j in self.genertor_link.items()}, name='TURNOVER')
            self._turnover = df
        return self._turnover