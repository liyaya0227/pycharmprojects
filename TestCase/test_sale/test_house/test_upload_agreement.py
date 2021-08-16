#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_upload_agreement.py
@time: 2021/06/22
"""

import pytest
import allure
from utils.logger import log
from config.conf import cm
from common.readconfig import ini
from utils.jsonutil import get_value
from page_object.login.loginpage import LoginPage
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.rightviewpage import MainRightViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.main.certificateexaminepage import CertificateExaminePage
from page_object.house.tablepage import HouseTablePage
from page_object.house.detailpage import HouseDetailPage
from page_object.agreement.listpage import AgreementListPage

house_code = ''


@allure.feature("测试房源模块")
class TestUploadAgreement(object):

    json_file_path = cm.test_data_dir + "/test_sale/test_house/test_upload_agreement.json"
    written_entrustment_agreement = get_value(json_file_path, 'written_entrustment_agreement')
    key_entrustment_certificate = get_value(json_file_path, 'key_entrustment_certificate')
    vip_service_entrustment_agreement = get_value(json_file_path, 'vip_service_entrustment_agreement')
    deed_tax_invoice_information = get_value(json_file_path, 'deed_tax_invoice_information')
    owner_identification_information = get_value(json_file_path, 'owner_identification_information')
    original_purchase_contract_information = get_value(json_file_path, 'original_purchase_contract_information')
    property_ownership_certificate = get_value(json_file_path, 'property_ownership_certificate')

    @pytest.fixture(scope="class", autouse=True)
    def test_prepare(self, web_driver):
        global house_code

        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        login = LoginPage(web_driver)

        main_leftview.change_role('经纪人')
        house_code = house_table.get_house_code_by_db(flag='买卖')
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        yield
        main_leftview.log_out()
        login.log_in(ini.user_account, ini.user_password)

    @allure.story("测试房源上传协议用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_001(self, web_driver):

        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)
        certificate_examine = CertificateExaminePage(web_driver)

        main_leftview.click_agreement_list_label()  # 获取协议编号
        if ini.environment == 'sz':
            agreement_list.input_agreement_name_search('一般委托书')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            written_entrustment_agreement_number = agreement_list.get_written_entrustment_agreement_number()
            self.written_entrustment_agreement['委托协议编号'] = written_entrustment_agreement_number
            agreement_list.input_agreement_name_search('钥匙托管协议')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            key_entrustment_certificate_number = agreement_list.get_key_entrustment_certificate_number()
            self.key_entrustment_certificate['协议编号'] = key_entrustment_certificate_number
            agreement_list.input_agreement_name_search('房屋出售委托协议VIP版')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            vip_service_entrustment_agreement_number = agreement_list.get_vip_service_entrustment_agreement_number()
            self.vip_service_entrustment_agreement['委托协议编号'] = vip_service_entrustment_agreement_number
        if ini.environment == 'wx':
            agreement_list.input_agreement_name_search('限时委托代理销售协议')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            written_entrustment_agreement_number = agreement_list.get_written_entrustment_agreement_number()
            self.written_entrustment_agreement['委托协议编号'] = written_entrustment_agreement_number

        main_leftview.click_all_house_label()  # 进入房源详情
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.expand_certificates_info()  # 上传协议
        if house_detail.check_upload_written_entrustment_agreement() != '未上传':
            house_detail.delete_written_entrustment_agreement()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_written_entrustment_agreement(self.written_entrustment_agreement)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('书面委托协议已上传')
        if ini.environment == 'sz':
            house_detail.expand_certificates_info()
            if house_detail.check_upload_key_entrustment_certificate() != '未上传':
                house_detail.delete_key_entrustment_certificate()
                assert main_topview.find_notification_content() == '操作成功'
                house_detail.page_refresh()
                house_detail.expand_certificates_info()
            house_detail.upload_key_entrustment_certificate(self.key_entrustment_certificate)
            assert main_topview.find_notification_content() == '上传成功'
            log.info('钥匙委托凭证已上传')
            house_detail.expand_certificates_info()
            if house_detail.check_upload_vip_service_entrustment_agreement() != '未上传':
                house_detail.delete_vip_service_entrustment_agreement()
                assert main_topview.find_notification_content() == '操作成功'
                house_detail.page_refresh()
                house_detail.expand_certificates_info()
            house_detail.upload_vip_service_entrustment_agreement(self.vip_service_entrustment_agreement)
            assert main_topview.find_notification_content() == '上传成功'
            log.info('VIP服务委托协议已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_deed_tax_invoice() != '未上传':
            house_detail.delete_deed_tax_invoice()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_deed_tax_invoice_information(self.deed_tax_invoice_information)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('契税票已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_owner_identification_information() != '未上传':
            house_detail.delete_owner_identification_information()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_owner_identification_information(self.owner_identification_information)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('身份证明已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_original_purchase_contract_information() != '未上传':
            house_detail.delete_original_purchase_contract_information()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_original_purchase_contract_information(self.original_purchase_contract_information)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('原始购房合同已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_property_ownership_certificate() != '未上传':
            house_detail.delete_property_ownership_certificate()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_property_ownership_certificate(self.property_ownership_certificate)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('房产证已上传')
        main_leftview.change_role('赋能经理')
        main_rightview.click_certificate_examine()
        assert certificate_examine.get_table_count() > 0
        certificate_examine.pass_written_entrustment_agreement_examine(house_code)
        if ini.environment == 'sz':
            certificate_examine.pass_key_entrustment_certificate_examine(house_code)
            certificate_examine.pass_vip_service_entrustment_agreement_examine(house_code)
        certificate_examine.pass_property_ownership_certificate_examine(house_code)
