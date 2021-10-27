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

detail = Element('jrgj/web/contract/detail')


class ContractDetailPage(WebPage):

    def click_contract_detail_tab(self):
        self.is_click(detail['合同详情标签'])

    def click_achievement_detail_tab(self):
        self.is_click(detail['业绩详情标签'])

    def click_finance_detail_tab(self):
        self.is_click(detail['财务详情标签'])

    def click_preview_button(self):
        self.is_click(detail['预览按钮'])

    def check_cancel_button_exist(self):
        return self.element_is_exist(detail['解约按钮'], wait_time=2)

    def click_cancel_button(self):
        self.is_click(detail['解约按钮'])

    def check_change_button_exist(self):
        return self.element_is_exist(detail['变更按钮'], wait_time=2)

    def click_change_button(self):
        self.is_click(detail['变更按钮'])

    def click_go_examine_button(self):
        self.is_click(detail['去提审按钮'], sleep_time=2)

    def get_contract_price(self):  # 获取合同价格
        return self.element_text(detail['合同价格标签'])[:-1]

    def get_last_seal_time(self):  # 获取最新一次盖章时间
        return self.element_text(detail['最新一次盖章时间标签'])

    def get_sign_time(self):  # 获取签约时间
        return self.element_text(detail['签约时间标签'])

    def get_create_time(self):  # 获取创建时间
        return self.element_text(detail['创建时间标签'])

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
        self.is_click(detail['主体合同标签'], sleep_time=1)

    def upload_two_sign_contract(self):
        sleep()
        self.is_click(detail['上传双方签字合同按钮'])
        self.is_click(detail['选择签约时间输入框'])
        time = dt_strftime('%Y-%m-%d %H:%M:%S')
        sleep()
        self.input_text_with_enter(detail['选择签约时间输入框'], time)
        self.dialog_click_confirm_button()

    def upload_pictures(self, pictures_path):
        for picture_path in pictures_path:
            self.input_text(detail['上传图片输入框'], picture_path)
            # self.is_click(detail['上传图片按钮'])
            # upload_file(picture_path)
            sleep(2)

    def click_submit_button(self):
        self.is_click(detail['提交按钮'], sleep_time=2)

    def click_attachment_info(self):
        self.is_click(detail['备件信息标签'])

    def upload_lessor_identification(self, pictures_path):
        for picture_path in pictures_path:
            # self.is_click(detail['出租方_身份证明_上传图片按钮'])
            # upload_file(picture_path)
            self.input_text(detail['出租方_身份证明_上传图片输入框'], picture_path)
            sleep()

    def upload_lessor_house_identification(self, pictures_path):
        for picture_path in pictures_path:
            # self.is_click(detail['出租方_房屋所有权证_上传图片按钮'])
            # upload_file(picture_path)
            self.input_text(detail['出租方_房屋所有权证_上传图片输入框'], picture_path)
            sleep()

    def upload_tenantry_identification(self, pictures_path):
        for picture_path in pictures_path:
            # self.is_click(detail['承租方_身份证明_上传图片按钮'])
            # upload_file(picture_path)
            self.input_text(detail['承租方_身份证明_上传图片输入框'], picture_path)
            sleep()

    def upload_other_attachment(self, pictures_path):
        for picture_path in pictures_path:
            # self.is_click(detail['其他备件_其他备件_上传图片按钮'])
            # upload_file(picture_path)
            self.input_text(detail['其他备件_其他备件_上传图片输入框'], picture_path)
            sleep()

    def upload_other_registration_form(self, pictures_path):
        for picture_path in pictures_path:
            # self.is_click(detail['其他备件_委托登记表_上传图片按钮'])
            # upload_file(picture_path)
            self.input_text(detail['其他备件_委托登记表_上传图片输入框'], picture_path)
            sleep()

    def upload_other_delivery_note(self, pictures_path):
        for picture_path in pictures_path:
            # self.is_click(detail['其他备件_物业交割单_上传图片按钮'])
            # upload_file(picture_path)
            self.input_text(detail['其他备件_物业交割单_上传图片输入框'], picture_path)
            sleep()

    def click_submit_examine_button(self):
        self.is_click(detail['提交审核按钮'], sleep_time=2)

    def check_dialog_exist(self):
        return self.element_is_exist(detail['弹窗_页面'])

    def click_report_achievement_button(self):
        self.is_click(detail['报业绩按钮'], sleep_time=1)

    def dialog_click_confirm_button(self):
        self.is_click(detail['弹窗_确定按钮'], sleep_time=1)

    def dialog_click_close_button(self):
        self.is_click(detail['弹窗_关闭按钮'])

    def get_contract_info(self):
        contract_info = {'create_time': self.element_text(detail['创建时间标签']),
                         'sign_time': self.element_text(detail['签约时间标签'])}
        return contract_info

    def cancel_change_dialog_input_reason(self, reason):  # 解约变更弹窗，输入解约原因
        self.input_text(detail['弹窗_解约变更_原因'], reason)

    def cancel_change_dialog_upload_picture(self, picture_list):  # 解约变更弹窗，上传图片
        for picture in picture_list:
            self.input_text(detail['弹窗_解约变更_上传图片输入框'], picture)
            sleep()
