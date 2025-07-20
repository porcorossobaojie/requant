# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 10:44:33 2025

@author: Porco Rosso
"""

from functools import reduce

from pandas import DataFrame as meta_DataFrame
from pandas import Series as Series

from factors.config import factorlize, LIMIT
import flow

    
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

    def reversal(self, periods=3, how='mean'):
        returns = flow.stock('s_dq_pctchange').unstack().rolling(periods)
        returns = getattr(returns, how)()
        x = self.stats.neutral(fac=returns).resid
        return x
    
    def barra_neutral(self,
                      neutral_factors=None
        ):
        from factors import barra
        neu_class = getattr(barra, factorlize.BARRA_MODEL)
        neutral_factors = factorlize.BARRA_NEUTRAL if neutral_factors is None else neutral_factors   
        x = neu_class.neutral(self, neutral_factors=neutral_factors)
        return x
        
    def limit(
        self, 
        st_limit=None, 
        on_list_limit=None
    ):
        st_limit = LIMIT.IS_ST_FILTER if st_limit is None else st_limit
        on_list_limit = LIMIT.ON_LIST_LIMIT if on_list_limit is None else on_list_limit
        x = self[(flow.is_st() <= st_limit) & flow.be_list(on_list_limit)]
        x = x.capital
        return x
    
    def members(
        self, 
        index_code_list = ['000016.XSHG', # 上证50
                           '000852.XSHG', # 中证1000
                           '000905.XSHG', # 中证500
                           '000985.XSHG', # 中证全指
                           '399300.XSHE', # 沪深300 
                           '399303.XSHE'] # 国证2000
    ):
        if isinstance(index_code_list, str):
            index_code_list = [index_code_list]
        indexs = flow.index.index_member()
        indexs = [indexs[i].reindex_like(self).notnull() for i in index_code_list]
        indexs = reduce(lambda x, y: x | y, indexs)
        x = self[indexs]
        x = x.capital
        return x
    
