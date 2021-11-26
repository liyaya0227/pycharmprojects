#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: previewpage.py
@date: 2021/7/7 0007
"""
from page.webpage import WebPage
from common.readelement import Element
from utils.uploadfile import upload_file

preview = Element('jrgj/web/contract/preview')


class ContractPreviewPage(WebPage):

    def click_pass_button(self):
        self.click_element(preview['通过按钮'], sleep_time=2)

    def reject_examine_by_reason(self, reason):
        self.click_element(preview['驳回按钮'])
        self.input_text_into_element(preview['审核驳回弹窗_原因输入框'], reason)
        self.dialog_click_confirm_button()

    def click_reject_button(self):
        """点击驳回按钮"""
        self.click_element(preview['驳回按钮'])

    def reject_dialog_input_reason(self, reason):
        """驳回原因弹窗，输入原因"""
        self.input_text_into_element(preview['审核驳回弹窗_原因输入框'], reason)

    def reject_dialog_upload_picture(self, picture):
        """驳回原因弹窗，上传图片"""
        self.input_text_into_element(preview['审核驳回弹窗_上传图片输入框'], picture)

    def reject_dialog_upload_picture_by_windows(self, picture):
        """驳回原因弹窗，上传图片"""
        self.click_element(preview['审核驳回弹窗_上传图片按钮'])
        upload_file(picture)

    def click_update_button(self):
        self.click_element(preview['修改按钮'])

    def click_invalid_button(self):
        self.click_element(preview['无效按钮'])

    def click_print_without_sign_button(self):
        self.click_element(preview['无章打印按钮'], sleep_time=1)

    def click_print_with_sign_button(self):
        self.click_element(preview['有章打印按钮'], sleep_time=4)

    def click_signature_button(self):
        self.click_element(preview['签章按钮'], sleep_time=3)

    def cancel_print(self):
        self.browser_refresh()

    def dialog_click_confirm_button(self):  # 弹窗，点击确定按钮
        self.click_element(preview['弹窗_确定按钮'])

    def dialog_click_cancel_button(self):  # 弹窗，点击取消按钮
        self.click_element(preview['弹窗_取消按钮'])
