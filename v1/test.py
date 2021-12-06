from module.upbit import *
import datetime
from decimal import Decimal
import re
import time


if __name__ == "__main__":

    upbit = Upbit()
    upbit.set_ticker("KRW-XML")

    # buy
    # response = upbit_obj.buy_coin(100000)
    # print(response)

    order = upbit.get_wait_order()
    print(order)
    time.sleep(600)

    order = upbit.get_wait_order()
    print(order)
    time.sleep(600)

    order = upbit.get_wait_order()
    print(order)
    time.sleep(600)
