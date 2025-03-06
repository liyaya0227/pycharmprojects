"""
@author: lijiahui
@version: V1.0
@file: auth_service.py
@time: 2022/1/12
"""
from jsonpath import jsonpath

from api_object.auth.auth_api_object import AuthApiObject
from common.globalvar import GlobalVar


class AuthService(object):

    '''登录，并更新token值'''
    @staticmethod
    def login(account, password, scope):
        account_password_res = AuthApiObject.account_password_request(account, password, scope)
        pre_code = jsonpath(account_password_res, '$.code')[0]
        platform = jsonpath(account_password_res, '$.apps[0].platform')[0]
        region = jsonpath(account_password_res, '$.regions[0].abbreviated')[0]
        precode_res = AuthApiObject.precode_request(pre_code, platform, region)
        #更新token值
        GlobalVar.header['Authorization'] = 'Bearer ' + jsonpath(precode_res, '$.token')[0]

    @staticmethod
    def log_out(scope=1):  # 退出登录
        log_out_res = AuthApiObject.log_out_request(scope)

