#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: conftest.py
@time: 2021/06/22
"""

import base64
import pytest
import allure
from py.xml import html
from config.conf import cm
from selenium import webdriver
from common.readconfig import ini
from utils.timeutil import dt_strftime
from page_object.login.loginpage import LoginPage
from page_object.main.topviewpage import MainTopViewPage

wdriver = None


@pytest.fixture(scope='session')
def web_driver():
    global wdriver
    print('------------open browser------------')
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": cm.tmp_dir, "credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'load-extension'])
    wdriver = webdriver.Chrome(options=chrome_options)
    # web_driver = webdriver.Firefox(firefox_binary='C:/Program Files/Mozilla Firefox/firefox.exe')
    wdriver.maximize_window()
    wdriver.get(ini.url)
    login_page = LoginPage(wdriver)
    login_page.input_account(ini.user_account)
    login_page.input_password(ini.user_password)
    login_page.click_verify_button()
    # login_page.verify()
    # login_page.click_login_button()

    """图片验证"""
    login_page.slide_verification("./slider.png", "background.jpg", 5)

    main_topview = MainTopViewPage(wdriver)
    main_topview.wait_page_loading_complete()
    main_topview.wait_close_top_view()
    yield wdriver
    print('------------close browser------------')
    wdriver.quit()


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
    wdriver.save_screenshot(path)
    allure.attach.file(path, "失败截图", allure.attachment_type.PNG)
    with open(path, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()
