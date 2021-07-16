#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@time: 2021/06/22
"""

import re
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element
from config.conf import cm
from page_object.house.writtenentrustmentagreementpage import WrittenEntrustmentAgreementPage
from page_object.house.keyentrustmentcertificatepage import KeyEntrustmentCertificatePage
from page_object.house.vipserviceentrustmentagreementpage import VipServiceEntrustmentAgreementPage
from page_object.house.deedtaxinvoiceinformationpage import DeedTaxInvoiceInformationPage
from page_object.house.owneridentificationinformation import OwnerIdentificationInformationPage
from page_object.house.originalpurchasecontractinformationpage import OriginalPurchaseContractInformationPage
from page_object.house.propertyownershipcertificatepage import PropertyOwnershipCertificatePage

house_detail = Element('house/detail')


class HouseDetailPage(WebPage):

    def get_house_code(self):
        value = self.element_text(house_detail['房源编号标签'])
        return re.search(r"：(\d+)", value).group(1)

    def get_house_type(self):
        value = self.element_text(house_detail['户型标签'])
        return re.search(r"(?P<room>\d+?)-(?P<livingroom>\d+?)-(?P<kitchen>\d+?)-(?P<bathroom>\d+)", value).groupdict()

    def get_orientations(self):
        value = self.element_text(house_detail['朝向标签'])
        return value.split(',')

    def get_floor(self):
        value = self.element_text(house_detail['楼层标签'])
        return value.split('/')[0]

    def get_inspect_type(self):
        value = self.element_text(house_detail['常规看房时间标签'])
        return value.split('： ')[1]

    def get_renovation_condition(self):
        value = self.element_text(house_detail['装修情况标签'])
        return value.split('： ')[1]

    def get_enable_watch_time(self):
        value = self.element_text(house_detail['可看时间标签'])
        return value.split('： ')[1]

    def check_exploration(self):
        value = self.element_text(house_detail['是否预约实勘标签'])
        if '已预约实勘' in value:
            return True
        else:
            return False

    def click_exploration_button(self):
        self.is_click(house_detail['预约实勘按钮'])

    def click_back_exploration_button(self):
        self.is_click(house_detail['实勘退单按钮'])

    def choose_normal_exploration(self):
        self.is_click(house_detail['选择实勘方式_普通实勘单选'])

    def choose_vr_exploration(self):
        self.is_click(house_detail['选择实勘方式_VR实勘单选'])

    def choose_photographer(self, photographer):
        self.is_click(house_detail['摄影师输入框'])
        self.input_text(house_detail['摄影师输入框'], photographer)
        photographer_list = self.find_elements(house_detail['摄影师下拉框'])
        for photographer_ele in photographer_list:
            if photographer in photographer_ele.text:
                photographer_ele.click()
                sleep(0.5)
                break

    def choose_exploration_time(self, date_time):
        self.is_click(house_detail['预约实勘时间_' + date_time[0] + '单选'])
        self.is_click(house_detail['预约实勘时间_时间选择框'])
        time_list = self.find_elements(house_detail['预约实勘时间_时间下拉框'])
        for time_ele in time_list:
            if time_ele.text == date_time[1]:
                time_ele.click()
                break

    def input_appointment_instructions(self, appointment_instructions):
        self.input_text(house_detail['预约说明输入框'], appointment_instructions)

    def click_exploration_confirm_button(self):  # 预约实勘弹窗，点击确认按钮
        self.is_click(house_detail['预约实勘_确认按钮'])

    def choose_back_exploration_reason(self, reason):
        self.is_click(house_detail['实勘退单_退单原因选择框'])
        reason_list = self.find_elements(house_detail['实勘退单_退单原因下拉框'])
        for reason_ele in reason_list:
            if reason_ele.text == reason:
                reason_ele.click()
                sleep()
                break

    def click_back_exploration_return_button(self):
        self.is_click(house_detail['实勘退单_退单按钮'])

    def expand_certificates_info(self):
        ele = self.find_element(house_detail['证件信息展开收起按钮'])
        if ele.text == '展开':
            ele.click()
            sleep()

    def retract_certificates_info(self):
        ele = self.find_element(house_detail['证件信息展开收起按钮'])
        if ele.text == '收起':
            ele.click()
            sleep()

    def click_written_entrustment_agreement_upload_button(self):
        self.__click_upload_button('书面委托协议')

    def click_key_entrustment_certificate_upload_button(self):
        self.__click_upload_button('钥匙委托凭证')

    def click_vip_service_entrustment_agreement_upload_button(self):
        self.__click_upload_button('VIP服务委托协议')

    def click_deed_tax_invoice_upload_button(self):
        self.__click_upload_button('契税票')

    def click_owner_identification_information_upload_button(self):
        self.__click_upload_button('身份证明')

    def click_original_purchase_contract_information_upload_button(self):
        self.__click_upload_button('原始购房合同')

    def click_property_ownership_certificate_upload_button(self):
        self.__click_upload_button('房产证')

    def __click_upload_button(self, certificate_name):
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[@class='blue' and text()='上传']"
        self.is_click(locator)

    def check_upload_written_entrustment_agreement(self):
        return self.__check_upload_certificate('书面委托协议')

    def check_upload_key_entrustment_certificate(self):
        return self.__check_upload_certificate('钥匙委托凭证')

    def check_upload_vip_service_entrustment_agreement(self):
        return self.__check_upload_certificate('VIP服务委托协议')

    def check_upload_deed_tax_invoice(self):
        return self.__check_upload_certificate('契税票')

    def check_upload_owner_identification_information(self):
        return self.__check_upload_certificate('身份证明')

    def check_upload_original_purchase_contract_information(self):
        return self.__check_upload_certificate('原始购房合同')

    def check_upload_property_ownership_certificate(self):
        return self.__check_upload_certificate('房产证')

    def __check_upload_certificate(self, certificate_name):
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[@class='blue']"
        if self.element_text(locator) == '查看':
            return True
        if self.element_text(locator) == '上传':
            return False

    def delete_written_entrustment_agreement(self):
        self.__delete_certificate('书面委托协议')

    def delete_key_entrustment_certificate(self):
        self.__delete_certificate('钥匙委托凭证')

    def delete_vip_service_entrustment_agreement(self):
        self.__delete_certificate('VIP服务委托协议')

    def delete_deed_tax_invoice(self):
        self.__delete_certificate('契税票')

    def delete_owner_identification_information(self):
        self.__delete_certificate('身份证明')

    def delete_original_purchase_contract_information(self):
        self.__delete_certificate('原始购房合同')

    def delete_property_ownership_certificate(self):
        self.__delete_certificate('房产证')

    def __delete_certificate(self, certificate_name):
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[text()='删除']"
        self.is_click(locator)
        self.is_click(house_detail['删除证件_确定按钮'])
        sleep(2)

    def upload_written_entrustment_agreement(self, written_entrustment_agreement):
        self.click_written_entrustment_agreement_upload_button()
        written_entrustment_agreement_page = WrittenEntrustmentAgreementPage(self.driver)
        written_entrustment_agreement_page.input_entrustment_agreement_number(
            written_entrustment_agreement.get('委托协议编号'))
        written_entrustment_agreement_page.input_entrustment_start_date(written_entrustment_agreement.get('委托日期开始日期'))
        written_entrustment_agreement_page.input_entrustment_end_date(written_entrustment_agreement.get('委托日期结束日期'))
        written_entrustment_agreement_page.input_remark(written_entrustment_agreement.get('备注'))
        written_entrustment_agreement_page.upload_picture([cm.tmp_picture_file])
        written_entrustment_agreement_page.click_submit_button()
        sleep()

    def upload_key_entrustment_certificate(self, key_entrustment_certificate):
        self.click_key_entrustment_certificate_upload_button()
        key_entrustment_certificate_page = KeyEntrustmentCertificatePage(self.driver)
        key_entrustment_certificate_page.input_agreement_number(key_entrustment_certificate.get('协议编号'))
        key_entrustment_certificate_page.choose_key_type(key_entrustment_certificate.get('钥匙'))
        key_entrustment_certificate_page.input_shop_space(key_entrustment_certificate.get('存放店面'))
        key_entrustment_certificate_page.input_remark(key_entrustment_certificate.get('备注说明'))
        key_entrustment_certificate_page.upload_picture([cm.tmp_picture_file])
        key_entrustment_certificate_page.click_save_button()
        sleep()

    def upload_vip_service_entrustment_agreement(self, vip_service_entrustment_agreement):
        self.click_vip_service_entrustment_agreement_upload_button()
        vip_service_entrustment_agreement_page = VipServiceEntrustmentAgreementPage(self.driver)
        vip_service_entrustment_agreement_page.upload_picture([cm.tmp_picture_file])
        vip_service_entrustment_agreement_page.input_entrustment_agreement_number(
            vip_service_entrustment_agreement.get('委托协议编号'))
        vip_service_entrustment_agreement_page.input_entrustment_date(vip_service_entrustment_agreement.get('委托日期'))
        vip_service_entrustment_agreement_page.input_entrustment_end_date(vip_service_entrustment_agreement.get('委托截止'))
        vip_service_entrustment_agreement_page.choose_entrustment_type(vip_service_entrustment_agreement.get('委托类型'))
        vip_service_entrustment_agreement_page.input_entrustment_price(vip_service_entrustment_agreement.get('委托价格'))
        vip_service_entrustment_agreement_page.input_deposit(vip_service_entrustment_agreement.get('保证金'))
        vip_service_entrustment_agreement_page.choose_payment_object(vip_service_entrustment_agreement.get('打款对象'))
        vip_service_entrustment_agreement_page.input_remark(vip_service_entrustment_agreement.get('备注'))
        vip_service_entrustment_agreement_page.click_submit_button()
        sleep()

    def upload_deed_tax_invoice_information(self, deed_tax_invoice_information):
        self.click_deed_tax_invoice_upload_button()
        deed_tax_invoice_information_page = DeedTaxInvoiceInformationPage(self.driver)
        deed_tax_invoice_information_page.upload_picture([cm.tmp_picture_file])
        deed_tax_invoice_information_page.input_filling_date(deed_tax_invoice_information.get('填发日期'))
        deed_tax_invoice_information_page.input_tax_money(deed_tax_invoice_information.get('计税金额'))
        deed_tax_invoice_information_page.input_remark(deed_tax_invoice_information.get('备注'))
        deed_tax_invoice_information_page.click_submit_button()
        sleep()

    def upload_owner_identification_information(self, owner_identification_information):
        self.click_owner_identification_information_upload_button()
        owner_identification_information_page = OwnerIdentificationInformationPage(self.driver)
        owner_identification_information_page.choose_seller_type(owner_identification_information.get('卖方类型'))
        owner_identification_information_page.choose_identity_type(owner_identification_information.get('证件类型'))
        owner_identification_information_page.upload_picture([cm.tmp_picture_file])
        owner_identification_information_page.choose_nationality(owner_identification_information.get('国籍'))
        owner_identification_information_page.input_owner_name(owner_identification_information.get('业主姓名'))
        owner_identification_information_page.input_valid_period_start(
            owner_identification_information.get('有效期限_开始日期'))
        owner_identification_information_page.input_valid_period_end(owner_identification_information.get('有效期限_结束日期'))
        owner_identification_information_page.input_remark(owner_identification_information.get('备注'))
        owner_identification_information_page.click_submit_button()
        sleep()

    def upload_original_purchase_contract_information(self, original_purchase_contract_information):
        self.click_original_purchase_contract_information_upload_button()
        original_purchase_contract_information_page = OriginalPurchaseContractInformationPage(self.driver)
        original_purchase_contract_information_page.input_contract_registration_date(
            original_purchase_contract_information.get('原始购房合同登记日期'))
        original_purchase_contract_information_page.input_building_area(
            original_purchase_contract_information.get('建筑面积'))
        original_purchase_contract_information_page.input_room_area(original_purchase_contract_information.get('套内面积'))
        original_purchase_contract_information_page.choose_is_share(original_purchase_contract_information.get('是否共有'))
        original_purchase_contract_information_page.input_remark(original_purchase_contract_information.get('备注'))
        original_purchase_contract_information_page.upload_picture([cm.tmp_picture_file])
        original_purchase_contract_information_page.click_submit_button()
        sleep()

    def upload_property_ownership_certificate(self, property_ownership_certificate):
        self.click_property_ownership_certificate_upload_button()
        property_ownership_certificate_page = PropertyOwnershipCertificatePage(self.driver)
        property_ownership_certificate_page.upload_picture([cm.tmp_picture_file])
        property_ownership_certificate_page.input_contract_registration_date(property_ownership_certificate.get('登记日期'))
        property_ownership_certificate_page.choose_is_share(property_ownership_certificate.get('是否共有'))
        property_ownership_certificate_page.input_building_area(property_ownership_certificate.get('建筑面积'))
        property_ownership_certificate_page.input_room_area(property_ownership_certificate.get('套内面积'))
        property_ownership_certificate_page.input_remark(property_ownership_certificate.get('备注'))
        property_ownership_certificate_page.click_submit_button()
        sleep()

    def click_invalid_house_button(self):
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        self.move_mouse_to_element(house_detail['无效该房源按钮'])
        self.is_click(house_detail['无效该房源按钮'])
        self.is_click(house_detail['无效房源弹窗_确定按钮'])

    def input_invalid_reason(self, invalid_reason):
        self.input_text(house_detail['无效理由输入框'], invalid_reason)

    def click_invalid_reason_confirm_button(self):
        self.is_click(house_detail['无效理由_确认按钮'])

    def click_invalid_reason_cancel_button(self):
        self.is_click(house_detail['无效理由_取消按钮'])

    def get_house_property_address(self):
        self.is_click(house_detail['右侧菜单地址按钮'])
        estate_name = self.element_text(house_detail['房源物业地址_楼盘名称显示框']).split('楼盘名称')[1]
        building_name = self.element_text(house_detail['房源物业地址_楼栋显示框']).split('楼栋')[1]
        unit_name = self.element_text(house_detail['房源物业地址_单元显示框']).split('单元')[1]
        door_name = self.element_text(house_detail['房源物业地址_门牌显示框']).split('门牌')[1]
        self.is_click(house_detail['房源物业地址_关闭按钮'])
        return {
            'estate_name': estate_name,
            'building_name': building_name,
            'unit_name': unit_name,
            'door_name': door_name
        }

    def page_refresh(self):
        self.refresh()
        sleep(2)
