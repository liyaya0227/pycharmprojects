"""
@author: lijiahui
@version: V1.0
@file: test_left_view.py
@time: 2022/1/9
"""
import pytest

from common.readconfig import ini
from page_object.login.loginpage import LoginPage
from page_object.mian.leftviewpage import LeftViewPage
from utils.timeutil import sleep


class Test_Left_View:

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        login_page = LoginPage(web_driver)
        login_page.log_in(ini.user_account, ini.user_password)

    def test_left_view(self, web_driver):
        leftview = LeftViewPage(web_driver)
        leftview.change_role_name('合同法务')
        sleep(2)


if __name__ == '__main__':
    pytest.main(['TestCase/main/test_left_view.py'])