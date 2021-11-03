#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@time: 2021/06/22
"""
from utils.timeutil import sleep
from page.webpage import WebPage
from page_object.jrgj.web.customer.addpage import CustomerAddPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from common.readelement import Element

customer_table = Element('jrgj/web/customer/table')


class CustomerTablePage(WebPage):

    def click_add_button(self):
        self.click_element(customer_table['录入客源按钮'])

    def input_search_text(self, search_text):
        self.clear_text(customer_table['搜索输入框'])
        self.input_text(customer_table['搜索输入框'], search_text)

    def click_search_button(self):
        self.click_element(customer_table['查询按钮'])
        sleep(2)

    def click_all_tab(self):
        self.click_element(customer_table['全部标签'])

    def click_sale_tab(self):
        self.click_element(customer_table['买二手标签'])

    def click_rent_tab(self):
        self.click_element(customer_table['租赁标签'])

    def click_new_house_tab(self):
        self.click_element(customer_table['新房标签'])

    def click_made_deal_tab(self):
        self.click_element(customer_table['已成交标签'])

    def choose_customer_wish(self, customer_wish):
        if customer_wish == '不限':
            self.click_element(customer_table['意愿等级_不限'])
        elif customer_wish == '三星':
            self.click_element(customer_table['意愿等级_三星'])
        elif customer_wish == '二星':
            self.click_element(customer_table['意愿等级_二星'])
        elif customer_wish == '一星':
            self.click_element(customer_table['意愿等级_一星'])
        else:
            raise ValueError('传值错误')

    def go_customer_detail_by_row(self, row=1):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]//div[contains(@class,'customesList')]//table/tbody/tr["\
                  + str(row) + "]/td[" + str(self.__get_column_by_title('姓名') + 1) + "]/a/div"
        self.click_element(locator, sleep_time=4)

    def get_customer_table_count(self):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[contains(@class,'customesList')]//table/tbody/tr"
        table_count = self.find_elements(locator)
        if table_count[0].text == '暂无数据':
            return 0
        return len(table_count)

    def get_customer_code_by_row(self, row=1):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[contains(@class,'customesList')]//table/tbody/tr["\
                  + str(row) + "]/td[" + str(self.__get_column_by_title('编号') + 1) + "]/a/div"
        return self.get_element_text(locator)

    def get_customer_name_by_row(self, row=1):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[contains(@class,'customesList')]//table/tbody/tr["\
                  + str(row) + "]/td[" + str(self.__get_column_by_title('姓名') + 1) + "]/a/div"
        return self.get_element_text(locator)

    def get_customer_detailed_requirements_by_row(self, row=1):
        expand_locator = 'xpath', "//div[not(contains(@style,'display'))]/div[contains(@class,'customesList')]" \
                                  "//table/tbody/tr[" + str(row) + "]/td[" + \
                         str(self.__get_column_by_title('详细需求') + 1) + "]/div/div/a"
        if self.element_is_exist(expand_locator, timeout=2):
            self.click_element(expand_locator)
        locator = 'xpath', "//div[not(contains(@style,'display'))]/div[contains(@class,'customesList')]" \
                           "//table/tbody/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('详细需求') + 1) + \
                  "]//div[@class='ant-row']/div[1]"
        requirement_list = self.find_elements(locator)
        value = []
        for requirement_ele in requirement_list:
            value.append(requirement_ele.text)
        return value

    def __get_column_by_title(self, title):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[contains(@class,'customesList')]//table/thead//th"
        title_list = self.find_elements(locator)
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele)

    def add_customer(self, test_data):
        main_leftview = MainLeftViewPage(self.driver)
        main_upview = MainUpViewPage(self.driver)
        customer_add = CustomerAddPage(self.driver)
        self.click_add_button()
        customer_add.input_customer_name(test_data['姓名'])
        customer_add.choose_customer_sex(test_data['性别'])
        customer_add.choose_phone_area(test_data['电话号_区域'])
        customer_add.input_customer_phone(test_data['电话号'])
        customer_add.choose_customer_wish(test_data['客户意愿'])
        customer_add.add_customer_requirements(test_data['需求类型'])
        customer_add.click_next_step_button()
        customer_add.choose_purchase_house_purpose(test_data['购房目的'])
        customer_add.input_psychology_price(test_data['心理价位'])
        customer_add.input_area(test_data['面积'])
        customer_add.input_room(test_data['居室'])
        customer_add.choose_business_district(test_data['商圈'])
        customer_add.choose_use(test_data['用途'])
        customer_add.choose_pay_type(test_data['付款方式'])
        customer_add.input_first_pay(test_data['首付'])
        customer_add.input_month_pay(test_data['月供'])
        customer_add.choose_decoration(test_data['装修'])
        customer_add.choose_orientation(test_data['朝向'])
        customer_add.choose_floor(test_data['楼层'])
        customer_add.choose_floor_year(test_data['楼龄'])
        customer_add.click_complete_button()
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        self.click_all_tab()
        self.choose_customer_wish('不限')
        self.input_search_text(test_data['电话号'])
        self.click_search_button()
