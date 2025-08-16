# -*- coding: utf-8 -*-
"""
Created on Thu May  8 17:10:40 2025

@author: Porco Rosso
"""

import pandas as pd

from libs.__pandas__.config import BACK_TEST
from libs.back_test.main import Series, DataFrame

@pd.api.extensions.register_dataframe_accessor(BACK_TEST.CLASS_NAME)
class capital():
    """
    ===========================================================================

    Extends pandas DataFrame with back-testing functionalities.

    ---------------------------------------------------------------------------

    使用回测功能扩展pandas DataFrame。

    ---------------------------------------------------------------------------
    """
    def __new__(cls, pandas_obj: pd.DataFrame) -> DataFrame:
        """
        ===========================================================================

        Factory to create a back-testing DataFrame object.

        Parameters
        ----------
        pandas_obj : pd.DataFrame
            The pandas DataFrame to be extended.

        Returns
        -------
        DataFrame
            An instance of the back-testing DataFrame.

        ---------------------------------------------------------------------------

        创建回测DataFrame对象的工厂。

        参数
        ----------
        pandas_obj : pd.DataFrame
            要扩展的pandas DataFrame。

        返回
        -------
        DataFrame
            回测DataFrame的实例。

        ---------------------------------------------------------------------------
        """
        return DataFrame(pandas_obj)
    
@pd.api.extensions.register_series_accessor(BACK_TEST.CLASS_NAME)
class capital():
    """
    ===========================================================================

    Extends pandas Series with back-testing functionalities.

    ---------------------------------------------------------------------------

    使用回测功能扩展pandas Series。

    ---------------------------------------------------------------------------
    """
    def __new__(cls, pandas_obj: pd.Series) -> Series:
        """
        ===========================================================================

        Factory to create a back-testing Series object.

        Parameters
        ----------
        pandas_obj : pd.Series
            The pandas Series to be extended.

        Returns
        -------
        Series
            An instance of the back-testing Series.

        ---------------------------------------------------------------------------

        创建回测Series对象的工厂。

        参数
        ----------
        pandas_obj : pd.Series
            要扩展的pandas Series。

        返回
        -------
        Series
            回测Series的实例。

        ---------------------------------------------------------------------------
        """
        return Series(pandas_obj)
