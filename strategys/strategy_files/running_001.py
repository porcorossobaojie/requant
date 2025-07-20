# -*- coding: utf-8 -*-
"""
Created on Tue May 13 00:09:57 2025

@author: Porco Rosso
"""

import factors
factors.daily()
import flow

from strategys.strategy_files import meta
from account import accounts
from strategys.config import running_001 as strategy_config
from strategys.account_system import main as account_system

import pandas as pd
pd.capitalize()
from libs.utils.functions import filter_class_attrs
from typing import Any, Dict, List, Optional, Union

class main(account_system, meta.main):
    """
    ===========================================================================

    Implements the 'running_001' trading strategy.

    ---------------------------------------------------------------------------

    实现'running_001'交易策略。

    ---------------------------------------------------------------------------
    """
    core: List[Any] = [factors.volatility]
    
    @classmethod
    def __internal_data__(cls) -> Dict[int, pd.DataFrame]:
        """
        ===========================================================================

        Loads and processes internal data for the 'running_001' strategy.

        Returns
        -------
        Dict[int, pd.DataFrame]
            A dictionary of internal data DataFrames.

        ---------------------------------------------------------------------------

        为'running_001'策略加载和处理内部数据。

        返回
        -------
        Dict[int, pd.DataFrame]
            内部数据DataFrames的字典。

        ---------------------------------------------------------------------------
        """
        if not hasattr(cls, '_internal_data'):
            x = [cls.core[0].volatility(), cls.core[0].abnormal1()]
            cls._internal_data = {i:j for i,j in enumerate(x)}
        return cls._internal_data
    
    @classmethod
    def __factor__(cls) -> pd.DataFrame:
        """
        ===========================================================================

        Calculates and processes the main factor for the 'running_001' strategy.

        Returns
        -------
        pd.DataFrame
            The calculated factor DataFrame.

        ---------------------------------------------------------------------------

        计算和处理'running_001'策略的主因子。

        返回
        -------
        pd.DataFrame
            计算出的因子DataFrame。

        ---------------------------------------------------------------------------
        """
        if not hasattr(cls, '_factor'):
            x = [cls.core[0].filter(i) for i in cls.__internal_data__().values()]
            x = cls.core[0].merge(*x)
            x = x.rollings(10).min(2).mean()
            x = cls.core[0].filter(x)
            cls._factor = x
        x = cls._factor
        return x
      
            
if __name__ == '__main__':
    self = main()
    # mini = 0.2 if pd.Timestamp.today().weekday() != 3 else 0
    mini: float = 0.2
    
    # Example usage (commented out in original, kept for reference):
    # self(**filter_class_attrs(accounts['BJ_13611823855']), **getattr(strategy_config, 'BJ_13611823855'))
    # self(**filter_class_attrs(accounts['HZG_15201991795']), **getattr(strategy_config, 'HZG_15201991795'))
    # self.factor()
    
    for i,j in accounts.items():
        self(**filter_class_attrs(j), **getattr(strategy_config, i))
        self.run(mini=mini)
