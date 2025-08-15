# -*- coding: utf-8 -*-
"""
Created on Sat May 10 15:59:35 2025

@author: Porco Rosso

"""

from typing import Dict, List, Any

PATH: Dict[str, str] = {
    'account_path':     'd:/account', 
    'order_dir':        'order', 
    'settle_dir':       'settle',
    'test_dir':         'test'
}

ACCOUNTS: List[Dict[str, Any]] = [
    {
        'name':        'BJ_13611823855', 
        'id':          '1196777',
        'password':    '314159',
        'broker':      'guotai',
        'assets':      None,
        'type':        'trade',
        'data_format': 'tonghua'
    },
    
    {
        'name':        'HZG_15201991795', 
        'id':          '325319056109',
        'password':    '025410',
        'broker':      'pingan',
        'assets':      1000000,
        'type':        'trade',
        'data_format': 'tonghua'
    },
    
    {
        'name':        'CSQ_stockay', 
        'type':        'test',
    },
    
    {
        'name':         'ZHA_jingantu',         
        'type':         'test'
    },
    
    {
        'name':        'CHM_18916489338', 
        'id':          '1196777',
        'password':    '314159',
        'broker':      'guotai',
        'assets':      1000000,
        'type':        'trade',
        'data_format': 'tonghua'
    },

    {
        'name':        'ALEXLOU88', 
        'id':          '0331330018804897',
        'password':    '379103',
        'broker':      'guotai',
        'assets':      790000,
        'type':        'trade',
        'data_format': 'tonghua'
    },
]
