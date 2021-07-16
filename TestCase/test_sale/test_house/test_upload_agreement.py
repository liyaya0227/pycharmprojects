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
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.choose_estate_name_search(ini.house_community_name)
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        table_count = house_table.get_house_table_count()
        assert table_count > 0
        for row in range(table_count):
            house_table.go_house_detail_by_row(row + 1)
            house_property_address = house_detail.get_house_property_address()
            if house_property_address['estate_name'] == ini.house_community_name \
                    and house_property_address['building_name'] == ini.house_building_id \
                    and house_property_address['door_name'] == ini.house_doorplate:
                house_code = house_detail.get_house_code()
                main_upview.close_title_by_name(house_property_address['estate_name'])
                break
            main_upview.close_title_by_name(house_property_address['estate_name'])
            house_table.clear_filter('买卖')
            house_table.choose_estate_name_search(ini.house_community_name)
            house_table.choose_building_name_search(ini.house_building_id)
            house_table.click_search_button()
        assert house_code != ''
        log.info('创建合同的房源编号: ' + house_code)
        main_upview.clear_all_title()

    @allure.story("测试房源上传协议用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=2)
    def test_001(self, web_driver):

        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)
        certificate_examine = CertificateExaminePage(web_driver)

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
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row()
        house_detail.expand_certificates_info()  # 上传协议
        if house_detail.check_upload_written_entrustment_agreement():
            house_detail.delete_written_entrustment_agreement()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_written_entrustment_agreement(self.written_entrustment_agreement)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('书面委托协议已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_key_entrustment_certificate():
            house_detail.delete_key_entrustment_certificate()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_key_entrustment_certificate(self.key_entrustment_certificate)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('钥匙委托凭证已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_vip_service_entrustment_agreement():
            house_detail.delete_vip_service_entrustment_agreement()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_vip_service_entrustment_agreement(self.vip_service_entrustment_agreement)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('VIP服务委托协议已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_deed_tax_invoice():
            house_detail.delete_deed_tax_invoice()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_deed_tax_invoice_information(self.deed_tax_invoice_information)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('契税票已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_owner_identification_information():
            house_detail.delete_owner_identification_information()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_owner_identification_information(self.owner_identification_information)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('身份证明已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_original_purchase_contract_information():
            house_detail.delete_original_purchase_contract_information()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_original_purchase_contract_information(self.original_purchase_contract_information)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('原始购房合同已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_property_ownership_certificate():
            house_detail.delete_property_ownership_certificate()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_property_ownership_certificate(self.property_ownership_certificate)
        assert main_topview.find_notification_content() == '上传成功'
        log.info('房产证已上传')
        main_leftview.change_role('赋能经理')
        main_rightview.click_certificate_examine()
        certificate_examine.pass_written_entrustment_agreement_examine(house_code)
        certificate_examine.pass_key_entrustment_certificate_examine(house_code)
        certificate_examine.pass_vip_service_entrustment_agreement_examine(house_code)
        certificate_examine.pass_property_ownership_certificate_examine(house_code)
        main_upview.clear_all_title()


if __name__ == '__main__':
    pytest.main(["-v", "-s", "/TestCase/test_sale/test_house/test_upload_agreement.py"])
    # pytest.main(["-v", "-k", "house and not appointment"])
