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
from case_service.jrgj.web.house.house_service import HouseService
from case_service.jrgj.web.survey.survey_service import SurveyService
from common_enum.trade_certificate_type import TradeCertificateTypeEnum
from page_object.common.web.login.loginpage import LoginPage
from utils.logger import logger
from config.conf import cm
from common.readconfig import ini
from utils.jsonutil import get_value, get_data
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.main.certificateexaminepage import CertificateExaminePage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.agreement.listpage import AgreementListPage

HOUSE_TYPE = 'sale'
house_info = ''
gl_web_driver = None
survey_service = SurveyService()


@allure.feature("买卖房源详情模块-上传证书")
class TestUploadAgreement(object):
    add_house_json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_add.json"
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_upload_agreement.json"
    written_entrustment_agreement = get_value(json_file_path, 'written_entrustment_agreement')
    key_entrustment_certificate = get_value(json_file_path, 'key_entrustment_certificate')
    vip_service_entrustment_agreement = get_value(json_file_path, 'vip_service_entrustment_agreement')
    deed_tax_invoice_information = get_value(json_file_path, 'deed_tax_invoice_information')
    owner_identification_information = get_value(json_file_path, 'owner_identification_information')
    original_purchase_contract_information = get_value(json_file_path, 'original_purchase_contract_information')
    property_ownership_certificate = get_value(json_file_path, 'property_ownership_certificate')

    @pytest.fixture(scope="class", autouse=True)
    def prepare_house(self, web_driver):
        global gl_web_driver, house_info
        gl_web_driver = web_driver
        house_service = HouseService(gl_web_driver)
        test_data = get_data(self.add_house_json_file_path)
        house_info = house_service.prepare_house(test_data, HOUSE_TYPE)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self):
        self.login_page = LoginPage(gl_web_driver)
        self.main_up_view = MainUpViewPage(gl_web_driver)
        self.main_top_view = MainTopViewPage(gl_web_driver)
        self.main_left_view = MainLeftViewPage(gl_web_driver)
        self.main_right_view = MainRightViewPage(gl_web_driver)
        self.house_table_page = HouseTablePage(gl_web_driver)
        self.house_detail_page = HouseDetailPage(gl_web_driver)
        self.agreement_list_page = AgreementListPage(gl_web_driver)
        self.certificate_examine_page = CertificateExaminePage(gl_web_driver)
        yield
        self.main_up_view.clear_all_title()

    # @allure.step("进入房源详情")
    # def enter_house_detail(self, house_code):
    #     self.main_left_view.change_role('超级管理员')
    #     self.main_left_view.click_all_house_label()
    #     self.house_table_page.input_house_code_search(house_code)
    #     self.house_table_page.click_search_button()
    #     self.house_table_page.go_house_detail_by_row(1)
    @allure.step("进入房源详情")
    def enter_house_detail(self, house_code):
        self.main_left_view.change_role('超级管理员')
        self.main_left_view.click_all_house_label()
        self.house_table_page.input_house_code_search(house_code)
        for i in range(4):
            number = self.house_table_page.get_house_number()
            if int(number) > 0:
                self.house_detail_page.enter_house_detail()
                break
            else:
                self.house_table_page.click_search_button()

    @allure.step("获取协议编号")
    def get_agreement_no(self):
        self.main_left_view.click_agreement_list_label()  # 获取协议编号
        if ini.environment == 'wx':
            self.agreement_list_page.input_agreement_name_search('无锡【芫家】一般委托书【出租】【出售】')
            self.agreement_list_page.click_query_button()
            self.agreement_list_page.click_download_button_by_row(1)
            written_entrustment_agreement_number = self.agreement_list_page.get_written_entrustment_agreement_number()
            self.written_entrustment_agreement['委托协议编号'] = written_entrustment_agreement_number
        else:
            self.agreement_list_page.input_agreement_name_search('一般委托书')
            self.agreement_list_page.click_query_button()
            self.agreement_list_page.click_download_button_by_row(1)
            written_entrustment_agreement_number = self.agreement_list_page.get_written_entrustment_agreement_number()
            self.written_entrustment_agreement['委托协议编号'] = written_entrustment_agreement_number
            self.agreement_list_page.input_agreement_name_search('钥匙托管协议')
            self.agreement_list_page.click_query_button()
            self.agreement_list_page.click_download_button_by_row(1)
            key_entrustment_certificate_number = self.agreement_list_page.get_key_entrustment_certificate_number()
            self.key_entrustment_certificate['协议编号'] = key_entrustment_certificate_number
            self.agreement_list_page.input_agreement_name_search('房屋出售委托协议VIP版')
            self.agreement_list_page.click_query_button()
            self.agreement_list_page.click_download_button_by_row(1)
            vip_service_entrustment_agreement_number = self.agreement_list_page. \
                get_vip_service_entrustment_agreement_number()
            self.vip_service_entrustment_agreement['委托协议编号'] = vip_service_entrustment_agreement_number

    @allure.step("验证证书是否已上传")
    def check_certificate_uploaded(self, certificate_name):
        self.house_detail_page.expand_certificates_info()
        if self.house_detail_page.check_certificate_uploaded(certificate_name) != '未上传':
            self.house_detail_page.delete_uploaded_certificate(certificate_name)
            for i in range(4):  # 验证展开按钮是否存在
                if not self.house_detail_page.verify_btn_exists():
                    self.house_detail_page.page_refresh()
                    print('刷新次数', i)
                else:
                    self.house_detail_page.expand_certificates_info()
                    break

    @allure.story("测试上传协议")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=2)
    def test_upload_agreement(self):
        house_code = house_info[0]
        self.get_agreement_no()  # 获取协议编号
        self.enter_house_detail(house_code)  # 进入房源详情
        self.check_certificate_uploaded(TradeCertificateTypeEnum.tradeHouseDelegateInfoVO.value)  # 上传书面委托协议
        self.house_detail_page.verify_upload_btn_exists(
            TradeCertificateTypeEnum.tradeHouseDelegateInfoVO.value)  # 校验上传按钮是否存在
        self.house_detail_page.upload_written_entrustment_agreement(self.written_entrustment_agreement)
        assert self.main_top_view.find_notification_content() == '上传成功'
        logger.info('书面委托协议已上传')
        if ini.environment != 'wx':
            self.check_certificate_uploaded(TradeCertificateTypeEnum.keyInfoVO.value)  # 上传钥匙委托协议
            self.house_detail_page.verify_upload_btn_exists(
                TradeCertificateTypeEnum.keyInfoVO.value)  # 校验上传按钮是否存在
            self.house_detail_page.upload_key_entrustment_certificate(self.key_entrustment_certificate)
            assert self.main_top_view.find_notification_content() == '上传成功'
            logger.info('钥匙委托凭证已上传')
            self.check_certificate_uploaded(TradeCertificateTypeEnum.tradeHouseVipDelegateInfoVO.value)  # 上传vip服务委托协议
            self.house_detail_page.verify_upload_btn_exists(
                TradeCertificateTypeEnum.tradeHouseVipDelegateInfoVO.value)  # 校验上传按钮是否存在
            self.house_detail_page.upload_vip_service_entrustment_agreement(self.vip_service_entrustment_agreement)
            assert self.main_top_view.find_notification_content() == '上传成功'
            logger.info('VIP服务委托协议已上传')
        self.check_certificate_uploaded(TradeCertificateTypeEnum.tradeHouseTaxInfoVO.value)  # 上传契税
        self.house_detail_page.verify_upload_btn_exists(
            TradeCertificateTypeEnum.tradeHouseTaxInfoVO.value)  # 校验上传按钮是否存在
        self.house_detail_page.upload_deed_tax_invoice_information(self.deed_tax_invoice_information)
        # assert self.main_top_view.find_notification_content() == '上传成功'
        logger.info('契税票已上传')
        self.check_certificate_uploaded(TradeCertificateTypeEnum.tradeHouseIdentityInfoVO.value)  # 上传身份证明
        self.house_detail_page.verify_upload_btn_exists(
            TradeCertificateTypeEnum.tradeHouseIdentityInfoVO.value)  # 校验上传按钮是否存在
        self.house_detail_page.upload_owner_identification_information(self.owner_identification_information)
        # assert self.main_top_view.find_notification_content() == '上传成功'
        logger.info('身份证明已上传')
        self.check_certificate_uploaded(TradeCertificateTypeEnum.tradeHouseContractInfoVO.value)  # 上传原始购房合同
        self.house_detail_page.verify_upload_btn_exists(
            TradeCertificateTypeEnum.tradeHouseContractInfoVO.value)  # 校验上传按钮是否存在
        self.house_detail_page.upload_original_purchase_contract_information(
            self.original_purchase_contract_information)
        # assert self.main_top_view.find_notification_content() == '上传成功'
        logger.info('原始购房合同已上传')
        self.check_certificate_uploaded(TradeCertificateTypeEnum.tradeHouseRoomInfoVO.value)  # 上传房产证
        self.house_detail_page.verify_upload_btn_exists(
            TradeCertificateTypeEnum.tradeHouseRoomInfoVO.value)  # 校验上传按钮是否存在
        self.house_detail_page.upload_property_ownership_certificate(self.property_ownership_certificate)
        # assert self.main_top_view.find_notification_content() == '上传成功'
        logger.info('房产证已上传')
        self.main_left_view.change_role('赋能经理')
        self.main_right_view.click_certificate_examine()
        assert self.certificate_examine_page.get_table_count() > 0
        self.certificate_examine_page.pass_written_entrustment_agreement_examine(house_code)
        if ini.environment != 'wx':
            self.certificate_examine_page.pass_key_entrustment_certificate_examine(house_code)
            self.certificate_examine_page.pass_vip_service_entrustment_agreement_examine(house_code)
            self.certificate_examine_page.pass_property_ownership_certificate_examine(house_code)
