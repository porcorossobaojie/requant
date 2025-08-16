# config file

from data_source.joinquant.config import TABLE_INFO_AND_PUBLIC_KEYS

class COLUMNS_INFO(TABLE_INFO_AND_PUBLIC_KEYS):
    drop_columns = [TABLE_INFO_AND_PUBLIC_KEYS.primary_key, TABLE_INFO_AND_PUBLIC_KEYS.id_key]
    
class FILTER:
    ann_start = '2011-12-31 15:00'
    trade_start = '2014-01-01 15:00'
    
class DB_INFO:
    schema_info = 'TABLE_SCHEMA'
    table_info = 'TABLE_NAME'
    columns_info = 'COLUMN_NAME'
    comment_info = 'COLUMN_COMMENT'

class FACTORIZE:
    on_list_limit = 126
    index_mapping =  {
        '50': '000016.XSHG',
        '000016': '000016.XSHG', 
        '000016.XSHG': '000016.XSHG',
        '300': '399300.XSHE',
        '399300': '399300.XSHE',
        '399300.XSHE': '399300.XSHE',
        '500': '000905.XSHG',
        '000905': '000905.XSHG',
        '000905.XSHG': '000905.XSHG',
        '1000': '000852.XSHG',
        '000852': '000852.XSHG',
        '000852.XSHG': '000852.XSHG',
        '2000': '399303.XSHE',
        '399303': '399303.XSHE',
        '399303.XSHE': '399303.XSHE',
        'full': '000985.XSHG',
        '000985': '000985.XSHG',
        '000985.XSHG':'000985.XSHG',
        }
    star_info = ['002', '300', '688', '301']