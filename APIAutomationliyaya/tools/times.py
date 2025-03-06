#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: timeutil.py
@time: 2021/06/22
"""

import time
import datetime
from functools import wraps


def timestamp():
    """时间戳"""
    return time.time()


def dt_strftime(fmt="%Y%m"):
    """
    datetime格式化时间
    :param fmt "%Y%m%d %H%M%S
    """
    return datetime.datetime.now().strftime(fmt)


def dt_strftime_with_delta(day, fmt="%Y%m"):
    """
    datetime格式化时间
    :param day
    :param fmt "%Y%m%d %H%M%S
    """
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=day)
    n_days = now + delta
    return n_days.strftime(fmt)


def sleep(seconds=1.0):
    """
    睡眠时间
    """
    time.sleep(seconds)


def running_time(func):
    """函数运行时间"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        res = func(*args, **kwargs)
        print("校验元素done！用时%.3f秒！" % (timestamp() - start))
        return res

    return wrapper


if __name__ == '__main__':
    # print(dt_strftime("%Y%m%d%H%M%S"))
    print(dt_strftime_with_delta(1, '%Y-%m-%d %H:%M:%S'))