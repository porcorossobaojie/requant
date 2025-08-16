# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 13:05:00 2025

@author: Porco Rosso
"""

from local.login_info import SOURCE


class DB:
    """
    ===========================================================================

    Public parameters for class "DB".

    ---------------------------------------------------------------------------

    "DB"类的公共参数。

    ---------------------------------------------------------------------------
    """
    CLASS_NAME: str = 'db'


class ANALYSIS:
    """
    ===========================================================================

    Configuration class for analysis module.

    This class holds static configuration values for the analysis module.

    ---------------------------------------------------------------------------

    分析模块的配置类。

    此类包含分析模块的静态配置值。

    ---------------------------------------------------------------------------
    """
    CLASS_NAME: str = 'analysis'


class BUILD:
    """
    ===========================================================================

    Configuration class for build module.

    This class holds static configuration values for the build module.

    ---------------------------------------------------------------------------

    构建模块的配置类。

    此类包含构建模块的静态配置值。

    ---------------------------------------------------------------------------
    """
    CLASS_NAME: str = 'build'


class ROLLS:
    """
    ===========================================================================

    Configuration class for rolls module.

    This class holds static configuration values for the rolls module.

    ---------------------------------------------------------------------------

    滚动模块的配置类。

    此类包含滚动模块的静态配置值。

    ---------------------------------------------------------------------------
    """
    CLASS_NAME: str = 'rollings'


class STATS:
    """
    ===========================================================================

    Configuration class for stats module.

    This class holds static configuration values for the stats module.

    ---------------------------------------------------------------------------

    统计模块的配置类。

    此类包含统计模块的静态配置值。

    ---------------------------------------------------------------------------
    """
    CLASS_NAME: str = 'stats'


class TOOLS:
    """
    ===========================================================================

    Configuration class for tools module.

    This class holds static configuration values for the tools module.

    ---------------------------------------------------------------------------

    工具模块的配置类。

    此类包含工具模块的静态配置值。

    ---------------------------------------------------------------------------
    """
    CLASS_NAME: str = 'tools'
        
class BACK_TEST:
    CLASS_NAME:str = 'capital'
        
class FACTORIZE:
    CLASS_NAME:str = 'f'
        
        