# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 13:14:44 2025

@author: Porco Rosso
"""

import data_source
daily = data_source.daily

import factors.barra
from factors.volatility.main import main as volatility
volatility = volatility()
