"""
@author: lijiahui
@version: V1.0
@file: test_add_house.py
@time: 2022/1/17
"""
import pytest

from config.conf import cm
from page_object.jrxf.house.addnewhouse import AddNewHouse
from utils.jsonutil import get_data
from utils.timeutil import sleep


class Test_Add_House:
    json_file_path = cm.json_file('jrxf/house/add_house')
    test_data = get_data(json_file_path)

    def test_add_house(self, xf_driver):
        addhouse = AddNewHouse(xf_driver)
        sleep(0.5)
        addhouse.add_house_baseinfo(self.test_data)
        sleep(2)
        addhouse.editor_house_baseinfo(self.test_data)
        sleep(2)
        addhouse.examine_contract(self.test_data)
        sleep(2)
        addhouse.save_detail_baseinfo(self.test_data)
        sleep(2)
        addhouse.ready_sale_examine(self.test_data)
        sleep(2)
        addhouse.delete_estate(self.test_data)

if __name__ == '__main__':
    pytest.main(['TestCase/jrxf/house/add_house.py'])
