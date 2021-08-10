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
from utils.logger import log
from common.readconfig import ini
from config.conf import cm
from utils.jsonutil import get_value
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.rightviewpage import MainRightViewPage
from page_object.house.tablepage import HouseTablePage
from page_object.house.detailpage import HouseDetailPage
from page_object.agreement.listpage import AgreementListPage
from page_object.main.certificateexaminepage import CertificateExaminePage

house_code = ''


@allure.feature("测试房源模块")
class TestOutShow(object):

    json_file_path = cm.test_data_dir + "/test_sale/test_house/test_out_show.json"
    exploration_info = get_value(json_file_path, 'exploration_info')
    written_entrustment_agreement = get_value(json_file_path, 'written_entrustment_agreement')

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code

        main_leftview = MainLeftViewPage(web_driver)
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

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=12)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        house_detail.expand_certificates_info()
        if house_detail.check_upload_written_entrustment_agreement():
            log.info('删除委托协议')
            house_detail.delete_key_entrustment_certificate()
            assert main_topview.find_notification_content() == '操作成功'
        if house_detail.check_exploration():
            log.info('实勘已预约,实勘退单')
            house_detail.click_back_exploration_button()
            house_detail.choose_back_exploration_reason('其他')
            house_detail.click_back_exploration_return_button()
            assert main_topview.find_notification_content() == '退单成功'
        house_detail.click_go_top_button()
        house_detail.choose_out_show()
        assert main_topview.find_notification_content() == '该房源不存在有效的委托协议或者没有上传实勘图'

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=12)
    def test_002(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        house_detail.expand_certificates_info()
        if house_detail.check_upload_written_entrustment_agreement():
            house_detail.delete_key_entrustment_certificate()
            assert main_topview.find_notification_content() == '操作成功'
        if not house_detail.check_exploration():
            log.info('')
            house_detail.click_exploration_button()
            house_detail.choose_normal_exploration()
            house_detail.choose_photographer(self.exploration_info['photographer'])
            house_detail.choose_exploration_time(self.exploration_info['exploration_time'])
            house_detail.input_appointment_instructions(self.exploration_info['appointment_instructions'])
            house_detail.click_exploration_confirm_button()
        house_detail.click_go_top_button()
        house_detail.choose_out_show()
        assert main_topview.find_notification_content() == '该房源不存在有效的委托协议或者没有上传实勘图'

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=12)
    def test_003(self, web_driver, android_driver):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)
        certificate_examine = CertificateExaminePage(web_driver)

        house_detail.expand_certificates_info()
        if not house_detail.check_upload_written_entrustment_agreement():
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
            house_detail.expand_certificates_info()
            assert house_detail.check_upload_written_entrustment_agreement()
        if house_detail.check_exploration():
            log.info('实勘已预约,实勘退单')
            house_detail.click_back_exploration_button()
            house_detail.choose_back_exploration_reason('其他')
            house_detail.click_back_exploration_return_button()
            assert main_topview.find_notification_content() == '退单成功'
        house_detail.click_go_top_button()
        house_detail.choose_out_show()
        assert main_topview.find_notification_content() == '该房源不存在有效的委托协议或者没有上传实勘图'

    @allure.story("测试房源外网呈现用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=12)
    def test_004(self, web_driver, android_driver):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)
        certificate_examine = CertificateExaminePage(web_driver)

        house_detail.expand_certificates_info()
        if not house_detail.check_upload_written_entrustment_agreement():
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
            house_detail.expand_certificates_info()
            assert house_detail.check_upload_written_entrustment_agreement()
        if not house_detail.check_exploration():
            log.info('未预约实勘，进行实勘预约')
            house_detail.click_exploration_button()
            house_detail.choose_normal_exploration()
            house_detail.choose_photographer(self.exploration_info['photographer'])
            house_detail.choose_exploration_time(self.exploration_info['exploration_time'])
            house_detail.input_appointment_instructions(self.exploration_info['appointment_instructions'])
            house_detail.click_exploration_confirm_button()

        house_detail.click_go_top_button()
        house_detail.choose_out_show()
