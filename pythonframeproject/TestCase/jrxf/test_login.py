"""
@author: lijiahui
@version: V1.0
@file: loginpage.py
@time: 2022/1/17
"""
import logging

import pytest

from common.readconfig import ini
from page_object.jrxf.main.loginpage import LoginPage
from utils.logger import log


class Testlogin():
    def test_login(self, xf_driver):
        loginpage = LoginPage(xf_driver)
        loginpage.log_in(ini.xf_user_account, ini.xf_user_password)
        log.info('登录成功')

if __name__ == '__main__':
    pytest.main(['TestCase/jrxf/main/test_login.py'])