#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: lijiahui
@version: V1.0
@file: conf.py
@time: 2022/1/10
"""

import os
from tools.times import dt_strftime


class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 日志目录
    LOG_PATH = os.path.join(BASE_DIR, 'logs')

    # 报告目录

    REPORT_PATH = os.path.join(BASE_DIR, 'report/allure_report', 'index.html')

    # 测试数据目录
    TEST_DATA_PATH = os.path.join(BASE_DIR, 'test_data')

    # 接口参数文件路径
    API_PARAMS_PATH = os.path.join(BASE_DIR, 'api_params')

    # yaml数据目录

    TESTYAML_PATH = os.path.join(BASE_DIR, 'api_definition')

    # 日志目录
    TMP_PATH = os.path.join(BASE_DIR, 'tmp')

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
    def ini_file(self):
        # 配置文件
        _file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(_file):
            raise FileNotFoundError("配置文件%s不存在！" % _file)
        return _file

    def testdata_file(self, name):
        """测试数据文件"""
        test_data_path = os.path.join(self.TEST_DATA_PATH, '%s.yaml' % name)
        if not os.path.exists(test_data_path):
            raise FileNotFoundError("%s 文件不存在！" % test_data_path)
        return test_data_path

    def yaml_file(self, name):
        """接口定义文件"""
        file_path = os.path.join(self.BASE_DIR, 'api_definition', '%s.yaml' % name)
        if not os.path.exists(file_path):
            raise FileNotFoundError("%s 文件不存在！" % file_path)
        return file_path

    def xml_file(self, name):
        """xml文件"""
        file_path = os.path.join(self.TEST_DATA_PATH, '%s.xml' % name.lstrip('/'))
        if not os.path.exists(file_path):
            raise FileNotFoundError("%s 文件不存在！" % file_path)
        return file_path

    def api_params_json_file(self, name):
        """测试数据文件-json"""
        api_params_json_file = os.path.join(self.API_PARAMS_PATH, '%s.json' % name.lstrip('/'))
        if not os.path.exists(api_params_json_file):
            raise FileNotFoundError("%s 文件不存在！" % api_params_json_file)
        return api_params_json_file

    def testdata_json_file(self, name):
        """测试数据文件-json"""
        test_data_json_path = os.path.join(self.TEST_DATA_PATH, '%s.json' % name.lstrip('/'))
        if not os.path.exists(test_data_json_path):
            raise FileNotFoundError("%s 文件不存在！" % test_data_json_path)
        return test_data_json_path

    @property
    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime('%Y%m%d')))

    @property
    def screen_file(self):
        now_time = dt_strftime("%Y%m%d%H%M%S")
        # 截图目录
        screenshot_dir = os.path.join(self.BASE_DIR, 'screen_capture')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        screen_path = os.path.join(screenshot_dir, "{}.png".format(now_time))
        return now_time, screen_path

    def tmp_file_path(self, file_name):
        """临时文件路径"""
        tmp_file = os.path.join(self.BASE_DIR, 'tmp', file_name)
        if not os.path.exists(tmp_file):
            raise FileNotFoundError("配置文件%s不存在！" % tmp_file)
        return tmp_file


cm = ConfigManager()
