"""
@desc:house的单接口预处理，主要进行接口的如入参构造，接口的请求和响应值的返回
@author: lijiahui
@version: V1.0
@file: house_api_object.py
@time: 2022/1/20
"""
from api_decorator.api_decorator import interface_handle
from common.globalvar import GlobalVar
from common.readconfig import ini
from common.readyaml import ReadYaml
from request_handler.request_handler import RequestHandler


class HouseAPIObject(object):

    __house_host = ini.schema + '://' + ini.xf_host
    __house_api = ReadYaml('jrxf/house/add')
    return_flag = 'response'

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def houseManage_add_base_request(method, url, add_new_house_params):
        '''添加基础信息api'''
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=add_new_house_params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def houseManage_list_request(method, url, new_house_name):
        '''获取房源id api'''
        json = {
            "regionOrName": new_house_name,
            "countryAreaId": None,
            "tradeAreaId": None,
            "houseKeeperType": None,
            "status": None,
            "orderBy": [],
            "page": 1,
            "size": 20
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def contract_upload_request(method, url, contract_img_list, new_house_id):
        '''添加合同api'''
        json = {
            "contractImgList": contract_img_list,
            "hid": new_house_id,
            "contractType": 1
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def contract_audit_request(method, url, new_house_id):
        '''合同审批api'''
        json = {
            "hid": new_house_id,
            "status": 2,
            "contractType": 1
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def CaseUser_query_request(method, url, username):
        '''添加角色查询api'''
        json = {
            "userName": username,
            "caseUserType": "A232",
            "page": 1,
            "size": 20
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def unRelease_edit_base_request(method, url, edit_new_house_params):
        '''待上架房源编辑信息api'''
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=edit_new_house_params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def released_audit_request(method, url, new_house_id):
        '''待上架房源审批api'''
        json = {
            "houseId": new_house_id,
            "status": 2
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)

    @staticmethod
    @interface_handle(__house_host, __house_api, return_flag='response')
    def new_es_lis_request(method, url, new_house_name):
        '''合作楼盘查询api'''
        json = {
            "attentionType": None,
            "regionOrName": new_house_name,
            "salePriceRangeList": [],
            "status": [],
            "roomList": [],
            "cityAreaId": None,
            "countryAreaId": None,
            "houseKeeperType": [],
            "tradeAreaId": None,
            "tag": [],
            "orderBy": [],
            "page": 1,
            "size": 20,
            "isShowOutSide": True
        }
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=json)


