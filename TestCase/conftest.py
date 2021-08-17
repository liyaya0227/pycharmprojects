#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: conftest.py
@time: 2021/08/10
"""
import allure
import pytest
from common.readconfig import ini
from page_object.login.loginpage import LoginPage
from page_object.main.topviewpage import MainTopViewPage


@pytest.fixture(scope='function', autouse=False)
@allure.story("苏州-管理员登录")
def sz_login_admin(request, drivers):
    driver = drivers
    name = ini.user_account
    pwd = ini.user_password
    # name, pwd = ini.user_account_by_role('ADMIN')
    login_page = LoginPage(driver)
    login_page.log_in(name, pwd)
    main_topview = MainTopViewPage(driver)
    main_topview.wait_page_loading_complete()
    main_topview.click_close_button()

    def logout():
        login_page.log_out()

    request.addfinalizer(logout)
    return driver



