
from module.upbit import *

if __name__ == "__main__":

    # init
    upbit_obj = Upbit()

    upbit_obj.set_ticker("")
    upbit_obj.buy_coin(500000)
