#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: conftest.py
@time: 2021/06/22
"""

import pytest
from py.xml import html
from common.readconfig import ini
from selenium import webdriver
from config.conf import cm
from page_object.login.loginpage import LoginPage


@pytest.fixture(scope='session')
def web_driver():
    print('------------open browser------------')
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": cm.tmp_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    web_driver = webdriver.Chrome(options=chrome_options)
    # web_driver = webdriver.Firefox(firefox_binary='C://Program Files//Mozilla Firefox//firefox.exe')
    web_driver.maximize_window()
    web_driver.get(ini.url)
    login_page = LoginPage(web_driver)
    login_page.input_account(ini.user_account)
    login_page.input_password(ini.user_password)
    login_page.click_verify_button()
    login_page.verify()
    login_page.click_login_button()
    yield web_driver
    print('------------close browser------------')
    web_driver.quit()

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item):
#     """
#     当测试失败的时候，自动截图，展示到html报告中
#     :param item:
#     """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     report.description = str(item.function.__doc__)
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_") + ".png"
#             screen_img = _capture_screenshot()
#             if file_name:
#                 html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % screen_img
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra
#
#
# def pytest_html_results_table_header(cells):
#     cells.insert(1, html.th('用例名称'))
#     cells.insert(2, html.th('Test_nodeid'))
#     cells.pop(2)
#
#
# def pytest_html_results_table_row(report, cells):
#     cells.insert(1, html.td(report.description))
#     cells.insert(2, html.td(report.nodeid))
#     cells.pop(2)
#
#
# def pytest_html_results_table_html(report, data):
#     if report.passed:
#         del data[:]
#         data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))
#
#
# def _capture_screenshot():
#     return driver.get_screenshot_as_base64()
