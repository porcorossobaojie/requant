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
