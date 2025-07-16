# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 20:23:04 2025

@author: Porco Rosso

"""
from typing import Any, Literal

import jqdatasdk as jq
import pandas as pd

from data_source.joinquant.config import ANN_DT_TABLES as config
from data_source.joinquant.meta.main import main as meta


class main(meta):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def pipeline(self, **kwargs: Any) -> pd.DataFrame:
        df = super().pipeline(**kwargs)
        return df

    def daily(self, if_exists: Literal['append', 'replace'] = 'append') -> None:
        if if_exists == 'replace':
            self.drop_table()

        if not self.table_exist():
            self.create_table()

        id_key = self.__find_max_of_exist_table__(self.ann_dt)
        days = self._trade_days.copy()
        days = days[days > id_key]

        for i in days:
            if jq.get_query_count()['spare'] <= 5000000:
                break
            df = self.pipeline(date=f'{i.date()}')
            print(i)
            self.write(df, log=True)


'''
test:

self = main(**config.asharebalancesheet)
self.daily()
'''