
from module.upbit import *

if __name__ == "__main__":

    # init
    upbit_obj = Upbit()
    upbit_obj.set_ticker("KRW-ETH")

    # buy
    response = upbit_obj.buy_coin(500000)
    print(response)
