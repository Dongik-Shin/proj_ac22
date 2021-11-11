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
            current_price = format(current_price, ",")
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
                    in_sudden_check += 0.05

                if changes_1min < de_sudden_check:
                    msg = f"""
                        ticker : {ticker}
                        sudden decrease     
                        current_price : {current_price}                  
                        changes_1min : {changes_1min}
                    """
                    slack_obj.post_to_slack(msg)
                    log_obj.write_log(msg)
                    de_sudden_check -= 0.05

            # report_term 간격으로 보고
            if cal_time_changes(flag_time) > report_term:

                hour_before_price_1 = upbit_obj.get_target_hour_avg_price(1)
                if hour_before_price_1:
                    hour_before_price_1 = format(hour_before_price_1, ",")
                time.sleep(0.15)

                hour_before_price_2 = upbit_obj.get_target_hour_avg_price(2)
                if hour_before_price_2:
                    hour_before_price_2 = format(hour_before_price_2, ",")
                time.sleep(0.15)

                hour_before_price_3 = upbit_obj.get_target_hour_avg_price(3)
                if hour_before_price_3:
                    hour_before_price_3 = format(hour_before_price_3, ",")
                time.sleep(0.15)

                hour_before_price_6 = upbit_obj.get_target_hour_avg_price(6)
                if hour_before_price_6:
                    hour_before_price_6 = format(hour_before_price_6, ",")
                time.sleep(0.15)

                hour_before_price_12 = upbit_obj.get_target_hour_avg_price(12)
                if hour_before_price_12:
                    hour_before_price_12 = format(hour_before_price_12, ",")
                time.sleep(0.15)

                day_before_price_1 = upbit_obj.get_target_hour_avg_price(24)
                if day_before_price_1:
                    day_before_price_1 = format(day_before_price_1, ",")
                time.sleep(0.15)

                day_before_price_2 = upbit_obj.get_target_hour_avg_price(48)
                if day_before_price_2:
                    day_before_price_2 = format(day_before_price_2, ",")
                time.sleep(0.15)

                day_before_price_3 = upbit_obj.get_target_hour_avg_price(72)
                if day_before_price_3:
                    day_before_price_3 = format(day_before_price_3, ",")
                time.sleep(0.15)

                msg = f"""
                    ticker : {ticker}
                    current_price : {current_price}
                    --------------------------
                    1 hour before : {hour_before_price_1} 
                    2 hour before : {hour_before_price_2} 
                    3 hour before : {hour_before_price_3} 
                    6 hour before : {hour_before_price_6} 
                    12 hour before : {hour_before_price_12} 
                    1 day before : {day_before_price_1} 
                    2 day before : {day_before_price_2} 
                    3 day before : {day_before_price_3} 
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
