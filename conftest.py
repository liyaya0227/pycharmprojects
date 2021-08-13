#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: conftest.py
@time: 2021/06/22
"""

import os
import base64
import pytest
import allure
from py.xml import html
from config.conf import cm
from selenium import webdriver
from appium import webdriver as androiddriver
from common.readconfig import ini
from utils.timeutil import dt_strftime
from page_object.login.loginpage import LoginPage
from page_object.main.topviewpage import MainTopViewPage

wdriver = None
adriver = None


@pytest.fixture(scope='session')
def web_driver():
    global wdriver
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": cm.tmp_dir,
             "credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'load-extension'])
    wdriver = webdriver.Chrome(options=chrome_options)
    # web_driver = webdriver.Firefox(firefox_binary='C:/Program Files/Mozilla Firefox/firefox.exe')
    wdriver.maximize_window()
    wdriver.get(ini.url)
    login_page = LoginPage(wdriver)
    login_page.log_in(ini.user_account, ini.user_password)
    main_topview = MainTopViewPage(wdriver)
    main_topview.wait_page_loading_complete()
    main_topview.click_close_button()
    yield wdriver
    wdriver.quit()


@pytest.fixture(scope='session')
def android_driver():
    global adriver
    desired_caps = {
        'automationName': 'appium',  # 自动化引擎，默认appium
        'platformName': 'Android',  # 操作系统
        'platformVersion': '6.0.1',  # 操作系统版本
        'deviceName': '127.0.0.1:7555',  # MUMU
        # 'platformVersion': '5.1.1',  # 操作系统版本
        # 'deviceName': '127.0.0.1:62001',  # 夜神
        # 'platformVersion': '7.1.2',  # 操作系统版本
        # 'deviceName': '721QEDRE2H7DT',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
        'noReset': True,  # 应用状态是否需要重置，默认true
        'fullReset': False,  # 执行完测试后是否卸载app，默认false
        'appPackage': ini.app_package,  # 应用的包名
        'appActivity': ini.app_package + '.MainActivity',  # 应用的第一个启动Activity
        'newCommandTimeout': 60 * 60,  # 命令超时时间，单位：秒；超时自动结束会话
        'unicodeKeyboard': True,  # 使用unicode编码方式发送字符串；输入中文需要
        'resetKeyboard': True  # 将键盘隐藏起来，默认true；输入中文需要
    }
    adriver = androiddriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 连接Appium
    # login_page = AppLoginPage(adriver)
    # login_page.input_account(ini.user_account)
    # login_page.input_password(ini.user_password)
    # login_page.choose_read()
    # login_page.click_login_button()
    yield adriver
    adriver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    获取每个用例状态的钩子函数
    :param item:
    :return:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_img = _capture_screenshot()
            if screen_img:
                report_html = '<div><img src="data:image/png;base64,%s" alt="screenshot" ' \
                              'style="width:1024px;height:768px;" onclick="window.open(this.src)" ' \
                              'align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(report_html))
        report.extra = extra


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


def pytest_html_report_title(report):
    report.title = "京日找房Web端UI自动化测试报告"


def _capture_screenshot():
    """截图保存为base64"""
    file_name = dt_strftime("%Y%m%d%H%M%S") + ".png"
    path = cm.tmp_dir + "\\screen_capture\\" + file_name
    if not os.path.exists(cm.tmp_dir + "\\screen_capture"):
        os.makedirs(cm.tmp_dir + "\\screen_capture")
    wdriver.save_screenshot(path)
    allure.attach.file(path, "失败截图", allure.attachment_type.PNG)
    with open(path, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()
