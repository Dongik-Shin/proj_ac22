
from module.upbit import *

if __name__ == "__main__":

    # init
    upbit_obj = Upbit()

    upbit_obj.set_ticker("KRW-ARK")
    upbit_obj.sell_coin()
