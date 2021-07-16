#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: createrentorderpage.py
@date: 2021/7/13 0013
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

create_rent_order = Element('contract/createrentorder')


class ContractCreateRentOrderPage(WebPage):

    def input_contract_content(self, test_data):
        self.input_buyer_info(test_data['房屋出租方信息'])
        self.input_seller_info(test_data['房屋承租方信息'])
        self.input_first_info(test_data['第一条信息'])
        self.input_second_info(test_data['第二条信息'])
        self.input_third_info(test_data['第三条信息'])
        self.input_four_info(test_data['第四条信息'])
        self.input_five_info(test_data['第五条信息'])
        self.input_six_info(test_data['第六条信息'])
        self.input_nine_info(test_data['第九条信息'])
        self.input_ten_info(test_data['第十条信息'])
        self.input_twelve_info(test_data['第十二条信息'])

    def input_buyer_info(self, buyer_info):
        self.input_text(create_rent_order['房屋出租方_姓名输入框'], buyer_info['房屋出租方_姓名'])
        self.input_text(create_rent_order['房屋出租方_英文名输入框'], buyer_info['房屋出租方_英文名'])
        self.is_click(create_rent_order['房屋出租方_性别选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出租方_性别'])
        self.input_text(create_rent_order['房屋出租方_国籍输入框'], buyer_info['房屋出租方_国籍'])
        self.is_click(create_rent_order['房屋出租方_出生日期输入框'])
        self.input_text_with_enter(create_rent_order['房屋出租方_出生日期输入框'], buyer_info['房屋出租方_出生日期'])
        self.is_click(create_rent_order['房屋出租方_证件名称选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出租方_证件名称'])
        self.input_text(create_rent_order['房屋出租方_证件号码输入框'], buyer_info['房屋出租方_证件号码'])
        self.input_text(create_rent_order['房屋出租方_联系电话输入框'], buyer_info['房屋出租方_联系电话'])
        self.input_text(create_rent_order['房屋出租方_电子邮箱输入框'], buyer_info['房屋出租方_电子邮箱'])
        self.input_text(create_rent_order['房屋出租方_通讯地址输入框'], buyer_info['房屋出租方_通讯地址'])

    def input_seller_info(self, seller_info):
        self.input_text(create_rent_order['房屋承租方_姓名输入框'], seller_info['房屋承租方_姓名'])
        self.input_text(create_rent_order['房屋承租方_英文名输入框'], seller_info['房屋承租方_英文名'])
        self.is_click(create_rent_order['房屋承租方_性别选择框'])
        self.__choose_value_in_drop_down_box(seller_info['房屋承租方_性别'])
        self.input_text(create_rent_order['房屋承租方_国籍输入框'], seller_info['房屋承租方_国籍'])
        self.is_click(create_rent_order['房屋承租方_出生日期输入框'])
        self.input_text_with_enter(create_rent_order['房屋承租方_出生日期输入框'], seller_info['房屋承租方_出生日期'])
        self.is_click(create_rent_order['房屋承租方_证件名称选择框'])
        self.__choose_value_in_drop_down_box(seller_info['房屋承租方_证件名称'])
        self.input_text(create_rent_order['房屋承租方_证件号码输入框'], seller_info['房屋承租方_证件号码'])
        self.input_text(create_rent_order['房屋承租方_联系电话输入框'], seller_info['房屋承租方_联系电话'])
        self.input_text(create_rent_order['房屋承租方_电子邮箱输入框'], seller_info['房屋承租方_电子邮箱'])
        self.input_text(create_rent_order['房屋承租方_通讯地址输入框'], seller_info['房屋承租方_通讯地址'])

    def input_first_info(self, first_info):
        self.is_click(create_rent_order['一_1_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['区'])
        self.input_text(create_rent_order['一_1_2_输入框'], first_info['详细地址'])
        self.input_text(create_rent_order['一_1_3_输入框'], first_info['建筑面积'])
        self.input_text(create_rent_order['一_2_1_输入框'], first_info['所有权证书编号'])
        self.input_text(create_rent_order['一_2_2_输入框'], first_info['房屋来源证明名称'])
        self.input_text(create_rent_order['一_2_3_输入框'], first_info['房屋所有权人'])
        if first_info['抵押情况'] == 1:
            self.is_click(create_rent_order['一_2_4_1_单选按钮'])
        elif first_info['抵押情况'] == 2:
            self.is_click(create_rent_order['一_2_4_2_单选按钮'])
        else:
            raise ValueError("选项填值错误")

    def input_second_info(self, second_info):
        self.input_text(create_rent_order['二_1_1_输入框'], second_info['租赁用途'])
        self.input_text(create_rent_order['二_1_2_输入框'], second_info['居住人数'])
        self.input_text(create_rent_order['二_1_3_输入框'], second_info['最多人数'])

    def input_third_info(self, third_info):
        self.is_click(create_rent_order['三_1_1_输入框'])
        self.input_text_with_enter(create_rent_order['三_1_1_输入框'], third_info['开始日期'])
        self.is_click(create_rent_order['三_1_2_输入框'])
        self.input_text_with_enter(create_rent_order['三_1_2_输入框'], third_info['结束日期'])
        self.input_text(create_rent_order['三_1_3_输入框'], third_info['三'])
        self.input_text(create_rent_order['三_1_4_输入框'], third_info['四'])

    def input_four_info(self, four_info):
        self.input_text(create_rent_order['四_1_1_1_输入框'], four_info['租金_人民币'])
        if four_info['租金_支付方式'] == 1:
            self.is_click(create_rent_order['四_1_2_1_单选按钮'])
        elif four_info['租金_支付方式'] == 2:
            self.is_click(create_rent_order['四_1_2_2_单选按钮'])
        elif four_info['租金_支付方式'] == 3:
            self.is_click(create_rent_order['四_1_2_3_单选按钮'])
        else:
            raise ValueError("选项填值错误")
        self.input_text(create_rent_order['四_1_3_1_输入框'], four_info['租金_押'])
        self.input_text(create_rent_order['四_1_3_2_输入框'], four_info['租金_付'])
        self.input_text(create_rent_order['四_1_4_输入框'], four_info['租金_支付日期'])
        self.input_text(create_rent_order['四_2_1_输入框'], four_info['押金_人民币'])

    def input_five_info(self, five_info):
        if 1 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_1_勾选框'])
        if 2 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_2_勾选框'])
        if 3 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_3_勾选框'])
        if 4 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_4_勾选框'])
        if 5 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_5_勾选框'])
        if 6 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_6_勾选框'])
        if 7 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_7_勾选框'])
        if 8 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_8_勾选框'])
        if 9 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_9_勾选框'])
        if 10 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_10_勾选框'])
        if 11 in five_info['出租方承担费用']:
            self.is_click(create_rent_order['五_1_11_勾选框'])
        if five_info['出租方承担其他费用'] != "":
            self.is_click(create_rent_order['五_1_12_勾选框'])
            self.input_text(create_rent_order['五_1_12_输入框'], five_info['出租方承担其他费用'])
        if 1 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_1_勾选框'])
        if 2 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_2_勾选框'])
        if 3 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_3_勾选框'])
        if 4 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_4_勾选框'])
        if 5 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_5_勾选框'])
        if 6 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_6_勾选框'])
        if 7 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_7_勾选框'])
        if 8 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_8_勾选框'])
        if 9 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_9_勾选框'])
        if 10 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_10_勾选框'])
        if 11 in five_info['承租方承担费用']:
            self.is_click(create_rent_order['五_2_11_勾选框'])
        if five_info['承租方承担其他费用'] != "":
            self.is_click(create_rent_order['五_2_12_勾选框'])
            self.input_text(create_rent_order['五_2_12_输入框'], five_info['承租方承担其他费用'])

    def input_six_info(self, six_info):
        self.input_text(create_rent_order['六_2_1_1_1_输入框'], six_info['出租方_金额'])
        if six_info['出租方_支付方式'] == 1:
            self.is_click(create_rent_order['六_2_1_2_1_单选按钮'])
        elif six_info['出租方_支付方式'] == 2:
            self.is_click(create_rent_order['六_2_1_2_2_单选按钮'])
        elif six_info['出租方_支付方式'] == 3:
            self.is_click(create_rent_order['六_2_1_2_3_单选按钮'])
        else:
            raise ValueError("选项填值错误")
        self.input_text(create_rent_order['六_2_2_1_1_输入框'], six_info['承租方_金额'])
        if six_info['承租方_支付方式'] == 1:
            self.is_click(create_rent_order['六_2_2_2_1_单选按钮'])
        elif six_info['承租方_支付方式'] == 2:
            self.is_click(create_rent_order['六_2_2_2_2_单选按钮'])
        elif six_info['承租方_支付方式'] == 3:
            self.is_click(create_rent_order['六_2_2_2_3_单选按钮'])
        else:
            raise ValueError("选项填值错误")

    def input_nine_info(self, nine_info):
        self.input_text(create_rent_order['九_5_1_输入框'], nine_info['一'])
        self.input_text(create_rent_order['九_5_2_输入框'], nine_info['二'])

    def input_ten_info(self, ten_info):
        self.input_text(create_rent_order['十_1_1_输入框'], ten_info['一_1'])
        self.input_text(create_rent_order['十_1_2_输入框'], ten_info['一_2'])
        self.input_text(create_rent_order['十_3_1_输入框'], ten_info['三'])

    def input_twelve_info(self, twelve_info):
        self.input_text(create_rent_order['十二_输入框'], twelve_info['其他约定事项'])

    def __choose_value_in_drop_down_box(self, choose_value):
        ele_list = self.find_elements(create_rent_order['合同内容下拉框'])
        if choose_value == '':
            ele_list[0].click()
            sleep()
        else:
            for ele in ele_list:
                if ele.text == choose_value:
                    ele.click()
                    sleep()
                    break
