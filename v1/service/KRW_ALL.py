import time
import datetime

from module.upbit import *
from module.slack import *
from module.mysql import *
from module.mongo import *
from module.log import *

from common.function.common_function import *


def monitoring(ticker="KRW-BTC", report_term=3600, sudden_term=5, sudden_per=0.5):
    """

    def description : 모니터링 

    Parameters
    ----------
    ticker : 티커 (string)
    report_term : 리포트 주기 (sec, int)
    sudden_term : 서든 기준 텀 (min, int)
    sudden_per :  서든 기준 퍼센티지 (percent, float)

    Returns
    -------
    current_price : 현재변화율 (float)
    """

    # object init
    upbit = Upbit()
    log = Log()
    slack = Slack()
    mysql = Mysql()
    mongo = Mongo()

    # start 메세지 전송
    msg_s = f"monitoring start!, ticker : {ticker}, started at : {datetime.datetime.now()}"
    slack.post_to_slack(msg_s)

    # log 생성
    log.create_log(f"{os.path.abspath(os.curdir)}/log/{str(generate_now_day())}")
    log.write_log(msg_s)

    # mongo DB 셋팅
    ticker_col = ticker.replace("-", "_")
    if ticker_col not in mongo.get_col_list():
        print("mongo DB Collection, needed")
        return False

    mongo.set_col(ticker.replace("-", "_"))

    # 변수 셋팅
    # 리포팅
    flag_time = time.time()                 # 시간 체커

    # 서든 체커
    SUDDEN_MIN = sudden_term                # 서든 기준 텀 (min)
    SUDDEN_SEC = sudden_term * 60           # 서든 기준 텀 (sec)
    sudden_checker_init_term = 900          # 서든 체커 초기화 텀

    org_in_sudden_check = sudden_per        # 원본 인크리즈 체커 퍼센티지
    org_de_sudden_check = -(sudden_per)     # 원본 디크리즈 체커 퍼센티지
    in_sudden_check = org_in_sudden_check   # 인크리즈 체커
    de_sudden_check = org_de_sudden_check   # 디크리즈 체커

    while True:
        try:

            upbit.set_ticker(ticker)

            # 현재가 산출
            current_price = upbit.get_current_price()
            print(f"{ticker} : {format(current_price, ',')}")
            time.sleep(0.15)

            # sudden in/de crease check by sudden_time
            changes_5min = upbit.get_min_changes(SUDDEN_MIN)
            print(f"{changes_5min}, by api")

            time.sleep(0.15)

            # sudden in/de crease check
            if changes_5min:
                if changes_5min > in_sudden_check:
                    msg = f"ticker : {ticker}, sudden increase, current_price : {current_price}"
                    slack.post_to_slack(msg)
                    log.write_log(msg)
                    in_sudden_check += 0.05

                if changes_5min < de_sudden_check:
                    msg = f"ticker : {ticker}, sudden decrease, current_price : {current_price}"
                    slack.post_to_slack(msg)
                    log.write_log(msg)
                    de_sudden_check -= 0.05

            # 일정 간격으로 서든 값 초기화
            if cal_time_changes(flag_time) > sudden_checker_init_term:
                de_sudden_check = org_de_sudden_check
                in_sudden_check = org_in_sudden_check
                flag_time = time.time()

            # cross_state 변화 체크
            cross_state = upbit.get_cross_state()
            prev_cross_state = mongo.get_doc_one()["cross_state"]

            if prev_cross_state != cross_state:
                msg = f"ticker : {ticker}, cross changed, cross_state : {cross_state}, current_price : {current_price}"
                slack.post_to_slack(msg)
                log.write_log(msg)

            # 신규데이터 삽입
            post = {
                "ticker": ticker,
                "current_price": current_price,
                "cross_state": cross_state,
                "date": datetime.datetime.now()
            }
            mongo.insert_doc(post)
            time.sleep(0.7)

            # report_term 간격으로 보고
            # if cal_time_changes(flag_time) > report_term:
            #     pass

        except Exception as ex:
            log.write_log(str(ex))
            log.write_log("=====================")
            time.sleep(3)


def catch_krw_new_public():
    """
    원화 상장 먹는 로직
    """

    # init
    upbit = Upbit()
    slack = Slack()
    mysql = Mysql()
    log = Log()

    # log 생성
    log.create_log(
        f"{os.path.abspath(os.curdir)}/log/{str(generate_now_day())}")

    # start 메세지 전송
    msg = f"catch_new_krw_public start!, started at : {datetime.datetime.now()}"
    slack.post_to_slack(msg)
    log.write_log(msg)

    # 기능 변수
    time_cut = 360
    buy_time = None
    try_flag = False
    balance_status = "keep"

    # 기존 티커 리스트
    KRW_tickers_old = upbit.get_KRW_tickers()
    old_cnt = len(KRW_tickers_old)

    while True:

        try:
            # 매수 이전
            if balance_status == "keep":

                # 신규 티커 리스트
                KRW_tickers_new = upbit.get_KRW_tickers()
                new_cnt = len(KRW_tickers_new)

                # 신규 티커 확인 후, 신규 티커 존재하면 매수 시도 시간 갱신 후 매수 시도
                diff_ticker = set(KRW_tickers_new) - set(KRW_tickers_old)
                diff_ticker_cnt = len(diff_ticker)
                if diff_ticker_cnt > 0:
                    if new_cnt > old_cnt:

                        # 매수 시도 시간 갱신
                        if try_flag == False:
                            buy_time = time.time()

                        # 매수 시도
                        new_ticker = list(diff_ticker)[0]
                        upbit.set_ticker(new_ticker)
                        response = upbit.buy_coin(500000)
                        if response["status"] == "success":
                            balance_status == "buy"
                            msg = f"new_ticker : {new_ticker}, buying success"
                            slack.post_to_slack(msg)
                            log.write_log(msg)

                        # 매수 실패
                        else:
                            msg = f"new_ticker : {new_ticker}, buying fail"
                            slack.post_to_slack(msg)
                            log.write_log(msg)

                        try_flag = True

            # 매수 이후
            else:
                # 매수 시도 시점을 기점으로 타임 컷 실행
                if cal_time_changes(buy_time) > time_cut:

                    # 매도 시도
                    response = upbit.sell_coin()
                    if response["status"] == "success":
                        msg = f"new_ticker : {new_ticker}, selling success"
                        slack.post_to_slack(msg)
                        log.write_log(msg)
                        return

                    # 매도 실패
                    else:
                        msg = f"new_ticker : {new_ticker}, selling fail"
                        slack.post_to_slack(msg)
                        log.write_log(msg)

            time.sleep(0.05)

        except Exception as ex:
            log.write_log(str(ex))
            log.write_log("=====================")
            time.sleep(3)
