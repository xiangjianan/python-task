import time


def cal_time(func):
    """
    装饰器：计算函数运行时间
    :param func:
    :return:
    """

    def inner(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        use_time = end_time - start_time
        print(f'\033[1;32mRunning time：{use_time}s\033[0m')
        return res

    return inner
