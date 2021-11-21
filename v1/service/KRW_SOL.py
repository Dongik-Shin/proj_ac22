import time
import datetime

from module.upbit import *
from module.slack import *
from module.mysql import *
from module.log import *

from common.function.common_function import *


def monitoring(ticker="KRW-SOL"):

    # init
    upbit_obj = Upbit()
    slack_obj = Slack()
    mysql_obj = Mysql()
    log_obj = Log()

    flag_time = time.time()  # 시간 체커
    report_term = 1800        # 리포트 텀(sec)
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
            print(f"{ticker} : {format(current_price, ',')}")
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
                
                hour_1_before_price = upbit_obj.get_target_hour_avg_price(1)
                if hour_1_before_price:
                    hour_1_change_rate = cal_price_changes(hour_1_before_price, current_price)
                    hour_1_before_price = format(hour_1_before_price, ",")
                time.sleep(0.15)

                hour_2_before_price = upbit_obj.get_target_hour_avg_price(2)
                if hour_2_before_price:
                    hour_2_change_rate = cal_price_changes(hour_2_before_price, current_price)
                    hour_2_before_price = format(hour_2_before_price, ",")
                time.sleep(0.15)

                hour_3_before_price = upbit_obj.get_target_hour_avg_price(3)
                if hour_3_before_price:
                    hour_3_change_rate = cal_price_changes(hour_3_before_price, current_price)
                    hour_3_before_price = format(hour_3_before_price, ",")
                time.sleep(0.15)

                hour_6_before_price = upbit_obj.get_target_hour_avg_price(6)
                if hour_6_before_price:
                    hour_6_change_rate = cal_price_changes(hour_6_before_price, current_price)
                    hour_6_before_price = format(hour_6_before_price, ",")
                time.sleep(0.15)

                hour_12_before_price = upbit_obj.get_target_hour_avg_price(12)
                if hour_12_before_price:
                    hour_12_change_rate = cal_price_changes(hour_12_before_price, current_price)
                    hour_12_before_price = format(hour_12_before_price, ",")
                time.sleep(0.15)

                day_1_before_price = upbit_obj.get_target_day_avg_price(1)
                if day_1_before_price:
                    day_1_before_rate = cal_price_changes(day_1_before_price, current_price)
                    day_1_before_price = format(day_1_before_price, ",")
                time.sleep(0.15)

                day_2_before_price = upbit_obj.get_target_day_avg_price(2)
                if day_2_before_price:
                    day_2_before_rate = cal_price_changes(day_2_before_price, current_price)
                    day_2_before_price = format(day_2_before_price, ",")
                time.sleep(0.15)

                day_3_before_price = upbit_obj.get_target_day_avg_price(3)
                if day_3_before_price:
                    day_3_before_rate = cal_price_changes(day_3_before_price, current_price)
                    day_3_before_price = format(day_3_before_price, ",")
                time.sleep(0.15)
                
                msg = f"""
ticker : {ticker}
current_price : {current_price}
--------------------------
1 hour before : {hour_1_before_price},   {hour_1_change_rate} % 
2 hour before : {hour_2_before_price},   {hour_2_change_rate} %
3 hour before : {hour_3_before_price},   {hour_3_change_rate} % 
6 hour before : {hour_6_before_price},   {hour_6_change_rate} % 
h day before : {hour_12_before_price},  {hour_12_change_rate} % 
1 day before : {day_1_before_price},   {day_1_before_rate} %
2 day before : {day_2_before_price},   {day_2_before_rate} % 
3 day before : {day_3_before_price},   {day_3_before_rate} %
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
