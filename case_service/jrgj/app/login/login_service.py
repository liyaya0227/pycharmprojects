#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: login_service.py
@date: 2021/11/12 0012
"""
from utils.timeutil import sleep
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.mine.minepage import AppMinePage


class LoginService(object):

    def __init__(self, android_driver):
        self.__login = AppLoginPage(android_driver)
        self.__main = AppMainPage(android_driver)
        self.__mine = AppMinePage(android_driver)

    def login_app(self, user_account, user_password):
        """登录App"""
        sleep(6)
        if not self.__login.check_login_page():
            self.__main.close_top_view()
            self.__main.click_mine_button()
            self.__mine.log_out()
        self.__login.log_in(user_account, user_password)
        self.__main.close_top_view()

    def back_login_page(self):
        """回到登录界面"""
        sleep(6)
        if not self.__login.check_login_page():
            self.__main.close_top_view()
            self.__main.click_mine_button()
            self.__mine.log_out()
