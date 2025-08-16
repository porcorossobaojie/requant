# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:23:09 2025

@author: Porco Rosso
"""

from libs import __flow__ as flow
from typing import Dict, Any, List

PROPERTY_ATTRS_DIC: Dict[str, str] = ({
    i.split('S_DQ_')[-1].lower():i 
    for i in flow.stock.help('ashareeodprices')[flow.config.DB_INFO.columns_info].values 
    if 'S_DQ_' in i
    } |
    {
    i.split('S_DQ_')[-1].lower():i 
    for i in flow.stock.help('ashareeodderivativeindicator')[flow.config.DB_INFO.columns_info].values 
    if 'S_DQ_' in i
    })

PROPERTY_ATTRS_CLS: type = type('PROPERTY_ATTRS' , (), PROPERTY_ATTRS_DIC)

class LIMIT:
    """
    ===========================================================================

    Configuration for various limits and filters applied to factors.

    ---------------------------------------------------------------------------

    应用于因子的各种限制和过滤的配置。

    ---------------------------------------------------------------------------
    """
    IS_ST_FILTER: int = 0
    ON_LIST_LIMIT: int = 126

class volatility:
    """
    ===========================================================================

    Configuration for volatility-related factors.

    ---------------------------------------------------------------------------

    波动率相关因子的配置。

    ---------------------------------------------------------------------------
    """
    class __AMOUNT__:
        """
        ===========================================================================

        Configuration for amount-based volatility factors.

        ---------------------------------------------------------------------------

        基于成交量的波动率因子的配置。

        ---------------------------------------------------------------------------
        """
        periods: List[int] = [42, 63, 126]

    class __TURNOVER__:
        """
        ===========================================================================

        Configuration for turnover-based volatility factors.

        ---------------------------------------------------------------------------

        基于换手率的波动率因子的配置。

        ---------------------------------------------------------------------------
        """
        periods: List[int] = [42, 63, 126]

    class __REVERSAL__:
        """
        ===========================================================================

        Configuration for reversal-based volatility factors.

        ---------------------------------------------------------------------------

        基于反转的波动率因子的配置。

        ---------------------------------------------------------------------------
        """
        periods: List[int] = [42, 63, 126]

class industry:
    """
    ===========================================================================

    Configuration for industry classification factors.

    ---------------------------------------------------------------------------

    行业分类因子的配置。

    ---------------------------------------------------------------------------
    """
    SW_KEYS: List[str] = ['S_SWL1_CODE', 'S_SWL2_CODE', 'S_SWL3_CODE']
    ZJ_KEYS: List[str] = ['S_ZJW_CODE']
    JQ_KEYS: List[str] = ['S_JQL1_CODE', 'S_JQL2_CODE']
    IND_KEYS: List[str] = SW_KEYS + ZJ_KEYS + JQ_KEYS
    
class factorlize:
    BARRA_MODEL = 'cn4'
    BARRA_NEUTRAL = ['L1_Size', 'L1_Bm', 'L1_Non_size', 'L1_Beta', 'L1_Momentum', 'L1_Earning']
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
