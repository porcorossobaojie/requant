#
from libs.__flow__ import (
    stock,
    index,
    help,
    data_init as __data_init__,
    stock_finance,
    letter_finance,
    is_st,
    be_list,
    trade_days,
    code_standard,)

from libs.__flow__.config import *

from libs import __pandas__
__pandas__.factorize()

def data_init(how='full'):
    __data_init__(how)
    if how == 'full':
        __pandas__.capitalize()



