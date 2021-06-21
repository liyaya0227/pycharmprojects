# -*- coding:utf-8 -*-
import pytest
from utils.logger import log
from page_object.custom.customtablepage import CustomTablePage
from page_object.main.maintopviewpage import MainTopViewPage


@pytest.mark.contract
class TestContract(object):

    @pytest.fixture(scope="class", autouse=True)
    def close_topview(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_topview.click_close_button()

    @pytest.mark.xfail
    def test_001(self, web_driver):
        custom_table = CustomTablePage(web_driver)
        custom_table.click_add()


if __name__ == '__main__':
    pytest.main(['D:/PythonProject/UIAutomation/ui/TestCase/test_process/test_contract.py'])
