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
from common.readconfig import ini
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from utils.logger import log

gl_driver = None
account_name = ''
rent_house_code = ''
maintainer_phone = ''
actual_maintainer_name = ''


@allure.feature("租赁房源详情页-相关模块")
class TestHouseDetail(object):
    main_up_view = None
    main_top_view = None
    main_left_view = None
    house_detail_page = None

    @pytest.fixture(scope="function", autouse=True)
    def data_prepare(self, web_driver):
        global gl_driver, rent_house_code, account_name
        gl_driver = web_driver
        self.login_page = LoginPage(gl_driver)
        self.main_up_view = MainUpViewPage(gl_driver)
        self.main_top_view = MainTopViewPage(gl_driver)
        self.main_left_view = MainLeftViewPage(gl_driver)
        self.house_detail_page = HouseDetailPage(gl_driver)
        account_name = self.house_detail_page.get_account_name()
        rent_house_code = self.house_detail_page.get_house_info_by_db(account_name, '租赁')
        yield
        self.main_up_view.clear_all_title()

    @pytest.fixture(scope="function", autouse=False)
    def data_recovery(self):
        global rent_house_code
        # account_name = self.house_detail_page.get_account_name()
        # rent_house_code = self.house_detail_page.get_house_info_by_db(account_name, '租赁')
        yield
        self.main_left_view.log_out()
        self.login_page.log_in(maintainer_phone, 'Autotest1')
        self.main_top_view.wait_page_loading_complete()
        self.main_top_view.click_close_button()
        self.house_detail_page.change_role('经纪人')
        rent_house_code = self.house_detail_page.get_house_info_by_db(actual_maintainer_name, '租赁')
        num = self.house_detail_page.get_house_num(rent_house_code, '租赁')
        if int(num) > 0:
            self.house_detail_page.enter_house_detail()
            self.house_detail_page.replace_maintainer(account_name)

    @allure.story("查看租赁房源基本信息")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_view_basic_information(self, flag):
        self.house_detail_page.change_role('经纪人')
        num = self.house_detail_page.get_house_num(rent_house_code, flag)
        if int(num) > 0:
            self.house_detail_page.enter_house_detail()
            self.house_detail_page.view_basic_information()
            ele = self.house_detail_page.verify_view_success()
            assert ele is not None
        else:
            log.error('当前维护人没有租赁房源')
            assert False

    @allure.story("维护人提交修改租赁房源状态审核，商圈经理驳回审核")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_modify_house_state(self, flag):
        self.house_detail_page.change_role('经纪人')
        num = self.house_detail_page.get_house_num(rent_house_code, flag)
        if int(num) > 0:  # 判断当前用户的房源数量
            self.house_detail_page.enter_house_detail()
            house_no = self.house_detail_page.get_house_info_in_detail_page(flag)[0]
            res = self.house_detail_page.verify_can_modify()
            if res:  # 校验当前房源是否支持修改状态
                log.error(f'存在待审核的租赁记录，不允许再次修改')
                assert False
            else:
                self.house_detail_page.submit_modify_state_application()
                actual_submit_result = self.house_detail_page.verify_submit_success()
                assert actual_submit_result == '申请提交成功！'  # 校验修改房源状态审核是否提交成功
                actual_result = self.house_detail_page.verify_get_application_success('商圈经理', house_no)
                assert actual_result  # 校验房源状态审核列表更新
                actual_reject_result = self.house_detail_page.verify_reject_application_sucess(house_no)
                assert not actual_reject_result  # 校验驳回审核是否成功
        else:
            log.error("当前维护人没有租赁房源")
            assert False

    @allure.story("修改租赁房源价格-从调整价格进入")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_modify_house_price(self, flag):
        self.house_detail_page.change_role('经纪人')
        num = self.house_detail_page.get_house_num(rent_house_code, flag)
        if int(num) > 0:
            self.house_detail_page.enter_house_detail()
            house_no, initial_price, house_area = self.house_detail_page.get_house_info_in_detail_page(flag)
            initial_price_in_dialog = self.house_detail_page.get_initial_price_in_dialog()
            expect_final_price = self.house_detail_page.modify_house_price(initial_price)
            pytest.assume(initial_price == initial_price_in_dialog)  # 校验修改价格弹窗中的初始价格是否正确
            actual_price_in_detail_page = self.house_detail_page.get_modified_price_in_detail_page(flag,
                                                                                                   expect_final_price,
                                                                                                   house_area)
            pytest.assume(expect_final_price == actual_price_in_detail_page)  # 校验修改后详情页面的价格更新
            actual_text, expect_text = self.house_detail_page.verify_record_list_update(initial_price,
                                                                                        expect_final_price, flag)
            pytest.assume(actual_text == expect_text)  # 校验调价记录列表更新
        else:
            log.error("当前维护人没有租赁房源")
            assert False

    @allure.story("修改租赁房源价格-从房源基础信息进入")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_modify_price_by_information(self, flag):
        self.house_detail_page.change_role('经纪人')
        num = self.house_detail_page.get_house_num(rent_house_code, flag)
        if int(num) > 0:
            self.house_detail_page.enter_house_detail()
            house_no, initial_price, house_area = self.house_detail_page.get_house_info_in_detail_page(flag)
            expect_final_price = self.house_detail_page.modify_price_from_basic_information_page()
            actual_price_in_detail_page = self.house_detail_page.get_modified_price_in_detail_page('租赁',
                                                                                                   expect_final_price,
                                                                                                   house_area)
            pytest.assume(expect_final_price == actual_price_in_detail_page)  # 校验修改后详情页面的价格更新
            actual_text, expect_text = self.house_detail_page.verify_record_list_update(initial_price,
                                                                                        expect_final_price, flag)
            pytest.assume(actual_text == expect_text)  # 校验调价记录列表更新
            res = self.house_detail_page.verify_log_list_update(account_name)
            self.house_detail_page.click_blank_area()
            assert res  # 校验操作日志列表是否更新
        else:
            log.error('当前维护人没有租赁房源')
            assert False

    @allure.story("举报租赁房源并驳回举报")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['租赁'])
    def test_report_house(self, flag):
        self.house_detail_page.change_role('经纪人')
        num = self.house_detail_page.get_house_num(rent_house_code, flag)
        if int(num) > 0:
            self.house_detail_page.enter_house_detail()
            house_no = self.house_detail_page.get_house_info_in_detail_page(flag)[0]
            res = self.house_detail_page.verify_can_report()
            if res:  # 校验当前房源是否支持举报
                log.error(f'存在待审核的{flag}记录，不允许再次举报'.format(flag=flag))
                assert False
            else:
                actual_submit_result = self.house_detail_page.report_house()
                assert actual_submit_result == '举报房源提交成功!'  # 校验举报房源是否提交成功
                actual_result = self.house_detail_page.verify_report_list_update('平台品管', house_no)
                assert actual_result  # 校验举报房源列表是否更新
                self.house_detail_page.reject_report()
                actual_reject_result = self.house_detail_page.verify_reject_report_success(house_no)
                assert not actual_reject_result  # 校验驳回房源举报是否成功
        else:
            log.error('当前维护人没有租赁房源')
            assert False

    @allure.story("更换当前租赁房源的维护人")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    # @pytest.mark.run(order=2)  # 保证调整价格等用例执行结束后再执行更换房源维护人用例
    def test_replace_maintainer(self, data_recovery):
        global maintainer_phone, actual_maintainer_name
        self.house_detail_page.change_role('经纪人')
        num = self.house_detail_page.get_house_num(rent_house_code, '租赁')
        if int(num) > 0:
            self.house_detail_page.enter_house_detail()
            expect_maintainer_name = self.house_detail_page.replace_maintainer('自动化测试AAAAA')
            actual_maintainer_name, maintainer_phone = self.house_detail_page.get_current_maintainer()
            assert expect_maintainer_name == actual_maintainer_name


if __name__ == '__main__':
    pytest.main(['-q', 'test_more.py'])
