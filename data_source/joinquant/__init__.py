#
import jqdatasdk as jq

from data_source.joinquant.ann_dt_table import daily as ann_dt_daily
from data_source.joinquant.trade_dt_table import daily as trade_dt_daily

normalize_code = jq.normalize_code

def daily():
    ann_dt_daily()
    trade_dt_daily()
