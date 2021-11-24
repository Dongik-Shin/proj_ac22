
from module.upbit import *

if __name__ == "__main__":

    # init
    upbit_obj = Upbit()
    upbit_obj.set_ticker("KRW-ARK")
    response = (upbit_obj.buy_coin(490000))
    print(response)
