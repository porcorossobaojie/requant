# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:18:48 2025

@author: Porco Rosso

"""

# Standard library imports
from typing import Any, Callable, Dict, List, Optional, Union

# Third-party library imports
import numpy as np
import pandas as pd

# Local project-specific imports
from libs.utils.finance.roll.main import rolls
from __pandas__.config import ROLLS as config


@pd.api.extensions.register_series_accessor(config.CLASS_NAME)
@pd.api.extensions.register_dataframe_accessor(config.CLASS_NAME)
class main:
    def __init__(self, pandas_obj: pd.Series):
        self._obj = pandas_obj

    def __call__(
        self, 
        window: int, 
        min_periods: Optional[int] = None
    ) -> rolls:

        x = rolls(self._obj.to_frame(), window, min_periods)
        return x

@pd.api.extensions.register_dataframe_accessor(config.CLASS_NAME)
class main():
    def __init__(self, pandas_obj: pd.Series):
        self._obj = pandas_obj

    def __call__(
        self, 
        window: int, 
        min_periods: Optional[int] = None
    ) -> rolls:

        x = rolls(self._obj.to_frame(), window, min_periods)
        return x








