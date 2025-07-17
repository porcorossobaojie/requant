#


from data_source.joinquant import daily as __jq_daily__

def daily():
    from local.login_info import JQ_LOGIN_INFO
    import jqdatasdk as jq
    jq.auth (**JQ_LOGIN_INFO)
    __jq_daily__()

