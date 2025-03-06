"""
@desc:auth的单接口预处理，主要进行接口的如入参构造，接口的请求和响应值的返回
@author: lijiahui
@version: V1.0
@file: auth_api_object.py
@time: 2022/1/20
"""
from api_decorator.api_decorator import interface_handle
from common.globalvar import GlobalVar
from common.readconfig import ini
from common.readyaml import ReadYaml
from request_handler.request_handler import RequestHandler


class AuthAPIObject(object):
    __auth_host = ini.schema + '://' + ini.public_host
    __auth_api = ReadYaml('jrxf/auth/auth_api')
    __auth_pre_host = ini.schema + '://' + ini.xf_host

    @staticmethod
    @interface_handle(__auth_host, __auth_api)
    def account_password_request(method, url, account, password, scope):
        '''账号密码验证api'''
        json = {
            "account": account,
            "password": password,
            "s": 1642661492971,
            "scope": scope
        }
        # 参数：请求方式、url、请求头、请求主体
        # 返回值类型是json
        return RequestHandler().requests_api(method, url, GlobalVar.clean_header, json=json)

    @staticmethod
    @interface_handle(__auth_pre_host, __auth_api)
    def precode_request(method, url, pre_code, platform, region, role):
        """获取token api"""
        json = {
            "preCode": pre_code,
            "platform": platform,
            "region": region,
            "role": role
        }
        return RequestHandler().requests_api(method, url, GlobalVar.clean_header, json=json)

    @staticmethod
    @interface_handle(__auth_host, __auth_api)
    def log_out_request(method, url, scope):
        """退出登录api"""
        params = {
            'scope': scope
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, params=params)
