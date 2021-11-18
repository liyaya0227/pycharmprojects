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
from case_service.jrgj.web.house.house_service import HouseService
from config.conf import cm
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from utils.jsonutil import get_data
from utils.logger import logger

HOUSE_TYPE = 'sale'
gl_driver = None
house_info = ''
account_name = ''
house_service = None
maintainer_phone = ''
actual_maintainer_name = ''


@allure.feature("买卖房源详情模块-更多")
class TestHouseDetail(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def prepare_house(self, web_driver):
        global gl_driver, house_info, house_service
        gl_driver = web_driver
        house_service = HouseService(gl_driver)
        house_info = house_service.prepare_house(self.test_data, HOUSE_TYPE)

    @pytest.fixture(scope="function", autouse=True)
    def data_prepare(self):
        global account_name, house_service
        self.login_page = LoginPage(gl_driver)
        self.main_up_view = MainUpViewPage(gl_driver)
        self.main_top_view = MainTopViewPage(gl_driver)
        self.main_left_view = MainLeftViewPage(gl_driver)
        self.main_right_view = MainRightViewPage(gl_driver)
        self.house_table_page = HouseTablePage(gl_driver)
        self.house_detail_page = HouseDetailPage(gl_driver)
        account_name = self.house_detail_page.get_account_name()
        self.enter_house_detail(house_info[0])
        current_maintainer_name, current_maintainer_phone = self.house_detail_page.get_current_maintainer()
        if current_maintainer_name != account_name:
            self.main_left_view.log_out()
            house_service.replace_house_maintainer(current_maintainer_phone, 'Autotest1', house_info[0],
                                                   account_name, HOUSE_TYPE)
        yield
        self.main_up_view.clear_all_title()

    @pytest.fixture(scope="function", autouse=False)
    def data_recovery(self):
        yield
        self.main_left_view.log_out()
        self.login_page.log_in(maintainer_phone, 'Autotest1')
        self.main_top_view.wait_page_loading_complete()
        self.main_top_view.click_close_button()
        self.main_left_view.change_role('经纪人')
        self.enter_house_detail(house_info[0])
        self.house_detail_page.replace_maintainer(account_name)

    # @allure.step("进入房源详情")
    # def enter_house_detail(self, house_code):
    #     self.main_left_view.click_all_house_label()
    #     self.house_table_page.input_house_code_search(house_code)
    #     self.house_detail_page.enter_house_detail()
    @allure.step("进入房源详情")
    def enter_house_detail(self, house_code):
        self.main_left_view.click_all_house_label()
        self.house_table_page.input_house_code_search(house_code)
        for i in range(4):
            number = self.house_table_page.get_house_number()
            if int(number) > 0:
                self.house_detail_page.enter_house_detail()
                break
            else:
                self.house_table_page.click_search_button()

    @allure.story("查看房源基本信息")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    def test_view_basic_information(self):
        # self.enter_house_detail(house_info[0])
        self.house_detail_page.view_basic_information()
        self.house_detail_page.close_dialog()
        assert self.house_detail_page.verify_view_success()

    @allure.story("修改房源状态并审核")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    def test_modify_house_status(self):
        if self.house_detail_page.verify_can_modify():  # 已存在待审核记录，先驳回
            self.main_up_view.clear_all_title()
            self.main_left_view.change_role('商圈经理')
            self.main_right_view.click_review_house_state()
            self.house_detail_page.reject_application()
            self.main_top_view.close_notification()
            self.main_up_view.clear_all_title()
            self.main_left_view.change_role('经纪人')
            self.enter_house_detail(house_info[0])
            self.house_detail_page.move_mouse_to_operation_item('房源状态')
        else:
            logger.info('不存在待审核记录的修改房源状态记录')
        self.house_detail_page.submit_modify_state_application()
        assert self.house_detail_page.verify_submit_success() == '申请提交成功！'  # 校验修改房源状态审核是否提交成功
        self.main_left_view.change_role('商圈经理')
        self.main_right_view.click_review_house_state()
        assert self.house_detail_page.verify_get_application_success(house_info[0])  # 校验房源状态审核列表更新
        self.house_detail_page.reject_application()
        self.main_top_view.close_notification()
        assert not self.house_detail_page.verify_reject_application_sucess(house_info[0])  # 校验驳回审核是否成功

    @allure.story("修改房源价格-从调整价格进入")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    def test_modify_house_price(self):
        initial_price, house_area = self.house_detail_page.get_house_info_in_detail_page(HOUSE_TYPE)
        initial_price_in_dialog = self.house_detail_page.get_initial_price_in_dialog()
        expect_final_price = self.house_detail_page.modify_house_price(initial_price)
        pytest.assume(initial_price == initial_price_in_dialog)  # 校验修改价格弹窗中的初始价格是否正确
        actual_price_in_detail_page, expect_final_unit_price, actual_unit_price_in_detail_page = \
            self.house_detail_page.get_modified_price_in_detail_page(HOUSE_TYPE, expect_final_price, house_area)
        pytest.assume(expect_final_price == actual_price_in_detail_page)  # 校验修改后详情页面的价格更新
        pytest.assume(expect_final_unit_price == actual_unit_price_in_detail_page)  # 校验修改后详情页面的单价更新
        actual_text, expect_text = self.house_detail_page.verify_record_list_update(initial_price,
                                                                                    expect_final_price, HOUSE_TYPE)
        assert actual_text == expect_text

    @allure.story("修改房源价格-从房源基础信息进入")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    def test_modify_price_by_information(self):
        initial_price, house_area = self.house_detail_page.get_house_info_in_detail_page(HOUSE_TYPE)
        expect_final_price = self.house_detail_page.modify_price_from_basic_information_page()
        actual_price_in_detail_page, expect_final_unit_price, actual_unit_price_in_detail_page = \
            self.house_detail_page.get_modified_price_in_detail_page(HOUSE_TYPE, expect_final_price, house_area)
        pytest.assume(expect_final_price == actual_price_in_detail_page)  # 校验修改后详情页面的价格更新
        assert (expect_final_unit_price == actual_unit_price_in_detail_page)  # 校验修改后详情页面的单价更新
        actual_text, expect_text = self.house_detail_page.verify_record_list_update(initial_price,
                                                                                    expect_final_price, HOUSE_TYPE)
        pytest.assume(actual_text == expect_text)  # 校验调价记录列表更新
        assert self.house_detail_page.verify_log_list_update(account_name)  # 校验操作日志列表是否更新
        self.house_detail_page.click_close_btn()

    @allure.story("举报房源并审核")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    def test_report_house(self):
        if self.house_detail_page.verify_can_report():  # 存在待审核的举报房源记录，先驳回
            self.main_up_view.clear_all_title()
            self.main_left_view.change_role('平台品管')
            self.main_right_view.click_review_house_report()
            self.house_detail_page.reject_report()
            self.main_top_view.close_notification()
            self.main_up_view.clear_all_title()
            self.main_left_view.change_role('经纪人')
            self.enter_house_detail(house_info[0])
            self.house_detail_page.move_mouse_to_operation_item('房源举报')
        else:
            logger.info('不存在待审核记录的修改房源状态记录')
        actual_submit_result = self.house_detail_page.report_house()
        assert actual_submit_result == '举报房源提交成功!'  # 校验举报房源是否提交成功
        self.main_left_view.change_role('平台品管')
        self.main_right_view.click_review_house_report()
        actual_result = self.house_detail_page.verify_report_list_update(house_info[0])
        assert actual_result  # 校验举报房源列表是否更新
        self.house_detail_page.reject_report()
        self.main_top_view.close_notification()
        actual_reject_result = self.house_detail_page.verify_reject_report_success(house_info[0])
        assert not actual_reject_result  # 校验驳回房源举报是否成功

    @allure.story("更换房源维护人")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=2)  # 保证调整价格等用例执行结束后再执行更换房源维护人用例
    def test_replace_maintainer(self, data_recovery):
        global maintainer_phone, actual_maintainer_name
        expect_maintainer_name = self.house_detail_page.replace_maintainer('自动化测试AAAAA')
        actual_maintainer_name, maintainer_phone = self.house_detail_page.get_current_maintainer()
        assert expect_maintainer_name == actual_maintainer_name


if __name__ == '__main__':
    pytest.main(['-q', 'test_more.py'])
