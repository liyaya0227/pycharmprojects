#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@time: 2021/06/22
"""
from common.readconfig import ini
from utils.timeutil import sleep
from utils.sqlutil import select_sql, update_sql
from page.webpage import WebPage
from common.readelement import Element
from page_object.web.house.detailpage import HouseDetailPage
from page_object.web.main.upviewpage import MainUpViewPage

house_table = Element('web/house/table')


class HouseTablePage(WebPage):

    def click_sale_tab(self):
        self.is_click(house_table['买卖标签'])

    def click_rent_tab(self):
        self.is_click(house_table['租赁标签'])

    def click_new_tab(self):
        self.is_click(house_table['新房标签'])

    def click_all_house_tab(self):
        self.is_click(house_table['全部房源标签'])

    def click_deal_house_tab(self):
        self.is_click(house_table['成交房源标签'])

    def click_add_house_button(self):
        self.is_click(house_table['新增房源按钮'])

    def click_add_new_house_button(self):
        self.is_click(house_table['新增楼盘按钮'])

    def click_off_shelf_house_tab(self):
        self.is_click(house_table['下架房源标签'])

    def choose_estate_name_search(self, community_name):
        self.input_text(house_table['楼盘输入框'], community_name)
        sleep(2)
        community_list = self.find_elements(house_table['楼盘下拉框'])
        for community in community_list:
            if community.text == community_name:
                community.click()
                sleep()
                break

    def choose_building_name_search(self, building_name):
        self.is_click(house_table['楼栋选择框'])
        sleep()
        building_name_list = self.find_elements(house_table['楼栋下拉框'])
        for building_name_ele in building_name_list:
            if building_name_ele.text == building_name:
                building_name_ele.click()
                sleep()
                break

    def choose_doorplate_search(self, doorplate):
        self.is_click(house_table['门牌选择框'])
        doorplate_list = self.find_elements(house_table['门牌下拉框'])
        for doorplate_ele in doorplate_list:
            if doorplate_ele.text == doorplate:
                doorplate_ele.click()
                break

    def choose_option(self, item_name, option): #根item和opiton定位选项
        option_xpath = "//div[not(contains(@style,'display'))]//label[text()=\'{item_name}\']/ancestor::" \
                       "div[contains(@class ,'ant-row ant-form-item')]//span[text()=\'{option}\']/parent::label".\
                        format(item_name=item_name, option=option)
        locator = ('xpath', option_xpath)
        self.is_click(locator)

    def input_house_code_search(self, house_code):
        self.input_text(house_table['房源编号搜索项'], house_code)
        sleep()

    def input_building_name_search(self, building_name):
        self.input_text(house_table['楼盘名称搜索项'], building_name)
        sleep()

    def click_search_button(self):
        sleep()
        self.is_click(house_table['搜索按钮'], sleep_time=2)
        self.wait_page_loading_complete()

    def click_reset_button(self):
        self.is_click(house_table['重置按钮'])
        sleep()

    def clear_filter(self, flag='买卖'):
        if flag == '租赁' or flag == '买卖':
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['关注筛选_不限'], 'class'):
                self.is_click(house_table['关注筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['角色筛选_不限'], 'class'):
                self.is_click(house_table['角色筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['区域筛选_不限'], 'class'):
                self.is_click(house_table['区域筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['价格筛选_不限'], 'class'):
                self.is_click(house_table['价格筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['面积筛选_不限'], 'class'):
                self.is_click(house_table['面积筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['户型筛选_不限'], 'class'):
                self.is_click(house_table['户型筛选_不限'])
            if flag == '买卖':
                if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['标签筛选_不限'],
                                                                                        'class'):
                    self.is_click(house_table['标签筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['装修筛选_不限'], 'class'):
                self.is_click(house_table['装修筛选_不限'])
        elif flag == '新房':
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['区域筛选_不限'], 'class'):
                self.is_click(house_table['区域筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['价格筛选_不限'], 'class'):
                self.is_click(house_table['价格筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['户型筛选_不限'], 'class'):
                self.is_click(house_table['户型筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['物业类型筛选_不限'], 'class'):
                self.is_click(house_table['物业类型筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['类型筛选_不限'], 'class'):
                self.is_click(house_table['类型筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['房源渠道筛选_不限'], 'class'):
                self.is_click(house_table['房源渠道筛选_不限'])
        sleep()

    def go_house_detail_by_row(self, row=1):
        self.wait_page_loading_complete()
        sleep()
        locator = 'xpath', "//div[not(contains(@style,'display'))]//div[@class='ant-row houseManage']//table/tbody/tr["\
                  + str(row) + "]/td[" + str(self.__get_column_by_title('楼盘名称') + 1) + "]"
        self.is_click(locator)
        self.wait_page_loading_complete()
        sleep(2)

    def verify_house_exist(self, building_name):  #验证列表中是否存在当前房源
        locator = 'xpath', "//div[not(contains(@style,'display'))]//div[@class='ant-row houseManage']//table/tbody/tr/" \
                  "td[" + str(self.__get_column_by_title('楼盘名称') + 1) + "]/a/span"
        ele_list = self.find_elements(locator)
        for ele in ele_list:
            if ele.text == building_name:
                return True
        return False

    def go_new_house_detail_by_row(self, row=1): #从新房列表进入详情
        locator = 'xpath', "//div[not(contains(@style,'display'))]//div[@class='ant-row houseManage']//table/tbody/tr["\
                  + str(row) + "]/td[" + str(self.__get_column_by_title('楼盘名称') + 1) + "]/a/span"
        self.is_click(locator)

    def get_house_table_count(self):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[@class='ant-row houseManage']//table//tbody" \
                  "/tr[@data-row-key]"
        table_count = self.find_elements(locator)
        if table_count[0].text == '暂无数据':
            return 0
        return len(table_count)

    def click_delete_button_by_row(self, row=1):
        locator = 'xpath', "//div[not(contains(@style,'display'))]//div[@class='ant-row houseManage']//table/tbody/tr["\
                  + str(row) + "]/td[" + str(self.__get_column_by_title('操作') + 1) + "]/p[contains(text(),'删除')]"
        self.is_click(locator)

    def __get_column_by_title(self, title):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[contains(@class,'houseManage')]//table/thead//th"
        title_list = self.find_elements(locator)
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele)

    def dialog_click_confirm_button(self):
        self.is_click(house_table['弹窗_删除按钮'])

    def check_house_exist(self, test_data, flag='买卖'):
        table = HouseTablePage(self.driver)
        house_detail = HouseDetailPage(self.driver)
        main_upview = MainUpViewPage(self.driver)
        if flag == '买卖':
            table.click_sale_tab()
        table.click_reset_button()
        table.clear_filter(flag)
        table.choose_estate_name_search(test_data['楼盘'])
        table.choose_building_name_search(test_data['楼栋'])
        table.click_search_button()
        table_count = table.get_house_table_count()
        if table_count == 0:
            return False
        else:
            for row in range(table_count):
                table.go_house_detail_by_row(row + 1)
                house_property_address = house_detail.get_address_dialog_house_property_address()
                if house_property_address['estate_name'] == test_data['楼盘'] \
                        and house_property_address['building_name'] == test_data['楼栋'] \
                        and house_property_address['door_name'] == test_data['门牌号']:
                    main_upview.close_title_by_name(house_property_address['estate_name'])
                    return True
                main_upview.close_title_by_name(house_property_address['estate_name'])
                if flag == '买卖':
                    table.click_sale_tab()
                table.clear_filter(flag)
                table.choose_estate_name_search(test_data['楼盘'])
                table.choose_building_name_search(test_data['楼栋'])
                table.click_search_button()
            return False

    @staticmethod
    def get_house_code_by_db(flag='买卖'):
        estate_sql = "select id from estate_new_base_info where [name]='" + ini.house_community_name + "'"
        estate_id = select_sql(estate_sql)[0][0]
        if flag == '买卖':
            house_sql = "select house_code from trade_house where location_estate_id='" + str(estate_id) + \
                        "' and location_building_number='" + ini.house_building_id + \
                        "' and location_building_cell='" + ini.house_building_cell + \
                        "' and location_floor='" + ini.house_floor + \
                        "' and location_doorplate='" + ini.house_doorplate + "' and is_valid='1' and [status]='0'"
        elif flag == '租赁':
            house_sql = "select house_code from rent_house where location_estate_id='" + str(estate_id) + \
                        "' and location_building_number='" + ini.house_building_id + \
                        "' and location_building_cell='" + ini.house_building_cell + \
                        "' and location_floor='" + ini.house_floor + \
                        "' and location_doorplate='" + ini.house_doorplate + "' and is_valid='1' and [status]='0'"
        else:
            raise "传值错误"
        try:
            house_code = select_sql(house_sql)[0][0]
            return house_code
        except IndexError:
            return ''

    @staticmethod
    def update_house_create_time_by_db(house_code, create_time, flag='买卖'):
        if flag == '买卖':
            sql = "update trade_house set create_time='" + create_time + "' where house_code='" + house_code + "'"
        elif flag == '租赁':
            sql = "update rent_house set create_time='" + create_time + "' where house_code='" + house_code + "'"
        else:
            raise "传值错误"
        update_sql(sql)
