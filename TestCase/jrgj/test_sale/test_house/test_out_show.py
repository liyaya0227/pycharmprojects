#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_out_show.py
@date: 2021/8/9 0009
"""

import pytest
import allure
from case_service.jrgj.web.house.house_service import HouseService
from case_service.jrgj.web.survey.survey_service import SurveyService
from config.conf import cm
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from utils.logger import logger
from common.readconfig import ini
from utils.jsonutil import get_value, get_data
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.agreement.listpage import AgreementListPage
from page_object.jrgj.web.main.certificateexaminepage import CertificateExaminePage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.mine.minepage import AppMinePage

HOUSE_TYPE = 'sale'
house_info = ''
gl_web_driver = None
gl_app_driver = None
survey_service = SurveyService()


@allure.feature("房源详情模块-外网呈现")
class TestOutShow(object):
    add_house_json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_add.json"
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_out_show.json"
    test_data = get_data(add_house_json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def prepare_house(self, web_driver):
        global gl_web_driver, house_info
        gl_web_driver = web_driver
        house_service = HouseService(gl_web_driver)
        house_info = house_service.prepare_house(self.test_data, HOUSE_TYPE)

    @pytest.fixture(scope="function", autouse=True)
    def data_prepare(self, android_driver):
        global gl_app_driver
        gl_app_driver = android_driver
        self.login_page = LoginPage(gl_web_driver)
        self.main_up_view = MainUpViewPage(gl_web_driver)
        self.main_top_view = MainTopViewPage(gl_web_driver)
        self.main_left_view = MainLeftViewPage(gl_web_driver)
        self.main_right_view = MainRightViewPage(gl_web_driver)
        self.house_table_page = HouseTablePage(gl_web_driver)
        self.house_detail_page = HouseDetailPage(gl_web_driver)
        self.agreement_list_page = AgreementListPage(gl_web_driver)
        self.certificate_examine_page = CertificateExaminePage(gl_web_driver)
        self.app_main_page = AppMainPage(gl_app_driver)
        self.app_mine_page = AppMinePage(gl_app_driver)
        self.app_login_page = AppLoginPage(gl_app_driver)
        yield
        self.house_detail_page.choose_not_out_show()
        self.main_up_view.clear_all_title()

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

    @allure.step("获取书面委托协议编号")
    def get_delegate_agreement_no(self):
        self.main_left_view.click_agreement_list_label()
        if ini.environment == 'sz' or ini.environment == 'ks':
            self.agreement_list_page.input_agreement_name_search('一般委托书')
        if ini.environment == 'wx':
            self.agreement_list_page.input_agreement_name_search('无锡【芫家】一般委托书【出租】【出售】')
        self.agreement_list_page.click_query_button()
        self.agreement_list_page.click_download_button_by_row(1)
        delegate_agreement_no = self.agreement_list_page.get_written_entrustment_agreement_number()
        return delegate_agreement_no

    @allure.step("上传书面委托协议并审核")
    def upload_delegate_agreement(self, written_entrustment_agreement_params):
        self.house_detail_page.expand_certificates_info()
        self.house_detail_page.upload_written_entrustment_agreement(written_entrustment_agreement_params)
        self.main_left_view.change_role('赋能经理')
        self.main_right_view.click_certificate_examine()
        self.certificate_examine_page.pass_written_entrustment_agreement_examine(house_info[0])

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=3)
    def test_out_show(self):
        survey_person_info = get_value(self.json_file_path, ini.environment)
        exploration_info = get_value(self.json_file_path, 'exploration_info')
        written_entrustment_agreement_params = get_value(self.json_file_path, 'written_entrustment_agreement')
        self.enter_house_detail(house_info[0])
        if self.house_detail_page.check_survey_status() != '已上传':
            logger.info('未上传实勘，进行实勘预约')
            if self.house_detail_page.check_survey_status() == '已预约':  # 实勘退单
                self.house_detail_page.click_back_survey_button()
                self.house_detail_page.dialog_choose_back_exploration_reason('其他')
                self.house_detail_page.dialog_click_back_exploration_return_button()
            survey_service.order_survey(gl_web_driver, survey_person_info['photographer'],
                                        exploration_info['exploration_time'],  # 预约实勘
                                        exploration_info['appointment_instructions'])
            if not self.app_login_page.check_login_page():  # 拍摄实勘
                self.app_main_page.close_top_view()
                self.app_main_page.click_mine_button()
                self.app_mine_page.log_out()
            self.app_login_page.log_in(survey_person_info['photographer_phone'],
                                       survey_person_info['photographer_password'])
            self.app_main_page.click_mine_button()
            if '实勘人员' not in self.app_mine_page.get_user_role():
                self.app_mine_page.click_setting_center_button()
                self.app_mine_page.change_role_choose_role('实勘人员')
                self.app_mine_page.change_role_click_confirm_button()
            self.app_main_page.click_order_button()  # 拍摄实勘
            exploration_time = exploration_info['exploration_time'][0].split(',')[0]
            survey_service.shoot_survey(gl_app_driver, house_info[0], exploration_time)
            self.main_left_view.log_out()  # 上传实勘
            self.login_page.log_in(survey_person_info['photographer_phone'],
                                   survey_person_info['photographer_password'])
            self.main_left_view.change_role('实勘人员')
            survey_service.upload_survey(gl_web_driver, house_info[0])
            self.main_top_view.close_notification()
            self.main_left_view.log_out()
            self.login_page.log_in(ini.user_account, ini.user_password)
            self.enter_house_detail(house_info[0])
        self.house_detail_page.expand_certificates_info()  # 上传并审核书面委托协议
        if self.house_detail_page.check_upload_written_entrustment_agreement() != '审核通过':
            if self.house_detail_page.check_upload_written_entrustment_agreement() == '待审核':
                self.house_detail_page.delete_written_entrustment_agreement()
            self.main_up_view.clear_all_title()
            delegate_agreement_no = self.get_delegate_agreement_no()
            written_entrustment_agreement_params['委托协议编号'] = delegate_agreement_no
            self.enter_house_detail(house_info[0])
            self.upload_delegate_agreement(written_entrustment_agreement_params)
            self.main_left_view.change_role('经纪人')
            self.enter_house_detail(house_info[0])
        self.house_detail_page.click_go_top_button()
        self.house_detail_page.choose_out_show()
        assert self.house_detail_page.get_out_show()


if __name__ == '__main__':
    pytest.main(['-q', 'test_out_show.py'])
