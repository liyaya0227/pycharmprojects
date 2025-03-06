"""
@desc:
@author: lijiahui
@version: V1.0
@file: test_add_workflow.py
@time: 2022/2/10
"""
from jsonpath import jsonpath

from case_service.jrxf.auth.auth_service import AuthService
from case_service.jrxf.house.add_workflow_service import AddWorkflowService
from case_service.jrxf.system.system_service import SystemService
from common.assertutils import AssertUtil
from common.readconfig import ini
from config.conf import cm
from tools.jsonutil import get_data
from tools.logger import log

system_services = SystemService()

class TestAddWorkflow(object):
    api_params = get_data(cm.api_params_json_file('jrxf/house/add_workflow'))
    add_report_request_params = api_params["add_report_params"]
    add_takelook_request_params = api_params["add_takelook_params"]
    add_subscribe_request_params = api_params["add_subscribe_params"]
    check_subscribe_params = api_params["check_subscribe_params"]
    add_sign_request_params = api_params["add_sign_params"]
    add_sell_request_params = api_params["add_sell_params"]

    new_house_name = '露露新房01'
    takelook_img_list = add_takelook_request_params["fileList"]
    subscribe_img_list = add_subscribe_request_params["attachmentList"]
    subscribe_check_img_list = check_subscribe_params["attachmentList"]
    sell_img_list = add_sell_request_params["fileList"]
    img_url = ''

    def test_add_workflow(self):
        AuthService().login(ini.xf_user_account, ini.xf_user_password, 6)
        upload_res = system_services.upload_img('作业.jpg')  # 上传图片
        self.img_url = jsonpath(upload_res, '$.data.path')[0]
        '''更换带看图片'''
        self.takelook_img_list = self.img_url
        print(self.takelook_img_list)

        '''更换认购图片'''
        for img_item in self.subscribe_img_list:
            img_item["path"] = self.img_url

        '''更换认购审核图片'''
        for img_item in self.subscribe_check_img_list:
            img_item["path"] = self.img_url

        '''更换成销图片'''
        self.sell_img_list = self.img_url

        add_house_workflow_res = AddWorkflowService.add_new_house_workflow(self.new_house_name,
                                                                           self.add_report_request_params,
                                                                           self.add_takelook_request_params,
                                                                           self.add_subscribe_request_params,
                                                                           self.check_subscribe_params,
                                                                           self.add_sign_request_params,
                                                                           self.add_sell_request_params)
        # print(jsonpath(add_house_service_res, '$.code')[0])
        # print(jsonpath(add_house_service_res, '$.errorMsg')[0])
        # AssertUtil().assert_code(jsonpath(add_house_workflow_res, '$.code')[0], 0)
        # AssertUtil().assert_body(jsonpath(add_house_workflow_res, '$.errorMsg')[0], None)
        log.info('新房作业流程结束')