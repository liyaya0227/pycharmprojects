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
from page_object.main.maintopviewpage import MainTopViewPage
from page_object.main.mianleftviewpage import MainLeftViewPage
from page_object.house.housetablepage import HouseTablePage
from page_object.house.housedatailpage import HouseDetailPage
from page_object.agreement.agreementlistpage import AgreementListPage


@allure.feature("测试房源模块")
class TestUploadAgreement(object):

    json_file_path = cm.test_data_dir + "/test_business/test_house/test_upload_agreement.json"
    written_entrustment_agreement = get_value(json_file_path, 'written_entrustment_agreement')
    key_entrustment_certificate = get_value(json_file_path, 'key_entrustment_certificate')
    vip_service_entrustment_agreement = get_value(json_file_path, 'vip_service_entrustment_agreement')
    deed_tax_invoice_information = get_value(json_file_path, 'deed_tax_invoice_information')
    owner_identification_information = get_value(json_file_path, 'owner_identification_information')
    original_purchase_contract_information = get_value(json_file_path, 'original_purchase_contract_information')
    property_ownership_certificate = get_value(json_file_path, 'property_ownership_certificate')

    @pytest.fixture(scope="class", autouse=True)
    def close_topview(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_topview.click_close_button()
        main_leftview.change_role('经纪人')
        main_topview.click_close_button()

    @allure.story("测试房源上传协议用例")
    @pytest.mark.business_house_update
    @pytest.mark.run(order=2)
    @pytest.mark.dependency(depends=['ui/TestCase/test_business/test_house/test_add.py::TestAdd::test_001'],
                            scope='session')
    def test_001(self, web_driver):

        main_leftview = MainLeftViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)

        main_leftview.click_agreement_list()  # 获取协议编号
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

        main_leftview.click_all_house_label()  # 进入房源详情
        house_table.click_reset_button()
        house_table.clear_filter()
        house_table.choose_estate_name_search(ini.house_community_name)
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        house_table.go_house_detail_by_row()
        house_detail.expand_certificates_info()  # 上传协议
        house_detail.upload_written_entrustment_agreement(self.written_entrustment_agreement)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('书面委托协议已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_key_entrustment_certificate(self.key_entrustment_certificate)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('钥匙委托凭证已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_vip_service_entrustment_agreement(self.vip_service_entrustment_agreement)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('VIP服务委托协议已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_deed_tax_invoice_information(self.deed_tax_invoice_information)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('契税票已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_owner_identification_information(self.owner_identification_information)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('身份证明已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_original_purchase_contract_information(self.original_purchase_contract_information)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('原始购房合同已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_property_ownership_certificate(self.property_ownership_certificate)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('房产证已上传')


if __name__ == '__main__':
    pytest.main(["-v", "-s", "/TestCase/test_business/test_house/test_upload_agreement.py"])
    # pytest.main(["-v", "-k", "house and not appointment"])
