import time
import datetime

from module.upbit import *
from module.slack import *
from module.mysql import *
from module.log import *

from common.function.common_function import *


def monitoring(ticker="KRW-ETH"):

    # init
    upbit_obj = Upbit()
    slack_obj = Slack()
    mysql_obj = Mysql()
    log_obj = Log()

    flag_time = time.time()  # 시간 체커
    report_term = 900        # 리포트 텀(sec)
    org_de_sudden_check = -0.4
    org_in_sudden_check = abs(org_de_sudden_check)
    de_sudden_check = org_de_sudden_check
    in_sudden_check = org_in_sudden_check

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
            time.sleep(0.15)

            # 특정 기간동안 변화율 산출
            changes_1min = upbit_obj.get_min_changes(1)
            time.sleep(0.15)

            # sudden in/de crease check
            if changes_1min:

                if changes_1min > in_sudden_check:

                    msg = f"""
                        ticker : {ticker}
                        sudden increase   
                        current_price : {current_price}
                        changes_1min : {changes_1min}
                    """
                    slack_obj.post_to_slack(msg)
                    log_obj.write_log(msg)
                    in_sudden_check += 0.1

                if changes_1min < de_sudden_check:
                    msg = f"""
                        ticker : {ticker}
                        sudden decrease     
                        current_price : {current_price}                  
                        changes_1min : {changes_1min}
                    """
                    slack_obj.post_to_slack(msg)
                    log_obj.write_log(msg)
                    de_sudden_check -= 0.1

            # report_term 간격으로 보고
            if cal_time_changes(flag_time) > report_term:

                changes_15min = upbit_obj.get_min_changes(15)
                time.sleep(0.15)
                changes_30min = upbit_obj.get_min_changes(30)
                time.sleep(0.15)
                changes_1hour = upbit_obj.get_hour_changes(1)
                time.sleep(0.15)
                changes_3hour = upbit_obj.get_hour_changes(3)
                time.sleep(0.15)
                changes_6hour = upbit_obj.get_hour_changes(6)
                time.sleep(0.15)
                changes_12hour = upbit_obj.get_hour_changes(12)
                time.sleep(0.15)
                changes_24hour = upbit_obj.get_hour_changes(24)

                msg = f"""
                    ticker : {ticker}
                    current_price : {current_price}
                    --------------------------
                    min 15: {changes_15min} %
                    min 30 : {changes_30min} %
                    --------------------------
                    hour 1 : {changes_1hour} %
                    hour 3 : {changes_3hour} % 
                    --------------------------
                    hour 6 : {changes_6hour} %  
                    hour 12 : {changes_12hour} %    
                    --------------------------
                    hour 24 : {changes_24hour} %        
                """
                slack_obj.post_to_slack(msg)
                log_obj.write_log(msg)

                flag_time = time.time()
                de_sudden_check = org_de_sudden_check
                in_sudden_check = org_in_sudden_check

            time.sleep(0.5)

        except Exception as ex:
            log_obj.write_log(str(ex))
            log_obj.write_log("=====================")
            time.sleep(3)
