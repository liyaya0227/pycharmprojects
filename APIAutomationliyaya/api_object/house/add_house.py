"""
@desc:house单接口预处理，主要进行单接口的入参构造
@author: lijiahui
@version: V1.0
@file: add_house.py
@time: 2022/1/14
"""
from api_decorator.api_decorator import interface_handle
from api_params_build.api_params_build import ApiParamsBuild
from common.globalvar import GlobalVar
from common.readconfig import ini
from common.readyaml import ReadYaml
from config.conf import cm
from request_handler.request_handler import RequestHandler

api_params_build = ApiParamsBuild()


class AddHouseAPI(object):
    __house_host = ini.schema + '://' + ini.host
    __house_api = ReadYaml('house/sale_house/add_house')


    @staticmethod
    @interface_handle(__house_host, __house_api)
    def add_preowned_house_request(method, url, change_params):
        """新增买卖房源api"""
        params_json_file = cm.API_PARAMS_PATH + '/house/add_sale_house.json'
        params = api_params_build.request_params_build(params_json_file, change_params)
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=params)

    @staticmethod
    @interface_handle(__house_host, __house_api)
    def add_rent_house_request(method, url, change_params):
        """新增租赁房源api"""
        params_json_file = cm.API_PARAMS_PATH + '/house/add_rent_house.json'
        params = api_params_build.request_params_build(params_json_file, change_params)
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=params)

    # @staticmethod
    # @set_header(host, house_api)
    # def add_preowned_house_request(method, url, add_sale_house_params, community_id, building_id):
    #     """增加买卖房源"""
    #     input_params = ApiParamsBuild().add_sale_house_params_build(add_sale_house_params, community_id, building_id)
    #     return RequestHandler().requests_api(method, url, GlobalVar.header, json=input_params)

# class ApiParamsBuild():
#
#     @staticmethod
#     def add_sale_house_params_build(add_sale_house_params, community_id, building_id):
#         """
#         增加买卖房源接口的参数
#         :param building_id: 楼层id
#         :param community_id: 楼盘id
#         :param add_sale_house_params:存放接口参数
#         :return:add_sale_house_params
#         """
#         add_sale_house_params['locationInfo']['communityId'] = community_id
#         add_sale_house_params['locationInfo']['buildingId'] = building_id
#         add_sale_house_params['locationInfo']['locationId'] = GlobalVar.house_location_id
#         add_sale_house_params['locationInfo']['buildingCell'] = ini.house_building_cell
#         add_sale_house_params['locationInfo']['doorplate'] = ini.house_doorplate

