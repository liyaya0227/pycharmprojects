#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import configparser
import functools
from config.conf import cm


def check_environment():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *arg, **kwargs):
            if self.environment in ['ks', 'zjg']:
                env = 'sz'
            else:
                env = self.environment
            func(self, env, *arg, **kwargs)
        return wrapper
    return decorator


class ReadConfig:
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
    def environment(self):
        return self._get('ENVIRONMENT', 'environment')

    @property
    def public_host(self):
        return self._get('HOST', 'public_host')

    @property
    def job_host(self):
        return self._get('HOST', 'job_host')

    @property
    def host(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        elif self.environment in ['tl']:
            env = 'hz'
        else:
            env = self.environment
        return self._get('HOST', env + '_host')

    @property
    def xf_host(self):
        return self._get('HOST', 'xf' + '_host')

    @property
    def schema(self):
        return self._get('SCHEMA', 'schema')

    @property
    def account(self):
        return self._get('USER', 'account')

    @property
    def password(self):
        return self._get('USER', 'password')

    @property
    def cw_system_user_account(self):
        return self._get('CW_SYSTEM_USER', 'account')

    @property
    def cw_system_user_password(self):
        return self._get('CW_SYSTEM_USER', 'password')

    @property
    def user_account(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        elif self.environment in ['tl']:
            env = 'hz'
        else:
            env = self.environment
        return self._get(env.upper() + '_USER', 'account')

    @property
    def user_password(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        elif self.environment in ['tl']:
            env = 'hz'
        else:
            env = self.environment
        return self._get(env.upper() + '_USER', 'password')

    @property
    def xf_user_account(self):
        return self._get('XF_USER', 'account')

    @property
    def xf_user_password(self):
        return self._get('XF_USER', 'password')

    @property
    def survey_user_account(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        elif self.environment in ['tl']:
            env = 'hz'
        else:
            env = self.environment
        return self._get(env.upper() + '_USER', 'survey_account')

    @property
    def survey_user_password(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        elif self.environment in ['tl']:
            env = 'hz'
        else:
            env = self.environment
        return self._get(env.upper() + '_USER', 'survey_password')

    @property
    def od_user_account(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        elif self.environment in ['tl']:
            env = 'hz'
        else:
            env = self.environment
        return self._get(env.upper() + '_USER', 'od_account')

    @property
    def od_user_password(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        elif self.environment in ['tl']:
            env = 'hz'
        else:
            env = self.environment
        return self._get(env.upper() + '_USER', 'od_password')

    @property
    def database_server(self):
        return self._get('DATABASE', 'database_server')

    @property
    def database_account(self):
        return self._get('DATABASE', 'database_account')

    @property
    def database_password(self):
        return self._get('DATABASE', 'database_password')

    @property
    def database_name(self):
        if self.environment in ['ks', 'zjg']:
            env = 'sz'
        elif self.environment in ['tl']:
            env = 'hz'
        else:
            env = self.environment
        database_name = self._get('DATABASE', 'database_name')
        database_name = database_name.replace("@env", env.upper())
        return database_name

    @property
    def mysql_database_host(self):
        return self._get('MYSQL_DATABASE', 'database_host')

    @property
    def mysql_database_port(self):
        return self._get('MYSQL_DATABASE', 'database_port')

    @property
    def mysql_database_account(self):
        return self._get('MYSQL_DATABASE', 'database_account')

    @property
    def mysql_database_password(self):
        return self._get('MYSQL_DATABASE', 'database_password')

    @property
    def finance_database_name(self):
        return self._get('DATABASE_NAME', 'finance_database_name')

    @property
    def xf_database_server(self):
        return self._get('XF_DATABASE', 'database_server')

    @property
    def xf_database_port(self):
        return self._get('XF_DATABASE', 'database_port')

    @property
    def xf_database_account(self):
        return self._get('XF_DATABASE', 'database_account')

    @property
    def xf_database_password(self):
        return self._get('XF_DATABASE', 'database_password')

    @property
    def xf_database_name(self):
        return self._get('XF_DATABASE', 'database_name')

    @property
    def house_estate_name(self):
        return self._get('HOUSE', 'estate_name')

    @property
    def new_house_name(self):
        new_house_name = self._get('NEW_HOUSE', 'NAME')
        # new_house_name = new_house_name.replace("@env", self.environment.upper())
        return new_house_name

    @property
    def house_building_number(self):
        return self._get('HOUSE', 'building_number')

    @property
    def house_building_cell(self):
        return self._get('HOUSE', 'building_cell')

    @property
    def house_floor(self):
        return self._get('HOUSE', 'floor')

    @property
    def house_doorplate(self):
        return self._get('HOUSE', 'doorplate')

    @property
    def custom_phone(self):
        return self._get('CUSTOM', 'telephone')

    @property
    def super_verify_code(self):
        return self._get('VERIFY_CODE', 'SUPER_VERIFY_CODE')


ini = ReadConfig()

if __name__ == '__main__':
    print(ini.host)
