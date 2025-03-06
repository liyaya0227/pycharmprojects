#用来存放需要被很多文件同时执行的DDT数据
#merit：不需要导入，自动执行
#需要固件：@pytest.fixture(scope="function/class/session")作用域

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
from py.xml import html
from selenium import webdriver

from common.readconfig import ini
from config.conf import cm
from page_object.login.loginpage import LoginPage

#封装并传递driver

@pytest.fixture(scope='session', autouse=True)
def web_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        #更改chrome的默认下载文件夹：
        "download.default_directory": cm.tmp_dir,
        #以下两个参数避免密码提示弹出框的弹出：
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
    #以下两个可以取消"Chrome正受到自动软件的控制"
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'load-extension'])
    #wdriver = webdriver.Chrome(options=chrome_options)
    wdriver = webdriver.Chrome(executable_path=r'/Users/liyaya/Downloads/chromedriver', options=chrome_options)
    # web_driver = webdriver.Firefox(firefox_binary='C:/Program Files/Mozilla Firefox/firefox.exe')
    wdriver.maximize_window()
    #打开网站
    wdriver.get(ini.url)
    #作用是类似return ，在用例执行完成后会返回继续执行yield后面代码
    yield wdriver
    wdriver.quit()

# @pytest.fixture(scope='session', autouse=True)
# def setup_and_teardown(web_driver):
#     login_page = LoginPage(web_driver)
#     # main_topview = MainTopViewPage(web_driver)
#     # main_leftview = MainLeftViewPage(web_driver)
#
#     login_page.log_in(ini.user_account, ini.user_password)
#     # main_topview.wait_page_loading_complete()
#     # main_topview.click_close_button()
#     # yield
#     # main_leftview.log_out()


"""python自带的report，没啥用"""
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
#     '''
#     截图保存为base64
#     :return:
#     '''
#     return driver.get_screenshot_as_base64()

