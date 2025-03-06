"""
@desc:house_workflow的单接口预处理，主要进行接口的如入参构造，接口的请求和响应值的返回
@author: lijiahui
@version: V1.0
@file: workflow_api_object.py
@time: 2022/2/10
"""
from api_decorator.api_decorator import interface_handle
from common.globalvar import GlobalVar
from common.readconfig import ini
from common.readyaml import ReadYaml
from request_handler.request_handler import RequestHandler


class WorkflowAPIObject(object):

    __house_host = ini.schema + '://' + ini.xf_host
    __house_api = ReadYaml('jrxf/house/workflow')
    return_flag = 'response'

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def get_new_house_list_request(method, url, new_house_name):
        '''获取新房信息'''
        json = {
              "regionOrName": new_house_name,
              "price_S": None,
              "price_E": None,
              "status": None,
              "room": None,
              "houseKeeperType": None,
              "countryAreaId": None,
              "tradeAreaId": None,
              "tag": None,
              "orderBy": [],
              "page": 1,
              "size": 20,
              "isShowOutSide": True
            }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def add_report_request(method, url, add_report_request_params):
        '''新增报备'''
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=add_report_request_params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def get_report_id_request(method, url, estateName):
        '''获取报备id'''
        json = {
            "estateName": estateName,
            "cooperativeCompanyId": "",
            "status": "",
            "createTimeStart": "",
            "createTimeEnd": "",
            "sortItemVOList": [],
            "page": 1,
            "size": 20
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def check_report_request(method, url, report_id):
        '''审核报备'''
        json = {
              "status": 1,
              "id": report_id,
              "checkRemark": ""
            }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def add_takelook_request(method, url, add_takelook_request_params):
        '''新增带看'''
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=add_takelook_request_params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def get_takelook_id_request(method, url, reportNum):
        '''获取带看id'''
        json = {
              "reportNum": reportNum,
              "cooperativeCompanyId": "",
              "status": "",
              "takeLookTimeStart": "",
              "takeLookTimeEnd": "",
              "sortItemVOList": [],
              "page": 1,
              "size": 20
            }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def check_takelook_request(method, url, takelook_id):
        '''审核带看'''
        json = {
              "status": 1,
              "id": takelook_id,
              "checkRemark": ""
            }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def add_subscribe_request(method, url, add_subscribe_request_params):
        '''新增认购'''
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=add_subscribe_request_params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def get_subscribe_id_request(method, url, reportNum):
        '''获取认购id'''
        json = {
              "reportNum": reportNum,
              "cooperativeCompanyId": "",
              "status": "",
              "subscribeTimeStart": "",
              "subscribeTimeEnd": "",
              "sortItemVOList": [],
              "page": 1,
              "size": 20
            }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def check_subscribe_request(method, url, check_subscribe_params):
        '''审核认购'''
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=check_subscribe_params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def add_sign_request(method, url, add_sign_request_params):
        '''新增草网签'''
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=add_sign_request_params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def get_sign_id_request(method, url, reportNum):
        '''获取草网签id'''
        json = {
              "reportNum": reportNum,
              "cooperativeCompanyId": "",
              "status": "",
              "signTimeStart": "",
              "signTimeEnd": "",
              "sortItemVOList": [],
              "page": 1,
              "size": 20
            }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def check_sign_request(method, url, sign_id):
        '''审核草网签'''
        json = {
            "status": 1,
            "id": sign_id,
            "checkRemark": ""
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def add_sell_request(method, url, add_sell_request_params):
        '''新增成销'''
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=add_sell_request_params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def get_sell_id_request(method, url, reportNum):
        '''获取成销id'''
        json = {
            "reportNum": reportNum,
            "cooperativeCompanyId": "",
            "status": "",
            "signTimeStart": "",
            "signTimeEnd": "",
            "sortItemVOList": [],
            "page": 1,
            "size": 20
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def check_sell_request(method, url, sell_id):
        '''审核成销'''
        json = {
            "status": 1,
            "id": sell_id,
            "checkRemark": ""
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

