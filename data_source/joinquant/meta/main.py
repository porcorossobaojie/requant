# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 09:26:48 2025

@author: Porco Rosso

"""
import numpy as np
import pandas as pd
import jqdatasdk as jq
from typing import Any, Dict, List, Union

from data_source.joinquant.config import TABLE_INFO_AND_PUBLIC_KEYS, FILTER
from libs import db
from libs.DB import config
from libs.utils.functions import filter_class_attrs, merge_dicts
from local.login_info import SOURCE


class main(db.__DB_CLASS_DIC__[SOURCE], TABLE_INFO_AND_PUBLIC_KEYS, FILTER, getattr(config, SOURCE)):
    def __init__(self, **kwargs: Any) -> None:
        self.source = SOURCE
        super().__init__(**kwargs)
        self.__env_init__()
        self._stock = jq.get_all_securities('stock', date=None).index.tolist()
        trade_days = pd.to_datetime(jq.get_trade_days('2005-01-01')) + self.time_bias
        self._trade_days = trade_days[trade_days <= pd.Timestamp.today() - pd.Timedelta(5, 'h')]
    
    @property
    def columns(self) -> Dict:
        if isinstance(self.columns_information, dict):
            x = merge_dicts(*list(self.columns_information.values()))
        else:
            x = jq.get_table_info(self.columns_information)
            x.iloc[:, 0] = x.iloc[:, 0].replace(self.columns_replace).str.upper()
            x.iloc[:, 2] = x.iloc[:, 2].replace({'date': 'datetime', 'DATE': 'datetime'})
            x = x.set_index(x.columns[0]).iloc[:, [1, 0]].T.to_dict('list')
        return x

    def __columns_rename__(self, df: pd.DataFrame) -> pd.DataFrame:
        if isinstance(self.columns_information, dict):
            rename_dic = {i: list(j.keys())[0] for i, j in self.columns_information.items()}
        else:
            rename_dic = self.columns_replace
        df = df.reset_index().rename(rename_dic, axis=1)
        # it may be multi index here(individual_table.ashareindustrys)
        # and it is impossible to reanme from 2-dim multi-index object to 1-dim index
        # so it fix the problem here
        if df.columns.nlevels > 1:
            df.columns = [rename_dic.get(col, col) for col in df.columns]
        df.columns = df.columns.str.upper()
        df = df.loc[:, df.columns.isin(list(self.columns.keys()))]
        return df

    def __get_data_from_jq_remote__(self, **kwargs: Any) -> pd.DataFrame:
        df = eval(self.jq_command.format(**kwargs))
        return df

    def __data_standard__(self, df: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
        df = self.__columns_rename__(df)
        for i in [self.ann_dt, self.trade_dt]:
            if i in df.columns:
                df[i] = pd.to_datetime(df[i]) + self.time_bias
            if (i not in df.columns) and i in self.columns.keys():
                try:
                    df[i] = pd.to_datetime(kwargs['date']) + self.time_bias
                except KeyError:
                    pass
        df = df.replace({np.inf: np.nan, -np.inf: np.nan})
        return df

    def pipeline(self, **kwargs: Any) -> pd.DataFrame:
        df = self.__get_data_from_jq_remote__(**kwargs)
        df = self.__data_standard__(df, **kwargs)
        return df

    def __find_max_of_exist_table__(
        self, columns: str, **kwargs: Any
        ) -> Union[int, float, pd.Timestamp]:
        id_key = None
        if self.table_exist():
            id_key = self.__read__(columns=f'MAX({columns})', show_time=False, **kwargs).iloc[0, 0]
            id_key = None if pd.isnull(id_key) else id_key

        if id_key is None:
            if 'DATE' in self.columns.get(columns, ['None'])[0].upper():
                id_key = self.trade_start
            else:
                id_key = 0
        return id_key

    def create_table(self, **kwargs: Any) -> None:
        parameters = {'columns': self.columns, 'log': True}
        if self.source == 'MySQL':
            keys = (
                self.ann_dt
                if self.trade_dt not in self.columns.keys()
                else self.trade_dt
                )
            partition = None if keys != self.trade_dt else {self.trade_dt: self.partition}
            parameters = (
                self.__parameters__()
                | {'keys': keys, 'partition': partition}
                | {'columns': self.columns, 'log': True}
                | kwargs
                )
        else:
            parameters = self.__parameters__(parameters, kwargs)

        super().__create_table__(**parameters)

    def drop_table(self, **kwargs: Any) -> None:
        parameters = self.__parameters__({'log': True}, kwargs)
        super().__drop_table__(**parameters)
        
    def table_exist(self):
        return super().__table_exist__()
        
        
'''        
from local.login_info import JQ_LOGIN_INFO
import jqdatasdk as jq
jq.auth (**JQ_LOGIN_INFO)
    
from data_source.joinquant.config import ANN_DT_TABLES as config
config = config()
self = main(**config.asharebalancesheet)
self.daily()
        
 '''       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        