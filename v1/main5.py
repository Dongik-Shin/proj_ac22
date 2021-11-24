
from module.upbit import *

if __name__ == "__main__":

    # init
    upbit_obj = Upbit()
    upbit_obj.set_ticker("KRW-ETH")
    response = upbit_obj.buy_coin(10000)
    print(response)

    response = upbit_obj.sell_coin()
    print(response)
