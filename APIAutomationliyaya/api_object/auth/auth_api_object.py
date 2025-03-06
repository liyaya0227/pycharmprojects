"""
@author: lijiahui
@version: V1.0
@file: auth_api_object.py
@time: 2022/1/12
"""
from api_decorator.api_decorator import interface_handle
from common.globalvar import GlobalVar
from common.readconfig import ini
from common.readyaml import ReadYaml
from request_handler.request_handler import RequestHandler


class AuthApiObject(object):

    __auth_host = ini.schema + '://' + ini.public_host
    __auth_api = ReadYaml('auth/auth_api')

    # 类里面不想某个方法使用类属性和调用其它方法就可以使用静态方法，只用来处理参数
    # 不需要实例化类调用该方法
    @staticmethod
    @interface_handle(__auth_host, __auth_api)
    def account_password_request(method, url, account, password, scope):
        '''账号密码验证api'''
        json = {
            'account': account,
            'password': password,
            'scope': scope,
            "s": 1642065569987
        }
        # 参数：请求方式、url、请求头、请求主体
        # 返回值类型是json
        return RequestHandler().requests_api(method, url, GlobalVar.clean_header, json=json)

    @staticmethod
    @interface_handle(__auth_host, __auth_api)
    def precode_request(method, url, pre_code, platform, region, role=None):
        """获取token api"""
        json = {
            'preCode': pre_code,
            'platform': platform,
            'region': region,
            'role': role
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__auth_host, __auth_api)
    def log_out_request(method, url, scope):
        """退出登录api"""
        params = {
            'scope': scope
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, params=params)