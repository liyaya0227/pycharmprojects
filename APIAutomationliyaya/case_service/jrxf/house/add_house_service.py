"""
@desc:将多接口的场景封装：楼盘上架
@author: lijiahui
@version: V1.0
@file: add_house_service.py
@time: 2022/1/20
"""
from jsonpath import jsonpath

from api_object.jrxf.house.house_api_object import HouseAPIObject
from config.conf import cm
from tools.jsonutil import get_data

house_api = HouseAPIObject()


class AddHouseService(object):
    @staticmethod
    def release_house(add_new_house_params, new_house_name, contract_img_list, edit_new_house_params):
        '''上架楼盘'''
        house_api.houseManage_add_base_request(add_new_house_params)
        house_manage_list_res = house_api.houseManage_list_request(new_house_name)
        new_house_id = jsonpath(house_manage_list_res, '$.records[0].newHouseId')[0]
        house_api.contract_upload_request(contract_img_list, new_house_id)
        house_api.contract_audit_request(new_house_id)
        # CaseUser_query_res = house_api.CaseUser_query_request(userName)
        edit_new_house_params["newHouseId"] = new_house_id
        house_api.unRelease_edit_base_request(edit_new_house_params)
        house_api.released_audit_request(new_house_id)
        new_es_lis_res = house_api.new_es_lis_request(new_house_name)

        return new_es_lis_res



