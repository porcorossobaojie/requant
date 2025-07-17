#

from libs.DB import __DB_CLASS__
from local.login_info import DB_LOGIN_INFO, SOURCE
from libs.utils.functions import filter_class_attrs as __filter_class_attrs__

db = __DB_CLASS__(source=SOURCE)
[getattr(db, i)(**__filter_class_attrs__(j)) for i,j in __filter_class_attrs__(DB_LOGIN_INFO).items()]
