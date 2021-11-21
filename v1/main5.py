
from module.upbit import *

if __name__ == "__main__":

    # init
    upbit_obj = Upbit()

    upbit_obj.set_ticker("KRW-ARK")
    print(type(upbit_obj.get_krw_balance()))


    response = (upbit_obj.buy_coin(490000))
    print(response)
