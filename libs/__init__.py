#

from libs.DB.__database_struct__.main import main as db
from libs.DB import config as __STATMETOD_CONFIG__

class __DUCKDB_STATSMETHOD__(db.__DB_CLASS_DIC__['DuckDB'], getattr(__STATMETOD_CONFIG__, 'DuckDB')):
    pass

class __MYSQL_STATSMETHOD__(db.__DB_CLASS_DIC__['MySQL'], getattr(__STATMETOD_CONFIG__, 'MySQL')):
    pass
