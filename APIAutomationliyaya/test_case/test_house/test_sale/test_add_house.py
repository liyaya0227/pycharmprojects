"""
@author: lijiahui
@version: V1.0
@file: test_add_house.py
@time: 2022/1/16
"""
from jsonpath import jsonpath

from api_object.house.add_house import AddHouseAPI
from common.assertutils import AssertUtil
from common.globalvar import GlobalVar
from common.readconfig import ini
from config.conf import cm
from tools.jsonutil import get_data

add_house_api = AddHouseAPI()


class TestAddSaleHouse:
    test_data = get_data(cm.testdata_json_file('house/sale_house/test_add_sale_house'))
    add_sale_house_params = test_data["tc01_add_sale_house"][0]

    def test_add_sale_house(self):
        add_sale_house_res = add_house_api.add_preowned_house_request(self.add_sale_house_params,
                                                                  GlobalVar.house_estate_id,
                                                                  GlobalVar.house_building_number_id)
        AssertUtil().assert_code(jsonpath(add_sale_house_res, '$.code')[0], 0)
        AssertUtil().assert_body(jsonpath(add_sale_house_res, '$.errorMsg')[0], 'ok')
        # search_house_change_params = {
        #     'estateName': ini.house_estate_name
        # }
        # search_house_res = add_house_api.search_house_request(self.search_house_params, search_house_change_params)
        # house_list = jsonpath(search_house_res, '$.data.data')[0]
        # if len(house_list) > 0:
        #     for house in house_list:
        #         if house['locationDoorplate'] == ini.house_doorplate:
        #             assert True