# -*- coding: utf-8 -*-
"""
Created on Mon May 12 22:52:06 2025

@author: Porco Rosso
"""

import re
import factors
import flow
from flow.config import COLUMNS_INFO
flow.data_init()
import pandas as pd
pd.capitalize()
from typing import Any, Dict, List, Optional, Union

class main():
    """
    ===========================================================================

    Meta-class for trading strategies, providing functionalities for factor filtering, ranking, order generation, and testing.

    ---------------------------------------------------------------------------

    交易策略的元类，提供因子过滤、排名、订单生成和测试等功能。

    ---------------------------------------------------------------------------
    """
    core: Optional[List[Any]] = None # list of factor instance, i.e. [factors.volatility()]

    @classmethod
    def star_filter(
        cls, 
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Filters out stocks based on specific stock code prefixes (e.g., ST, *ST).

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame of stock data.

        Returns
        -------
        pd.DataFrame
            The filtered DataFrame.

        ---------------------------------------------------------------------------

        根据特定的股票代码前缀（例如，ST，*ST）过滤股票。

        参数
        ----------
        df : pd.DataFrame
            股票数据的输入DataFrame。

        返回
        -------
        pd.DataFrame
            过滤后的DataFrame。

        ---------------------------------------------------------------------------
        """
        x = df.loc[:, [i[:3] not in ['002', '300', '688', '301'] for i in df.columns]]
        return x

    @classmethod
    def __internal_data__(cls) -> Dict[int, pd.DataFrame]:
        """
        ===========================================================================

        Placeholder for internal data loading and processing.

        Returns
        -------
        Dict[int, pd.DataFrame]
            A dictionary of internal data DataFrames.

        ---------------------------------------------------------------------------

        内部数据加载和处理的占位符。

        返回
        -------
        Dict[int, pd.DataFrame]
            内部数据DataFrames的字典。

        ---------------------------------------------------------------------------
        """
        # i.e.
        # if not hasattr(cls, '_internal_data'):
        #     x = [cls.core[0].volatility(), cls.core[0].abnormal1()]
        #     cls._internal_data = {i:j for i,j in enumerate(x)}
        # return cls._internal_data
        pass # Placeholder, replace with actual implementation

    @classmethod
    def __factor__(cls) -> pd.DataFrame:
        """
        ===========================================================================

        Placeholder for factor calculation and processing.

        Returns
        -------
        pd.DataFrame
            The calculated factor DataFrame.

        ---------------------------------------------------------------------------

        因子计算和处理的占位符。

        返回
        -------
        pd.DataFrame
            计算出的因子DataFrame。

        ---------------------------------------------------------------------------
        """
        # if not hasattr(cls, '_factor'):
        #     x = [cls.core[0].filter(i) for i in cls.__internal_data__.values()]
        #     x = cls.core[0].merge(*x)
        #     x = x.rollings(10).min(2).mean()
        #     x = cls.core[0].filter(x)
        #     cls._factor = x
        # x = cls._factor
        # return x
        pass # Placeholder, replace with actual implementation
        
    @property
    def internal_data(self) -> Dict[int, pd.DataFrame]:
        """
        ===========================================================================

        Accesses the internal data of the strategy.

        Returns
        -------
        Dict[int, pd.DataFrame]
            A dictionary of internal data DataFrames.

        ---------------------------------------------------------------------------

        访问策略的内部数据。

        返回
        -------
        Dict[int, pd.DataFrame]
            内部数据DataFrames的字典。

        ---------------------------------------------------------------------------
        """
        return self.__internal_data__()
    
    @property
    def factor(self) -> pd.DataFrame:
        """
        ===========================================================================

        Accesses the calculated factor for the strategy, with optional star stock filtering.

        Returns
        -------
        pd.DataFrame
            The calculated factor DataFrame.

        ---------------------------------------------------------------------------

        访问策略的计算因子，可选进行星级股票过滤。

        返回
        -------
        pd.DataFrame
            计算出的因子DataFrame。

        ---------------------------------------------------------------------------
        """
        x = self.__factor__()
        if self.not_star:
            x = self.star_filter(x)
        return x
    
    
    def ranker(
        self, 
        codes: Optional[List[str]] = None, 
        date: Optional[Union[int, pd.Timestamp]] = None
    ) -> pd.Series:
        """
        ===========================================================================

        Ranks stocks based on the strategy's factor.

        Parameters
        ----------
        codes : Optional[List[str]], optional
            A list of stock codes to rank. If None, all stocks are ranked. Defaults to None.
        date : Optional[Union[int, pd.Timestamp]], optional
            The date or index to retrieve the factor data for ranking. Defaults to None (last available date).

        Returns
        -------
        pd.Series
            A Series of ranked stocks.

        ---------------------------------------------------------------------------

        根据策略因子对股票进行排名。

        参数
        ----------
        codes : Optional[List[str]], optional
            要排名的股票代码列表。如果为 None，则对所有股票进行排名。默认为 None。
        date : Optional[Union[int, pd.Timestamp]], optional
            用于排名的数据的日期或索引。默认为 None（最后一个可用日期）。

        返回
        -------
        pd.Series
            排名股票的Series。

        ---------------------------------------------------------------------------
        """
        date = -1 if date is None else date
        if isinstance(date, int):
            x = self.factor.iloc[date]
        else:
            x = self.factor.loc[date]
        x = x.rank(ascending=False)
        if codes is not None:
            x = x.reindex(codes).sort_values()
        else:
            x = x.sort_values()
        return x
        
    def __order__(
        self, 
        settle: Optional[pd.Series], 
        assets: float, 
        count: int, 
        max_filter: int, 
        high_low_adjust: bool = True, 
        mini: float = 0.2, 
        date: Optional[Union[int, pd.Timestamp]] = None
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Generates trading orders based on ranking and current holdings.

        Parameters
        ----------
        settle : Optional[pd.Series]
            Previous settlement data (current holdings). If None, assumes no prior holdings.
        assets : float
            Total assets available for trading.
        count : int
            Number of top-ranked stocks to target.
        max_filter : int
            Maximum filter for holding stocks.
        high_low_adjust : bool, optional
            Whether to adjust for high/low limit prices. Defaults to True.
        mini : float, optional
            Minimum order size as a percentage of assets per stock. Defaults to 0.2.
        date : Optional[Union[int, pd.Timestamp]], optional
            The date or index for ranking. Defaults to None.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the generated orders.

        ---------------------------------------------------------------------------

        根据排名和当前持仓生成交易订单。

        参数
        ----------
        settle : Optional[pd.Series]
            以前的结算数据（当前持仓）。如果为 None，则假定没有先前的持仓。
        assets : float
            可用于交易的总资产。
        count : int
            目标排名前N的股票数量。
        max_filter : int
            持有股票的最大过滤器。
        high_low_adjust : bool, optional
            是否根据涨跌停价格进行调整。默认为 True。
        mini : float, optional
            每只股票最小订单量占资产的百分比。默认为 0.2。
        date : Optional[Union[int, pd.Timestamp]], optional
            用于排名的日期或索引。默认为 None。

        返回
        -------
        pd.DataFrame
            表示生成的订单的DataFrame。

        ---------------------------------------------------------------------------
        """
        if settle is None:
            rank = self.ranker(date=date)
            order = rank.iloc[:count].notnull().capital.to('share', assets=assets, is_adj=False).round(-2)
            order = pd.concat([order, rank.reindex(order.index)], axis=1)
        else:
            settle = settle[settle > 0]
            settle = settle[settle.index.isin(settle.internal_data.index)]
            assets = settle.total_assets()
            rank = self.ranker(date=date)
            hold_rank = rank.reindex(settle.index)
            if high_low_adjust:
                close_high = settle.internal_data.loc[settle.index]
                close_high = close_high.S_DQ_CLOSE == close_high.S_DQ_HIGH_LIMIT
                close_low = settle.internal_data.loc[settle.index]
                close_low = close_low.S_DQ_CLOSE == close_low.S_DQ_LOW_LIMIT
                still_hold = hold_rank[~close_low & (hold_rank <=count + max_filter) | close_high] # must sell if close == low_liomit, no sell if close == high_limit
            else:
                still_hold = hold_rank[hold_rank <=count + max_filter]
            if high_low_adjust:
                high_low_limit = settle.internal_data
                high_low_limit = (high_low_limit.S_DQ_CLOSE < high_low_limit.S_DQ_HIGH_LIMIT) & (high_low_limit.S_DQ_CLOSE > high_low_limit.S_DQ_LOW_LIMIT)
                high_low_limit = high_low_limit[high_low_limit]
                rank = rank[rank.index.isin(high_low_limit.index)]
                hope_hold = rank[~rank.index.isin(still_hold.index)].iloc[:max(count - still_hold.shape[0], 0)]
            else:
                hope_hold = rank.drop(still_hold.index).iloc[:max(count - still_hold.shape[0], 0)]
            hope = pd.concat([still_hold, hope_hold])
            order = (hope.notnull().capital.to('share', assets=assets, is_adj=False) - settle).round(-2)
            mini = assets / count * mini
            order = order[order.to('assets').reindex(order.index).abs() > mini]
            order = pd.concat([order, rank.reindex(order.index)], axis=1)
        order.columns = ['share'] + [rank.name]
        order = order.sort_values(rank.name)
        return order

    def order(
        self, 
        high_low_adjust: bool = True, 
        mini: float = 0.2, 
        date: Optional[Union[int, pd.Timestamp]] = None
    ) -> pd.DataFrame:
        """
        ===========================================================================

        Generates trading orders for the strategy.

        Parameters
        ----------
        high_low_adjust : bool, optional
            Whether to adjust for high/low limit prices. Defaults to False.
        mini : float, optional
            Minimum order size as a percentage of assets per stock. Defaults to 0.2.
        date : Optional[Union[int, pd.Timestamp]], optional
            The date or index for ranking. Defaults to None.

        Returns
        -------
        pd.DataFrame
            A DataFrame representing the generated orders.

        ---------------------------------------------------------------------------

        为策略生成交易订单。

        参数
        ----------
        high_low_adjust : bool, optional
            是否根据涨跌停价格进行调整。默认为 False。
        mini : float, optional
            每只股票最小订单量占资产的百分比。默认为 0.2。
        date : Optional[Union[int, pd.Timestamp]], optional
            用于排名的日期或索引。默认为 None。

        返回
        -------
        pd.DataFrame
            表示生成的订单的DataFrame。

        ---------------------------------------------------------------------------
        """
        settle = self.last_settle()
        assets = self.assets
        count = self.count
        max_filter = self.max_filter
        order = self.__order__(settle, assets, count, max_filter, high_low_adjust, mini, date)
        return order        
        
    def trade(
        self, 
        mini: float = 0.2, 
        **kwargs: Any
    ):
        """
        ===========================================================================

        Executes the trading process: generates, standardizes, and saves orders.

        Parameters
        ----------
        mini : float, optional
            Minimum order size as a percentage of assets per stock. Defaults to 0.2.
        **kwargs : Any
            Additional keyword arguments passed to the order generation.

        ---------------------------------------------------------------------------

        执行交易过程：生成、标准化和保存订单。

        参数
        ----------
        mini : float, optional
            每只股票最小订单量占资产的百分比。默认为 0.2。
        **kwargs : Any
            传递给订单生成的附加关键字参数。

        ---------------------------------------------------------------------------
        """
        order = self.order(mini=mini, **kwargs)
        order = self.order_standard(order)
        self.order_save(order)
        print(f'<{self.name}> order completed.')
        
    def test(
        self, 
        **kwargs: Any
    ):
        """
        ===========================================================================

        Performs a back-test of the strategy, saving test results.

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        执行策略回测，保存测试结果。

        参数
        ----------
        **kwargs : Any
            附加关键字参数。

        ---------------------------------------------------------------------------
        """
        df = self.factor.iloc[-2:, :].rank(ascending=False, axis=1).T
        df = df[(df <= self.count).any(axis=1)]
        df['returns_today'] = df.iloc[:, -1].capital.internal_data['S_DQ_PCTCHANGE']
        stock_name = pd.db.read(table='asharestatus').drop_duplicates(subset=COLUMNS_INFO.code, keep='last')[[COLUMNS_INFO.code, 'NAME']]
        df = pd.merge(stock_name, df, left_on=COLUMNS_INFO.code, right_index=True, how='right').set_index(COLUMNS_INFO.code)
        df = self.code_standard(df)
        self.test_save(df)
        print(f'<{self.name}> test completed.')
    
        
    def run(
        self, 
        **kwargs: Any
    ):
        """
        ===========================================================================

        Runs the strategy based on its configured type (e.g., 'trade' or 'test').

        Parameters
        ----------
        **kwargs : Any
            Additional keyword arguments passed to the specific strategy function.

        ---------------------------------------------------------------------------

        根据配置的类型（例如，'trade' 或 'test'）运行策略。

        参数
        ----------
        **kwargs : Any
            传递给特定策略函数的附加关键字参数。

        ---------------------------------------------------------------------------
        """
        self.__account_create__()
        func = getattr(self, self.type)
        func(**kwargs)  
