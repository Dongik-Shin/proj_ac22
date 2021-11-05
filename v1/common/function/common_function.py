import datetime
import time


def check_required_value(data, required_list):
    """
    =======================================================================
    Def Decription          : 인풋 요청에서 필수데이터 체크
    Comments 

    - 각 define 참조
    =======================================================================
    """
    for required in required_list:
        if required not in data:
            response_object = {
                "status": "fail",
                "message": "request data validation failed, %s is required " % (required),
                "missing_value": required
            }
            return response_object

    response_object = {
        "status": "success",
        "message": "all required values are requested"
    }
    return response_object


def generate_now_date():
    """ 
    def description : 오늘 날짜 연월일 시분초 산출

    Parameters
    ----------
    없음 

    Returns
    -------
    datetime
        오늘 날짜 연월일 시분초
    """
    now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_date


def generate_now_day():
    """ 
    def description : 오늘 날짜 연월일 산출

    Parameters
    ----------
    없음 

    Returns
    -------
    datetime
        오늘 날짜 연월일
    """
    now_day = datetime.datetime.now().strftime("%Y-%m-%d")
    return now_day


def generate_now_time():
    """ 
    def description : 오늘 날짜 시분초 산출

    Parameters
    ----------
    없음 

    Returns
    -------
    datetime
        오늘 날짜 시분초
    """
    now_time = datetime.datetime.now().strftime("%H:%M:%S")
    return now_time


def generate_micro_date():
    """ 
    def description : 오늘 날짜 마이크로 세컨드까지 산출 

    Parameters
    ----------
    없음 

    Returns
    -------
    datetime
        오늘 날짜 마이크로 세컨드
    """
    now_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")

    return now_date


def cal_time_changes(flag_time):
    """ 
    def description : 시간변화 체크

    Parameters
    ----------
    start_time : 시작 시간 

    Returns
    -------
    float : 시작 시간으로부터 현재 시간 차이 (sec)
    """

    now_time = time.time()
    time_diff = (now_time - flag_time)
    return time_diff
