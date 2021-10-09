#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: createsaleorder_szpage.py
@date: 2021/7/2 0002
"""
import datetime
from utils.timeutil import sleep, dt_strftime_with_delta, dt_strftime
from page.webpage import WebPage
from common.readelement import Element

create_sale_order_detail_zjg = Element('web/contract/createsaleorder_zjg')


class ContractCreateSaleOrderDetailZJGPage(WebPage):

    def input_contract_content(self, test_data):
        self.choose_house_administrative_region(test_data['房屋所属行政区'])
        self.input_buyer_info(test_data['出卖人信息'])
        self.input_seller_info(test_data['买受人信息'])
        self.input_first_info(test_data['第一条信息'])
        self.input_second_info(test_data['第二条信息'])
        self.input_third_info(test_data['第三条信息'])
        self.input_four_info(test_data['第四条信息'])
        self.input_six_info(test_data['第六条信息'])
        self.input_twelve_info(test_data['第十二条信息'])
        self.input_commission_confirmation_info(test_data['房地产经纪佣金确认书一'])
        self.input_commission_confirmation2_info(test_data['房地产经纪佣金确认书二'])

    def choose_house_administrative_region(self, region_info):
        self.is_click(create_sale_order_detail_zjg['房屋所属行政区选择框'])
        self.__choose_value_in_drop_down_box(region_info)

    def input_buyer_info(self, buyer_info):
        self.input_text(create_sale_order_detail_zjg['出卖人_姓名输入框'], buyer_info['出卖人_姓名'])
        self.input_text(create_sale_order_detail_zjg['出卖人_证件号码输入框'], buyer_info['出卖人_身份证号'])

    def input_seller_info(self, seller_info):
        self.input_text(create_sale_order_detail_zjg['买受人_姓名输入框'], seller_info['买受人_姓名'])
        self.input_text(create_sale_order_detail_zjg['买受人_证件号码输入框'], seller_info['买受人_身份证号'])

    def input_first_info(self, first_info):
        self.input_text(create_sale_order_detail_zjg['一_1_1_输入框'], first_info['一'])
        self.input_text(create_sale_order_detail_zjg['一_2_1_输入框'], first_info['二'])
        self.is_click(create_sale_order_detail_zjg['一_3_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['三'][0])
        self.input_text(create_sale_order_detail_zjg['一_3_2_输入框'], first_info['三'][1])
        self.input_text(create_sale_order_detail_zjg['一_3_3_输入框'], self.date_handle(first_info['三'][2]), enter=True)
        self.input_text(create_sale_order_detail_zjg['一_4_1_输入框'], first_info['四'])
        self.is_click(create_sale_order_detail_zjg['一_5_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['五'])
        self.is_click(create_sale_order_detail_zjg['一_6_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['六'])
        self.input_text(create_sale_order_detail_zjg['一_7_1_输入框'], first_info['七'])
        self.input_text(create_sale_order_detail_zjg['一_8_1_输入框'], first_info['八'][0])
        self.input_text(create_sale_order_detail_zjg['一_8_2_输入框'], first_info['八'][1])
        self.input_text(create_sale_order_detail_zjg['一_8_3_输入框'], first_info['八'][2])
        self.input_text(create_sale_order_detail_zjg['一_8_4_输入框'], first_info['八'][3])

    def input_second_info(self, second_info):
        self.is_click(create_sale_order_detail_zjg['二_2_选择框'])
        self.__choose_value_in_drop_down_box(second_info['二'])
        for n, value in enumerate(second_info['二_1']):
            date_locator = 'xpath', "//div[@style='']//input[@id='earnestList_" + str(n) + "_c2_2_2']"
            self.input_text(date_locator, self.date_handle(value[0]), enter=True)
            money_locator = 'xpath', "//div[@style='']//input[@id='earnestList_" + str(n) + "_c2_2_3']"
            self.input_text(money_locator, value[1])
            pay_type_locator = 'xpath', "//div[@style='']//input[@id='earnestList_" + str(n) \
                               + "_c2_2_5']/ancestor::div[@class='ant-select-selector']"
            self.is_click(pay_type_locator)
            if 0 < value[2][0] <= 3:
                self.__choose_index_in_drop_down_box(value[2][0])
                if value[2][0] == 3:
                    finishing_locator = 'xpath', "//div[@style='']//input[@id='earnestList_" + str(n) + "_c2_2_6']"
                    self.input_text(finishing_locator, value[2][1])
            else:
                raise ValueError('传值错误')
            if len(second_info['二_1']) - n != 1:
                self.is_click(create_sale_order_detail_zjg['二_2_1_定金按钮'])
        for n, value in enumerate(second_info['二_2']):
            date_locator = 'xpath', "//div[@style='']//input[@id='housePaymentList_" + str(n) + "_c2_2_2']"
            self.input_text(date_locator, self.date_handle(value[0]), enter=True)
            money_locator = 'xpath', "//div[@style='']//input[@id='housePaymentList_" + str(n) + "_c2_2_3']"
            self.input_text(money_locator, value[1])
            pay_type_locator = 'xpath', "//div[@style='']//input[@id='housePaymentList_" + str(n) \
                               + "_c2_2_5']/ancestor::div[@class='ant-select-selector']"
            self.is_click(pay_type_locator)
            if 0 < value[2][0] <= 3:
                self.__choose_index_in_drop_down_box(value[2][0])
                if value[2][0] == 3:
                    finishing_locator = 'xpath', "//div[@style='']//input[@id='housePaymentList_" + str(n) + "_c2_2_6']"
                    self.input_text(finishing_locator, value[2][1])
            else:
                raise ValueError('传值错误')
            if len(second_info['二_2']) - n != 1:
                self.is_click(create_sale_order_detail_zjg['二_2_2_房款按钮'])
        for n, value in enumerate(second_info['二_3']):
            date_locator = 'xpath', "//div[@style='']//input[@id='initialPaymentList_" + str(n) + "_c2_2_2']"
            self.input_text(date_locator, self.date_handle(value[0]), enter=True)
            money_locator = 'xpath', "//div[@style='']//input[@id='initialPaymentList_" + str(n) + "_c2_2_3']"
            self.input_text(money_locator, value[1])
            pay_type_locator = 'xpath', "//div[@style='']//input[@id='initialPaymentList_" + str(n) \
                               + "_c2_2_5']/ancestor::div[@class='ant-select-selector']"
            self.is_click(pay_type_locator)
            if 0 < value[2][0] <= 3:
                self.__choose_index_in_drop_down_box(value[2][0])
                if value[2][0] == 3:
                    finishing_locator = 'xpath', "//div[@style='']//input[@id='initialPaymentList_" + str(n) \
                                        + "_c2_2_6']"
                    self.input_text(finishing_locator, value[2][1])
            else:
                raise ValueError('传值错误')
            if len(second_info['二_3']) - n != 1:
                self.is_click(create_sale_order_detail_zjg['二_2_3_添加按钮'])
        if second_info['二'] == '贷款':
            self.is_click(create_sale_order_detail_zjg['二_2_4_1_选择框'])
            self.__choose_value_in_drop_down_box(second_info['二_4'][0])
            self.input_text(create_sale_order_detail_zjg['二_2_4_2_输入框'], second_info['二_4'][1])
        self.input_text(create_sale_order_detail_zjg['二_2_5_1_输入框'], second_info['二_5'][0])
        if 0 < second_info['二_5'][1][0] <= 4:
            self.is_click(create_sale_order_detail_zjg['二_2_5_3_选择框'])
            self.__choose_index_in_drop_down_box(second_info['二_5'][1][0])
            if second_info['二_5'][1][0] == 1:
                self.input_text(create_sale_order_detail_zjg['二_2_5_3_输入框'],
                                self.date_handle(second_info['二_5'][1][1]), enter=True)
            elif second_info['二_5'][1][0] == 4:
                self.input_text(create_sale_order_detail_zjg['二_2_5_3_输入框'], second_info['二_5'][1][1])
            else:
                pass
        else:
            raise ValueError('传值错误')
        if 0 < second_info['二_5'][2][0] <= 3:
            self.is_click(create_sale_order_detail_zjg['二_2_5_4_选择框'])
            self.__choose_index_in_drop_down_box(second_info['二_5'][2][0])
            if second_info['二_5'][2][0] == 2:
                self.input_text(create_sale_order_detail_zjg['二_2_5_5_输入框'], second_info['二_5'][2][1])
        else:
            raise ValueError('传值错误')

    def input_third_info(self, third_info):
        self.input_text(create_sale_order_detail_zjg['三_1_输入框'], self.date_handle(third_info[0]), enter=True)
        if 0 < third_info[1][0] <= 2:
            self.is_click(create_sale_order_detail_zjg['三_2_选择框'])
            self.__choose_index_in_drop_down_box(third_info[1][0])
            self.input_text(create_sale_order_detail_zjg['三_2_输入框'], third_info[1][1])
        else:
            raise ValueError('传值错误')

    def input_four_info(self, four_info):
        if 0 < four_info[0] <= 3:
            self.is_click(create_sale_order_detail_zjg['四_选择框'])
            self.__choose_index_in_drop_down_box(four_info[0])
            if four_info[0] == 1:
                self.input_text(create_sale_order_detail_zjg['四_输入框'], self.date_handle(four_info[1]), enter=True)
            else:
                self.input_text(create_sale_order_detail_zjg['四_输入框'], four_info[1])
        else:
            raise ValueError('传值错误')

    def input_six_info(self, six_info):
        self.is_click(create_sale_order_detail_zjg['六_1_1_1_选择框'])
        self.__choose_value_in_drop_down_box(six_info['一_1'])
        if six_info['一_2'] == 1:
            self.is_click(create_sale_order_detail_zjg['六_1_2_1_单选按钮'])
        elif six_info['一_2'] == 2:
            self.is_click(create_sale_order_detail_zjg['六_1_2_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_zjg['六_2_1_输入框'], six_info['二'])
        if six_info['三'][0] == 1:
            self.is_click(create_sale_order_detail_zjg['六_3_1_单选按钮'])
        elif six_info['三'][0] == 2:
            self.is_click(create_sale_order_detail_zjg['六_3_2_单选按钮'])
        elif six_info['三'][0] == 3:
            self.is_click(create_sale_order_detail_zjg['六_3_3_单选按钮'])
        elif six_info['三'][0] == 4:
            self.is_click(create_sale_order_detail_zjg['六_3_4_单选按钮'])
            self.input_text(create_sale_order_detail_zjg['六_3_4_输入框'], six_info['三'][1])
        else:
            raise ValueError('传值错误')

    def input_twelve_info(self, twelve_info):
        self.input_text(create_sale_order_detail_zjg['十二_5_输入框'], twelve_info['5'])

    def input_commission_confirmation_info(self, commission_confirmation_info):
        self.input_text(create_sale_order_detail_zjg['佣金确认书_佣金金额_输入框'], commission_confirmation_info['佣金金额'])
        self.is_click(create_sale_order_detail_zjg['佣金确认书_支付日期_选择框'])
        self.__choose_index_in_drop_down_box(commission_confirmation_info['支付日期'][0])
        if commission_confirmation_info['支付日期'][0] == 2:
            self.input_text(create_sale_order_detail_zjg['佣金确认书_支付日期_输入框'], commission_confirmation_info['支付日期'][1])

    def input_commission_confirmation2_info(self, commission_confirmation_info):
        self.input_text(create_sale_order_detail_zjg['佣金确认书二_佣金金额_输入框'], commission_confirmation_info['佣金金额'])
        self.is_click(create_sale_order_detail_zjg['佣金确认书二_支付日期_选择框'])
        self.__choose_index_in_drop_down_box(commission_confirmation_info['支付日期'][0])
        if commission_confirmation_info['支付日期'][0] == 2:
            self.input_text(create_sale_order_detail_zjg['佣金确认书二_支付日期_输入框'], commission_confirmation_info['支付日期'][1])

    def __choose_value_in_drop_down_box(self, choose_value):
        sleep(0.5)
        ele_list = self.find_elements(create_sale_order_detail_zjg['合同内容下拉框'])
        if choose_value == '':
            ele_list[0].click()
        else:
            for ele in ele_list:
                if ele.text == choose_value:
                    ele.click()
                    return True
            raise ValueError('传值错误')

    def __choose_index_in_drop_down_box(self, index=1):
        sleep(0.5)
        locator = "xpath", \
                  "(//div[contains(@class, 'ant-select-dropdown') and " \
                  "not(contains(@class, 'ant-select-dropdown-hidden'))]//div[@class='rc-virtual-list']" \
                  "//div[@class='ant-select-item-option-content'])[" + str(index + 1) + "]"
        self.is_click(locator)

    @staticmethod
    def date_handle(value):
        if isinstance(value, int):
            return dt_strftime_with_delta(value, "%Y-%m-%d")
        elif isinstance(value, str):
            if value == "":
                return dt_strftime("%Y-%m-%d")
            elif isinstance(value, datetime.date):
                return value
            else:
                raise ValueError('传值错误')
        else:
            raise ValueError('传值错误')
