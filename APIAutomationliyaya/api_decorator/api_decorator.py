"""
@author: lijiahui
@version: V1.0
@file: api_decorator.py
@time: 2022/1/12
"""
import functools
#jsonpath是强大的json解析器，可以解析复杂的json数据
from jsonpath import jsonpath


def interface_handle(host, api, return_flag='data', check_code=True):
    """
    :params return_flag data：只返回data数据；response：返回接口所有数据
    :params check_code True：检查接口返回code值 False：不检查接口返回code值，直接返回接口所有数据
    """
    def decorator(func):
        # @functools.wraps(func)的作用就是保留原有函数的名称和docstring
        @functools.wraps(func)
        def wrapper(*arg, **kwargs):
            # func.__name__:用来获取值
            method = api[func.__name__]['method']
            url = host+api[func.__name__]['url']
            return_value = func(method, url, *arg, **kwargs)
            if not check_code:
                return return_value
            if jsonpath(return_value, '$.code')[0] == 0:
                if return_flag == 'data':
                    return jsonpath(return_value, '$.data')[0]
                elif return_flag == 'response':
                    return return_value
                else:
                    raise ValueError('传值错误')
            else:
                raise ValueError('interface retuen error' + jsonpath(return_value, '$.errorMsg')[0])
        return wrapper
    return decorator


def set_header(host, api):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*arg, **kwargs):
            method = api[func.__name__]['method']
            url = host + api[func.__name__]['url']
            return_value = func(method, url, *arg, **kwargs)
            return return_value
        return wrapper
    return decorator
