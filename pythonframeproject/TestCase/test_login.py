#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
import pytest

from page_object.login.loginpage import LoginPage
from utils.logger import log
from common.readconfig import ini


class Test_Login:

    def test_login(self, web_driver):
        login_page = LoginPage(web_driver)
        login_page.log_in(ini.user_account, ini.user_password)


if __name__ == '__main__':
    pytest.main(['TestCase/test_login.py'])

