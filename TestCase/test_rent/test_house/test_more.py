#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_more.py
@time: 2021/08/26
"""
import allure
import pytest
from page_object.web.house.detailpage import HouseDetailPage
from page_object.web.login.loginpage import LoginPage
from page_object.web.main.leftviewpage import MainLeftViewPage
from page_object.web.main.topviewpage import MainTopViewPage
from page_object.web.main.upviewpage import MainUpViewPage
from utils.logger import log

rent_house_code = ''
maintainer_phone = ''
actual_maintainer_name = ''

@allure.feature("租赁房源详情页-相关模块")
class TestHouseDetail(object):

    @pytest.fixture(scope="class", autouse=True)
    def data_prepare_and_recovery(self, web_driver):
        global rent_house_code
        house_detail = HouseDetailPage(web_driver)
        account_name = house_detail.get_account_name()
        rent_house_code = house_detail.get_house_info_by_db(account_name, '租赁')
        yield
        main_leftview = MainLeftViewPage(web_driver)
        main_leftview.log_out()
        login_page = LoginPage(web_driver)
        login_page.log_in(maintainer_phone, 'Autotest1')
        main_topview = MainTopViewPage(web_driver)
        main_topview.wait_page_loading_complete()
        main_topview.click_close_button()
        house_detail = HouseDetailPage(web_driver)
        house_detail.change_role('经纪人')
        rent_house_code = house_detail.get_house_info_by_db(actual_maintainer_name, '租赁')
        num = house_detail.get_house_num(rent_house_code, '租赁')
        if int(num) > 0:
            house_detail.enter_house_detail()
            house_detail.replace_maintainer(account_name)

    @pytest.fixture(scope="function", autouse=True)
    def teardown(self, web_driver):
        main_upview = MainUpViewPage(web_driver)
        yield
        main_upview.clear_all_title()

    @allure.story("查看租赁房源基本信息")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_view_basic_information(self, web_driver, flag):
        house_detail = HouseDetailPage(web_driver)
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(rent_house_code, flag)
        if int(num) > 0:
            house_detail.enter_house_detail()
            house_detail.view_basic_information()
            ele = house_detail.verify_view_success()
            assert ele!= None
        else:
            log.error('当前维护人没有租赁房源')
            assert False

    @allure.story("维护人提交修改租赁房源状态审核，商圈经理驳回审核")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_modify_house_state(self, web_driver, flag):
        house_detail = HouseDetailPage(web_driver)
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(rent_house_code, flag)
        if int(num) > 0:  # 判断当前用户的房源数量
            house_detail.enter_house_detail()
            house_no = house_detail.get_house_info_in_detail_page(flag)[0]
            res = house_detail.verify_can_modify()
            if res:  # 校验当前房源是否支持修改状态
                log.error(f'存在待审核的租赁记录，不允许再次修改')
                assert False
            else:
                house_detail.submit_modify_state_application()
                actual_submit_result = house_detail.verify_submit_success()
                assert actual_submit_result == '申请提交成功！'  # 校验修改房源状态审核是否提交成功
                actual_result = house_detail.verify_get_application_success('商圈经理', house_no)
                assert actual_result   # 校验房源状态审核列表更新
                actual_reject_result = house_detail.verify_reject_application_sucess(house_no)
                assert not actual_reject_result   # 校验驳回审核是否成功
        else:
            log.error("当前维护人没有租赁房源")
            assert False

    @allure.story("修改租赁房源价格-从调整价格进入")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_modify_house_price(self, web_driver, flag):
        house_detail = HouseDetailPage(web_driver)
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(rent_house_code, flag)
        if int(num) > 0:
            house_detail.enter_house_detail()
            house_no, initial_price, house_area = house_detail.get_house_info_in_detail_page(flag)
            initial_price_in_dialog = house_detail.get_initial_price_in_dialog()
            expect_final_price = house_detail.modify_house_price(initial_price)
            pytest.assume(initial_price == initial_price_in_dialog)  # 校验修改价格弹窗中的初始价格是否正确
            actual_price_in_detail_page = house_detail.get_modified_price_in_detail_page(flag, expect_final_price, house_area)
            pytest.assume(expect_final_price == actual_price_in_detail_page)  # 校验修改后详情页面的价格更新
            actual_text, expect_text = house_detail.verify_record_list_update(initial_price, expect_final_price, flag)
            pytest.assume(actual_text == expect_text)  # 校验调价记录列表更新
        else:
            log.error("当前维护人没有租赁房源")
            assert False


    @allure.story("修改租赁房源价格-从房源基础信息进入")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_modify_price_by_information(self, web_driver, flag):
        house_detail = HouseDetailPage(web_driver)
        account_name = house_detail.get_account_name()
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(rent_house_code, flag)
        if int(num) > 0:
            house_detail.enter_house_detail()
            house_no, initial_price, house_area = house_detail.get_house_info_in_detail_page(flag)
            expect_final_price = house_detail.modify_price_from_basic_information_page()
            actual_price_in_detail_page = house_detail.get_modified_price_in_detail_page('租赁', expect_final_price, house_area)
            pytest.assume(expect_final_price == actual_price_in_detail_page)  # 校验修改后详情页面的价格更新
            actual_text, expect_text = house_detail.verify_record_list_update(initial_price, expect_final_price, flag)
            pytest.assume(actual_text == expect_text)  # 校验调价记录列表更新
            res = house_detail.verify_log_list_update(account_name)
            house_detail.click_blank_area()
            assert res  # 校验操作日志列表是否更新
        else:
            log.error('当前维护人没有租赁房源')
            assert False


    @allure.story("举报租赁房源并驳回举报")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_report_house(self, web_driver, flag):
        house_detail = HouseDetailPage(web_driver)
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(rent_house_code, flag)
        if int(num) > 0:
            house_detail.enter_house_detail()
            house_no = house_detail.get_house_info_in_detail_page(flag)[0]
            res = house_detail.verify_can_report()
            if res:  # 校验当前房源是否支持举报
                log.error(f'存在待审核的{flag}记录，不允许再次举报'.format(flag=flag))
                assert False
            else:
                actual_submit_result = house_detail.report_house()
                assert actual_submit_result == '举报房源提交成功!'  # 校验举报房源是否提交成功
                actual_result = house_detail.verify_report_list_update('平台品管', house_no)
                assert actual_result   # 校验举报房源列表是否更新
                house_detail.reject_report()
                actual_reject_result = house_detail.verify_reject_report_success(house_no)
                assert not actual_reject_result  # 校验驳回房源举报是否成功
        else:
            log.error('当前维护人没有租赁房源')
            assert False


    @allure.story("更换当前租赁房源的维护人")
    @pytest.mark.run(order=2)  # 保证调整价格等用例执行结束后再执行更换房源维护人用例
    def test_replace_maintainer(self, web_driver):
        global maintainer_phone
        global actual_maintainer_name
        house_detail = HouseDetailPage(web_driver)
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(rent_house_code, '租赁')
        if int(num) > 0:
            house_detail.enter_house_detail()
            expact_maintainer_name = house_detail.replace_maintainer()
            actual_maintainer_name, maintainer_phone = house_detail.get_current_maintainer()
            assert expact_maintainer_name == actual_maintainer_name


if __name__ == '__main__':
    pytest.main(['-q', 'test_more.py'])
