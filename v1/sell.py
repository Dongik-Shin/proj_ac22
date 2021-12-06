
from module.upbit import *

if __name__ == "__main__":

    # init
    upbit_obj = Upbit()
    upbit_obj.set_ticker("KRW-ETH")

    # sell
    response = upbit_obj.sell_coin()
    print(response)
