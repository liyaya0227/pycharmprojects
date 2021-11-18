#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: loginpage.py
@time: 2021/06/24
"""

from page.androidpage import AndroidPage
from common.readelement import Element

login = Element('jrgj/app/login/login')


class AppLoginPage(AndroidPage):

    def input_account(self, account):
        self.input_text_into_element(login['账号输入框'], account)

    def input_password(self, password):
        self.input_text_into_element(login['密码输入框'], password)

    def click_login_button(self):
        self.click_element(login['登录按钮'])

    def choose_read(self):
        self.click_element(login['协议已阅读勾选'])

    def log_in(self, account, password):
        self.input_account(account)
        self.input_password(password)
        self.choose_read()
        self.click_login_button()

    def check_login_page(self):
        return self.check_element_is_exist(login['标题'], timeout=5)

    def check_is_logged_in(self):
        return self.is_exists(login['标题'])

    def check_agreement_dialog(self):
        return self.check_element_is_exist(login['协议弹窗'], timeout=5)

    def dialog_click_agree_button(self):
        self.click_element(login['弹窗_同意按钮'])
