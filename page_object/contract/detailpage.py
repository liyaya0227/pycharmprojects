#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/7/6 0006
"""

from utils.timeutil import dt_strftime
from utils.timeutil import sleep
from utils.uploadfile import upload_file
from page.webpage import WebPage
from common.readelement import Element
from selenium.common.exceptions import TimeoutException

detail = Element('contract/detail')


class ContractDetailPage(WebPage):

    def click_contract_detail_tab(self):
        self.is_click(detail['合同详情标签'])

    def click_achievement_detail_tab(self):
        self.is_click(detail['业绩详情标签'])

    def click_preview_button(self):
        self.is_click(detail['预览按钮'])

    def click_go_examine_button(self):
        self.is_click(detail['去提审按钮'])
        sleep(2)

    def create_contract_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_创建合同图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def submit_examine_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_提交签前审核图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def pass_examine_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_签前审核通过图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def pass_attachment_examine_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_备件审核通过图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def last_sign_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_最新一次盖章图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def last_sign_print_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_最新一次有章打印图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def sign_time_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_签约时间图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def upload_contract_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_上传主体合同图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def transfer_house_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_过户完成图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def trade_complete_icon_is_light(self):
        value = self.get_element_attribute(detail['流程_交易完结图标'], 'class')
        if 'ant-steps-item-process' in value or 'ant-steps-item-finish' in value:
            return True
        else:
            return False

    def click_subject_contract(self):
        self.is_click(detail['主体合同标签'])

    def upload_two_sign_contract(self):
        self.is_click(detail['上传双方签字合同按钮'])
        self.is_click(detail['选择签约时间输入框'])
        time = dt_strftime('%Y-%m-%d %H:%M:%S')
        sleep()
        self.input_text_with_enter(detail['选择签约时间输入框'], time)
        self.click_confirm_button()
        sleep()

    def upload_pictures(self, pictures_path):
        for picture_path in pictures_path:
            self.is_click(detail['上传图片按钮'])
            upload_file(picture_path)
            sleep(2)

    def click_submit_button(self):
        self.is_click(detail['提交按钮'])
        sleep(2)

    def click_attachment_info(self):
        self.is_click(detail['备件信息标签'])

    def upload_lessor_identification(self, pictures_path):
        for picture_path in pictures_path:
            self.is_click(detail['出租方_身份证明_上传图片按钮'])
            upload_file(picture_path)
            sleep()

    def upload_lessor_house_identification(self, pictures_path):
        for picture_path in pictures_path:
            self.is_click(detail['出租方_房屋所有权证_上传图片按钮'])
            upload_file(picture_path)
            sleep()

    def upload_tenantry_identification(self, pictures_path):
        for picture_path in pictures_path:
            self.is_click(detail['承租方_身份证明_上传图片按钮'])
            upload_file(picture_path)
            sleep()

    def upload_other_attachment(self, pictures_path):
        for picture_path in pictures_path:
            self.is_click(detail['其他备件_其他备件_上传图片按钮'])
            upload_file(picture_path)
            sleep()

    def upload_other_registration_form(self, pictures_path):
        for picture_path in pictures_path:
            self.is_click(detail['其他备件_委托登记表_上传图片按钮'])
            upload_file(picture_path)
            sleep()

    def upload_other_delivery_note(self, pictures_path):
        for picture_path in pictures_path:
            self.is_click(detail['其他备件_物业交割单_上传图片按钮'])
            upload_file(picture_path)
            sleep()

    def click_submit_examine_button(self):
        self.is_click(detail['提交审核按钮'])
        sleep(2)

    def check_dialog_exist(self):
        try:
            self.find_element(detail['弹窗_页面'])
            return True
        except TimeoutException:
            return False

    def click_report_achievement_button(self):
        self.is_click(detail['报业绩按钮'])
        sleep()

    def click_confirm_button(self):
        self.is_click(detail['弹窗_确定按钮'])
        sleep()

    def click_close_button(self):
        self.is_click(detail['弹窗_关闭按钮'])

    def get_contract_info(self):
        contract_info = {'create_time': self.element_text(detail['创建时间标签']),
                         'sign_time': self.element_text(detail['签约时间标签'])}
        return contract_info
