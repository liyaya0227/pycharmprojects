#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_more.py
@time: 2021/08/10
"""
import allure
import pytest
from page_object.house.detailpage import HouseDetailPage
from utils.logger import log


@allure.feature("测试房源详情页面相关功能")
class TestHouseDetail(object):

    # json_file_path = cm.test_data_dir + "/test_sale/test_house/test_add.json"
    # test_data = get_data(json_file_path)
    @allure.story("查看房源基本信息")
    def test_view_basic_information(self, sz_login_admin):
        driver = sz_login_admin
        house_detail = HouseDetailPage(driver)
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num()
        # print('test_view_basic_information', num)
        if int(num) > 0:
            house_detail.enter_house_detail()
            house_detail.click_more_btn()
            house_detail.view_basic_information()
            res = house_detail.is_view_success()
            assert res
        else:
            log.info('当前维护人没有房源')
            assert False

    @allure.story("维护人提交修改房源状态审核，商圈经理驳回审核")
    def test_modify_house_state(self, sz_login_admin):
        driver = sz_login_admin
        house_detail = HouseDetailPage(driver)
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num()
        if int(num) > 0: #判断当前用户的房源数量
            house_no = house_detail.enter_house_detail()[0]
            house_detail.click_more_btn()
            res = house_detail.verify_can_modify()
            print('test_view_basic_information', res)
            if res:  #判断当前房源是否可修改状态
                log.info('存在待审核的记录，不允许再次修改')
                assert False
            else:
                house_detail.submit_modify_state_application()
                res1 = house_detail.is_submit_success()
                if res1:  # 判断提交修改房源状态审核是否成功
                    res2 = house_detail.is_get_application_success('商圈经理', house_no)
                    if res2: #判断商圈经理是否收到申请
                        res3 = house_detail.is_reject_application_sucess()
                        if res3 == False: #判断商圈经理驳回审核是否成功
                            log.info('商圈经理驳回审核失败')
                            assert False
                        assert res3
                    else:
                        log.info('商圈经理未收到修改房源状态申请')
                        assert False
                else:
                    log.info('提交修改房源状态审核失败')
                    assert False
        else:
            log.info('当前维护人没有房源')
            assert False

    # @allure.story("维护人提交修改房源状态审核，商圈经理驳回审核")
    # def test_modify_house_state(self, sz_login_admin):
    #     pass


if __name__ == '__main__':
    pytest.main(['-q','test_more.py'])



