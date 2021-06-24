#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: vipserviceentrustmentagreementpage.py
@time: 2021/06/22
"""

import pytest
import allure
from utils.logger import log
from config.conf import cm
from page_object.main.maintopviewpage import MainTopViewPage
from page_object.main.mianleftviewpage import MainLeftViewPage
from page_object.main.mainrightviewpage import MainRightViewPage
from page_object.main.invalidhousepage import InvalidHousePage
from page_object.house.housetablepage import HouseTablePage
from page_object.house.houseaddpage import HouseAddPage
from page_object.house.housedatailpage import HouseDetailPage
from page_object.agreement.agreementlistpage import AgreementListPage

import re


@allure.feature("测试房源模块")
class TestHouse(object):
    community_name = '自动化测试楼盘'
    building_id = '1'
    building_cell = '1'
    floor = '1'
    doorplate = '102'

    @pytest.fixture(scope="class", autouse=True)
    def close_topview(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_topview.click_close_button()
        main_leftview.change_role('经纪人')
        main_topview.click_close_button()
        main_leftview.click_all_house_label()

    @allure.story("测试新增房源，查看搜索结果用例")
    # @pytest.mark.skip
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        house_owner_name = 'ceshi'
        house_owner_phone = '18112591866'
        house_types = ['2', '2', '2', '1']
        area = '120'
        orientations = ['南']
        sale_price = '200'
        inspect_type = '下班后可看'

        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        house_table = HouseTablePage(web_driver)
        invalid_house_page = InvalidHousePage(web_driver)
        house_add = HouseAddPage(web_driver)

        house_table.click_add_house_button()
        house_add.choose_sale_radio()
        house_add.choose_estate_name(self.community_name)
        house_add.choose_building_id(self.building_id)
        house_add.choose_building_cell(self.building_cell)
        house_add.choose_floor(self.floor)
        house_add.choose_doorplate(self.doorplate)
        house_add.choose_sale_radio()
        house_add.click_next_button()
        content = main_topview.find_notification_content()
        if content != '':
            log.info('房源已存在')
            house_code = re.search(r"房源编号(\d+?)，", content).group(1)
            main_leftview.click_all_house_label()
            house_table.clear_filter()
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row()
            house_detail.click_invalid_house_button()
            house_detail.input_invalid_reason("测试需要")
            house_detail.click_invalid_reason_confirm_button()
            content = main_topview.find_notification_content()
            if content == '错误':
                log.info('无效申请已提交')
                house_detail.click_invalid_reason_cancel_button()
            main_leftview.change_role('超级管理员')
            main_rightview.click_invalid_house()
            invalid_house_page.click_pass_by_housecode(house_code)
            invalid_house_page.click_invalid_house_confirm_button()
            content = main_topview.find_notification_content()
            if content != '成功':
                invalid_house_page.click_pass_by_housecode(house_code)
                invalid_house_page.click_invalid_house_confirm_button()
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_add_house_button()
            house_add.choose_rent_radio()
            house_add.choose_estate_name(self.community_name)
            house_add.choose_building_id(self.building_id)
            house_add.choose_building_cell(self.building_cell)
            house_add.choose_floor(self.floor)
            house_add.choose_doorplate(self.doorplate)
            house_add.choose_sale_radio()
            house_add.click_next_button()
        log.info('填写物业地址成功')
        house_add.input_house_owner_name(house_owner_name)
        house_add.input_house_owner_phone(house_owner_phone)
        log.info('填写业主信息成功')
        house_add.choose_house_type(house_types)
        house_add.input_area(area)
        house_add.choose_orientations(orientations)
        house_add.input_sale_price(sale_price)
        house_add.choose_inspect_type(inspect_type)
        house_add.click_add_button()
        log.info('填写房源信息成功')
        main_leftview.click_all_house_label()
        house_table.choose_estate_name_search(self.community_name)
        house_table.choose_building_name_search(self.building_id)
        # house_table.input_doorplate_search(self.doorplate)
        house_table.click_search_button()
        assert house_table.get_house_table_count() == 1
        log.info('搜索结果正确')

    @allure.story("测试房源预约实勘用例")
    # @pytest.mark.skip
    @pytest.mark.dependency(depends=['test_001'], scope='class')
    def test_002(self, web_driver):
        photographer = 'A1经纪人18400000000'
        exploration_time = ['明天', '16:00-17:00']
        appointment_instructions = '预约实勘，请留意'

        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_reset_button()
        house_table.clear_filter()
        house_table.choose_estate_name_search(self.community_name)
        house_table.choose_building_name_search(self.building_id)
        # house_table.input_doorplate_search(self.doorplate)
        house_table.click_search_button()
        house_table.go_house_detail_by_row()
        house_detail.click_exploration_button()
        house_detail.choose_normal_exploration()
        house_detail.choose_photographer(photographer)
        house_detail.choose_exploration_time(exploration_time)
        house_detail.input_appointment_instructions(appointment_instructions)
        house_detail.click_exploration_confirm_button()
        log.info('预约实勘申请已提交')

    @allure.story("测试房源上传协议用例")
    # @pytest.mark.skip
    @pytest.mark.dependency(depends=['test_001'], scope='class')
    def test_003(self, web_driver):
        written_entrustment_agreement = {'委托协议编号': '', '委托日期开始日期': '2021-06-22', '委托日期结束日期': '2021-07-22',
                                         '备注': '书面委托协议信息', '图片': [cm.tmp_dir + '\\picture.JPG']}
        key_entrustment_certificate = {'协议编号': '', '钥匙': ['密码钥匙', '123456'], '存放店面': '新平街888号',
                                       '备注说明': '登记钥匙', '照片': [cm.tmp_dir + '\\picture.JPG']}
        vip_service_entrustment_agreement = {'图片': [cm.tmp_dir + '\\picture.JPG'], '委托协议编号': '', '委托日期': '2021-06-22',
                                             '委托截止': '2022-06-22', '委托类型': 'VIP服务', '委托价格': '2', '保证金': '8000',
                                             '打款对象': '业主', '备注': 'VIP服务委托协议'}
        deed_tax_invoice_information = {'图片': [cm.tmp_dir + '\\picture.JPG'], '填发日期': '2021-01-22', '计税金额': '200',
                                        '备注': '契税票信息'}
        owner_identification_information = {'卖方类型': '个人', '证件类型': '身份证', '图片': [cm.tmp_dir + '\\picture.JPG'],
                                            '国籍': '中国大陆', '业主姓名': '测试A', '有效期限_开始日期': '2021-01-22',
                                            '有效期限_结束日期': '2091-01-22', '备注': '业主身份证明信息'}
        original_purchase_contract_information = {'原始购房合同登记日期': '2021-01-22', '建筑面积': '120', '套内面积': '118',
                                                  '是否共有': '是', '备注': '原始购房合同信息', '图片': [cm.tmp_dir + '\\picture.JPG']}
        property_ownership_certificate = {'图片': [cm.tmp_dir + '\\picture.JPG'], '登记日期': '2021-01-22', '是否共有': '是',
                                          '建筑面积': '120', '套内面积': '118', '备注': '房产证信息'}

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
        written_entrustment_agreement['委托协议编号'] = written_entrustment_agreement_number
        agreement_list.input_agreement_name_search('钥匙托管协议')
        agreement_list.click_query_button()
        agreement_list.click_download_button_by_row(1)
        key_entrustment_certificate_number = agreement_list.get_key_entrustment_certificate_number()
        key_entrustment_certificate['协议编号'] = key_entrustment_certificate_number
        agreement_list.input_agreement_name_search('房屋出售委托协议VIP版')
        agreement_list.click_query_button()
        agreement_list.click_download_button_by_row(1)
        vip_service_entrustment_agreement_number = agreement_list.get_vip_service_entrustment_agreement_number()
        vip_service_entrustment_agreement['委托协议编号'] = vip_service_entrustment_agreement_number

        main_leftview.click_all_house_label()  # 进入房源详情
        house_table.click_reset_button()
        house_table.clear_filter()
        house_table.choose_estate_name_search(self.community_name)
        house_table.choose_building_name_search(self.building_id)
        house_table.click_search_button()
        house_table.go_house_detail_by_row()
        house_detail.expand_certificates_info()  # 上传协议
        house_detail.upload_written_entrustment_agreement(written_entrustment_agreement)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('书面委托协议已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_key_entrustment_certificate(key_entrustment_certificate)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('钥匙委托凭证已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_vip_service_entrustment_agreement(vip_service_entrustment_agreement)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('VIP服务委托协议已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_deed_tax_invoice_information(deed_tax_invoice_information)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('契税票已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_owner_identification_information(owner_identification_information)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('身份证明已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_original_purchase_contract_information(original_purchase_contract_information)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('原始购房合同已上传')
        house_detail.expand_certificates_info()
        house_detail.upload_property_ownership_certificate(property_ownership_certificate)
        assert '成功' in main_topview.find_notification_content()
        main_topview.close_notification()
        log.info('房产证已上传')


if __name__ == '__main__':
    pytest.main(['D:/PythonProject/UIAutomation/ui/TestCase/test_process/test_house.py'])
