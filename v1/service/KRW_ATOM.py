import time
import datetime

from module.upbit import *
from module.slack import *
from module.mysql import *
from module.log import *

from common.function.common_function import *


def monitoring(ticker="KRW-ATOM"):

    # init
    upbit_obj = Upbit()
    slack_obj = Slack()
    mysql_obj = Mysql()
    log_obj = Log()

    flag_time = time.time()  # 시간 체커
    report_term = 300        # 리포트 텀(sec)

    # log 생성
    log_obj.create_log(
        f"{os.path.abspath(os.curdir)}/log/{str(generate_now_day())}"
    )

    # start 메세지 전송
    msg = f"""
        monitoring start!
        ticker : {ticker}
        started at : {datetime.datetime.now()}
    """
    slack_obj.post_to_slack(msg)
    log_obj.write_log(msg)

    while True:
        try:
            upbit_obj.set_ticker(ticker)

            # 현재가 산출
            current_price = upbit_obj.get_current_price()
            print(f"{ticker} : {current_price}")
            time.sleep(0.2)

            # 특정 기간동안 변화율 산출
            changes_1min = upbit_obj.get_min_changes(1)
            changes_3min = upbit_obj.get_min_changes(3)
            time.sleep(0.2)
            changes_5min = upbit_obj.get_min_changes(5)
            changes_10min = upbit_obj.get_min_changes(10)
            time.sleep(0.2)
            changes_15min = upbit_obj.get_min_changes(15)
            changes_30min = upbit_obj.get_min_changes(30)
            time.sleep(0.2)

            changes_1hour = upbit_obj.get_hour_changes(1)
            changes_2hour = upbit_obj.get_hour_changes(2)
            changes_3hour = upbit_obj.get_hour_changes(3)

            # sudden in/de crease check
            if changes_1min and changes_3min and changes_5min:

                if changes_1min > 0.5 or changes_3min > 1 or changes_5min > 1.5:

                    msg = f"""
                        ticker : {ticker}
                        sudden increase   
                        changes_1min : {changes_1min}
                        changes_3min : {changes_3min}
                        changes_5min : {changes_5min}
                    """
                    slack_obj.post_to_slack(msg)
                    log_obj.write_log(msg)

                if changes_1min < -0.5 or changes_3min < -1 or changes_5min < -1.5:
                    msg = f"""
                        ticker : {ticker}
                        sudden decrease                       
                        changes_1min : {changes_1min}
                        changes_3min : {changes_3min}
                        changes_5min : {changes_5min}
                    """
                    slack_obj.post_to_slack(msg)
                    log_obj.write_log(msg)

            # report_term 간격으로 보고
            if cal_time_changes(flag_time) > report_term:

                msg = f"""
                    ticker : {ticker}
                    current_price : {current_price}
                    min 1: {changes_1min} %
                    min 5: {changes_3min} %
                    min 5: {changes_5min} %
                    min 10 : {changes_10min} %
                    min 30 : {changes_15min} %
                    min 30 : {changes_30min} %
                    hour 1 : {changes_1hour} %
                    hour 2 : {changes_2hour} %
                    hour 3 : {changes_3hour} %        
                """
                slack_obj.post_to_slack(msg)
                log_obj.write_log(msg)

                flag_time = time.time()

            time.sleep(0.5)

        except Exception as ex:
            log_obj.write_log(str(ex))
            log_obj.write_log("=====================")
            time.sleep(3)
