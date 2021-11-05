import time
import datetime

from module.upbit import *
from module.slack import *
from module.mysql import *
from module.log import *

from common.function.common_function import *


def monitoring(ticker=None):

    # init
    upbit_obj = Upbit()
    slack_obj = Slack()
    mysql_obj = Mysql()
    log_obj = Log()

    # log 생성
    log_obj.create_log(
        f"{os.path.abspath(os.curdir)}/log/{str(generate_now_day())}"
    )

    # start 전송
    msg = f"""
        monitoring start!
        ticker : {ticker}
        started at : {datetime.datetime.now()}
    """
    slack_obj.post_to_slack(msg)
    log_obj.write_log(msg)

    while True:
        current_price = upbit_obj.get_current_price(ticker)
        time.sleep(0.2)

        changes_1min = upbit_obj.get_min_changes(ticker, 1)
        changes_3min = upbit_obj.get_min_changes(ticker, 3)
        changes_5min = upbit_obj.get_min_changes(ticker, 5)
        time.sleep(0.2)

        changes_10min = upbit_obj.get_min_changes(ticker, 10)
        changes_15min = upbit_obj.get_min_changes(ticker, 15)
        changes_30min = upbit_obj.get_min_changes(ticker, 30)
        time.sleep(0.2)

        changes_1hour = upbit_obj.get_hour_changes(ticker, 1)
        changes_2hour = upbit_obj.get_hour_changes(ticker, 2)
        changes_3hour = upbit_obj.get_hour_changes(ticker, 3)
        time.sleep(0.2)

    return
