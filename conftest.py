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
from common.readconfig import ini
from selenium import webdriver
from config.conf import cm
from utils.timeutil import timestamp
from utils.sendmail import send_report
from page_object.login.loginpage import LoginPage
from page_object.main.leftviewpage import MainLeftViewPage
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
    login_page.verify()
    login_page.click_login_button()
    main_topview = MainTopViewPage(wdriver)
    main_topview.wait_page_loading_complete()
    main_topview.click_close_button()
    yield wdriver
    print('------------close browser------------')
    wdriver.quit()


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
#                 html1 = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;"' \
#                         'onclick="window.open(this.src)" align="right"/></div>' % screen_img
#                 extra.append(pytest_html.extras.html(html1))
#         report.extra = extra


# def pytest_html_results_table_header(cells):
#     cells.insert(1, html.th('用例名称'))
#     cells.insert(2, html.th('Test_node_id'))
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


# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     """收集测试结果"""
#     result = {
#         "total": terminalreporter._numcollected,
#         'passed': len(terminalreporter.stats.get('passed', [])),
#         'failed': len(terminalreporter.stats.get('failed', [])),
#         'error': len(terminalreporter.stats.get('error', [])),
#         'skipped': len(terminalreporter.stats.get('skipped', [])),
#         # terminalreporter._sessionstarttime 会话开始时间
#         'total times': timestamp() - terminalreporter._sessionstarttime
#     }
#     print(result)
#     if result['failed'] or result['error']:
#         send_report()


def _capture_screenshot():
    """截图保存为base64"""
    now_time, screen_file = cm.screen_path
    wdriver.save_screenshot(screen_file)
    allure.attach.file(screen_file,
                       "失败截图{}".format(now_time),
                       allure.attachment_type.PNG)
    with open(screen_file, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()
