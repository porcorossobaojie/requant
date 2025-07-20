# -*- coding: utf-8 -*-
"""
Created on Sat May 10 15:52:25 2025

@author: Porco Rosso
"""

from account.main import main as meta_account
from account.config import ACCOUNTS, PATH

accounts = [meta_account(**i, **PATH) for i in ACCOUNTS]
accounts = {i.name:i for i in accounts}













