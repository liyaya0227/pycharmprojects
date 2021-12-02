#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: conftest.py
@time: 2021/10/14
"""
import pytest
from config.conf import cm
from selenium import webdriver
from appium import webdriver as androiddriver
from common.readconfig import ini
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from case_service.jrgj.app.login.login_service import LoginService as AppLoginService
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage as GjMainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage as GjMainTopViewPage


app_driver = None
web_driver = None
gl_gj_web_driver = None


@pytest.fixture(scope='session', autouse=False)
def xf_web_driver():
    global web_driver
    if web_driver is None:
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": cm.tmp_dir,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'load-extension'])
        web_driver = webdriver.Chrome(options=chrome_options)
        web_driver.maximize_window()
        web_driver.get(ini.xf_url)
        login_page = LoginPage(web_driver)
        login_page.log_in(ini.user_account, ini.user_password)
    yield web_driver
    main_left_view = MainLeftViewPage(web_driver)
    main_left_view.log_out()
    web_driver.quit()


@pytest.fixture(scope='session', autouse=False)
def xf_android_driver():
    """mumu"""
    desired_caps = {
        'automationName': 'appium',  # 自动化引擎，默认appium
        'platformName': 'Android',  # 操作系统
        'platformVersion': '6.0.1',  # 操作系统版本
        'deviceName': '127.0.0.1:7555',  # MUMU
        # 'platformVersion': '7.1.2',  # 操作系统版本
        # 'deviceName': '127.0.0.1:62001',  # 夜神
        # 'platformVersion': '11',  # 操作系统版本
        # 'deviceName': '192.168.101.192',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
        'noReset': True,  # 应用状态是否需要重置，默认true
        'fullReset': False,  # 执行完测试后是否卸载app，默认false
        'appPackage': ini.xf_app_package,  # 应用的包名
        'appActivity': ini.xf_app_package + '.MainActivity',  # 应用的第一个启动Activity
        'newCommandTimeout': 60 * 60 * 60,  # 命令超时时间，单位：秒；超时自动结束会话
        'unicodeKeyboard': True,  # 使用unicode编码方式发送字符串；输入中文需要
        'resetKeyboard': True  # 将键盘隐藏起来，默认true；输入中文需要
    }
    driver = androiddriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 连接Appium
    login_service = AppLoginService(driver)
    login_service.back_login_page()
    yield driver
    driver.quit()


# @pytest.fixture(scope='session', autouse=True)
# def setup_and_teardown(xf_web_driver):
#     login_page = LoginPage(xf_web_driver)
#     login_page.log_in(ini.user_account, ini.user_password)
#     yield
#     main_left_view = MainLeftViewPage(web_driver)
#     main_left_view.log_out()


@pytest.fixture(scope='session', autouse=False)
def gj_web_driver():
    global gl_gj_web_driver
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": cm.tmp_dir,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'load-extension'])
    gl_gj_web_driver = webdriver.Chrome(options=chrome_options)
    gl_gj_web_driver.maximize_window()
    gl_gj_web_driver.get(ini.url)
    login_page = LoginPage(gl_gj_web_driver)
    login_page.log_in(ini.user_account, ini.user_password)
    main_top_view = GjMainTopViewPage(gl_gj_web_driver)
    main_top_view.wait_page_loading_complete()
    main_top_view.click_close_button()
    yield gl_gj_web_driver
    main_left_view = GjMainLeftViewPage(gl_gj_web_driver)
    main_left_view.log_out()
    gl_gj_web_driver.quit()

