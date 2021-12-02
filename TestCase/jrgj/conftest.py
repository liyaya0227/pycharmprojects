#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: conftest.py
@time: 2021/06/22
"""
import pytest
from config.conf import cm
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage as XfMainLeftViewPage
from utils.logger import logger
from common.readconfig import ini
from selenium import webdriver
from appium import webdriver as androiddriver
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from case_service.jrgj.app.login.login_service import LoginService as AppLoginService


@pytest.fixture(scope='session', autouse=False)
def web_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": cm.tmp_dir,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    # chrome_options.add_argument('--headless')  # 无头启动，无窗口加载
    # chrome_options.add_argument('--disable-gpu')  # 不开启gpu加速
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'load-extension'])
    wdriver = webdriver.Chrome(options=chrome_options)
    # wdriver = webdriver.Chrome(executable_path="D:/Program Files/Python/chromedriver", options=chrome_options)
    # web_driver = webdriver.Firefox(firefox_binary='C:/Program Files/Mozilla Firefox/firefox.exe')
    wdriver.maximize_window()
    wdriver.get(ini.url)
    logger.info("初始化driver")
    login_page = LoginPage(wdriver)
    login_page.log_in(ini.user_account, ini.user_password)
    main_topview = MainTopViewPage(wdriver)
    main_topview.wait_page_loading_complete()
    main_topview.click_close_button()
    yield wdriver
    main_leftview = MainLeftViewPage(wdriver)
    main_leftview.log_out()
    wdriver.quit()


@pytest.fixture(scope='session', autouse=False)
def android_driver():
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
        'appPackage': ini.app_package,  # 应用的包名
        'appActivity': ini.app_package + '.MainActivity',  # 应用的第一个启动Activity
        'newCommandTimeout': 60 * 60 * 60,  # 命令超时时间，单位：秒；超时自动结束会话
        'unicodeKeyboard': True,  # 使用unicode编码方式发送字符串；输入中文需要
        'resetKeyboard': True  # 将键盘隐藏起来，默认true；输入中文需要
    }
    driver = androiddriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 连接Appium
    login_service = AppLoginService(driver)
    login_service.back_login_page()
    yield driver
    driver.quit()


# @pytest.fixture(scope='session', autouse=False)
# def android_driver():
#     """oppo"""
#     desired_caps = {
#         'automationName': 'appium',  # 自动化引擎，默认appium
#         'platformName': 'Android',  # 操作系统
#         # 'platformVersion': '6.0.1',  # 操作系统版本
#         # 'deviceName': '127.0.0.1:7555',  # MUMU
#         # 'platformVersion': '5.1.1',  # 操作系统版本
#         # 'deviceName': '127.0.0.1:62001',  # 夜神
#         'platformVersion': '11',  # 操作系统版本
#         'deviceName': '192.168.101.192',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
#         'noReset': True,  # 应用状态是否需要重置，默认true
#         'fullReset': False,  # 执行完测试后是否卸载app，默认false
#         'appPackage': ini.app_package,  # 应用的包名
#         'appActivity': ini.app_package + '.MainActivity',  # 应用的第一个启动Activity
#         'newCommandTimeout': 60 * 60 * 60,  # 命令超时时间，单位：秒；超时自动结束会话
#         'unicodeKeyboard': True,  # 使用unicode编码方式发送字符串；输入中文需要
#         'resetKeyboard': True  # 将键盘隐藏起来，默认true；输入中文需要
#     }
#     adriver = androiddriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 连接Appium
#     login_service = AppLoginService(adriver)
#     login_service.back_login_page()
#     yield adriver
#     adriver.quit()


@pytest.fixture(scope='session', autouse=False)
def android_driver2():
    """nox"""
    desired_caps = {
        'automationName': 'appium',  # 自动化引擎，默认appium
        'platformName': 'Android',  # 操作系统
        # 'platformVersion': '6.0.1',  # 操作系统版本
        # 'deviceName': '127.0.0.1:7555',  # MUMU
        'platformVersion': '7.1.2',  # 操作系统版本
        'deviceName': '127.0.0.1:62001',  # 夜神
        # 'platformVersion': '7.1.2',  # 操作系统版本
        # 'deviceName': '721QEDRE2H7DT',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
        'noReset': True,  # 应用状态是否需要重置，默认true
        'fullReset': False,  # 执行完测试后是否卸载app，默认false
        'appPackage': ini.app_package,  # 应用的包名
        'appActivity': ini.app_package + '.MainActivity',  # 应用的第一个启动Activity
        'newCommandTimeout': 60 * 60 * 60,  # 命令超时时间，单位：秒；超时自动结束会话
        'unicodeKeyboard': True,  # 使用unicode编码方式发送字符串；输入中文需要
        'resetKeyboard': True  # 将键盘隐藏起来，默认true；输入中文需要
    }
    second_adriver = androiddriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 连接Appium
    login_service = AppLoginService(second_adriver)
    login_service.back_login_page()
    yield second_adriver
    second_adriver.quit()


@pytest.fixture(scope='session', autouse=False)
def xf_web_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": cm.tmp_dir,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'load-extension'])
    gl_xf_web_driver = webdriver.Chrome(options=chrome_options)
    gl_xf_web_driver.maximize_window()
    gl_xf_web_driver.get(ini.xf_url)
    login_page = LoginPage(gl_xf_web_driver)
    login_page.log_in(ini.user_account, ini.user_password)
    yield gl_xf_web_driver
    main_left_view = XfMainLeftViewPage(gl_xf_web_driver)
    main_left_view.log_out()
    gl_xf_web_driver.quit()

# @pytest.fixture(scope='session', autouse=False)
# def android_driver2():
#     """nox"""
#     desired_caps = {
#         'automationName': 'appium',  # 自动化引擎，默认appium
#         'platformName': 'Android',  # 操作系统
#         # 'platformVersion': '6.0.1',  # 操作系统版本
#         # 'deviceName': '127.0.0.1:7555',  # MUMU
#         'platformVersion': '7.1.2',  # 操作系统版本
#         'deviceName': '127.0.0.1:62001',  # 夜神
#         # 'platformVersion': '7.1.2',  # 操作系统版本
#         # 'deviceName': '721QEDRE2H7DT',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
#         'noReset': True,  # 应用状态是否需要重置，默认true
#         'fullReset': False,  # 执行完测试后是否卸载app，默认false
#         'appPackage': ini.app_package,  # 应用的包名
#         'appActivity': ini.app_package + '.MainActivity',  # 应用的第一个启动Activity
#         'newCommandTimeout': 60 * 60 * 60,  # 命令超时时间，单位：秒；超时自动结束会话
#         'unicodeKeyboard': True,  # 使用unicode编码方式发送字符串；输入中文需要
#         'resetKeyboard': True  # 将键盘隐藏起来，默认true；输入中文需要
#     }
#     second_adriver = androiddriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 连接Appium
#     login_service = AppLoginService(second_adriver)
#     login_service.back_login_page()
#     yield second_adriver
#     second_adriver.quit()
