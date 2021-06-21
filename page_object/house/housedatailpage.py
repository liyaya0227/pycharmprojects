# -*- coding:utf-8 -*-
from page.webpage import WebPage
from common.readelement import Element

house_detail = Element('house/housedetail')


class HouseDetailPage(WebPage):

    def click_exploration_button(self):
        self.is_click(house_detail['预约实勘按钮'])

    def choose_normal_exploration(self):
        self.is_click(house_detail['选择实勘方式_普通实勘单选'])

    def choose_vr_exploration(self):
        self.is_click(house_detail['选择实勘方式_VR实勘单选'])

    def choose_photographer(self, photographer):
        self.is_click(house_detail['摄影师输入框'])
        photographer_list = self.find_elements(house_detail['摄影师下拉框'])
        for photographer_ele in photographer_list:
            if photographer_ele.text == photographer:
                photographer_ele.click()
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

    def expand_certificates_info(self):
        ele = self.find_element(house_detail['证件信息展开收起按钮'])
        if ele.text == '展开':
            ele.click()

    def retract_certificates_info(self):
        ele = self.find_element(house_detail['证件信息展开收起按钮'])
        if ele.text == '收起':
            ele.click()

    def click_written_entrustment_agreement_upload_button(self):
        self.__click_upload_button('书面委托协议')

    def click_key_entrustment_certificate_upload_button(self):
        self.__click_upload_button('钥匙委托凭证')

    def click_vip_service_entrustment_agreement_upload_button(self):
        self.__click_upload_button('VIP服务委托协议')

    def click_deed_tax_invoice_upload_button(self):
        self.__click_upload_button('契税票')

    def click_proof_of_identity_upload_button(self):
        self.__click_upload_button('身份证明')

    def click_original_purchase_contract_upload_button(self):
        self.__click_upload_button('原始购房合同')

    def click_property_ownership_certificate_upload_button(self):
        self.__click_upload_button('房产证')

    def __click_upload_button(self, certificate_name):
        locator = 'xpath', "//span[text()='" + certificate_name + "']/ancestor::ul[@class='upTop']//span[@class='blue' and text()='上传']"
        self.is_click(locator)

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
