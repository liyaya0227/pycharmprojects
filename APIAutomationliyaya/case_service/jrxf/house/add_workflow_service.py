"""
@desc:将多接口的场景封装：新房作业流程
@author: lijiahui
@version: V1.0
@file: add_workflow_service.py
@time: 2022/2/10
"""
from jsonpath import jsonpath

from api_object.jrxf.house.workflow_api_object import WorkflowAPIObject

workflow_api = WorkflowAPIObject()


class AddWorkflowService(object):
    @staticmethod
    def add_new_house_workflow(new_house_name,
                               add_report_request_params,
                               add_takelook_request_params,
                               add_subscribe_request_params,
                               check_subscribe_params,
                               add_sign_request_params,
                               add_sell_request_params):
        '''创建新房作业流程'''
        new_house_list_res = workflow_api.get_new_house_list_request(new_house_name)
        new_house_id = jsonpath(new_house_list_res, '$.data[0].newHouseId')[0]
        add_report_request_params['newHouseIdList'] = [new_house_id]
        workflow_api.add_report_request(add_report_request_params)
        get_report_id_res = workflow_api.get_report_id_request(new_house_name)
        report_id = jsonpath(get_report_id_res, '$.data[0].id')[0]
        report_num = jsonpath(get_report_id_res, '$.data[0].reportNum')[0]
        workflow_api.check_report_request(report_id)
        add_takelook_request_params['newHouseId'] = new_house_id
        add_takelook_request_params['reportId'] = report_id
        workflow_api.add_takelook_request(add_takelook_request_params)
        get_takelook_id_res = workflow_api.get_takelook_id_request(report_num)
        takelook_id = jsonpath(get_takelook_id_res, '$.data[0].id')[0]
        workflow_api.check_takelook_request(takelook_id)
        add_subscribe_request_params['takeLookId'] = takelook_id
        add_subscribe_request_params['reportId'] = report_id
        workflow_api.add_subscribe_request(add_subscribe_request_params)
        get_subscribe_id_res = workflow_api.get_subscribe_id_request(report_num)
        subscribe_id = jsonpath(get_subscribe_id_res, '$.data[0].id')[0]
        check_subscribe_params['id'] = subscribe_id
        workflow_api.check_subscribe_request(check_subscribe_params)
        add_sign_request_params['newHouseId'] = new_house_id
        add_sign_request_params['reportId'] = report_id
        add_sign_request_params['subscribeId'] = subscribe_id
        workflow_api.add_sign_request(add_sign_request_params)
        get_sign_id_res = workflow_api.get_sign_id_request(report_num)
        sign_id = jsonpath(get_sign_id_res, '$.data[0].id')[0]
        workflow_api.check_sign_request(sign_id)
        add_sell_request_params['reportId'] = report_id
        add_sell_request_params['signId'] = sign_id
        add_sell_request_params['newHouseId'] = new_house_id
        workflow_api.add_sell_request(add_sell_request_params)
        get_sell_id_res = workflow_api.get_sell_id_request(report_num)
        sell_id = jsonpath(get_sell_id_res, '$.data[0].id')[0]
        workflow_api.check_sell_request(sell_id)
