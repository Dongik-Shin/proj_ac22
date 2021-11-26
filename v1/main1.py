from service.KRW_ALL import *


if __name__ == "__main__":

    # 21600마다 리포트 쓴다
    # 5분 동안 1퍼센트가 변하면 알러트쏘고
    # 15분 뒤에 상황정리
    monitoring(
        ticker="KRW-BTC",
        report_term=720,
        sudden_term=5,
        sudden_per=1,
        sudden_init_term=15
    )
