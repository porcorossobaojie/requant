#
from data_source.joinquant.ann_dt_table.main import main as __meta_ann_dt_tables__

from data_source.joinquant.config import ANN_DT_TABLES as __config__
from libs.utils.functions import filter_class_attrs

def daily():
    for i,j in filter_class_attrs(__config__).items():
        instance = __meta_ann_dt_tables__(**j)
        instance.daily()
    