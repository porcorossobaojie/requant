# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 20:23:04 2025

@author: Porco Rosso

"""
from typing import Any, Literal

import jqdatasdk as jq
import pandas as pd

from data_source.joinquant.config import TRADE_DT_TABLES as config
from data_source.joinquant.meta.main import main as meta


class main(meta):
    
    def __init__(self, **kwargs: Any) -> None:
        
        super().__init__(**kwargs)

    def pipeline(self, **kwargs: Any) -> pd.DataFrame:
        
        df = super().pipeline(**kwargs)

        # special fix:
        # 1. construct returns of portfolio by calculated with close price(first use adj price if have)
        # 2. adjust weight total from 100 to 1
        pct_key = 'S_DQ_PCTCHANGE'
        weight_key = 'S_DQ_IDXWEIGHT'
        if pct_key in self.columns.keys():
            try:
                df[pct_key] = df['S_DQ_CLOSE_ADJ'] / df['S_DQ_PRECLOSE_ADJ'] - 1
            except Exception:
                df[pct_key] = df['S_DQ_CLOSE'] / df['S_DQ_PRECLOSE'] - 1
        if weight_key in self.columns.keys():
            df[weight_key] = df[weight_key] / 100

        df = df[df.notnull().sum(axis=1) > df.shape[1] * 0.6]
        return df

    def daily(self, if_exists: Literal['append', 'replace'] = 'append') -> None:
        
        if self.table == 'asharelisting':  # this table inform the on list time for each stock, which will replace every day
            if_exists = 'replace'

        if if_exists == 'replace':
            self.drop_table()

        if not self.table_exist():
            self.create_table()

        id_key = self.__find_max_of_exist_table__(self.trade_dt)
        if self.table == 'ashareconcept':  # this table inform the ’题材‘ and '概念' for which not have data at 2010, the earlest data appeared at 2015
            id_key = max(pd.to_datetime('2015-01-01 15:00'), id_key)
        days = self._trade_days.copy()
        days = days[days > id_key]
        if self.table == 'asharelisting' and len(days):
            days = days[-1:]

        for i in days:
            if jq.get_query_count()['spare'] <= 5000000:
                break
            df = self.pipeline(date=f'{i.date()}')
            print(i)
            self.__write__(df, log=True)


