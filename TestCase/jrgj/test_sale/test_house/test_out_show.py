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
from random import randint
from config.conf import cm
from page_object.common.web.login.loginpage import LoginPage
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_value
from utils.timeutil import dt_strftime
from utils.timeutil import dt_strftime_with_delta
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.survey.tablepage import SurveyTablePage
from page_object.jrgj.web.survey.detailpage import SurveyDetailPage
from page_object.jrgj.web.agreement.listpage import AgreementListPage
from page_object.jrgj.web.main.certificateexaminepage import CertificateExaminePage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.jrgj.app.order.tablepage import AppOrderTablePage
from page_object.jrgj.app.order.detailpage import AppOrderDetailPage

house_code = ''


@allure.feature("测试房源模块")
class TestOutShow(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_out_show.json"
    exploration_info = get_value(json_file_path, 'exploration_info')
    survey_person_info = get_value(json_file_path, ini.environment)
    written_entrustment_agreement = get_value(json_file_path, 'written_entrustment_agreement')

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)

        main_leftview.change_role('经纪人')
        house_code = house_table.get_house_code_by_db(flag='买卖')
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        yield
        main_upview.clear_all_title()

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=12)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)

        house_detail.expand_certificates_info()
        if house_detail.check_upload_written_entrustment_agreement() != '未上传':
            log.info('删除委托协议')
            house_detail.delete_written_entrustment_agreement()
        if house_detail.check_survey_status() == '已上传':
            log.info('实勘已上传,实勘退单')
            main_leftview.change_role('超级管理员')
            house_code = house_table.get_house_code_by_db(flag='买卖')
            assert house_code != ''
            log.info('房源编号为：' + house_code)
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
            house_detail.click_delete_survey_button()
            house_detail.dialog_click_confirm_button()
        house_detail.click_go_top_button()
        house_detail.choose_out_show()
        assert main_topview.find_notification_content() == '该房源不存在有效的委托协议或者没有上传实勘图'

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=12)
    def test_002(self, web_driver, android_driver):
        login = LoginPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        survey_table = SurveyTablePage(web_driver)
        survey_detail = SurveyDetailPage(web_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)
        app_login = AppLoginPage(android_driver)
        app_order_table = AppOrderTablePage(android_driver)
        app_order_detail = AppOrderDetailPage(android_driver)

        house_detail.expand_certificates_info()
        if house_detail.check_upload_written_entrustment_agreement() != '未上传':
            house_detail.delete_written_entrustment_agreement()
            main_topview.close_notification()
        if house_detail.check_survey_status() != '已上传':
            log.info('未上传实勘，进行实勘预约')
            if house_detail.check_survey_status() == '已预约':
                house_detail.click_back_survey_button()
                house_detail.dialog_choose_back_exploration_reason('其他')
                house_detail.dialog_click_back_exploration_return_button()
            house_detail.click_survey_appointment_button()
            house_detail.dialog_choose_normal_survey()
            house_detail.dialog_choose_photographer(self.survey_person_info['photographer'])
            house_detail.dialog_choose_exploration_time(self.exploration_info['exploration_time'])
            house_detail.dialog_input_appointment_instructions(self.exploration_info['appointment_instructions'])
            house_detail.dialog_click_confirm_button()
            if not app_login.check_login_page():
                app_main.close_top_view()
                app_main.click_mine_button()
                app_mine.log_out()
            app_login.log_in(self.survey_person_info['photographer_phone'],
                             self.survey_person_info['photographer_password'])
            app_main.click_mine_button()
            if '实勘人员' not in app_mine.get_user_role():
                app_mine.click_setting_center_button()
                app_mine.change_role_choose_role('实勘人员')
                app_mine.change_role_click_confirm_button()
            app_main.click_order_button()
            app_order_table.click_search_button()
            app_order_table.input_search_content(house_code)
            if self.exploration_info['exploration_time'][0] == '今天':
                date = dt_strftime("%d %m %Y")
            elif self.exploration_info['exploration_time'][0] == '明天':
                date = dt_strftime_with_delta(1, "%d %m %Y")
            else:
                raise '传值错误'
            app_order_table.choose_date(date)
            app_order_table.go_order_detail_by_index(1)
            app_order_detail.click_start_shot_button()
            app_order_detail.click_end_shot_button()
            main_leftview.log_out()
            login.log_in(self.survey_person_info['photographer_phone'],
                         self.survey_person_info['photographer_password'])
            main_leftview.change_role('实勘人员')
            main_leftview.click_survey_management_label()
            survey_table.click_reset_button()
            survey_table.input_house_code_search(house_code)
            survey_table.click_search_button()
            survey_table.click_upload_survey_button_by_row(1)
            upload_pictures = [cm.tmp_picture_file, cm.tmp_picture_file]
            survey_detail.upload_picture(upload_pictures)
            survey_detail.set_title_picture_by_index(randint(1, len(upload_pictures)))
            survey_detail.click_save_button()
            main_leftview.log_out()
            login.log_in(ini.user_account, ini.user_password)
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
        house_detail.click_go_top_button()
        house_detail.choose_out_show()
        assert main_topview.find_notification_content() == '该房源不存在有效的委托协议或者没有上传实勘图'

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=12)
    def test_003(self, web_driver):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)
        certificate_examine = CertificateExaminePage(web_driver)

        main_leftview.change_role('超级管理员')
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)

        house_detail.expand_certificates_info()
        if house_detail.check_upload_written_entrustment_agreement() != '审核通过':
            if house_detail.check_upload_written_entrustment_agreement() == '待审核':
                house_detail.delete_written_entrustment_agreement()
            main_upview.clear_all_title()
            main_leftview.click_agreement_list_label()
            if ini.environment == 'sz' or ini.environment == 'ks':
                agreement_list.input_agreement_name_search('一般委托书')
            if ini.environment == 'wx':
                agreement_list.input_agreement_name_search('限时委托代理销售协议')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            written_entrustment_agreement_number = agreement_list.get_written_entrustment_agreement_number()
            self.written_entrustment_agreement['委托协议编号'] = written_entrustment_agreement_number
            main_upview.clear_all_title()
            main_leftview.click_all_house_label()  # 进入房源详情
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter('买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row()
            house_detail.expand_certificates_info()
            house_detail.upload_written_entrustment_agreement(self.written_entrustment_agreement)
            main_leftview.change_role('赋能经理')
            main_rightview.click_certificate_examine()
            certificate_examine.pass_written_entrustment_agreement_examine(house_code)
            main_upview.clear_all_title()
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
        if house_detail.check_survey_status() == '已上传':
            log.info('实勘已上传,实勘退单')
            house_detail.click_delete_survey_button()
            house_detail.dialog_click_confirm_button()
        house_detail.click_go_top_button()
        house_detail.choose_out_show()
        assert main_topview.find_notification_content() == '该房源不存在有效的委托协议或者没有上传实勘图'

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=12)
    def test_004(self, web_driver, android_driver):
        login = LoginPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)
        certificate_examine = CertificateExaminePage(web_driver)
        survey_table = SurveyTablePage(web_driver)
        survey_detail = SurveyDetailPage(web_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)
        app_login = AppLoginPage(android_driver)
        app_order_table = AppOrderTablePage(android_driver)
        app_order_detail = AppOrderDetailPage(android_driver)

        house_detail.expand_certificates_info()
        if house_detail.check_upload_written_entrustment_agreement() != '审核通过':
            if house_detail.check_upload_written_entrustment_agreement() == '待审核':
                house_detail.delete_written_entrustment_agreement()
            main_upview.clear_all_title()
            main_leftview.click_agreement_list_label()
            if ini.environment == 'sz' or ini.environment == 'ks':
                agreement_list.input_agreement_name_search('一般委托书')
            if ini.environment == 'wx':
                agreement_list.input_agreement_name_search('限时委托代理销售协议')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            written_entrustment_agreement_number = agreement_list.get_written_entrustment_agreement_number()
            self.written_entrustment_agreement['委托协议编号'] = written_entrustment_agreement_number
            main_upview.clear_all_title()
            main_leftview.click_all_house_label()  # 进入房源详情
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter('买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row()
            house_detail.expand_certificates_info()
            house_detail.upload_written_entrustment_agreement(self.written_entrustment_agreement)
            main_leftview.change_role('赋能经理')
            main_rightview.click_certificate_examine()
            certificate_examine.pass_written_entrustment_agreement_examine(house_code)
            main_upview.clear_all_title()
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
        if house_detail.check_survey_status() != '已上传':
            log.info('未上传实勘，进行实勘预约')
            if house_detail.check_survey_status() == '已预约':
                house_detail.click_back_survey_button()
                house_detail.dialog_choose_back_exploration_reason('其他')
                house_detail.dialog_click_back_exploration_return_button()
            house_detail.click_survey_appointment_button()
            house_detail.dialog_choose_normal_survey()
            house_detail.dialog_choose_photographer(self.survey_person_info['photographer'])
            house_detail.dialog_choose_exploration_time(self.exploration_info['exploration_time'])
            house_detail.dialog_input_appointment_instructions(self.exploration_info['appointment_instructions'])
            house_detail.dialog_click_confirm_button()
            if not app_login.check_login_page():
                app_main.close_top_view()
                app_main.click_mine_button()
                app_mine.log_out()
            app_login.log_in(self.survey_person_info['photographer_phone'],
                             self.survey_person_info['photographer_password'])
            app_main.click_mine_button()
            if '实勘人员' not in app_mine.get_user_role():
                app_mine.click_setting_center_button()
                app_mine.change_role_choose_role('实勘人员')
                app_mine.change_role_click_confirm_button()
            app_main.click_order_button()
            app_order_table.click_search_button()
            app_order_table.input_search_content(house_code)
            if self.exploration_info['exploration_time'][0] == '今天':
                date = dt_strftime("%d %m %Y")
            elif self.exploration_info['exploration_time'][0] == '明天':
                date = dt_strftime_with_delta(1, "%d %m %Y")
            else:
                raise '传值错误'
            app_order_table.choose_date(date)
            app_order_table.go_order_detail_by_index(1)
            app_order_detail.click_start_shot_button()
            app_order_detail.click_end_shot_button()
            main_leftview.log_out()
            login.log_in(self.survey_person_info['photographer_phone'],
                         self.survey_person_info['photographer_password'])
            main_leftview.change_role('实勘人员')
            main_leftview.click_survey_management_label()
            survey_table.click_reset_button()
            survey_table.input_house_code_search(house_code)
            survey_table.click_search_button()
            survey_table.click_upload_survey_button_by_row(1)
            upload_pictures = [cm.tmp_picture_file, cm.tmp_picture_file]
            survey_detail.upload_picture(upload_pictures)
            survey_detail.set_title_picture_by_index(randint(1, len(upload_pictures)))
            survey_detail.click_save_button()
            main_leftview.log_out()
            login.log_in(ini.user_account, ini.user_password)
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
        house_detail.click_go_top_button()
        house_detail.choose_out_show()
        assert house_detail.get_out_show()


if __name__ == '__main__':
    pytest.main(['-q', 'test_out_show.py'])
