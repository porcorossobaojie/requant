# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 14:21:35 2025

@author: Porco Rosso

"""

from data_source.joinquant.meta.main import main as meta

from data_source.joinquant.config import ANN_DT_TABLES as config
from typing import Literal, Any

class main(meta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def daily(self, if_exists: Literal['append', 'replace'] = 'append'):
        if if_exists == 'replace':
            self.drop_table()
        
        if not self.table_exist():
            self.create_table()
        
        id_key = self.__find_max_of_exist_table__(self.id_key)
        df = self.pipeline(id_key=id_key)
        self.write(df, log=True)
        while len(df):
            id_key = df[self.id_key].max()
            df = self.pipeline(id_key=id_key)
            self.write(df, log=True)

'''
test:
self =main(**config.asharebalancesheet)
self.daily()

'''
    
    
    