from service.KRW_ALL import *


if __name__ == "__main__":

    # 720분 마다 리포트 쓴다
    # 5분 동안 1퍼센트가 변하면 알러트
    # 30분 뒤에 상황 초기화
    monitoring(
        ticker="KRW-BTC",
        report_term=720,
        sudden_term=5,
        sudden_per=1,
        sudden_init_term=30
    )
