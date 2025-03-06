#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#该文件对整体的目录进行管理
#在这个文件中我们可以设置自己的各个目录，也可以查看自己当前的目录

import os
from selenium.webdriver.common.by import By
from utils.timeutil import dt_strftime


class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 页面元素目录
    ELEMENT_PATH = os.path.join(BASE_DIR, 'page_element')

    # 报告文件
    REPORT_FILE = os.path.join(BASE_DIR, 'report.html')

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
        'username': '626725868@qq.com',  # 切换成你自己的地址
        'password': 'hjwtfjxlhmfpbcjf',
        'smtp_host': 'smtp.qq.com',
        'smtp_port': 465
    }

    # 收件人
    ADDRESSEE = [
        '626725868@qq.com',
    ]

    @property
    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime()))

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
        test_data_dir = os.path.join(self.BASE_DIR, 'TestData')
        if not os.path.exists(test_data_dir):
            raise FileNotFoundError("配置文件%s不存在！" % test_data_dir)
        return test_data_dir

    def xml_file(self, name):
        """xml文件"""
        file_path = os.path.join(self.BASE_DIR, 'TestData', '%s.xml' % name.lstrip('/'))
        if not os.path.exists(file_path):
            raise FileNotFoundError("%s 文件不存在！" % file_path)
        return file_path

    def json_file(self, name):
        """xml文件"""
        json_path = os.path.join(self.BASE_DIR, 'TestData', '%s.json' % name.lstrip('/'))
        if not os.path.exists(json_path):
            raise FileNotFoundError("%s 文件不存在！" % json_path)
        return json_path

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
    print(cm.BASE_DIR)
    print(cm.tmp_picture_file)
    print(cm.json_file('test_sale/house/test_add'))
