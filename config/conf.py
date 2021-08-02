#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: conf.py
@time: 2021/06/22
"""

import os
from selenium.webdriver.common.by import By
from utils.timeutil import dt_strftime


class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 页面元素目录
    ELEMENT_PATH = os.path.join(BASE_DIR, 'page_element')

    # 报告文件
    REPORT_FILE = os.path.join(BASE_DIR, 'reports', 'report.html')

    # 元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME
    }

    # 邮件信息
    EMAIL_INFO = {
        'username': '347869033@qq.com',
        'password': 'qybgpjtqpndycahh',
        'smtp_host': 'smtp.qq.com',
        'smtp_port': 465
    }

    # 收件人
    ADDRESSEE = [
        'jutao@jingrizf.com',
    ]

    @property
    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime('%Y%m%d')))

    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" % ini_file)
        return ini_file

    @property
    def tmp_dir(self):
        """配置文件"""
        tmp_dir = os.path.join(self.BASE_DIR, 'tmp')
        if not os.path.exists(tmp_dir):
            raise FileNotFoundError("配置文件%s不存在！" % tmp_dir)
        return tmp_dir

    @property
    def tmp_picture_file(self):
        """配置文件"""
        tmp_picture_file = os.path.join(self.BASE_DIR, 'tmp', 'picture.jpg')
        if not os.path.exists(tmp_picture_file):
            raise FileNotFoundError("配置文件%s不存在！" % tmp_picture_file)
        return tmp_picture_file

    @property
    def test_data_dir(self):
        """配置文件"""
        tmp_picture_file = os.path.join(self.BASE_DIR, 'TestData')
        if not os.path.exists(tmp_picture_file):
            raise FileNotFoundError("配置文件%s不存在！" % tmp_picture_file)
        return tmp_picture_file

    @property
    def screen_path(self):
        """截图目录"""
        screenshot_dir = os.path.join(self.BASE_DIR, 'tmp', 'screen_capture')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        now_time = dt_strftime("%Y%m%d%H%M%S")
        screen_file = os.path.join(screenshot_dir, "{}.png".format(now_time))
        return now_time, screen_file


cm = ConfigManager()
if __name__ == '__main__':
    print(cm.tmp_picture_file)
