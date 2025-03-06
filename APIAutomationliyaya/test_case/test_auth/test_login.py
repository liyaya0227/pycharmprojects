"""
@author: lijiahui
@version: V1.0
@file: test_login.py
@time: 2022/1/12
"""
import pytest

from case_service.auth.auth_service import AuthService
from common.readconfig import ini
from tools.logger import log


class Test_Login():

    def test_login(self):
        AuthService().login(ini.account, ini.password, 1)
        log.info('登录成功')

if __name__ == '__main__':
    pytest.main(['test_case/test_auth/test_login.py', '-vs'])
