# -*- coding: utf-8 -*-
"""
Created on Mon May 19 11:40:21 2025

@author: Porco Rosso
"""

import flow
from factors import barra, volatility
import numpy as np
import pandas as pd
from factors.meta.main import main as meta

flow.data_init()
gfac1, gfac2 = volatility.volatility(), volatility.abnormal1()

