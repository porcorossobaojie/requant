# config file

from data_source.joinquant.config import DATABASE as __DATABASE__

class DATABASE(__DATABASE__):
    drop_columns = ['UNIQUE_KEY', 'ID_KEY']
    
class FILTER:
    ann_dt_start = '2011-12-31 15:00'
    trade_start = '2014-01-01 15:00'
    
class DB_INFO:
    schema_info = 'TABLE_SCHEMA'
    table_info = 'TABLE_NAME'
    columns_info = 'COLUMN_NAME'
    comment_info = 'COLUMN_COMMENT'
