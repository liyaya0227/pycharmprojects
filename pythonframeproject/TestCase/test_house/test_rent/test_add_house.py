"""
@author: lijiahui
@version: V1.0
@file: test_add_house.py
@time: 2022/1/7
"""
import pytest
from selenium.webdriver.chrome import webdriver

from common.readconfig import ini
from config.conf import cm
from page_object.house.addhouse import AddHouse
from page_object.login.loginpage import LoginPage
from utils.jsonutil import get_data
from utils.timeutil import sleep


class Test_Add_House:
    json_file_path = cm.test_data_dir + "/test_rent/house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        login_page = LoginPage(web_driver)
        login_page.log_in(ini.user_account, ini.user_password)

    def test_add_house(self, web_driver):
        add_house = AddHouse(web_driver)
        add_house.input_property_address('出租')
        sleep(2)
        add_house.input_owner_info_and_house_info(self.test_data, '租赁')

if __name__ == '__main__':
    pytest.main(['TestCase/house/test_rent/test_add_house.py'])