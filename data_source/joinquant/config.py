# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 08:34:15 2025

@author: Porco Rosso

"""

from typing import Any, Dict, List, Tuple, Union

import jqdatasdk as jq
import pandas as pd

from data_source.config import PUBLIC_KEYS

class TABLE_INFO_AND_PUBLIC_KEYS(PUBLIC_KEYS):
    
    partition: pd.DatetimeIndex = pd.date_range(
        '2005-01-01', '2030-12-31', freq='YE'
        )
    primary_key: str = 'UNIQUE_KEY'
    id_key: str = 'ID_KEY'
    columns_replace: Dict[str, Dict[str, str]] = {
        'id': 'ID_KEY',
        'code': 'S_INFO_WINDCODE',
        'pub_date': 'ANN_DT',
        'implementation_pub_date': 'ANN_DT',
        'date': 'REPORT_PERIOD',
        'report_date': 'REPORT_PERIOD',
        'time': 'TRADE_DT',
        'day': 'TRADE_DT',
        }


class FILTER:
    
    trade_start = pd.to_datetime('2010-01-01 15:00')

class ANN_DT_TABLES:
    def __init__(self):
        self.asharebalancesheet: Dict[str, Union[str, Any]] = {
            'table': 'asharebalancesheet',
            'columns_information': jq.finance.STK_BALANCE_SHEET,
            'jq_command': (
                'jq.finance.run_query(jq.query(jq.finance.STK_BALANCE_SHEET)'
                '.order_by(jq.finance.STK_BALANCE_SHEET.id)'
                '.filter((jq.finance.STK_BALANCE_SHEET.source_id == 321003) '
                '& (jq.finance.STK_BALANCE_SHEET.report_type == 0) '
                '& (jq.finance.STK_BALANCE_SHEET.id > {id_key})).limit(5000))'
                ),
            }

        self.asharecashflow: Dict[str, Union[str, Any]] = {
            'table': 'asharecashflow',
            'columns_information': jq.finance.STK_CASHFLOW_STATEMENT,
            'jq_command': (
                'jq.finance.run_query(jq.query(jq.finance.STK_CASHFLOW_STATEMENT)'
                '.order_by(jq.finance.STK_CASHFLOW_STATEMENT.id)'
                '.filter((jq.finance.STK_CASHFLOW_STATEMENT.source_id == 321003) '
                '& (jq.finance.STK_CASHFLOW_STATEMENT.report_type == 0) '
                '& (jq.finance.STK_CASHFLOW_STATEMENT.id > {id_key})).limit(5000))'
                ),
            }

        self.ashareincome: Dict[str, Union[str, Any]] = {
            'table': 'ashareincome',
            'columns_information': jq.finance.STK_INCOME_STATEMENT,
            'jq_command': (
                'jq.finance.run_query(jq.query(jq.finance.STK_INCOME_STATEMENT)'
                '.order_by(jq.finance.STK_INCOME_STATEMENT.id)'
                '.filter((jq.finance.STK_INCOME_STATEMENT.source_id == 321003) '
                '& (jq.finance.STK_INCOME_STATEMENT.report_type == 0) '
                '& (jq.finance.STK_INCOME_STATEMENT.id > {id_key})).limit(5000))'
                ),
            }

        self.ashareperformanceletter: Dict[str, Union[str, Any]] = {
            'table': 'ashareperformance_lt',
            'columns_information': jq.finance.STK_PERFORMANCE_LETTERS,
            'jq_command': (
                'jq.finance.run_query(jq.query(jq.finance.STK_PERFORMANCE_LETTERS)'
                '.order_by(jq.finance.STK_PERFORMANCE_LETTERS.id)'
                '.filter((jq.finance.STK_PERFORMANCE_LETTERS.report_type == 0) '
                '& (jq.finance.STK_PERFORMANCE_LETTERS.id > {id_key})).limit(5000))'
                ),
            }

        self.ashareforcast: Dict[str, Union[str, Any]] = {
            'table': 'ashareforcast',
            'columns_information': jq.finance.STK_FIN_FORCAST,
            'jq_command': (
                'jq.finance.run_query(jq.query(jq.finance.STK_FIN_FORCAST)'
                '.order_by(jq.finance.STK_FIN_FORCAST.id)'
                '.filter(jq.finance.STK_FIN_FORCAST.id > {id_key}))'
                ),
            }

        self.asharedividend: Dict[str, Union[str, Any]] = {
            'table': 'asharedividend',
            'columns_information': jq.finance.STK_XR_XD,
            'jq_command': (
                'jq.finance.run_query(jq.query(jq.finance.STK_XR_XD)'
                '.order_by(jq.finance.STK_XR_XD.id)'
                '.filter((jq.finance.STK_XR_XD.id > {id_key}) '
                '& (jq.finance.STK_XR_XD.report_date >= "2004-01-01")))'
                ),
            }

        self.asharestatus: Dict[str, Union[str, Any]] = {
            'table': 'asharestatus',
            'columns_information': jq.finance.STK_STATUS_CHANGE,
            'jq_command': (
                'jq.finance.run_query(jq.query(jq.finance.STK_STATUS_CHANGE)'
                '.order_by(jq.finance.STK_STATUS_CHANGE.id)'
                '.filter((jq.finance.STK_STATUS_CHANGE.id > {id_key})).limit(5000))'
                ),
            }


class TRADE_DT_TABLES:
    
    def __init__(self):
        self.ashareeodprices: Dict[str, Union[str, Dict[str, List[Union[str, int]]], Any]] = {
            'table': 'ashareeodprices',
            'columns_information': {
                'time': {'TRADE_DT': ['datetime', '交易日']},
                'code': {'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码']},
                'open': {'S_DQ_OPEN': ['double(12, 2)', '开盘价(元)']},
                'close': {'S_DQ_CLOSE': ['double(12, 2)', '收盘价(元)']},
                'low': {'S_DQ_LOW': ['double(12, 2)', '最低价(元)']},
                'high': {'S_DQ_HIGH': ['double(12, 2)', '最高价(元)']},
                'volume': {'S_DQ_VOLUME': ['bigint', '成交量(股)']},
                'money': {'S_DQ_AMOUNT': ['bigint', '成交量(元)']},
                'high_limit': {'S_DQ_HIGH_LIMIT': ['double(12, 2)', '涨停价(元)']},
                'low_limit': {'S_DQ_LOW_LIMIT': ['double(12, 2)', '跌停价(元)']},
                'avg': {'S_DQ_AVGPRICE': ['double(12, 2)', 'VWAP(元)']},
                'pre_close': {'S_DQ_PRECLOSE': ['double(12, 2)', '昨收盘价(元)']},
                'paused': {'S_DQ_TRADESTATUS': ['int(1)', '交易状态']},
                'factor': {'S_DQ_POST_FACTOR': ['double(16, 6)', '后复权因子']},
                'open_adj': {'S_DQ_OPEN_ADJ': ['double(18, 8)', '后复权开盘价(元)']},
                'avg_adj': {'S_DQ_AVGPRICE_ADJ': ['double(18, 8)', '后复权VWAP(元)']},
                'close_adj': {'S_DQ_CLOSE_ADJ': ['double(18, 8)', '后复权收盘价(元)']},
                'pre_close_adj': {
                    'S_DQ_PRECLOSE_ADJ': ['double(18, 8)', '后复权昨收盘价(元)']
                    },
                '': {'S_DQ_PCTCHANGE': ['double(10, 8)', '涨跌幅']},
                },
            'jq_command': (
                "pd.merge("
                "jq.get_price(self._stock, fields=['open','close','low','high','volume','money', 'high_limit','low_limit','avg','pre_close','paused'], start_date='{date}', end_date='{date}', fq=None, skip_paused=False).set_index(['code']), "
                "jq.get_price(self._stock, fields=['factor', 'open', 'close', 'avg', 'pre_close'], start_date='{date}', end_date='{date}', fq='post', skip_paused=False).drop('time', axis=1).set_index(['code']),"
                "suffixes=('', '_adj'), left_index=True, right_index=True).reset_index()"
                ),
            }
    
        self.ashareeodderivativeindicator: Dict[
            str, Union[str, Dict[str, List[Union[str, int]]], Any]
            ] = {
                'table': 'ashareeodderivativeindicator',
                'columns_information': {
                    'day': {'TRADE_DT': ['datetime', '交易日']},
                    'code': {'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码']},
                    'capitalization': {'S_VAL_SHR': ['double(20, 4)', '总股本']},
                    'circulating_cap': {'S_DQ_SHR': ['double(20, 4)', '流通股本']},
                    'market_cap': {'S_VAL_MV': ['double(20, 4)', '总市值']},
                    'a_market_cap': {'S_VAL_AMV': ['double(20, 4)', '总市值(A股)']},
                    'circulating_market_cap': {
                        'S_DQ_MV': ['double(20, 4)', '流通市值']
                        },
                    'turnover_ratio': {
                        'S_DQ_FREETURNOVER': [
                            'double(20, 4)',
                            '换手率\n[指定交易日成交量(手)100/截至该日股票的自由流通股本(股)]*100%'
                            ]
                        },
                    'pe_ratio': {
                        'S_DQ_PE_TTM': [
                            'double(20, 4)',
                            '市盈率(PE, TTM)\n市盈率（PE，TTM）=（股票在指定交易日期的收盘价 * '
                            '当日人民币外汇挂牌价* 截止当日公司总股本）/归属于母公司股东的净利润TTM'
                            ]
                        },
                    'pe_ratio_lyr': {
                        'S_DQ_PE_LYR': [
                            'double(20, 4)',
                            '市盈率(PE, LYR)\n市盈率（PE）=（股票在指定交易日期的收盘价 * '
                            '当日人民币外汇牌价 * 截至当日公司总股本）/归属母公司股东的净利润'
                            ]
                        },
                    'pb_ratio': {
                        'S_DQ_PB': [
                            'double(20,4)',
                            '市净率(PB)\n市净率=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * '
                            '截至当日公司总股本）/归属母公司股东的权益'
                            ]
                        },
                    'ps_ratio': {
                        'S_DQ_PS_TTM': [
                            'double(20, 4)',
                            '市销率(PS, TTM)\n市销率TTM=（股票在指定交易日期的收盘价 * '
                            '当日人民币外汇牌价 * 截至当日公司总股本）/营业总收入TTM'
                            ]
                        },
                    'pcf_ratio': {
                        'S_DQ_PCF_TTM': [
                            'double(20, 4)',
                            '市现率(PCF, 现金净流量TTM)\n市现率=（股票在指定交易日期的收盘价 * '
                            '当日人民币外汇牌价 * 截至当日公司总股本）/现金及现金等价物净增加额TTM'
                            ]
                        },
                    'pcf_ratio2': {
                        'S_DQ_POCF_TTM': [
                            'double(20, 4)',
                            '市现率(PCF, 经营现金净流量TTM)\n市现率=（股票在指定交易日期的收盘价 * '
                            '截至当日公司总股本）/经营活动现金及经营活动现金等价物净增加额TTM'
                            ]
                        },
                    'dividend_ratio': {
                        'S_DQ_DIVRATIO_TTM': [
                            'double(20, 4)',
                            '(近12个月派现合计/总市值)/100'
                            ]
                        },
                    'free_market_cap': {
                        'S_FREE_MV': [
                            'double(20, 4)',
                            '自由流通市值(亿元), A股收盘价*自由流通股本, '
                            '自由流通股本 = 流通股本-其他扣除数(如高管限售25%)'
                            ]
                        },
                    },
                'jq_command': 'jq.get_fundamentals(jq.query(jq.valuation), date="{date}")'
                }
    
        self.ashareindicator: Dict[str, Union[str, Any]] = {
            'table': 'ashareindicator',
            'columns_information': jq.indicator,
            'jq_command': 'jq.get_fundamentals_continuously(jq.query(jq.indicator),  end_date="{date}")',
            }
    
        self.aindexeodprices: Dict[
            str, Union[str, List[str], Dict[str, List[Union[str, int]]], Any]
            ] = {
                'table': 'aindexeodprices',
                'security': [
                    '000016.XSHG', '000852.XSHG', '000905.XSHG', '399300.XSHE',
                    '399303.XSHE', '000985.XSHG'
                    ],
                'fields': [
                    'avg', 'close', 'high', 'low', 'money', 'open', 'pre_close',
                    'volume'
                    ],
                'columns_information': {
                    'time': {'TRADE_DT': ['datetime', '交易日']},
                    'code': {
                        'S_INFO_WINDCODE': [
                            'VARCHAR(16)',
                            '股票代码: 000016(上证50), 000852(中证1000指数), '
                            '000905(中证500), 399300(沪深300), 399303(国证2000), '
                            '000985(中证全指)'
                            ]
                        },
                    'avg': {'S_DQ_AVGPRICE': ['double(20,4)', '均价(VWAP)']},
                    'high': {'S_DQ_HIGH': ['double(20,4)', '最高价']},
                    'low': {'S_DQ_LOW': ['double(20,4)', '最低价']},
                    'money': {'S_DQ_AMOUNT': ['double(20,6)', '成交金额(千元)']},
                    'open': {'S_DQ_OPEN': ['double(20,4)', '开盘价']},
                    'volume': {'S_DQ_VOLUME': ['double(20,6)', '成交量(手)']},
                    'close': {'S_DQ_CLOSE': ['double(20,4)', '收盘价']},
                    'pre_close': {'S_DQ_PRECLOSE': ['double(20,4)', '昨收盘价']},
                    '': {'S_DQ_PCTCHANGE': ['double(12,8)', '涨跌幅(%%)']},
                    },
                'jq_command': 'jq.get_price(self.security, fields=self.fields, start_date="{date}", end_date="{date}", fq=None, skip_paused=False)'  
                }
        self.aindexweights: Dict[
            str, Union[str, List[str], Dict[str, List[Union[str, int]]], Any]
            ] = {
                'table': 'aindexweights',
                'security': [
                    '000016.XSHG', '000852.XSHG', '000905.XSHG', '399300.XSHE', '399303.XSHE', '000985.XSHG'
                    ],
                'fields': ['date', 'weight'],
                'columns_information': {
                    'level_1': {
                        'S_INFO_WINDCODE': [
                            'VARCHAR(16)',
                            '股票代码: 000016(上证50), 000852(中证1000指数), 000905(中证500), 399300(沪深300), 399303(国证2000), 000985(中证全指)'
                            ]
                        },
                    'date': {'REPORT_PERIOD': ['datetime', '报告期']},
                    'weight': {'S_DQ_IDXWEIGHT': ['double(6, 4)', '权重']},
                    'level_0': {'S_INFO_IDXCODE': ['VARCHAR(16)', '指数代码']},
                    '': {'TRADE_DT': ['datetime', '交易日']},
                    },
                'jq_command': 'pd.concat({{sec:jq.get_index_weights(sec ,date="{date}")[self.fields] for sec in self.security}}).reset_index()' 
                }
        self.ashareindustrys: Dict[
            str, Union[str, Dict[str, List[Union[str, Tuple[str, str]]]], Any]
            ] = {
                'table': 'ashareindustrys',
                'columns_information': {
                    ('', ''): {'TRADE_DT': ['datetime', '交易日']},
                    ('index', ''): {'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码']},
                    ('sw_l1', 'industry_code'): {'S_SWL1_CODE': ['int', '申万一级分类']},
                    ('sw_l1', 'industry_name'): {'S_SWL1_NAME': ['varchar(16)', '申万一级分类']},
                    ('sw_l2', 'industry_code'): {'S_SWL2_CODE': ['int', '申万二级分类']},
                    ('sw_l2', 'industry_name'): {'S_SWL2_NAME': ['varchar(16)', '申万二级分类']},
                    ('sw_l3', 'industry_code'): {'S_SWL3_CODE': ['int', '申万三级分类']},
                    ('sw_l3', 'industry_name'): {'S_SWL3_NAME': ['varchar(16)', '申万三级分类']},
                    ('zjw', 'industry_code'): {'S_ZJW_CODE': ['varchar(16)', '证监会分类']},
                    ('zjw', 'industry_name'): {'S_ZJW_NAME': ['varchar(32)', '证监会分类']},
                    ('jq_l1', 'industry_code'): {'S_JQL1_CODE': ['varchar(16)', '聚宽一级分类']},
                    ('jq_l1', 'industry_name'): {'S_JQL1_NAME': ['varchar(16)', '聚宽一级分类']},
                    ('jq_l2', 'industry_code'): {'S_JQL2_CODE': ['varchar(16)', '聚宽二级分类']},
                    ('jq_l2', 'industry_name'): {'S_JQL2_NAME': ['varchar(16)', '聚宽二级分类']}},
                'jq_command': 'pd.concat({{i:pd.DataFrame(j) for i,j in jq.get_industry(self._stock, date="{date}").items()}}).unstack().reset_index()'  
                }
    
        self.asharelisting: Dict[
            str, Union[str, Dict[str, List[Union[str, int]]], Any]
            ] = {
                'table': 'asharelisting',
                'columns_information': {
                    'index': {'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码', ]},
                    'display_name': {'S_INFO_COMPNAME': ['VARCHAR(16)', '股票名称', ]},
                    'name': {'S_INFO_COMPNAME_EN': ['VARCHAR(16)', '股票名称_英文', ]},
                    'start_date': {'S_INFO_LISTDATE': ['datetime', '上市日期', ]},
                    'end_date': {'S_INFO_DELISTDATE': ['datetime', '退市日期', ]},
                    },
                'jq_command': "jq.get_all_securities(['stock'], None).reset_index()",
                }
    
        self.ashareconcept: Dict[
            str, Union[str, Dict[str, List[Union[str, int]]], Any]
            ] = {
                'table': 'ashareconcept',
                'columns_information': {
                    'level_1': {'TRADE_DT': ['datetime', '交易日']},
                    'level_0': {'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码']},
                    'concept_code': {'S_CONCEPT_CODE': ['VARCHAR(8)', '概念代码']},
                    'concept_name': {'S_CONCEPT_NAME': ['VARCHAR(16)', '概念名称']},
                    },
                'jq_command': "pd.concat({{i:pd.DataFrame(list(j.values())[0]) for i,j in jq.get_concept(self._stock, '{date}').items()}}).reset_index().assign(level_1=lambda x: x['level_1'].astype('str').str.replace(r'^\\d+$', '{date}', regex=True))"
                }    
        
        
        