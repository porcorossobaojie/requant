"""
===========================================================================

Initializes the pandas module.

This module sets up warnings, matplotlib configurations, and imports
sub-modules for pandas-related functionalities.

---------------------------------------------------------------------------

初始化 pandas 模块。

此模块设置警告、matplotlib 配置，并导入与 pandas 相关功能的子模块。

---------------------------------------------------------------------------
"""

# Standard library imports
import warnings

# Third-party library imports
import matplotlib.pyplot as plt
from pylab import mpl
import pandas as pd

# Local project-specific imports
from __pandas__ import __analysis__
from __pandas__ import __build__
from __pandas__ import __DB__
from __pandas__ import __rolls__
from __pandas__ import __stats__
from __pandas__ import __tools__
def capitalize():
    import __pandas__.__back_test__

        
pd.capitalize = capitalize
warnings.simplefilter(action='ignore')
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']


