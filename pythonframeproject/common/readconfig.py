#读取配置文件,以使用里面的信息
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
    #读取url
    @property
    def url(self):
        return self._get('HOST', 'HOST')

    # 读取新房url
    @property
    def xf_url(self):
        return self._get('HOST', 'XF_HOST')

    #读取账号密码
    @property
    def user_account(self):
        return self._get('USER', 'ACCOUNT')

    @property
    def user_password(self):
        return self._get('USER', 'PASSWORD')

    # 读取新房账号密码
    @property
    def xf_user_account(self):
        return self._get('XF_USER', 'ACCOUNT')

    @property
    def xf_user_password(self):
        return self._get('XF_USER', 'PASSWORD')

    #读取物业地址信息

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



ini = ReadConfig()

if __name__ == '__main__':
    print(ini.user_account)
    print(ini.user_password)
    print(ini.url)

