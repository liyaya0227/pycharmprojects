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
from selenium import webdriver
from common.readconfig import ini
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.common.web.login import LoginPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage


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
    yield wdriver
    wdriver.quit()


@pytest.fixture(scope='session', autouse=True)
def setup_and_teardown(web_driver):
    login_page = LoginPage(web_driver)
    main_topview = MainTopViewPage(web_driver)
    main_leftview = MainLeftViewPage(web_driver)

    login_page.log_in(ini.user_account, ini.user_password)
    main_topview.wait_page_loading_complete()
    main_topview.click_close_button()
    yield
    main_leftview.log_out()
