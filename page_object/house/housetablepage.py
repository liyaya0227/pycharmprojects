# -*- coding:utf-8 -*-
from utils.times import sleep

from page.webpage import WebPage
from common.readelement import Element

house_table = Element('house/housetable')


class HouseTablePage(WebPage):

    def click_add_house_button(self):
        self.is_click(house_table['新增房源按钮'])

    def input_community_name_search(self, community_name):
        self.input_text(house_table['楼盘输入框'], community_name)
        sleep(2)
        community_list = self.find_elements(house_table['楼盘下拉框'])
        for community in community_list:
            if community.text == community_name:
                community.click()
                break

    def input_building_id_search(self, building_id):
        self.is_click(house_table['楼栋选择框'])
        building_id_list = self.find_elements(house_table['楼栋下拉框'])
        for building_id_ele in building_id_list:
            if building_id_ele.text == building_id:
                building_id_ele.click()
                break

    def input_doorplate_search(self, doorplate):
        self.is_click(house_table['门牌选择框'])
        doorplate_list = self.find_elements(house_table['门牌下拉框'])
        for doorplate_ele in doorplate_list:
            if doorplate_ele.text == doorplate:
                doorplate_ele.click()
                break

    def input_house_code_search(self, house_code):
        self.input_text(house_table['房源编号搜索项'], house_code)

    def click_search_button(self):
        self.is_click(house_table['搜索按钮'])
        sleep()

    def click_reset_button(self):
        self.is_click(house_table['重置按钮'])
        sleep()

    def clear_filter(self):
        self.is_click(house_table['关注筛选_不限'])
        self.is_click(house_table['角色筛选_不限'])
        self.is_click(house_table['区域筛选_不限'])
        self.is_click(house_table['价格筛选_不限'])
        self.is_click(house_table['面积筛选_不限'])
        self.is_click(house_table['户型筛选_不限'])
        self.is_click(house_table['标签筛选_不限'])
        self.is_click(house_table['装修筛选_不限'])

    def go_house_detail_by_row(self, row=1):
        houses = self.find_element(house_table['房源列表'])
        house = houses.find_element_by_xpath("//div[@class='ant-row houseManage']//table/tbody/tr[" + str(row) + "]/td[2]")
        house.click()

    def get_house_table_count(self):
        houses = self.find_element(house_table['房源列表'])
        house = houses.find_elements_by_xpath("//div[@style='']//div[@class='ant-row houseManage']//table/tbody/tr")
        return len(house)


