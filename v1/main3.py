from service.KRW_ALL import *


if __name__ == "__main__":

    monitoring(
        ticker="KRW-ARK",
        report_term=21600,
        sudden_term=5,
        sudden_per=1
    )
