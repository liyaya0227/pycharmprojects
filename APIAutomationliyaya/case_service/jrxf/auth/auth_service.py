"""
@desc:将多接口场景步骤进行封装：登录
@author: lijiahui
@version: V1.0
@file: auth_service.py
@time: 2022/1/20
"""
from jsonpath import jsonpath

from api_object.jrxf.auth.auth_api_object import AuthAPIObject
from common.globalvar import GlobalVar

auth_api_object = AuthAPIObject()

class AuthService(object):
    @staticmethod
    def login(account, password, scope):
        '''登录，并更新token值'''
        account_password_res = auth_api_object.account_password_request(account, password, scope)
        pre_code = jsonpath(account_password_res, '$.code')[0]
        platform = jsonpath(account_password_res, '$.apps[0].platform')[0]
        region = jsonpath(account_password_res, '$.regions[0].abbreviated')[0]
        role = jsonpath(account_password_res, '$.role')[0]
        precode_res = auth_api_object.precode_request(pre_code, platform, region, role)
        # 更新token值
        GlobalVar.header['Authorization'] = 'Bearer ' + jsonpath(precode_res, '$.token')[0]

    @staticmethod
    def log_out(scope=6):
        '''退出登录'''
        log_out_res = auth_api_object.log_out_request(scope)
