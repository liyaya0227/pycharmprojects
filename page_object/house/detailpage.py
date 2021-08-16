#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@time: 2021/06/22
"""

import re

from common.readconfig import ini
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.rightviewpage import MainRightViewPage
from utils.sqlutil import select_sql
from utils.timeutil import sleep, dt_strftime_with_delta
from utils.timeutil import dt_strftime
from config.conf import cm
from page.webpage import WebPage
from utils.timeutil import dt_strftime
from common.readelement import Element
from utils.timeutil import sleep, dt_strftime_with_delta
from page_object.house.writtenentrustmentagreementpage import WrittenEntrustmentAgreementPage
from page_object.house.keyentrustmentcertificatepage import KeyEntrustmentCertificatePage
from page_object.house.vipserviceentrustmentagreementpage import VipServiceEntrustmentAgreementPage
from page_object.house.deedtaxinvoiceinformationpage import DeedTaxInvoiceInformationPage
from page_object.house.owneridentificationinformationpage import OwnerIdentificationInformationPage
from page_object.house.originalpurchasecontractinformationpage import OriginalPurchaseContractInformationPage
from page_object.house.propertyownershipcertificatepage import PropertyOwnershipCertificatePage

house_detail = Element('house/detail')


class HouseDetailPage(WebPage):

    def get_house_code(self):  # 获取房源详情房源编号
        value = self.element_text(house_detail['房源编号标签'])
        return re.search(r"：(\d+)", value).group(1)

    def get_house_label(self):  # 获取房源标签
        label_list = self.find_elements(house_detail['房源所有标签列标签'], wait_time=2)
        labels = []
        for label_ele in label_list:
            labels.append(label_ele.text)
        return labels

    def get_house_type(self):  # 获取房源详情户型信息
        value = self.element_text(house_detail['户型标签'])
        return re.search(r"(?P<room>\d+?)-(?P<livingroom>\d+?)-(?P<kitchen>\d+?)-(?P<bathroom>\d+)", value).groupdict()

    def get_size(self):  # 获取房源详情朝向信息
        return self.element_text(house_detail['面积标签'])

    def get_orientations(self):  # 获取房源详情朝向信息
        value = self.element_text(house_detail['朝向标签'])
        return value.split(',')

    def get_floor(self):  # 获取房源详情楼层信息
        value = self.element_text(house_detail['楼层标签'])
        return value

    def get_detail_floor(self):  # 获取房源详情具体楼层信息
        value = self.element_text(house_detail['楼层标签'])
        return value

    def get_out_show(self):  # 获取是否外网呈现
        flag = self.get_element_attribute(house_detail['外网呈现按钮'], 'aria-checked')
        if flag == 'false':
            return False
        if flag == 'true':
            return True

    def choose_out_show(self):  # 选择外网呈现
        if not self.get_out_show():
            self.is_click(house_detail['外网呈现按钮'])

    def choose_not_out_show(self):  # 选择外网不呈现
        if self.get_out_show():
            self.is_click(house_detail['外网呈现按钮'])

    def get_inspect_type(self):  # 获取房源详情左侧常规看房时间
        value = self.element_text(house_detail['常规看房时间标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def get_renovation_condition(self):  # 获取房源详情左侧装修情况
        value = self.element_text(house_detail['装修情况标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def get_house_state(self):  # 获取房源详情左侧房屋现状
        value = self.element_text(house_detail['房屋现状标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def get_has_pledge(self):  # 获取房源详情左侧抵押情况
        value = self.element_text(house_detail['抵押情况标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def get_enable_watch_time(self):  # 获取房源详情左侧可看时间
        value = self.element_text(house_detail['可看时间标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def check_survey_status(self):  # 是否已上传实勘
        value = self.element_text(house_detail['是否预约实勘标签'])
        if '下载实勘图' in value:
            return '已上传'
        if '已预约实勘' in value:
            return '已预约'
        if '预约实勘' in value:
            return '未预约'

    def click_survey_appointment_button(self):  # 点击预约实勘按钮
        self.is_click(house_detail['预约实勘按钮'])
        sleep(2)

    def click_back_survey_button(self):  # 点击实勘退单按钮
        self.is_click(house_detail['实勘退单按钮'])

    def dialog_choose_normal_survey(self):  # 预约实勘弹窗选择普通实勘
        self.is_click(house_detail['选择实勘方式_普通实勘单选'])

    def dialog_choose_vr_survey(self):  # 预约实勘弹窗选择VR实勘
        self.is_click(house_detail['选择实勘方式_VR实勘单选'])

    def dialog_choose_photographer(self, photographer):  # 预约实勘弹窗选择摄影师
        self.is_click(house_detail['摄影师输入框'])
        self.input_text(house_detail['摄影师输入框'], photographer)
        photographer_list = self.find_elements(house_detail['摄影师下拉框'])
        for photographer_ele in photographer_list:
            if photographer in photographer_ele.text:
                photographer_ele.click()
                break

    def dialog_choose_exploration_time(self, date_time):  # 预约实勘弹窗输入预约时间
        self.is_click(house_detail['预约实勘时间_' + date_time[0] + '单选'])
        self.is_click(house_detail['预约实勘时间_时间选择框'])
        time_list = self.find_elements(house_detail['预约实勘时间_时间下拉框'])
        for time_ele in time_list:
            if time_ele.text == date_time[1]:
                if "ant-select-item-option-disabled" not in time_ele.get_attribute('class'):
                    time_ele.click()
                    return
        for time_ele in time_list:
            if "ant-select-item-option-disabled" not in time_ele.get_attribute('class'):
                time_ele.click()
                break

    def dialog_input_appointment_instructions(self, appointment_instructions):  # 预约实勘弹窗输入预约说明
        self.input_text(house_detail['预约说明输入框'], appointment_instructions)

    def dialog_choose_back_exploration_reason(self, reason):  # 实勘退单弹窗选择退单原因
        self.is_click(house_detail['实勘退单_退单原因选择框'])
        reason_list = self.find_elements(house_detail['实勘退单_退单原因下拉框'])
        for reason_ele in reason_list:
            if reason_ele.text == reason:
                reason_ele.click()
                break

    def dialog_click_back_exploration_return_button(self):  # 点击实勘退单弹窗退单按钮
        self.is_click(house_detail['实勘退单_退单按钮'])

    def expand_certificates_info(self):  # 展开证书信息
        ele = self.find_element(house_detail['证件信息展开收起按钮'])
        if ele.text == '展开':
            ele.click()
            sleep()

    def retract_certificates_info(self):  # 收起证书信息
        ele = self.find_element(house_detail['证件信息展开收起按钮'])
        if ele.text == '收起':
            ele.click()
            sleep()

    def click_written_entrustment_agreement_upload_button(self):  # 点击书面委托协议证上传按钮
        self.__click_upload_button('书面委托协议')

    def click_key_entrustment_certificate_upload_button(self):  # 点击钥匙委托凭证证上传按钮
        self.__click_upload_button('钥匙委托凭证')

    def click_vip_service_entrustment_agreement_upload_button(self):  # 点击VIP服务委托协议证上传按钮
        self.__click_upload_button('VIP服务委托协议')

    def click_deed_tax_invoice_upload_button(self):  # 点击契税票证上传按钮
        self.__click_upload_button('契税票')

    def click_owner_identification_information_upload_button(self):  # 点击身份证明证上传按钮
        self.__click_upload_button('身份证明')

    def click_original_purchase_contract_information_upload_button(self):  # 点击原始购房合同证上传按钮
        self.__click_upload_button('原始购房合同')

    def click_property_ownership_certificate_upload_button(self):  # 点击房产证上传按钮
        self.__click_upload_button('房产证')

    def __click_upload_button(self, certificate_name):  # 点击证书上传按钮
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[@class='blue' and text()='上传']"
        self.is_click(locator)

    def check_upload_written_entrustment_agreement(self):  # 查看书面委托协议是否已上传
        return self.__check_upload_certificate('书面委托协议')

    def check_upload_key_entrustment_certificate(self):  # 查看钥匙委托凭证是否已上传
        return self.__check_upload_certificate('钥匙委托凭证')

    def check_upload_vip_service_entrustment_agreement(self):  # 查看VIP服务委托协议是否已上传
        return self.__check_upload_certificate('VIP服务委托协议')

    def check_upload_deed_tax_invoice(self):  # 查看契税票是否已上传
        return self.__check_upload_certificate('契税票')

    def check_upload_owner_identification_information(self):  # 查看身份证明是否已上传
        return self.__check_upload_certificate('身份证明')

    def check_upload_original_purchase_contract_information(self):  # 查看原始购房合同是否已上传
        return self.__check_upload_certificate('原始购房合同')

    def check_upload_property_ownership_certificate(self):  # 查看房产证是否已上传
        return self.__check_upload_certificate('房产证')

    def __check_upload_certificate(self, certificate_name):  # 查看证书是否已上传
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[@class='blue']"
        if self.element_text(locator) == '查看':
            certificate_locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::li" \
                                                                                  "//em[contains(text(),'证书')]/i"
            try:
                return self.element_text(certificate_locator)
            except AttributeError:
                return '审核通过'
        if self.element_text(locator) == '上传':
            return '未上传'

    def delete_written_entrustment_agreement(self):  # 删除书面委托协议
        self.__delete_certificate('书面委托协议')

    def delete_key_entrustment_certificate(self):  # 删除钥匙委托凭证
        self.__delete_certificate('钥匙委托凭证')

    def delete_vip_service_entrustment_agreement(self):  # 删除VIP服务委托协议
        self.__delete_certificate('VIP服务委托协议')

    def delete_deed_tax_invoice(self):  # 删除契税票
        self.__delete_certificate('契税票')

    def delete_owner_identification_information(self):  # 删除身份证明
        self.__delete_certificate('身份证明')

    def delete_original_purchase_contract_information(self):  # 删除原始购房合同
        self.__delete_certificate('原始购房合同')

    def delete_property_ownership_certificate(self):  # 删除房产证
        self.__delete_certificate('房产证')

    def __delete_certificate(self, certificate_name):  # 删除证书
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[text()='删除']"
        self.is_click(locator)
        self.is_click(house_detail['删除证件_确定按钮'])

    def upload_written_entrustment_agreement(self, written_entrustment_agreement):  # 上传书面委托协议
        self.click_written_entrustment_agreement_upload_button()
        written_entrustment_agreement_page = WrittenEntrustmentAgreementPage(self.driver)
        written_entrustment_agreement_page.input_entrustment_agreement_number(
            written_entrustment_agreement.get('委托协议编号'))
        start_date = ''
        if written_entrustment_agreement.get('委托日期开始日期') == '':
            start_date = dt_strftime('%Y-%m-%d')
        written_entrustment_agreement_page.input_entrustment_start_date(start_date)
        end_date = ''
        if written_entrustment_agreement.get('委托日期结束日期') == '':
            end_date = dt_strftime_with_delta(10, '%Y-%m-%d')
        written_entrustment_agreement_page.input_entrustment_end_date(end_date)
        written_entrustment_agreement_page.input_remark(written_entrustment_agreement.get('备注'))
        written_entrustment_agreement_page.upload_picture([cm.tmp_picture_file])
        written_entrustment_agreement_page.click_submit_button()

    def upload_key_entrustment_certificate(self, key_entrustment_certificate):  # 上传钥匙委托协议
        self.click_key_entrustment_certificate_upload_button()
        key_entrustment_certificate_page = KeyEntrustmentCertificatePage(self.driver)
        key_entrustment_certificate_page.input_agreement_number(key_entrustment_certificate.get('协议编号'))
        key_entrustment_certificate_page.choose_key_type(key_entrustment_certificate.get('钥匙'))
        key_entrustment_certificate_page.input_shop_space(key_entrustment_certificate.get('存放店面'))
        key_entrustment_certificate_page.input_remark(key_entrustment_certificate.get('备注说明'))
        key_entrustment_certificate_page.upload_picture([cm.tmp_picture_file])
        key_entrustment_certificate_page.click_save_button()

    def upload_vip_service_entrustment_agreement(self, vip_service_entrustment_agreement):  # 上传VIP服务委托协议
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

    def upload_deed_tax_invoice_information(self, deed_tax_invoice_information):  # 上传契税票
        self.click_deed_tax_invoice_upload_button()
        deed_tax_invoice_information_page = DeedTaxInvoiceInformationPage(self.driver)
        deed_tax_invoice_information_page.upload_picture([cm.tmp_picture_file])
        deed_tax_invoice_information_page.input_filling_date(deed_tax_invoice_information.get('填发日期'))
        deed_tax_invoice_information_page.input_tax_money(deed_tax_invoice_information.get('计税金额'))
        deed_tax_invoice_information_page.input_remark(deed_tax_invoice_information.get('备注'))
        deed_tax_invoice_information_page.click_submit_button()

    def upload_owner_identification_information(self, owner_identification_information):  # 上传身份证明
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

    def upload_original_purchase_contract_information(self, original_purchase_contract_information):  # 上传原始购房合同
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

    def upload_property_ownership_certificate(self, property_ownership_certificate):  # 上传房产证
        self.click_property_ownership_certificate_upload_button()
        property_ownership_certificate_page = PropertyOwnershipCertificatePage(self.driver)
        property_ownership_certificate_page.upload_picture([cm.tmp_picture_file])
        property_ownership_certificate_page.input_contract_registration_date(property_ownership_certificate.get('登记日期'))
        property_ownership_certificate_page.choose_is_share(property_ownership_certificate.get('是否共有'))
        property_ownership_certificate_page.input_building_area(property_ownership_certificate.get('建筑面积'))
        property_ownership_certificate_page.input_room_area(property_ownership_certificate.get('套内面积'))
        property_ownership_certificate_page.input_remark(property_ownership_certificate.get('备注'))
        property_ownership_certificate_page.click_submit_button()

    def click_share_button(self):  # 点击房源详情右侧分享按钮
        self.is_click(house_detail['右侧菜单分享按钮'])

    def share_dialog_get_community_name(self):  # 获取分享弹窗楼盘名称
        return self.element_text(house_detail['分享弹窗_楼盘名称标签'])

    def share_dialog_get_house_type(self):  # 获取分享弹窗户型
        value = self.element_text(house_detail['分享弹窗_户型标签'])
        return re.search(r"(?P<room>\d+?)-(?P<livingroom>\d+?)-(?P<kitchen>\d+?)-(?P<bathroom>\d+)", value).groupdict()

    def share_dialog_get_size(self):  # 获取分享弹窗面积
        return self.element_text(house_detail['分享弹窗_面积标签'])

    def share_dialog_get_orientations(self):  # 获取分享弹窗朝向
        value = self.element_text(house_detail['分享弹窗_朝向标签'])
        return value.split(',')

    def share_dialog_get_price(self):  # 获取分享弹窗价格
        return self.element_text(house_detail['分享弹窗_价格标签'])

    def share_dialog_get_name(self):  # 获取分享弹窗姓名
        return self.element_text(house_detail['分享弹窗_姓名标签'])

    def share_dialog_get_phone(self):  # 获取分享弹窗电话
        return self.element_text(house_detail['分享弹窗_电话标签'])

    def click_address_button(self):  # 点击房源详情右侧地址按钮
        self.is_click(house_detail['右侧菜单地址按钮'])

    def dialog_looked_count_exist(self):  # 弹窗返回今日已看是否存在
        if self.find_element(house_detail['弹窗_已看次数标签'], wait_time=1):
            return True
        else:
            return False

    def dialog_get_looked_count(self):  # 弹窗今日已看次数
        return self.element_text(house_detail['弹窗_已看次数标签'])

    def follow_dialog_exist(self):
        if self.find_element(house_detail['跟进弹窗_详细跟进输入框'], wait_time=1):
            return True
        else:
            return False

    def follow_dialog_input_detail_follow(self, detail_follow):
        self.input_text(house_detail['跟进弹窗_详细跟进输入框'], detail_follow)

    def click_floor_button(self):  # 点击房源详情右侧楼层按钮
        self.is_click(house_detail['右侧菜单楼层按钮'])

    def get_floor_dialog_detail_floor(self):  # 获取楼层弹窗具体楼层信息
        value = self.element_text(house_detail['楼层弹窗_具体楼层信息']).split('具体楼层')[1]
        return value.replace(' ', '')

    def click_phone_button(self):  # 点击房源详情右侧电话按钮
        self.is_click(house_detail['右侧菜单电话按钮'])

    def phone_dialog_click_check_button(self):  # 电话弹窗点击查看按钮
        self.is_click(house_detail['电话弹窗_查看按钮'])

    def phone_dialog_get_phone(self):  # 电话弹窗获取电话
        return self.element_text(house_detail['电话弹窗_电话标签']).split('手机')[1]

    def click_invalid_house_button(self):  # 点击房源详情右侧无效房源按钮
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        self.move_mouse_to_element(house_detail['无效该房源按钮'])
        self.is_click(house_detail['无效该房源按钮'])
        self.is_click(house_detail['无效房源弹窗_确定按钮'])

    def input_invalid_reason(self, invalid_reason):  # 无效房源弹窗输入无效理由
        self.input_text(house_detail['无效理由输入框'], invalid_reason)

    def click_invalid_reason_confirm_button(self):  # 点击无效弹窗确认按钮
        self.is_click(house_detail['无效理由_确认按钮'])

    def click_invalid_reason_cancel_button(self):  # 点击无效弹窗取消按钮
        self.is_click(house_detail['无效理由_取消按钮'])

    def click_delete_survey_button(self):  # 点击房源详情右侧删除实勘按钮
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        self.move_mouse_to_element(house_detail['删除实勘按钮'])
        self.is_click(house_detail['删除实勘按钮'])

    def get_tooltip_content(self):
        if self.find_element(house_detail['弹窗显示'], wait_time=2):
            return self.element_text(house_detail['弹窗显示'])
        else:
            return ''

    def get_address_dialog_house_property_address(self):  # 获取房源地址弹窗所有信息
        self.is_click(house_detail['右侧菜单地址按钮'])
        estate_name = self.element_text(house_detail['房源物业地址_楼盘名称显示框']).split('楼盘名称')[1]
        building_name = self.element_text(house_detail['房源物业地址_楼栋显示框']).split('楼栋')[1]
        unit_name = self.element_text(house_detail['房源物业地址_单元显示框']).split('单元')[1]
        door_name = self.element_text(house_detail['房源物业地址_门牌显示框']).split('门牌')[1]
        self.is_click(house_detail['房源物业地址_关闭按钮'])
        if self.follow_dialog_exist():
            self.follow_dialog_input_detail_follow('详细跟进信息')
            self.dialog_click_confirm_button()
        return {
            'estate_name': estate_name,
            'building_name': building_name,
            'unit_name': unit_name,
            'door_name': door_name
        }

    def click_go_top_button(self):  # 点击房源详情右侧顶部按钮
        self.is_click(house_detail['右侧菜单顶部按钮'])

    def page_refresh(self):
        self.refresh()
        sleep(2)

    def click_edit_house_key_info_button(self):  # 点击房源详情维护重点信息按钮
        self.is_click(house_detail['编辑重点维护信息按钮'])

    def dialog_choose_inspect_type(self, inspect_type):  # 维护重点信息弹窗页选择常规看房时间
        self.is_click(house_detail['常规看房时间选择框'])
        inspect_type_list = self.find_elements(house_detail['下拉框'])
        for inspect_type_ele in inspect_type_list:
            if inspect_type_ele.text == inspect_type:
                inspect_type_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_house_state(self, house_state):  # 维护重点信息弹窗页选择房屋现状
        self.is_click(house_detail['房屋现状选择框'])
        house_state_list = self.find_elements(house_detail['下拉框'])
        for house_state_ele in house_state_list:
            if house_state_ele.text == house_state:
                house_state_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_input_house_state_desc(self, house_state_desc):  # 维护重点信息弹窗页输入房屋现状说明
        self.clear_text(house_detail['房屋现状输入框'])
        self.input_text(house_detail['房屋现状输入框'], house_state_desc)

    def dialog_choose_is_unique(self, is_unique):  # 维护重点信息弹窗页选择是否唯一
        self.is_click(house_detail['是否唯一选择框'])
        is_unique_list = self.find_elements(house_detail['下拉框'])
        for is_unique_ele in is_unique_list:
            if is_unique_ele.text == is_unique:
                is_unique_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_input_pay_constraint(self, pay_constraint):  # 维护重点信息弹窗页输入付款要求
        self.clear_text(house_detail['付款要求输入框'])
        self.input_text(house_detail['付款要求输入框'], pay_constraint)

    def dialog_input_sale_reason(self, sale_reason):  # 维护重点信息弹窗页输入售房原因
        self.clear_text(house_detail['售房原因输入框'])
        self.input_text(house_detail['售房原因输入框'], sale_reason)

    def dialog_choose_register_state(self, register_state):  # 维护重点信息弹窗页选择户口情况
        self.is_click(house_detail['户口情况选择框'])
        register_state_list = self.find_elements(house_detail['下拉框'])
        for register_state_ele in register_state_list:
            if register_state_ele.text == register_state:
                register_state_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_has_pledge(self, has_pledge):  # 维护重点信息弹窗页选择抵押情况
        self.is_click(house_detail['抵押情况选择框'])
        has_pledge_list = self.find_elements(house_detail['下拉框'])
        for has_pledge_ele in has_pledge_list:
            if has_pledge_ele.text == has_pledge:
                has_pledge_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_check_out_right_now(self, check_out_right_now):  # 维护重点信息弹窗页选择是否随时可签
        self.is_click(house_detail['是否随时可签选择框'])
        check_out_right_now_list = self.find_elements(house_detail['下拉框'])
        for check_out_right_now_ele in check_out_right_now_list:
            if check_out_right_now_ele.text == check_out_right_now:
                check_out_right_now_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_has_school_places(self, has_school_places):  # 维护重点信息弹窗页选择学区名额
        self.is_click(house_detail['学区名额选择框'])
        has_school_places_list = self.find_elements(house_detail['下拉框'])
        for has_school_places_ele in has_school_places_list:
            if has_school_places_ele.text == has_school_places:
                has_school_places_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_decoration_state(self, decoration_state):  # 维护重点信息弹窗页选择装修情况
        self.is_click(house_detail['装修情况选择框'])
        decoration_state_list = self.find_elements(house_detail['下拉框'])
        for decoration_state_ele in decoration_state_list:
            if decoration_state_ele.text == decoration_state:
                decoration_state_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_house_property_limit(self, house_property_limit):  # 维护重点信息弹窗页选择产证年限
        self.is_click(house_detail['产证年限选择框'])
        house_property_limit_list = self.find_elements(house_detail['下拉框'])
        for house_property_limit_ele in house_property_limit_list:
            if house_property_limit_ele.text == house_property_limit:
                house_property_limit_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_house_usage(self, house_usage):  # 维护重点信息弹窗页选择房屋用途
        self.is_click(house_detail['房屋用途选择框'])
        house_usage_list = self.find_elements(house_detail['下拉框'])
        for house_usage_ele in house_usage_list:
            if house_usage_ele.text == house_usage:
                house_usage_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_click_confirm_button(self):  # 弹窗确定按钮
        self.is_click(house_detail['弹窗_确定按钮'])

    def dialog_click_cancel_button(self):  # 弹窗取消按钮
        self.is_click(house_detail['弹窗_取消按钮'])

    def check_dialog_cancel_button_disabled(self):
        if self.get_element_attribute(house_detail['弹窗_取消按钮'], 'disabled') == 'true':
            return True
        else:
            return False

    def dialog_click_close_button(self):  # 弹窗关闭按钮
        self.is_click(house_detail['弹窗_关闭按钮'])

    def edit_house_key_info(self, test_data):  # 点击房源详情维护重点信息按钮并填写弹窗页所有信息
        self.click_edit_house_key_info_button()
        self.dialog_choose_inspect_type(test_data['常规看房时间'])
        self.dialog_choose_house_state(test_data['房屋现状'][0])
        self.dialog_input_house_state_desc(test_data['房屋现状'][1])
        self.dialog_choose_is_unique(test_data['是否唯一'])
        self.dialog_input_pay_constraint(test_data['付款要求'])
        self.dialog_input_sale_reason(test_data['售房原因'])
        self.dialog_choose_register_state(test_data['户口情况'])
        self.dialog_choose_has_pledge(test_data['抵押情况'])
        self.dialog_choose_check_out_right_now(test_data['是否随时可签'])
        self.dialog_choose_has_school_places(test_data['学区名额'])
        self.dialog_choose_decoration_state(test_data['装修情况'])
        self.dialog_choose_house_property_limit(test_data['产证年限'])
        self.dialog_choose_house_usage(test_data['房屋用途'])
        self.dialog_click_confirm_button()

    def get_house_key_info(self):  # 获取房源详情重点信息
        inspect_type = self.element_text(house_detail['右侧_常规看房时间标签']).split('：')[1].replace(' ', '')
        house_state = self.element_text(house_detail['右侧_房屋现状标签']).split('：')[1].replace(' ', '')
        is_unique = self.element_text(house_detail['右侧_是否唯一标签']).split('：')[1].replace(' ', '')
        pay_constraint = self.element_text(house_detail['右侧_付款要求标签']).split('：')[1].replace(' ', '')
        sale_reason = self.element_text(house_detail['右侧_售房原因标签']).split('：')[1].replace(' ', '')
        register_state = self.element_text(house_detail['右侧_户口情况标签']).split('：')[1].replace(' ', '')
        has_pledge = self.element_text(house_detail['右侧_抵押情况标签']).split('：')[1].replace(' ', '')
        check_out_right_now = self.element_text(house_detail['右侧_是否随时可签标签']).split('：')[1].replace(' ', '')
        has_school_places = self.element_text(house_detail['右侧_学区名额标签']).split('：')[1].replace(' ', '')
        decoration_state = self.element_text(house_detail['右侧_装修情况标签']).split('：')[1].replace(' ', '')
        house_property_limit = self.element_text(house_detail['右侧_产证年限标签']).split('：')[1].replace(' ', '')
        house_usage = self.element_text(house_detail['右侧_房屋用途标签']).split('：')[1].replace(' ', '')
        house_key_info = {'inspect_type': '-' if inspect_type == '' else inspect_type,
                          'house_state': '-' if house_state == '' else house_state,
                          'is_unique': '-' if is_unique == '' else is_unique,
                          'pay_constraint': pay_constraint,
                          'sale_reason': sale_reason,
                          'register_state': '-' if register_state == '' else register_state,
                          'has_pledge': '-' if has_pledge == '' else has_pledge,
                          'check_out_right_now': '-' if check_out_right_now == '' else check_out_right_now,
                          'has_school_places': '-' if has_school_places == '' else has_school_places,
                          'decoration_state': '-' if decoration_state == '' else decoration_state,
                          'house_property_limit': '-' if house_property_limit == '' else house_property_limit,
                          'house_usage': '-' if house_usage == '' else house_usage}
        return house_key_info

    def change_role(self, role_name):
        """切换角色"""
        global main_leftview
        main_leftview = MainLeftViewPage(self.driver)
        main_leftview.change_role(role_name)

    def get_account_name(self):
        """获取当前账号的名字"""
        account_name = self.element_text(house_detail['当前账号名字']).split(' ')[0]
        return account_name

    def get_house_num(self, account_name):
        """获取当前维护人下的房源数量"""
        # account_name = self.element_text(house_detail['当前账号名字']).split(' ')[0]
        house_code = self.get_house_info_by_db(account_name)
        main_leftview.click_all_house_label()
        self.input_text(house_detail['房源编号输入框'], house_code)
        self.is_click(house_detail['搜索按钮'])
        num = self.element_text(house_detail['搜索结果总数'])[8:][:-1]
        return num

    def get_house_info_by_db(self, name):

        estate_sql = "select id from estate_new_base_info where [name]='" + ini.house_community_name + "'"
        estate_id = select_sql(estate_sql)[0][0]

        # house_sql = "select house_code from trade_house where coreinfo_maintainer_name='" + str(name) + \
        #             "' and location_estate_id='" + str(estate_id) + \
        #             "' and location_building_number='" + ini.house_building_id + \
        #             "' and location_building_cell='" + ini.house_building_cell + \
        #             "' and location_floor='" + ini.house_floor + \
        #             "' and location_doorplate='" + ini.house_doorplate + "' and is_valid='1' and [status]='0' order by create_time desc"

        house_sql = "select house_code from trade_house where coreinfo_maintainer_name='" + str(name) + \
                    "' and location_estate_id='" + str(estate_id) + \
                    "' and location_building_number='" + str(1) + \
                    "' and location_building_cell='" + str('1') + \
                    "' and location_floor='" + str('1') + \
                    "' and location_doorplate='" + str('1006') + "' and is_valid='1' and [status]='0' order by create_time desc"
        try:
            print('enter_house_detail', house_sql)
            house_code = select_sql(house_sql)[0][0]
            return house_code
        except IndexError:
            return ''

    def enter_house_detail(self):
        """进入房源详情页面，并获取房源编号、房源面积等信息"""
        self.is_click(house_detail['楼盘名称'])
        house_no = self.element_text(house_detail['房源详情页面的房源编号'])[5:]
        initial_price = self.element_text(house_detail['房源初始价格'])[:-1]
        house_area = self.element_text(house_detail['房源面积']).split('m')[0]
        # init_maintainer_name = self.element_text(house_detail['角色人名字']).split(' ')[1]
        init_maintainer_name = self.element_text(house_detail['角色人名字'])
        self.move_mouse_to_element(house_detail['更多按钮'])
        # print('enter_house_detail', house_area)
        return house_no, initial_price, house_area, init_maintainer_name

    # def click_more_btn(self):
    #     """点击详情页面的更多按钮"""
    #     self.move_mouse_to_element(house_detail['更多按钮'])

    def view_basic_information(self):
        """查看房源基础信息"""
        self.is_click(house_detail['房源基础信息按钮'])

    def verify_can_modify(self):
        """验证是否可以修改"""
        self.move_mouse_to_element(house_detail['房源状态按钮'])
        res = self.is_exists(house_detail['是否可修改状态提示'])
        return res

    def is_view_success(self):
        """验证查看房源基础信息是否成功"""
        res = self.is_exists(house_detail['房源基础信息弹窗title'])
        self.click_blank_area()
        return res

    def submit_modify_state_application(self):
        """提交修改房源状态申请"""
        self.is_click(house_detail['房源状态按钮'])
        self.is_click(house_detail['暂缓出售选项'])
        self.is_click(house_detail['房源状态弹窗确定按钮'])

    def is_submit_success(self):
        """验证提交申请是否成功"""
        res = self.is_exists(house_detail['申请提交成功提示'])
        if res:
            self.is_click(house_detail['弹窗_确定按钮'])
        return res

    def is_get_application_success(self, role_name, house_no):
        """验证商圈经理收到修改房源状态申请"""
        self.change_role(role_name)
        main_rightrview = MainRightViewPage(self.driver)
        main_rightrview.click_review_house_state()
        self.is_click(house_detail['暂缓房源审核选项'])
        xpath = "// span[contains(., '" + house_no + "')]"
        # print('HouseDetailPage1-xpath', xpath)
        res = self.is_exists(('xpath', xpath))
        return res

    def is_reject_application_sucess(self):
        """驳回申请并验证驳回成功"""
        self.is_click(house_detail['驳回按钮'])
        self.input_text(house_detail['驳回理由输入框'], '驳回')
        self.is_click(house_detail['驳回弹窗确定按钮'])
        res = self.is_exists(house_detail['审核成功驳回提示框'])
        self.click_blank_area()
        return res

    def is_modify_house_price_success(self, initial_price):
        """修改房源价格并验证是否提交成功"""
        self.is_click(house_detail['调整价格选项'])
        initial_price2 = self.element_text(house_detail['调价弹窗的房源价格']).split('.')[0] #调整弹窗中的房源初始价格
        if int(initial_price) == int(initial_price2):  #比较房源详情页面和调整价格弹窗中的价格
            is_equel = True
        else:
            is_equel = False

        final_price = int(initial_price) + random.randint(1,9)
        self.input_text(house_detail['房源价格输入框'], final_price)
        self.is_click(house_detail['调价弹窗确定按钮'])
        is_submit = self.is_exists(house_detail['调价成功提示框'])  #判断调价是否提交成功

        return is_equel, is_submit, str(final_price)
    def is_modify_success_by_information(self):
        """从基本信息修改房源价格并验证是否提交成功"""
        self.is_click(house_detail['房源基础信息按钮'])
        final_price = int(self.get_element_attribute(house_detail['详情页面售价输入框'], 'value')) + random.randint(1,9)
        # print('HouseDetailPage-基础详情页面价格', final_price)
        self.clear_text(house_detail['详情页面售价输入框'])
        self.input_text(house_detail['详情页面售价输入框'], final_price)
        self.is_click(house_detail['基础信息弹窗确定按钮'])
        text = self.find_element(house_detail['右上角弹窗_内容']).text
        # print('HouseDetailPage1', text)
        if text == '编辑成功':
            is_submit = True
        else:
            is_submit = False

        return is_submit, str(final_price)

    def is_correct(self, final_price, house_area):
        """验证调价提交成功后，详情页面的单价和总价正确"""
        initial_price3 = self.element_text(house_detail['房源初始价格'])[:-1]  #获取详情页面修改后的价格
        # print('HouseDetailPage-详情页价格', initial_price3)
        # print('HouseDetailPage-最终价格', final_price)
        if int(initial_price3) == int(final_price):  #验证修改后详情页面的价格是否更新
            is_equel2 = True
        else:
            is_equel2 = False

        unit_price = int(final_price)*10000/int(house_area)
        final_unit_price = self.get_house_unit_price(unit_price, 2) #根据修改后的房源价格及房源面积计算单价
        final_unit_price2 = self.element_text(house_detail['房源初始单价']) #获取详情页面修改后的单价
        # print('HouseDetailPage-计算出的最终单价', final_unit_price)
        # print('HouseDetailPage-页面的最终单价', final_unit_price2)
        if final_unit_price == final_unit_price2: #验证计算出的房源单价是否与详情页面展示的一致
            is_equel3 = True
        else:
            is_equel3 = False

        return is_equel2, is_equel3

    def is_record_correct(self, init_price, final_price):
        """验证调价记录列表是否更新"""
        self.is_click(house_detail['调价记录按钮'])
        xpath = "//p[contains(.,'上涨{increase_price}万元')]".format(increase_price = int(final_price) - int(init_price))
        res = self.is_exists(('xpath', xpath))
        if res:
            self.click_blank_area()
        # print('HouseDetailPage', res)
        return res

    def is_log_update(self, account_name):
        """验证操作日志是否更新"""
        self.is_click(house_detail['操作日志按钮'])
        lenth = len(self.find_elements(house_detail['操作人']))
        # print('HouseDetailPage', lenth)
        if lenth > 0:
            if self.is_exists(house_detail['调整价格操作']):
                return True
            else:
                return False
        else:
            return False

    def replace_maintainer(self, init_maintainer_name):
        """更新房源维护人"""
        self.is_click(house_detail['维护人管理按钮'])
        self.is_click(house_detail['选择人员输入框'])
        final_maintainer_name = self.find_elements(house_detail['下拉框'])[0].text
        # print('HouseDetailPage', final_maintainer_name)
        self.find_elements(house_detail['下拉框'])[0].click()
        self.is_click(house_detail['弹窗_确定按钮'])
        final_maintainer_name2 = self.find_elements(house_detail['角色人名字'])[2].text
        # print('HouseDetailPage2', final_maintainer_name2)
        if final_maintainer_name == final_maintainer_name2:
            return True
        else:
            return False

    def verify_can_report(self):
        """验证是否可以举报"""
        self.move_mouse_to_element(house_detail['房源举报按钮'])
        res = self.is_exists(house_detail['是否可举报提示'])
        return res

    def report_house(self):
        """举报房源"""
        self.is_click(house_detail['房源举报按钮'])
        self.is_click(house_detail['房源不卖选项'])
        self.is_click(house_detail['举报房源弹窗确认按钮'])
        text = self.find_element(house_detail['右上角弹窗_内容']).text
        # print('HouseDetailPage', text)
        if text == '举报房源提交成功!':
            return True
        else:
            return False

    def is_get_report(self, role_name, house_no):
        """验证平台品管收到房源举报"""
        self.change_role(role_name)
        main_rightrview = MainRightViewPage(self.driver)
        main_rightrview.click_review_house_report()
        xpath = "// span[contains(., '" + house_no + "')]"
        # print('HouseDetailPage1-xpath', xpath)
        res = self.is_exists(('xpath', xpath))
        return res

    def reject_report(self):
        """驳回房源举报并验证驳回成功"""
        self.is_click(house_detail['驳回按钮'])
        self.input_text(house_detail['驳回理由输入框'], '驳回')
        self.is_click(house_detail['驳回弹窗确定按钮'])
        res = self.is_exists(house_detail['审核成功驳回提示框'])
        self.click_blank_area()
        return res

    def get_house_unit_price(self, float_a , n):
        """根据四舍五入保留2位小数的原则计算房源单价"""
        string_a = str(float_a)
        a, b, c = string_a.partition('.')  # 此时的a、b和c的类型均为字符串类型
        if len(c) > 2:
            cc = c[:n]
            if int(c[n]) >= 5:
                ccc = int(cc) + 1
            else:
                ccc = int(cc)

            return a+b+str(ccc)
        else:
            c2 = int(c)
            # print('HouseDetailPage1-xpath', c2)
            # print('HouseDetailPage1-xpath-len', len(c))
            if len(c) == 1 and c2 == 0:
                # print('HouseDetailPage1-xpath', a)
                return a
            else:
                return a + b + c













