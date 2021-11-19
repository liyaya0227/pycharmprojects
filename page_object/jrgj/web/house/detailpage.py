#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@time: 2021/06/22
"""
import random
import re
from common.readxml import ReadXml
from config.conf import cm
from common.readconfig import ini
from page.webpage import WebPage
from utils.logger import logger
from utils.sqlutil import select_sql, update_sql
from utils.timeutil import dt_strftime
from common.readelement import Element
from selenium.common.exceptions import TimeoutException
from utils.timeutil import sleep, dt_strftime_with_delta
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.house.writtenentrustmentagreementpage import WrittenEntrustmentAgreementPage
from page_object.jrgj.web.house.keyentrustmentcertificatepage import KeyEntrustmentCertificatePage
from page_object.jrgj.web.house.vipserviceentrustmentagreementpage import VipServiceEntrustmentAgreementPage
from page_object.jrgj.web.house.deedtaxinvoiceinformationpage import DeedTaxInvoiceInformationPage
from page_object.jrgj.web.house.owneridentificationinformationpage import OwnerIdentificationInformationPage
from page_object.jrgj.web.house.originalpurchasecontractinformationpage import OriginalPurchaseContractInformationPage
from page_object.jrgj.web.house.propertyownershipcertificatepage import PropertyOwnershipCertificatePage

house_detail = Element('jrgj/web/house/detail')
house_sql = ReadXml("jrgj//test_rent/test_house/house_sql")


class HouseDetailPage(WebPage):

    def get_house_code(self):  # 获取房源详情房源编号
        value = self.get_element_text(house_detail['房源编号标签'])
        return re.search(r"：(\d+)", value).group(1)

    def get_house_label(self):  # 获取房源标签
        label_list = self.find_elements(house_detail['房源所有标签列标签'], timeout=2)
        labels = []
        for label_ele in label_list:
            labels.append(label_ele.text)
        return labels

    def get_house_type(self):  # 获取房源详情户型信息
        value = self.get_element_text(house_detail['户型标签'])
        return re.search(r"(?P<room>\d+?)-(?P<livingroom>\d+?)-(?P<kitchen>\d+?)-(?P<bathroom>\d+)", value).groupdict()

    def get_size(self):  # 获取房源详情朝向信息
        return self.get_element_text(house_detail['面积标签'])

    def get_orientations(self):  # 获取房源详情朝向信息
        value = self.get_element_text(house_detail['朝向标签'])
        return value.split(',')

    def get_floor(self):  # 获取房源详情楼层信息
        value = self.get_element_text(house_detail['楼层标签'])
        return value

    def get_detail_floor(self):  # 获取房源详情具体楼层信息
        value = self.get_element_text(house_detail['楼层标签'])
        return value.split('/')[0]

    def get_out_show(self):  # 获取是否外网呈现
        flag = self.get_element_attribute(house_detail['外网呈现按钮'], 'aria-checked')
        if flag == 'false':
            return False
        if flag == 'true':
            return True

    def choose_out_show(self):  # 选择外网呈现
        if not self.get_out_show():
            self.click_element(house_detail['外网呈现按钮'], sleep_time=1)

    def choose_not_out_show(self):  # 选择外网不呈现
        if self.get_out_show():
            self.click_element(house_detail['外网呈现按钮'], sleep_time=1)

    def get_inspect_type(self):  # 获取房源详情左侧常规看房时间
        value = self.get_element_text(house_detail['常规看房时间标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def get_renovation_condition(self):  # 获取房源详情左侧装修情况
        value = self.get_element_text(house_detail['装修情况标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def get_house_state(self):  # 获取房源详情左侧房屋现状
        value = self.get_element_text(house_detail['房屋现状标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def get_has_pledge(self):  # 获取房源详情左侧抵押情况
        value = self.get_element_text(house_detail['抵押情况标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def get_enable_watch_time(self):  # 获取房源详情左侧可看时间
        value = self.get_element_text(house_detail['可看时间标签'])
        try:
            return value.split('： ')[1]
        except IndexError:
            return ''

    def check_shopowner_recommend(self):
        if self.element_is_exist(house_detail['店长力荐标签']):
            return self.get_element_text(house_detail['店长力荐标签'])
        else:
            return ''

    def check_survey_status(self):  # 是否已上传实勘
        try:
            self.find_element(house_detail['实勘状态标签'], timeout=2)
            if self.get_element_text(house_detail['实勘状态标签']) == '下载实勘图':
                return '已上传'
            elif '已预约实勘' in self.get_element_text(house_detail['实勘状态标签']):
                return '已预约'
        except TimeoutException:
            return '未预约'

    def check_back_survey(self):  # 是否可退单
        return self.is_exists(house_detail['实勘退单按钮'])

    def click_survey_appointment_button(self):  # 点击预约实勘按钮
        sleep(0.5)
        self.click_element(house_detail['预约实勘按钮'], sleep_time=1.5)

    def click_back_survey_button(self):  # 点击实勘退单按钮
        target = self.find_element(house_detail['实勘退单按钮'])
        self.driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去
        # self.click_element(house_detail['实勘退单按钮'], sleep_time=1)

    def dialog_choose_normal_survey(self):  # 预约实勘弹窗选择普通实勘
        self.click_element(house_detail['选择实勘方式_普通实勘单选'], 1)

    def dialog_choose_vr_survey(self):  # 预约实勘弹窗选择VR实勘
        self.click_element(house_detail['选择实勘方式_VR实勘单选'])

    def dialog_choose_photographer(self, photographer):  # 预约实勘弹窗选择摄影师
        self.click_element(house_detail['摄影师输入框'], sleep_time=1)
        self.input_text(house_detail['摄影师输入框'], photographer)
        photographer_list = self.find_elements(house_detail['摄影师下拉框'])
        for photographer_ele in photographer_list:
            if photographer in photographer_ele.text:
                photographer_ele.click()
                break

    def dialog_choose_exploration_time(self, date_time):  # 预约实勘弹窗输入预约时间
        self.click_element(house_detail['预约实勘时间_' + date_time[0] + '单选'], 1)
        self.click_element(house_detail['预约实勘时间_时间选择框'], sleep_time=1)
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
        sleep(1)

    def dialog_choose_back_exploration_reason(self, reason):  # 实勘退单弹窗选择退单原因
        self.click_element(house_detail['实勘退单_退单原因选择框'])
        reason_list = self.find_elements(house_detail['实勘退单_退单原因下拉框'])
        for reason_ele in reason_list:
            if reason_ele.text == reason:
                reason_ele.click()
                break

    def dialog_click_back_exploration_return_button(self):  # 点击实勘退单弹窗退单按钮
        sleep(1)
        self.click_element(house_detail['实勘退单_退单按钮'], sleep_time=1)

    @staticmethod
    def update_survey_claim_create_time_by_db(house_code, create_time, flag='买卖'):
        if flag == '买卖':
            sql = "select id from trade_house where house_code='" + house_code + "'"
        elif flag == '租赁':
            sql = "select id from rent_house where house_code='" + house_code + "'"
        else:
            raise "传值错误"
        house_id = select_sql(sql)[0][0]
        update_survey_sql = "update survey_claim set create_time = '" + create_time + "' where house_id = '" \
                            + str(house_id) + "' and claim_status=30"
        update_sql(update_survey_sql)

    @staticmethod
    def update_approval_records_update_time_by_db(house_code, update_time, certificate_name, flag='买卖'):
        if flag == '买卖':
            sql = "select id from trade_house where house_code='" + house_code + "'"
        elif flag == '租赁':
            sql = "select id from rent_house where house_code='" + house_code + "'"
        else:
            raise "传值错误"
        house_id = select_sql(sql)[0][0]
        if certificate_name == '书面委托协议':
            update_survey_sql = "update approval_records set update_time = '" + update_time + "' where house_id = '" \
                                + str(house_id) + "' and is_valid = 1 and certificate_type = 3"
        elif certificate_name == '钥匙委托凭证':
            update_survey_sql = "update approval_records set update_time = '" + update_time + "' where house_id = '" \
                                + str(house_id) + "' and is_valid = 1 and certificate_type = 2"
        elif certificate_name == 'VIP服务委托协议':
            update_survey_sql = "update approval_records set update_time = '" + update_time + "' where house_id = '" \
                                + str(house_id) + "' and is_valid = 1 and certificate_type = 0"
        else:
            raise ValueError('传值错误')
        update_sql(update_survey_sql)

    def expand_certificates_info(self):  # 展开证书信息
        target_ele = self.find_element(house_detail['证件信息展开收起按钮'])
        self.driver.execute_script("arguments[0].scrollIntoView();", target_ele)  # 拖动到可见的元素去
        if target_ele.text == '展开':
            target_ele.click()
            sleep(5)
        # ele = self.find_element(house_detail['证件信息展开收起按钮'])
        # if ele.text == '展开':
        #     ele.click()
        #     sleep()

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
        self.click_element(locator)

    def verify_ele_exists(self):  # 验证证书信息按钮是否存在
        return self.is_exists(house_detail['证件信息'])

    def check_upload_btn_exists(self, certificate_name):  # 验证证书上传按钮是否存在
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[@class='blue' and text()='上传']"
        return self.is_exists(locator)

    def verify_upload_btn_exists(self, certificate_name):  # 验证证书上传按钮是否存在
        if self.is_exists(house_detail['证件信息展开收起按钮']):
            self.click_element(house_detail['证件信息展开收起按钮'])
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[@class='blue' and text()='上传']"
        for i in range(3):
            if not self.is_exists(locator):
                self.page_refresh()
                self.click_element(house_detail['证件信息展开收起按钮'])
            else:
                break

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
        text = self.get_element_text(locator)
        if text == '查看':
            certificate_locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::li//em[last()]"
            if '登记日期' in self.get_element_text(certificate_locator):
                return '审核通过'
            else:
                return '待审核'
        elif text == '上传':
            return '未上传'

    def check_certificate_uploaded(self, certificate_name):  # 查看证书是否已上传
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[@class='blue']"
        text = self.get_element_text(locator)
        if text == '查看':
            certificate_locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::li//em[last()]"
            if '登记日期' in self.get_element_text(certificate_locator):
                return '审核通过'
            else:
                return '待审核'
        elif text == '上传':
            return '未上传'

    def delete_uploaded_certificate(self, certificate_name):  # 删除证书
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::p//span[text()='删除']"
        self.click_element(locator)
        self.click_element(house_detail['删除证件_确定按钮'], 12)

    def click_delete_certificate(self):  # 删除证书
        self.expand_certificates_info()
        ele_list = self.find_elements(house_detail['删除证件'])
        for ele in ele_list:
            ele_list = self.find_elements(house_detail['删除证件'])
            ele_list[0].click()
            sleep(2)
            self.click_element(house_detail['删除证件_确定按钮'], 2)
            self.close_notification()
            target = self.find_element(house_detail['证件信息'])
            self.driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去
            if self.is_exists(house_detail['证件信息展开收起按钮']):
                self.click_element(house_detail['证件信息展开收起按钮'], 5)

    def close_notification(self):
        if self.element_is_exist(house_detail['右上角弹窗_关闭按钮'], timeout=5):
            sleep()
            self.click_element(house_detail['右上角弹窗_关闭按钮'], 3)

    def verify_certificate_uploaded(self):
        return self.is_exists(house_detail['删除证件'])

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
        self.click_element(locator)
        self.click_element(house_detail['删除证件_确定按钮'], sleep_time=10)

    def upload_written_entrustment_agreement(self, written_entrustment_agreement):  # 上传书面委托协议
        self.click_written_entrustment_agreement_upload_button()
        written_entrustment_agreement_page = WrittenEntrustmentAgreementPage(self.driver)
        written_entrustment_agreement_page.upload_picture([cm.tmp_picture_file, cm.tmp_picture_file])
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
        written_entrustment_agreement_page.click_submit_button()

    def upload_key_entrustment_certificate(self, key_entrustment_certificate):  # 上传钥匙委托协议
        self.click_key_entrustment_certificate_upload_button()
        key_entrustment_certificate_page = KeyEntrustmentCertificatePage(self.driver)
        key_entrustment_certificate_page.upload_picture([cm.tmp_picture_file])
        key_entrustment_certificate_page.input_agreement_number(key_entrustment_certificate.get('协议编号'))
        key_entrustment_certificate_page.choose_key_type(key_entrustment_certificate.get('钥匙'))
        key_entrustment_certificate_page.input_shop_space(key_entrustment_certificate.get('存放店面'))
        key_entrustment_certificate_page.input_remark(key_entrustment_certificate.get('备注说明'))
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
        owner_identification_information_page.upload_picture([cm.tmp_picture_file])
        owner_identification_information_page.choose_seller_type(owner_identification_information.get('卖方类型'))
        owner_identification_information_page.choose_identity_type(owner_identification_information.get('证件类型'))
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
        original_purchase_contract_information_page.upload_picture([cm.tmp_picture_file])
        original_purchase_contract_information_page.input_contract_registration_date(
            original_purchase_contract_information.get('原始购房合同登记日期'))
        original_purchase_contract_information_page.input_building_area(
            original_purchase_contract_information.get('建筑面积'))
        original_purchase_contract_information_page.input_room_area(original_purchase_contract_information.get('套内面积'))
        original_purchase_contract_information_page.choose_is_share(original_purchase_contract_information.get('是否共有'))
        original_purchase_contract_information_page.input_remark(original_purchase_contract_information.get('备注'))
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
        self.click_element(house_detail['右侧菜单分享按钮'])

    def share_dialog_get_community_name(self):  # 获取分享弹窗楼盘名称
        return self.get_element_text(house_detail['分享弹窗_楼盘名称标签'])

    def share_dialog_get_house_type(self):  # 获取分享弹窗户型
        value = self.get_element_text(house_detail['分享弹窗_户型标签'])
        return re.search(r"(?P<room>\d+?)-(?P<livingroom>\d+?)-(?P<kitchen>\d+?)-(?P<bathroom>\d+)", value).groupdict()

    def share_dialog_get_size(self):  # 获取分享弹窗面积
        return self.get_element_text(house_detail['分享弹窗_面积标签'])

    def share_dialog_get_orientations(self):  # 获取分享弹窗朝向
        value = self.get_element_text(house_detail['分享弹窗_朝向标签'])
        return value.split(',')

    def share_dialog_get_price(self):  # 获取分享弹窗价格
        return self.get_element_text(house_detail['分享弹窗_价格标签'])

    def share_dialog_get_name(self):  # 获取分享弹窗姓名
        return self.get_element_text(house_detail['分享弹窗_姓名标签'])

    def share_dialog_get_phone(self):  # 获取分享弹窗电话
        return self.get_element_text(house_detail['分享弹窗_电话标签'])

    def click_address_button(self):  # 点击房源详情右侧地址按钮
        self.click_element(house_detail['右侧菜单地址按钮'], sleep_time=1)

    def dialog_looked_count_exist(self):  # 弹窗返回今日已看是否存在
        return self.element_is_exist(house_detail['弹窗_已看次数标签'], timeout=1)

    def dialog_get_looked_count(self):  # 弹窗今日已看次数
        return self.get_element_text(house_detail['弹窗_已看次数标签'])

    def follow_dialog_exist(self):
        return self.element_is_exist(house_detail['跟进弹窗_详细跟进输入框'], timeout=1)

    def follow_dialog_input_detail_follow(self, detail_follow):
        self.input_text(house_detail['跟进弹窗_详细跟进输入框'], detail_follow)

    def click_floor_button(self):  # 点击房源详情右侧楼层按钮
        self.click_element(house_detail['右侧菜单楼层按钮'])

    def get_floor_dialog_detail_floor(self):  # 获取楼层弹窗具体楼层信息
        value = self.get_element_text(house_detail['楼层弹窗_具体楼层信息']).split('具体楼层')[1]
        return value.replace(' ', '')

    def click_phone_button(self):  # 点击房源详情右侧电话按钮
        self.click_element(house_detail['右侧菜单电话按钮'], sleep_time=2)

    def phone_dialog_click_check_button(self):  # 电话弹窗点击查看按钮
        self.click_element(house_detail['电话弹窗_查看按钮'], sleep_time=1)

    def phone_dialog_get_phone(self):  # 电话弹窗获取电话
        return self.get_element_text(house_detail['电话弹窗_电话标签']).split('手机')[1]

    def click_invalid_house_button(self):  # 点击房源详情右侧无效房源按钮
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        self.move_mouse_to_element(house_detail['无效该房源按钮'])
        self.click_element(house_detail['无效该房源按钮'])
        self.click_element(house_detail['无效房源弹窗_确定按钮'])

    def input_invalid_reason(self, invalid_reason):  # 无效房源弹窗输入无效理由
        self.input_text(house_detail['无效理由输入框'], invalid_reason)

    def click_invalid_reason_confirm_button(self):  # 点击无效弹窗确认按钮
        self.click_element(house_detail['无效理由_确认按钮'])

    def click_invalid_reason_cancel_button(self):  # 点击无效弹窗取消按钮
        self.click_element(house_detail['无效理由_取消按钮'])

    def click_delete_survey_button(self):  # 点击房源详情右侧删除实勘按钮
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        # self.move_mouse_to_element(house_detail['删除实勘按钮'])
        sleep(3)
        self.click_element(house_detail['删除实勘按钮'], 3)

    def get_tooltip_content(self):
        if self.element_is_exist(house_detail['弹窗显示'], timeout=1):
            return self.get_element_text(house_detail['弹窗显示'])
        else:
            return ''

    def get_address_dialog_house_property_address(self):  # 获取房源地址弹窗所有信息
        self.click_element(house_detail['右侧菜单地址按钮'], sleep_time=4)
        estate_name = self.get_element_text(house_detail['房源物业地址_楼盘名称显示框']).split('楼盘名称')[1]
        building_name = self.get_element_text(house_detail['房源物业地址_楼栋显示框']).split('楼栋')[1]
        unit_name = self.get_element_text(house_detail['房源物业地址_单元显示框']).split('单元')[1]
        door_name = self.get_element_text(house_detail['房源物业地址_门牌显示框']).split('门牌')[1]
        self.click_element(house_detail['弹窗_关闭按钮'])
        if self.follow_dialog_exist():
            self.follow_dialog_input_detail_follow('详细跟进信息')
            self.dialog_click_confirm_button()
        return {
            'estate_name': estate_name,
            'building_name': building_name,
            'unit_name': unit_name,
            'door_name': door_name
        }

    def get_floor_dialog_house_floor(self):  # 获取房源地址弹窗所有信息
        self.click_element(house_detail['右侧菜单楼层按钮'], sleep_time=1)
        floor = self.get_element_text(house_detail['楼层弹窗_具体楼层信息']).split('具体楼层')[1]
        self.click_element(house_detail['弹窗_关闭按钮'])
        return floor.split('/')[0].replace(' ', '')

    def click_go_top_button(self):  # 点击房源详情右侧顶部按钮
        self.click_element(house_detail['右侧菜单顶部按钮'])

    def page_refresh(self):
        self.browser_refresh()

    def get_vip_person(self):
        if self.element_is_exist(house_detail['VIP服务人_姓名标签'], timeout=1):
            return self.get_element_text(house_detail['VIP服务人_姓名标签'])
        else:
            return ''

    def get_all_valid_role_info(self):
        all_role_list = self.find_elements(house_detail['所有角色标签'])
        role_info_list = {}
        for role_ele in all_role_list:
            role = role_ele.text
            pass_flag_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[@class='houseDetail']" \
                                "//div[contains(@class,'roleInfo')]//i[@class='tip' and text()='" + role \
                                + "']/parent::div"
            if 'backgroundImg' in self.get_element_attribute(pass_flag_locator, 'class'):
                continue
            role_info = {}
            brand_locator = 'xpath', \
                            "//div[@style='' or not(@style)]/div[@class='houseDetail']" \
                            "//div[contains(@class,'roleInfo')]//i[@class='tip' and text()='" + role \
                            + "']/parent::div//i[@class='brand']"
            role_info['品牌'] = self.get_element_text(brand_locator)
            name_locator = 'xpath', \
                           "//div[@style='' or not(@style)]/div[@class='houseDetail']" \
                           "//div[contains(@class,'roleInfo')]//i[@class='tip' and text()='" + role \
                           + "']/parent::div//p[@class='card-text-p']/span/parent::p"
            role_info['姓名'] = self.get_element_text(name_locator)
            shop_group_locator = 'xpath', \
                                 "(//div[@style='' or not(@style)]/div[@class='houseDetail']" \
                                 "//div[contains(@class,'roleInfo')]//i[@class='tip' and text()='" + role \
                                 + "']/parent::div//p[@class='card-text-p'])[2]"
            role_info['店组'] = self.get_element_text(shop_group_locator)
            phone_locator = 'xpath', \
                            "//div[@style='' or not(@style)]/div[@class='houseDetail']" \
                            "//div[contains(@class,'roleInfo')]//i[@class='tip' and text()='" + role \
                            + "']/parent::div//p[contains(text(),'联系电话')]/span"
            role_info['电话'] = self.get_element_text(phone_locator)
            role_info_list['房源' + role] = role_info
        return role_info_list

    def click_edit_house_key_info_button(self):  # 点击房源详情维护重点信息按钮
        self.click_element(house_detail['编辑重点维护信息按钮'])

    def dialog_choose_inspect_type(self, inspect_type):  # 维护重点信息弹窗页选择常规看房时间
        self.click_element(house_detail['常规看房时间选择框'], sleep_time=0.5)
        inspect_type_list = self.find_elements(house_detail['下拉框'])
        for inspect_type_ele in inspect_type_list:
            if inspect_type_ele.text == inspect_type:
                inspect_type_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_house_state(self, house_state):  # 维护重点信息弹窗页选择房屋现状
        self.click_element(house_detail['房屋现状选择框'], sleep_time=0.5)
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
        self.click_element(house_detail['是否唯一选择框'], sleep_time=0.5)
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
        self.click_element(house_detail['户口情况选择框'], sleep_time=0.5)
        register_state_list = self.find_elements(house_detail['下拉框'])
        for register_state_ele in register_state_list:
            if register_state_ele.text == register_state:
                register_state_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_has_pledge(self, has_pledge):  # 维护重点信息弹窗页选择抵押情况
        self.click_element(house_detail['抵押情况选择框'], sleep_time=0.5)
        has_pledge_list = self.find_elements(house_detail['下拉框'])
        for has_pledge_ele in has_pledge_list:
            if has_pledge_ele.text == has_pledge:
                has_pledge_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_check_out_right_now(self, check_out_right_now):  # 维护重点信息弹窗页选择是否随时可签
        self.click_element(house_detail['是否随时可签选择框'], sleep_time=0.5)
        check_out_right_now_list = self.find_elements(house_detail['下拉框'])
        for check_out_right_now_ele in check_out_right_now_list:
            if check_out_right_now_ele.text == check_out_right_now:
                check_out_right_now_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_has_school_places(self, has_school_places):  # 维护重点信息弹窗页选择学区名额
        self.click_element(house_detail['学区名额选择框'], sleep_time=0.5)
        has_school_places_list = self.find_elements(house_detail['下拉框'])
        for has_school_places_ele in has_school_places_list:
            if has_school_places_ele.text == has_school_places:
                has_school_places_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_decoration_state(self, decoration_state):  # 维护重点信息弹窗页选择装修情况
        self.click_element(house_detail['装修情况选择框'], sleep_time=0.5)
        decoration_state_list = self.find_elements(house_detail['下拉框'])
        for decoration_state_ele in decoration_state_list:
            if decoration_state_ele.text == decoration_state:
                decoration_state_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_house_property_limit(self, house_property_limit):  # 维护重点信息弹窗页选择产证年限
        self.click_element(house_detail['产证年限选择框'], sleep_time=0.5)
        house_property_limit_list = self.find_elements(house_detail['下拉框'])
        for house_property_limit_ele in house_property_limit_list:
            if house_property_limit_ele.text == house_property_limit:
                house_property_limit_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_choose_house_usage(self, house_usage):  # 维护重点信息弹窗页选择房屋用途
        self.click_element(house_detail['房屋用途选择框'], sleep_time=0.5)
        house_usage_list = self.find_elements(house_detail['下拉框'])
        for house_usage_ele in house_usage_list:
            if house_usage_ele.text == house_usage:
                house_usage_ele.click()
                return True
        raise ValueError('传值错误')

    def dialog_click_confirm_button(self):  # 弹窗确定按钮
        sleep(2)
        self.click_element(house_detail['弹窗_确定按钮'], sleep_time=3)

    def dialog_click_cancel_button(self):  # 弹窗取消按钮
        self.click_element(house_detail['弹窗_取消按钮'])

    def check_dialog_cancel_button_disabled(self):
        if self.get_element_attribute(house_detail['弹窗_取消按钮'], 'disabled') == 'true':
            return True
        else:
            return False

    def dialog_click_close_button(self):  # 弹窗关闭按钮
        self.click_element(house_detail['弹窗_关闭按钮'], 1)

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
        inspect_type = self.get_element_text(house_detail['右侧_常规看房时间标签']).split('：')[1].replace(' ', '')
        house_state = self.get_element_text(house_detail['右侧_房屋现状标签']).split('：')[1].replace(' ', '')
        is_unique = self.get_element_text(house_detail['右侧_是否唯一标签']).split('：')[1].replace(' ', '')
        pay_constraint = self.get_element_text(house_detail['右侧_付款要求标签']).split('：')[1].replace(' ', '')
        sale_reason = self.get_element_text(house_detail['右侧_售房原因标签']).split('：')[1].replace(' ', '')
        register_state = self.get_element_text(house_detail['右侧_户口情况标签']).split('：')[1].replace(' ', '')
        has_pledge = self.get_element_text(house_detail['右侧_抵押情况标签']).split('：')[1].replace(' ', '')
        check_out_right_now = self.get_element_text(house_detail['右侧_是否随时可签标签']).split('：')[1].replace(' ', '')
        has_school_places = self.get_element_text(house_detail['右侧_学区名额标签']).split('：')[1].replace(' ', '')
        decoration_state = self.get_element_text(house_detail['右侧_装修情况标签']).split('：')[1].replace(' ', '')
        house_property_limit = self.get_element_text(house_detail['右侧_产证年限标签']).split('：')[1].replace(' ', '')
        house_usage = self.get_element_text(house_detail['右侧_房屋用途标签']).split('：')[1].replace(' ', '')
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

    def get_account_name(self):
        """获取当前账号的名字"""
        account_name = self.get_element_text(house_detail['当前账号名字']).split(' ')[0]
        return account_name

    def get_house_num(self, house_code, flag):
        """获取当前维护人下的房源数量"""
        if flag == '买卖':
            self.click_element(house_detail['买卖区域筛选_不限'], 5)
            self.input_text(house_detail['房源编号输入框'], house_code)
        else:
            self.click_element(house_detail['租赁菜单'], 5)
            self.click_element(house_detail['买卖区域筛选_不限'])
            self.input_text(house_detail['房源编号输入框'], house_code)
        # self.click_element(house_detail['搜索按钮'], 15)
        num = self.get_element_text(house_detail['搜索结果总数'])[8:][:-1]
        return num

    def enter_house_detail(self):
        """进入房源详情页面"""
        self.click_element(house_detail['列表中的第一条房源'], 10)

    def get_house_info_in_detail_page(self, flag):
        """获取房源编号、房源面积等信息"""
        initial_price = ''
        if flag == 'sale':
            initial_price = self.get_element_text(house_detail['房源初始价格'])[:-1]
        elif flag == 'rent':
            initial_price = self.get_element_text(house_detail['房源初始价格']).split('元')[0]
        house_area = self.get_element_text(house_detail['房源面积']).split('m')[0]
        return initial_price, house_area

    def view_basic_information(self):
        """查看房源基础信息"""
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        sleep(1)
        self.click_element(house_detail['房源基础信息按钮'], 1)

    def verify_can_modify(self):
        """验证是否可以修改"""
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        sleep(1)
        self.move_mouse_to_element(house_detail['房源状态按钮'])
        # res = self.is_exists(house_detail['是否可修改状态提示'])
        sleep(1)
        return self.is_exists(house_detail['是否可修改状态提示'])

    def move_mouse_to_operation_item(self, item):
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        sleep(1)
        locator = "xpath", "li[contains(text(), '" + item + "')]"
        self.move_mouse_to_element(locator)

    def verify_view_success(self):
        """验证查看房源基础信息是否成功"""
        res = self.is_exists(house_detail['房源基础信息弹窗title'])
        return res

    def close_dialog(self):
        """关闭弹窗"""
        self.click_element(house_detail['基础信息弹窗_关闭按钮'], 1)

    def submit_modify_state_application(self):
        """提交修改房源状态申请"""
        self.click_element(house_detail['房源状态按钮'], 1)
        self.click_element(house_detail['暂缓出售选项'], 1)
        self.click_element(house_detail['房源状态弹窗确定按钮'], 2)

    def verify_submit_success(self):
        """验证提交申请是否成功"""
        text = self.get_element_text(house_detail['弹窗_提交成功提示'])
        self.click_element(house_detail['弹窗_确定按钮'], 2)
        return text

    def verify_get_application_success(self, house_no):
        """验证商圈经理收到修改房源状态申请"""
        self.click_element(house_detail['暂缓房源审核选项'])
        sleep(1)
        locator = 'xpath', "//div[@class='invalid-housing-resource']//td[@class='ant-table-cell']/a/span[text()='" + house_no + "']"
        res = self.is_exists(locator)
        return res

    def reject_application(self):
        self.click_element(house_detail['驳回按钮'])
        self.input_text(house_detail['驳回理由输入框'], '驳回')
        self.click_element(house_detail['驳回弹窗确定按钮'], 2)

    def verify_reject_application_sucess(self, house_no):
        """驳回申请并验证驳回成功"""
        locator = 'xpath', "//div[@class='invalid-housing-resource']//td[@class='ant-table-cell']/a/span[text()='" + house_no + "']"
        res = self.is_exists(locator)
        return res

    def get_initial_price_in_dialog(self):
        """获取调价弹窗页面的初始房源价格"""
        # self.move_mouse_to_operation_item('调整价格')
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        sleep(1)
        self.move_mouse_to_element(house_detail['调整价格选项'])
        sleep(1)
        self.click_element(house_detail['调整价格选项'])
        # initial_price_in_dialog = self.get_element_text(house_detail['调价弹窗的房源价格']).split('.')[0]  # 调整弹窗中的房源初始价格
        initial_price_in_dialog = self.get_element_text(house_detail['调价弹窗的房源价格'])[0:-2]  # 调整弹窗中的房源初始价格
        return initial_price_in_dialog

    def modify_house_price(self, initial_price):
        """修改房源价格"""
        expect_final_price = int(initial_price) + random.randint(1, 9)
        self.input_text(house_detail['房源价格输入框'], expect_final_price)
        self.click_element(house_detail['调价弹窗确定按钮'], 2)
        return str(expect_final_price)

    def get_modified_price_in_detail_page(self, flag, expect_final_price, house_area):
        """修改后获取详情页面的价格和单价"""
        actual_price_in_detail_page = ''
        if flag == 'sale':
            ele_text = self.get_element_text(house_detail['房源初始价格'])  # 获取详情页面修改后的价格
            actual_price_in_detail_page = ele_text[:-1]
            unit_price = int(expect_final_price) * 10000 / int(house_area)
            expect_final_unit_price = self.get_house_unit_price(unit_price, 2)  # 根据修改后的房源价格及房源面积计算单价
            actual_unit_price_in_detail_page = self.get_element_text(house_detail['房源初始单价'])  # 获取详情页面修改后的单价
            return actual_price_in_detail_page, expect_final_unit_price, actual_unit_price_in_detail_page
        elif flag == 'rent':
            actual_price_in_detail_page = self.get_element_text(house_detail['房源初始价格']).split('元')[0]
        else:
            logger.info('传值错误')
        return actual_price_in_detail_page

    def verify_record_list_update(self, init_price, expect_final_price, flag):
        """验证调价记录列表是否更新"""
        expect_text = ''
        self.click_element(house_detail['调价记录按钮'], 2)
        actual_text = self.get_element_text(house_detail['调价记录第一条价格']).strip()
        if flag == 'sale':
            expect_text = '{init_price}万元 - {final_price}万元'.format(init_price=init_price,
                                                                    final_price=expect_final_price)
        elif flag == 'rent':
            expect_text = '{init_price}元 - {final_price}元'.format(init_price=init_price, final_price=expect_final_price)
        else:
            logger.info('传值错误')
        self.click_element(house_detail['弹窗_关闭按钮'], 2)
        return actual_text, expect_text

    def modify_price_from_basic_information_page(self):
        """从基本信息修改房源价格"""
        self.move_mouse_to_element(house_detail['右侧菜单更多按钮'])
        sleep(1)
        self.click_element(house_detail['房源基础信息按钮'], 1)
        expect_final_price = int(self.get_element_attribute(house_detail['详情页面售价输入框'], 'value')) + random.randint(1, 9)
        self.clear_text(house_detail['详情页面售价输入框'])
        self.input_text(house_detail['详情页面售价输入框'], expect_final_price)
        sleep(1)
        self.click_element(house_detail['基础信息弹窗确定按钮'], 2)
        return str(expect_final_price)

    def verify_log_list_update(self, account_name):
        """验证操作日志是否更新"""
        self.move_mouse_to_element(house_detail['更多按钮'])
        self.click_element(house_detail['操作日志按钮'], 2)
        ele_list = self.find_elements(house_detail['操作人'])
        if len(ele_list) > 0:
            return self.is_exists(house_detail['调整价格操作'])
        else:
            return False

    def click_close_btn(self):
        """点击弹窗关闭按钮"""
        sleep(1)
        self.click_element(house_detail['弹窗_关闭按钮'])

    def replace_maintainer(self, maintainer_name):
        """更新房源维护人"""
        self.move_mouse_to_element(house_detail['更多按钮'])
        sleep(1)
        locator = 'xpath', "//div[contains(@class, 'ant-select-dropdown') and not(contains(@class, " \
                           "'ant-select-dropdown-hidden'))]//div[@class='rc-virtual-list']" \
                           "//div[contains(@class,'ant-select-item ant-select-item-option') and @title='" + maintainer_name + "']"

        self.click_element(house_detail['维护人管理按钮'], 2)
        self.click_element(house_detail['选择人员输入框'], 2)
        target = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去
        if len(maintainer_name) > 0:
            expect_maintainer_name = self.get_element_text(locator)
            self.click_element(locator)
        else:
            expect_maintainer_name = self.find_elements(house_detail['下拉框'])[0].text
            self.find_elements(house_detail['下拉框'])[0].click()
        self.click_element(house_detail['分配弹窗确定按钮'], 5)
        return expect_maintainer_name

    def get_current_maintainer(self):
        """获取角色卡片中的最新房源维护人"""
        self.scroll_to_bottom()
        sleep(3)
        str_list = self.get_element_text(house_detail['角色人名字']).split(' ')
        if len(str_list) > 1:
            current_maintainer_name = str_list[1]
        else:
            current_maintainer_name = str_list[0]
        # current_maintainer_phone = self.get_element_text(house_detail['角色人手机号']).split(':')[1]
        current_maintainer_phone = self.get_element_text(house_detail['角色人手机号'])
        return current_maintainer_name, current_maintainer_phone

    def verify_can_report(self):
        """验证是否可以举报"""
        self.move_mouse_to_element(house_detail['更多按钮'])
        sleep(1)
        self.move_mouse_to_element(house_detail['房源举报按钮'])
        sleep(1)
        res = self.is_exists(house_detail['是否可举报提示'])
        sleep(0.5)
        return res

    def report_house(self):
        """举报房源"""
        self.click_element(house_detail['房源举报按钮'], 1)
        self.click_element(house_detail['房源不卖选项'], 1)
        self.click_element(house_detail['举报房源弹窗确认按钮'], 2)
        text = self.find_element(house_detail['右上角弹窗_内容']).text
        return text

    def verify_report_list_update(self, house_no):
        """验证平台品管收到房源举报"""
        locator = 'xpath', "//div[@class='invalid-housing-resource']//td[@class='ant-table-cell']/a/span[text()='" + house_no + "']"
        res = self.is_exists(locator)
        return res

    def reject_report(self):
        """驳回房源举报"""
        self.click_element(house_detail['驳回按钮'], 1)
        self.input_text(house_detail['驳回理由输入框'], '驳回')
        sleep(1)
        self.click_element(house_detail['驳回弹窗确定按钮'], 2)

    def verify_reject_report_success(self, house_no):
        """验证驳回成功"""
        locator = 'xpath', "//div[@class='invalid-housing-resource']//td[@class='ant-table-cell']/a/span[text()='" + house_no + "']"
        res = self.is_exists(locator)
        return res

    # 新房详情页
    def click_see_more(self):
        """新房详情查看更多"""
        self.click_element(house_detail['查看更多按钮'], 3)

    def go_upload_album(self):
        """进入楼盘相册上传页面"""
        self.click_element(house_detail['上传图片按钮'], 3)

    def switch_lab_by_name(self, lab_name):
        """上传图片弹窗根据名字切换lab"""
        locator = 'xpath', "//div[@class='ant-modal-wrap uploadModal']//span[text()='" + lab_name + "']"
        self.click_element(locator)

    def upload_image(self, pictures_path, lab_name):
        """楼盘相册-上传图片"""
        self.switch_lab_by_name(lab_name)
        sleep(2)
        for picture_path in pictures_path:
            if lab_name == '效果图':
                self.send_key(house_detail['首图input'], picture_path)
                sleep(1.5)
            else:
                self.send_key(house_detail['其他图片input'], picture_path)
                sleep(1.5)

    def click_upload_btn(self):
        """确定上传"""
        self.click_element(house_detail['弹窗_上传按钮'], 2)

    def get_dialog_text(self):
        """获取右上角弹窗提示信息"""
        text = self.get_element_text(house_detail['右上角弹窗_内容'])
        return text

    def click_batch_delete_btn(self):
        """点击批量删除按钮"""
        self.click_element(house_detail['批量删除按钮'], 2)

    def select_some_image_to_delete(self):
        """选取要删除的照片,默认选择第一张"""
        self.click_element(house_detail['弹窗_选中图片按钮'], 1)

    def select_all_image_to_delete(self):
        """选取所有照片"""
        label_list = self.find_elements(house_detail['删除弹窗_label'])
        for ele in label_list:
            sleep(1)
            ele.click()
            sleep(1)
            self.click_select_all_btn()

    def click_select_all_btn(self):
        """点击全选按钮"""
        self.click_element(house_detail['弹窗_全选按钮'], 1)

    def get_deleted_image_number(self):
        """获取删除图片数量"""
        text = self.get_element_text(house_detail['弹窗_删除按钮'])
        number = int(re.findall(r'[(](.*?)[)]', text)[0])
        # print('get_deleted_image_number', number)
        return number

    def click_delete_btn(self):
        """点击删除按钮"""
        sleep(1)
        self.click_element(house_detail['弹窗_删除按钮'], 2)

    def get_image_list_lenth(self):
        """获取相册列表中的图片数量"""
        ele_list = self.find_elements(house_detail['相册列表_图片'])
        return len(ele_list)

    def switch_tab_by_name(self, tab_name):
        """新房详情页根据tab名字切换tab"""
        locator = 'xpath', "//div[@class='ant-row ant-tabs-nav-list']/div[text()='" + tab_name + "']"
        self.click_element(locator, 1)

    def relese_house_trend_content(self, trend_title, trend_explain):
        """发布楼盘动态内容"""
        self.click_element(house_detail['发布动态按钮'])
        self.input_text(house_detail['动态标题输入框'], trend_title, True)
        self.input_text(house_detail['动态说明输入框'], trend_explain, True)
        self.click_element(house_detail['动态弹窗_确定按钮'], 1)
        return trend_explain

    def verify_trend_list_update(self, trend_explain):
        """验证动态列表是否更新"""
        locator = 'xpath', "//div[@class ='statetimeBox']/div[@class='stateNote' and text()='" + trend_explain + "']"
        res = self.is_exists(locator)
        return res

    def edit_house_selling_point(self, push_plate, detailed_description):
        """编辑楼盘卖点"""
        self.click_element(house_detail['编辑卖点按钮'])
        self.input_text(house_detail['一句话推盘输入框'], push_plate, True)
        self.input_text(house_detail['详细描述输入框'], detailed_description, True)
        self.click_element(house_detail['保存按钮'], 1)
        return push_plate

    def verify_celling_point_list_update(self):
        """验证卖点列表是否更新"""
        actual_result = self.get_element_text(house_detail['卖点列表_推盘'])
        return actual_result

    def click_share_btn(self):
        """点击分享按钮"""
        self.click_element(house_detail['分享按钮'], 3)

    def get_information_in_share_page(self):
        """获取分享页面的信息"""
        sleep(2)
        house_type = self.get_element_text(house_detail['分享弹窗_户型'])
        account_name = self.get_element_text(house_detail['分享弹窗_登录人账号'])
        account_phone = self.get_element_text(house_detail['分享弹窗_登录人手机号'])
        return house_type, account_name, account_phone

    def click_upload_house_type_btn(self):
        """点击上传户型介绍按钮"""
        self.click_element(house_detail['上传户型介绍按钮'], 1)

    def house_type_introduce_content(self, house_type_name, house_area, house_direction, pictures_path):
        """户型介绍内容"""
        self.input_text(house_detail['户型名称输入框'], house_type_name)
        self.click_element(house_detail['户型_室输入框'])
        self.find_elements(house_detail['户型下拉框'])[0].click()
        self.click_element(house_detail['户型_厅输入框'])
        self.find_elements(house_detail['户型下拉框'])[1].click()
        self.click_element(house_detail['户型_卫输入框'])
        self.find_elements(house_detail['户型下拉框'])[2].click()
        self.click_element(house_detail['户型_厨输入框'])
        self.find_elements(house_detail['户型下拉框'])[3].click()
        self.input_text(house_detail['面积输入框'], house_area)
        self.input_text(house_detail['户型朝向输入框'], house_direction)
        self.click_element(house_detail['户型价格待定选项'])
        self.send_key(house_detail['户型图片input'], pictures_path)
        sleep(2)
        self.click_element(house_detail['弹窗_确定按钮'], 1)

    def get_house_type_introduce_number(self):
        """获取户型介绍数量"""
        text = self.get_element_text(house_detail['户型介绍数量'])
        number = int(re.findall(r'[(](.*?)[)]', text)[0][1:-1])
        return number

    def get_house_type_in_detail_page(self):
        """获取详情页面的户型"""
        ele_list = self.find_elements(house_detail['详情页户型'])
        if len(ele_list) == 0:
            text = '0室0厅0卫0厨'
        else:
            text = ele_list[0].text.split(' ')[0]
        return text

    def choose_image_in_share_page(self):
        """分享页面选择图片"""
        self.click_element(house_detail['分享弹窗_效果图'])

    def click_generate_code_btn(self):
        """点击生成二维码按钮"""
        self.click_element(house_detail['生成海报二维码按钮'], 12)

    def verify_generate_code_success(self):
        """验证生成二维码成功"""
        sleep(4)
        res = self.is_exists(house_detail['海报二维码弹窗'])
        return res

    # 资料盘
    def click_transfer_to_rent_btn(self):
        """点击转出租验证"""
        self.click_element(house_detail['转出租验真按钮'])

    def click_transfer_to_sale_btn(self):
        """点击转在售验证"""
        self.click_element(house_detail['转在售验真按钮'])

    def transfer_house(self, verify_code):
        """房源转真"""
        self.click_element(house_detail['发送短信验证码按钮'])
        self.input_text(house_detail['验证码输入框'], verify_code)
        self.click_element(house_detail['提交按钮'])
        self.click_element(house_detail['知道了按钮'])

    @staticmethod
    def get_house_unit_price(float_a, n):
        """根据四舍五入保留2位小数的原则计算房源单价"""
        string_a = str(float_a)
        a, b, c = string_a.partition('.')  # 此时的a、b和c的类型均为字符串类型
        if len(c) > 2:
            cc = c[:n]
            if int(c[n]) >= 5:
                ccc = int(cc) + 1
            else:
                ccc = int(cc)
            return a + b + str(ccc)
        else:
            c2 = int(c)
            if len(c) == 1 and c2 == 0:
                return a
            else:
                return a + b + c

    @staticmethod
    def get_house_unit_price2(float_a, n):
        """根据四舍五入保留2位小数的原则计算房源单价"""
        string_a = str(float_a)
        integer, decimal_point, decimal = string_a.partition('.')  # 此时的integer、decimal_point和decimal的类型均为字符串类型
        if len(decimal) > 2:
            cc = decimal[:n]  # 前二位小数
            if int(decimal[n]) >= 5:  # 四舍五入
                cc = int(cc) + 1
            else:
                cc = int(cc)
            return integer + decimal_point + str(cc)
        else:
            c2 = int(decimal)
            if len(decimal) == 1 and c2 == 0:
                return integer
            else:
                return integer + decimal_point + decimal


