#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: loginpage.py
@date: 2021/10/15 0015
"""
from page.webpage import WebPage
from common.readelement import Element

login = Element('jrjob/login/login')


class LoginPage(WebPage):

    def input_account(self, account):
        """输入账号"""
        self.input_text(login['账号输入框'], account)

    def input_password(self, password):
        """输入账号"""
        self.input_text(login['密码输入框'], password)

    def click_login_button(self):
        """点击登录按钮"""
        self.click_element(login['登录按钮'], sleep_time=2)
