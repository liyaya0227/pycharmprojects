#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: readconfig.py
@time: 2021/06/22
"""

import configparser
from config.conf import cm


class ReadConfig(object):
    """配置文件"""

    def __init__(self):
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(cm.ini_file, encoding='utf-8')

    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(cm.ini_file, 'w') as f:
            self.config.write(f)

    @property
    def url(self):
        return self._get('HOST', 'HOST')

    @property
    def xf_url(self):
        return self._get('HOST', 'XF_HOST')

    @property
    def job_url(self):
        return self._get('HOST', 'JOB_HOST')

    @property
    def app_package(self):
        return self._get('APP', 'PACKAGE')

    @property
    def cw_user_account(self):
        return self._get('CW_USER', 'ACCOUNT')

    @property
    def cw_user_password(self):
        return self._get('CW_USER', 'PASSWORD')

    @property
    def job_user_account(self):
        return self._get('JOB_USER', 'ACCOUNT')

    @property
    def job_user_password(self):
        return self._get('JOB_USER', 'PASSWORD')

    @property
    def user_account(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        else:
            env = self.environment
        return self._get(env.upper() + '_USER', 'ACCOUNT')

    @property
    def user_password(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        else:
            env = self.environment
        return self._get(env.upper() + '_USER', 'PASSWORD')

    @property
    def s_user_account(self):
        return self._get(self.environment.upper() + '_USER', 'S_ACCOUNT')

    @property
    def s_user_password(self):
        return self._get(self.environment.upper() + '_USER', 'S_PASSWORD')

    @property
    def od_user_account(self):
        return self._get(self.environment.upper() + '_USER', 'OD_ACCOUNT')

    @property
    def od_user_password(self):
        return self._get(self.environment.upper() + '_USER', 'OD_PASSWORD')

    @property
    def database_server(self):
        return self._get('DATABASE', 'DATABASE_SERVER')

    @property
    def database_account(self):
        return self._get('DATABASE', 'DATABASE_ACCOUNT')

    @property
    def database_password(self):
        return self._get('DATABASE', 'DATABASE_PASSWORD')

    @property
    def database_name(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        else:
            env = self.environment
        database_name = self._get('DATABASE', 'DATABASE_NAME')
        database_name = database_name.replace("@env", env.upper())
        return database_name

    @property
    def environment(self):
        return self._get('ENVIRONMENT', 'ENVIRONMENT')

    @property
    def house_community_name(self):
        return self._get('HOUSE', 'COMMUNITY_NAME')

    @property
    def house_building_id(self):
        return self._get('HOUSE', 'BUILDING_ID')

    @property
    def house_building_cell(self):
        return self._get('HOUSE', 'BUILDING_CELL')

    @property
    def house_floor(self):
        return self._get('HOUSE', 'FLOOR')

    @property
    def house_doorplate(self):
        return self._get('HOUSE', 'DOORPLATE')

    @property
    def custom_telephone(self):
        return self._get('CUSTOM', 'TELEPHONE')

    @property
    def super_verify_code(self):
        return self._get('VERIFY_CODE', 'SUPER_VERIFY_CODE')


ini = ReadConfig()

if __name__ == '__main__':
    print(ini.user_account)
