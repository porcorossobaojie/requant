#


from data_source.joinquant import daily as __jq_daily__
import jqdatasdk as jq
def daily():
    from local.login_info import JQ_LOGIN_INFO
    jq.auth (**JQ_LOGIN_INFO)
    __jq_daily__()

