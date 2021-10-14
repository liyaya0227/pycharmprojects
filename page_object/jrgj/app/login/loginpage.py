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
        self.input_text(login['账号输入框'], account)

    def input_password(self, password):
        self.input_text(login['密码输入框'], password)

    def click_login_button(self):
        self.is_click(login['登录按钮'])

    def choose_read(self):
        self.is_click(login['协议已阅读勾选'])

    def log_in(self, account, password):
        self.input_account(account)
        self.input_password(password)
        self.choose_read()
        self.click_login_button()

    def check_login_page(self):
        if self.find_element(login['标题'], wait_time=5):
            return True
        else:
            return False

    def check_agreement_dialog(self):
        if self.find_element(login['协议弹窗'], wait_time=5):
            return True
        else:
            return False

    def dialog_click_agree_button(self):
        self.is_click(login['弹窗_同意按钮'])

