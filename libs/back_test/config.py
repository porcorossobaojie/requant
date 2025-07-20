# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 11:24:20 2025

@author: Pocro Rosso
"""



class DATA_INFO:
    """
    ===========================================================================

    Defines standard column names for various market data points used throughout the backtesting module.
    These names ensure consistent access to specific data fields.

    ---------------------------------------------------------------------------


    定义回测模块中使用的各种市场数据点的标准列名。
    这些名称确保对特定数据字段的一致访问。

    ---------------------------------------------------------------------------

    Examples
    --------
    >>> # Access the close price column name
    >>> close_price_col = DATA_INFO._close
    >>> print(close_price_col)
    'S_DQ_CLOSE'

    示例
    --------
    >>> # 访问收盘价列名
    >>> close_price_col = DATA_INFO._close
    >>> print(close_price_col)
    'S_DQ_CLOSE'
    """
    # the variable name with 'price' in, will be used in __back_test__.main for attributes "state" and "price"
    _close = 'S_DQ_CLOSE'  # English: Close price column name. 中文: 收盘价列名。
    _open = 'S_DQ_OPEN'  # English: Open price column name. 中文: 开盘价列名。
    _pre_close = 'S_DQ_PRECLOSE'  # English: Pre-close price column name. 中文: 昨收价列名。
    _avg = 'S_DQ_AVGPRICE'  # English: Average price column name. 中文: 均价列名。
    _low_limit = 'S_DQ_LOW_LIMIT'  # English: Lower price limit column name. 中文: 跌停价列名。
    _high_limit = 'S_DQ_HIGH_LIMIT'  # English: Upper price limit column name. 中文: 涨停价列名。
    _high = 'S_DQ_HIGH'  # English: High price column name. 中文: 最高价列名。
    _low = 'S_DQ_LOW'  # English: Low price column name. 中文: 最低价列名。
    _adj_label = '_ADJ'  # English: Adjustment label suffix. 中文: 复权标签后缀。
    _trade_status = 'S_DQ_TRADESTATUS'  # English: Trade status column name. 中文: 交易状态列名。
    _adj_factor = 'S_DQ_POST_FACTOR'  # English: Adjustment factor column name. 中文: 复权因子列名。
    _trade_price = 'S_DQ_AVGPRICE'  # English: Trade price column name (typically average price). 中文: 交易价格列名（通常为均价）。
    _settle_price = 'S_DQ_CLOSE'  # English: Settlement price column name (typically close price). 中文: 结算价格列名（通常为收盘价）。
    _order_price = 'S_DQ_CLOSE'  # English: Order price column name (typically close price). 中文: 委托价格列名（通常为收盘价）。
    _buyable = 'BUYABLE'  # English: Buyable status column name. 中文: 可买状态列名。
    _sellable = 'SELLABLE'  # English: Sellable status column name. 中文: 可卖状态列名。
    _st_filter = 'NOT_ST'  # English: Not ST (Special Treatment) status column name. 中文: 非ST股票状态列名。
    _pct_change = 'S_DQ_PCTCHANGE'
    
class TRADE_INFO:
    """
    ===========================================================================

    Specifies trading parameters such as buy/sell limits, transaction costs, and filters for ST (Special Treatment) stocks.

    ---------------------------------------------------------------------------


    指定交易参数，例如买入/卖出限制、交易成本和ST（特别处理）股票的筛选。

    ---------------------------------------------------------------------------

    Examples
    --------
    >>> # Access the buy limit
    >>> buy_limit = TRADE_INFO._buy_limit
    >>> print(buy_limit)
    0.005

    示例
    --------
    >>> # 访问买入限制
    >>> buy_limit = TRADE_INFO._buy_limit
    >>> print(buy_limit)
    0.005
    """
    _buy_limit = 0.005  # English: Buy price limit percentage. 中文: 买入价格限制百分比。
    _sell_limit = 0.005  # English: Sell price limit percentage. 中文: 卖出价格限制百分比。
    _trade_cost = 0.0005  # English: Transaction cost percentage. 中文: 交易成本百分比。
    _not_st = 1  # English: Value indicating a stock is not ST. 中文: 表示股票非ST的值。

class SERIES_ATTRIBUTES:
    """
    ===========================================================================

    Defines default attributes and their types for the custom Series object used in portfolio management.

    ---------------------------------------------------------------------------


    定义投资组合管理中使用的自定义Series对象的默认属性及其类型。

    ---------------------------------------------------------------------------

    Examples
    --------
    >>> # Access the default unit
    >>> default_unit = SERIES_ATTRIBUTES._unit
    >>> print(default_unit)
    'weight'

    示例
    --------
    >>> # 访问默认单位
    >>> default_unit = SERIES_ATTRIBUTES._unit
    >>> print(default_unit)
    'weight'
    """
    _unit_types = ['assets', 'weight', 'share']  # English: Valid unit types for the Series (assets, weight, share). 中文: Series的有效单位类型（资产、权重、份额）。
    _unit = 'weight'  # English: Default unit for the Series. 中文: Series的默认单位。
    _state = 'order'  # English: Default state for the Series (e.g., order, trade, settle). 中文: Series的默认状态（例如，订单、交易、结算）。
    _cash = 0  # English: Default cash amount associated with the Series. 中文: 与Series关联的默认现金金额。
    _is_adj = True  # English: Default flag indicating if prices are adjusted. 中文: 默认标志，指示价格是否复权。
