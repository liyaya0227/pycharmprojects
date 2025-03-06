"""
@desc:
@author: lijiahui
@version: V1.0
@file: test_add.py
@time: 2022/1/20
"""
import logging

import pytest
from jsonpath import jsonpath

from case_service.jrxf.auth.auth_service import AuthService
from case_service.jrxf.house.add_house_service import AddHouseService
from case_service.jrxf.system import system_service
from case_service.jrxf.system.system_service import SystemService
from common.assertutils import AssertUtil
from common.readconfig import ini
from config.conf import cm
from tools.jsonutil import get_data
from tools.logger import log

system_services = SystemService()

class TestAddHouse(object):
    api_params = get_data(cm.api_params_json_file('jrxf/house/add_house'))
    add_house_base_params = api_params["base_info"]
    new_house_name = api_params["base_info"]["newHouseName"]
    update_new_house_params = api_params["update_base_info"]
    contract_img_list = api_params["contractImgList"]
    img_url = ''

    def test_add_house(self):
        AuthService().login(ini.xf_user_account, ini.xf_user_password, 6)
        upload_res = system_services.upload_img('营业执照.jpg')  # 上传图片
        self.img_url = jsonpath(upload_res, '$.data.path')[0]
        for img_item in self.contract_img_list:
            img_item["imgUrl"] = self.img_url
        print(self.contract_img_list)

        add_house_service_res = AddHouseService.release_house(self.add_house_base_params,
                                                              self.new_house_name,
                                                              self.contract_img_list,
                                                              self.update_new_house_params)
        # print(jsonpath(add_house_service_res, '$.code')[0])
        # print(jsonpath(add_house_service_res, '$.errorMsg')[0])
        AssertUtil().assert_code(jsonpath(add_house_service_res, '$.code')[0], 0)
        AssertUtil().assert_body(jsonpath(add_house_service_res, '$.errorMsg')[0], None)
        log.info('楼盘上架成功')
