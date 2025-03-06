"""
@desc:登录测试脚本
@author: lijiahui
@version: V1.0
@file: test_login.py
@time: 2022/1/20
"""
import pytest

from case_service.jrxf.auth.auth_service import AuthService
from common.readconfig import ini
from tools.logger import log


class TestLogin():

    def test_login(self):
        auth_service = AuthService()
        auth_service.login(ini.xf_user_account, ini.xf_user_password, scope=6)
        log.info('登录成功')

if __name__ == '__main__':
    pytest.main(['jrxf/auth/test_login.py', '-vs'])
