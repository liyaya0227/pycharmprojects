#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: createsaleorder_wxpage.py
@date: 2021/7/2 0002
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

create_sale_order_detail_wx = Element('contract/createsaleorder_wx')


class ContractCreateSaleOrderDetailWXPage(WebPage):

    def input_contract_content(self, test_data):
        self.choose_house_administrative_region(test_data['房屋所属行政区'])
        self.input_buyer_info(test_data['房屋出卖人信息'])
        self.input_seller_info(test_data['房屋买受人信息'])
        self.input_sign_date_info(test_data['签署日期'])
        self.input_first_info(test_data['第一条信息'])
        self.input_second_info(test_data['第二条信息'])
        self.input_third_info(test_data['第三条信息'])
        self.input_five_info(test_data['第五条信息'])
        self.input_six_info(test_data['第六条信息'])
        self.input_seven_info(test_data['第七条信息'])
        self.input_eight_info(test_data['第八条信息'])
        self.input_twelve_info(test_data['第十二条信息'])
        self.input_attachment_one_info(test_data['附件一信息'])
        self.input_commission_confirmation_info(test_data['房地产经纪佣金确认书一'])
        self.input_commission_confirmation2_info(test_data['房地产经纪佣金确认书二'])
        self.input_receipt_info(test_data['收据'])

    def choose_house_administrative_region(self, region_info):
        self.is_click(create_sale_order_detail_wx['房屋所属行政区选择框'])
        self.__choose_value_in_drop_down_box(region_info)

    def input_buyer_info(self, buyer_info):
        self.input_text(create_sale_order_detail_wx['房屋出卖人_姓名输入框'], buyer_info['房屋出卖人_姓名'])
        self.input_text(create_sale_order_detail_wx['房屋出卖人_英文名输入框'], buyer_info['房屋出卖人_英文名'])
        self.is_click(create_sale_order_detail_wx['房屋出卖人_性别选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出卖人_性别'])
        self.input_text(create_sale_order_detail_wx['房屋出卖人_国籍输入框'], buyer_info['房屋出卖人_国籍'])
        self.is_click(create_sale_order_detail_wx['房屋出卖人_出生日期输入框'])
        self.input_text_with_enter(create_sale_order_detail_wx['房屋出卖人_出生日期输入框'], buyer_info['房屋出卖人_出生日期'])
        self.is_click(create_sale_order_detail_wx['房屋出卖人_证件名称选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出卖人_证件名称'])
        self.input_text(create_sale_order_detail_wx['房屋出卖人_证件号码输入框'], buyer_info['房屋出卖人_证件号码'])
        self.input_text(create_sale_order_detail_wx['房屋出卖人_联系电话输入框'], buyer_info['房屋出卖人_联系电话'])
        self.input_text(create_sale_order_detail_wx['房屋出卖人_电子邮箱输入框'], buyer_info['房屋出卖人_电子邮箱'])
        self.input_text(create_sale_order_detail_wx['房屋出卖人_通讯地址输入框'], buyer_info['房屋出卖人_通讯地址'])

    def input_seller_info(self, seller_info):
        keys = seller_info.keys()
        if '房屋买受人' in keys:
            main_seller_info = seller_info['房屋买受人']
            self.input_text(create_sale_order_detail_wx['房屋买受人_姓名输入框'], main_seller_info['房屋买受人_姓名'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_英文名输入框'], main_seller_info['房屋买受人_英文名'])
            self.is_click(create_sale_order_detail_wx['房屋买受人_性别选择框'])
            self.__choose_value_in_drop_down_box(main_seller_info['房屋买受人_性别'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_国籍输入框'], main_seller_info['房屋买受人_国籍'])
            self.is_click(create_sale_order_detail_wx['房屋买受人_出生日期输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['房屋买受人_出生日期输入框'], main_seller_info['房屋买受人_出生日期'])
            self.is_click(create_sale_order_detail_wx['房屋买受人_证件名称选择框'])
            self.__choose_value_in_drop_down_box(main_seller_info['房屋买受人_证件名称'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_证件号码输入框'], main_seller_info['房屋买受人_证件号码'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_联系电话输入框'], main_seller_info['房屋买受人_联系电话'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_电子邮箱输入框'], main_seller_info['房屋买受人_电子邮箱'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_通讯地址输入框'], main_seller_info['房屋买受人_通讯地址'])
        if '共同买受人' in keys:
            common_sellers_info = seller_info['共同买受人']
            self.input_common_seller_info(common_sellers_info)

    def input_common_seller_info(self, common_sellers_info):
        for common_seller_info in common_sellers_info:
            self.is_click(create_sale_order_detail_wx['房屋买受人_添加共同买受人按钮'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_姓名输入框'], common_seller_info['共同买受人_姓名'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_英文名输入框'], common_seller_info['共同买受人_英文名'])
            self.is_click(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                      + str(common_sellers_info.index(common_seller_info) + 1)
                                                      + '_性别选择框'])
            self.__choose_value_in_drop_down_box(common_seller_info['共同买受人_性别'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_国籍输入框'], common_seller_info['共同买受人_国籍'])
            self.is_click(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                      + str(common_sellers_info.index(common_seller_info) + 1)
                                                      + '_出生日期输入框'])
            self.input_text_with_enter(
                create_sale_order_detail_wx['房屋买受人_共同买受人' + str(common_sellers_info.index(common_seller_info) + 1)
                                            + '_出生日期输入框'], common_seller_info['共同买受人_出生日期'])
            self.is_click(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                      + str(common_sellers_info.index(common_seller_info) + 1)
                                                      + '_证件名称选择框'])
            self.__choose_value_in_drop_down_box(common_seller_info['共同买受人_证件名称'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_证件号码输入框'], common_seller_info['共同买受人_证件号码'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_联系电话输入框'], common_seller_info['共同买受人_联系电话'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_电子邮箱输入框'], common_seller_info['共同买受人_电子邮箱'])
            self.input_text(create_sale_order_detail_wx['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_通讯地址输入框'], common_seller_info['共同买受人_通讯地址'])

    def input_sign_date_info(self, sign_date_info):
        self.is_click(create_sale_order_detail_wx['签署日期_输入框'])
        self.input_text_with_enter(create_sale_order_detail_wx['签署日期_输入框'], sign_date_info)

    def input_first_info(self, first_info):
        self.input_text(create_sale_order_detail_wx['一_1_1_输入框'], first_info['详细地址'])
        self.input_text(create_sale_order_detail_wx['一_1_2_输入框'], first_info['建筑面积'])
        if first_info['二'][0] == 1:
            self.is_click(create_sale_order_detail_wx['一_2_1_单选按钮'])
        elif first_info['二'][0] == 2:
            self.is_click(create_sale_order_detail_wx['一_2_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        if first_info['二'][1] == 1:
            self.is_click(create_sale_order_detail_wx['一_2_3_单选按钮'])
        elif first_info['二'][1] == 2:
            self.is_click(create_sale_order_detail_wx['一_2_4_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_wx['一_3_1_选择框'])
        self.__choose_value_in_special_drop_down_box(first_info['三'][0])
        if first_info['三'][0] == 7:
            self.input_text(create_sale_order_detail_wx['一_3_1_输入框'], first_info['三'][1])
        if first_info['三'][0] > 7:
            raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_wx['一_4_1_选择框'])
        self.__choose_value_in_special_drop_down_box(first_info['三'][0])
        if first_info['四'][0] == 5:
            self.input_text(create_sale_order_detail_wx['一_4_1_输入框'], first_info['四'][1])
        if first_info['四'][0] > 5:
            raise ValueError('传值错误')

    def input_second_info(self, second_info):
        if second_info['一_权属状况'][0] == 1:
            self.is_click(create_sale_order_detail_wx['二_1_1_1_单选按钮'])
        elif second_info['一_权属状况'][0] == 2:
            self.is_click(create_sale_order_detail_wx['二_1_1_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_wx['二_1_1_2_输入框'], second_info['一_权属状况'][1])
        if second_info['一_共有情况'] == 1:
            self.is_click(create_sale_order_detail_wx['二_1_2_1_单选按钮'])
        elif second_info['一_共有情况'] == 2:
            self.is_click(create_sale_order_detail_wx['二_1_2_2_单选按钮'])
        elif second_info['一_共有情况'] == 3:
            self.is_click(create_sale_order_detail_wx['二_1_2_3_单选按钮'])
        else:
            raise ValueError('传值错误')
        if second_info['一_持证方式'][0] == 1:
            self.is_click(create_sale_order_detail_wx['二_1_3_1_单选按钮'])
        elif second_info['一_持证方式'][0] == 2:
            self.is_click(create_sale_order_detail_wx['二_1_3_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_wx['二_1_3_2_输入框'], second_info['一_持证方式'][1])
        self.input_text(create_sale_order_detail_wx['二_2_1_输入框'], second_info['二_土地使用权证证号'])
        self.is_click(create_sale_order_detail_wx['二_2_2_选择框'])
        self.__choose_value_in_drop_down_box(second_info['二_获得方式'])
        self.is_click(create_sale_order_detail_wx['二_2_3_输入框'])
        self.input_text_with_enter(create_sale_order_detail_wx['二_2_3_输入框'], second_info['二_土地使用年限'])
        if second_info['三'][0] == 1:
            self.is_click(create_sale_order_detail_wx['二_3_1_1_单选按钮'])
        elif second_info['三'][0] == 2:
            self.is_click(create_sale_order_detail_wx['二_3_1_2_单选按钮'])
            # for value in second_info['三'][1]:
            #     flag = second_info['三'][1].index(value)
            #     if flag > 2:
            #         break
            #     self.input_text(create_sale_order_detail_wx['二_3_' + str(flag + 2) + '_1_输入框'], value[0])
            #     self.input_text(create_sale_order_detail_wx['二_3_' + str(flag + 2) + '_2_输入框'], value[1])
            self.is_click(create_sale_order_detail_wx['二_3_4_1_选择框'])
            if second_info['三'][1][0] == 1:
                self.__choose_value_in_special_drop_down_box(1)
            else:
                raise ValueError('传值错误')
            self.is_click(create_sale_order_detail_wx['二_3_4_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['二_3_4_1_输入框'], second_info['三'][1][1])
            if second_info['三'][2][0] == 1:
                self.is_click(create_sale_order_detail_wx['二_3_5_1_单选按钮'])
            elif second_info['三'][2][0] == 2:
                self.is_click(create_sale_order_detail_wx['二_3_5_2_单选按钮'])
                self.input_text(create_sale_order_detail_wx['二_3_5_2_输入框'], second_info['三'][2][1])
        else:
            raise ValueError('传值错误')
        if second_info['四'][0] == 1:
            self.is_click(create_sale_order_detail_wx['二_4_1_1_单选按钮'])
        elif second_info['四'][0] == 2:
            self.is_click(create_sale_order_detail_wx['二_4_1_2_单选按钮'])
            self.is_click(create_sale_order_detail_wx['二_4_2_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['二_4_2_1_输入框'], second_info['四'][1])
            self.input_text(create_sale_order_detail_wx['二_4_2_2_输入框'], second_info['四'][2])
            self.input_text(create_sale_order_detail_wx['二_4_2_3_输入框'], second_info['四'][3])
            if second_info['四'][4][0] == 1:
                self.is_click(create_sale_order_detail_wx['二_4_3_1_单选按钮'])
                self.input_text(create_sale_order_detail_wx['二_4_3_1_输入框'], second_info['四'][4][1])
            elif second_info['四'][4][0] == 2:
                self.is_click(create_sale_order_detail_wx['二_4_3_2_单选按钮'])
            else:
                raise ValueError('传值错误')
        else:
            raise ValueError('传值错误')
        if second_info['五'][0] == 1:
            self.is_click(create_sale_order_detail_wx['二_5_1_1_单选按钮'])
        elif second_info['五'][0] == 2:
            self.is_click(create_sale_order_detail_wx['二_5_1_2_单选按钮'])
            self.is_click(create_sale_order_detail_wx['二_5_2_1_选择框'])
            if second_info['五'][1][0] < 3:
                self.__choose_value_in_special_drop_down_box(second_info['五'][1][0])
            else:
                raise ValueError('传值错误')
            self.input_text(create_sale_order_detail_wx['二_5_2_1_输入框'], second_info['五'][1][1])
            # self.input_text(create_sale_order_detail_wx['二_5_2_2_输入框'], second_info['五'][2])
            # self.input_text(create_sale_order_detail_wx['二_5_2_3_输入框'], second_info['五'][3])
            # self.input_text(create_sale_order_detail_wx['二_5_2_4_输入框'], second_info['五'][4])
        else:
            raise ValueError('传值错误')
        if second_info['六_房屋居住权情况'][0] == 1:
            self.is_click(create_sale_order_detail_wx['二_6_1_1_单选按钮'])
        elif second_info['六_房屋居住权情况'][0] == 2:
            self.is_click(create_sale_order_detail_wx['二_6_1_2_单选按钮'])
            self.input_text(create_sale_order_detail_wx['二_6_1_2_输入框'], second_info['六_房屋居住权情况'][1])
        else:
            raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_wx['二_6_2_1_选择框'])
        self.__choose_value_in_special_drop_down_box(second_info['六_房屋居住处理方式'][0])
        if second_info['六_房屋居住处理方式'][0] == 3:
            self.input_text(create_sale_order_detail_wx['二_6_2_1_输入框'], second_info['六_房屋居住处理方式'][1])
        if second_info['六_房屋居住处理方式'][0] > 3:
            raise ValueError('传值错误')
        # if second_info['六_房屋居住处理方式'][0] == 1:
        #     self.is_click(create_sale_order_detail_wx['二_6_2_1_单选按钮'])
        # elif second_info['六_房屋居住处理方式'][0] == 2:
        #     self.is_click(create_sale_order_detail_wx['二_6_2_2_单选按钮'])
        # elif second_info['六_房屋居住处理方式'][0] == 3:
        #     self.is_click(create_sale_order_detail_wx['二_6_2_3_单选按钮'])
        #     self.input_text(create_sale_order_detail_wx['二_6_2_3_输入框'], second_info['六_房屋居住权情况'][1])
        # else:
        #     raise ValueError('传值错误')

    def input_third_info(self, third_info):
        if third_info['二'] == 1:
            self.is_click(create_sale_order_detail_wx['三_2_1_单选按钮'])
        elif third_info['二'] == 2:
            self.is_click(create_sale_order_detail_wx['三_2_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        # if third_info['三_漏水'][0] == 1:
        #     self.is_click(create_sale_order_detail_wx['三_3_1_1_单选按钮'])
        # elif third_info['三_漏水'][0] == 2:
        #     self.is_click(create_sale_order_detail_wx['三_3_1_2_单选按钮'])
        #     if 1 in third_info['三_漏水'][1]:
        #         self.is_click(create_sale_order_detail_wx['三_3_2_1_勾选框'])
        #     elif 2 in third_info['三_漏水'][1]:
        #         self.is_click(create_sale_order_detail_wx['三_3_2_2_勾选框'])
        #     elif 3 in third_info['三_漏水'][1]:
        #         self.is_click(create_sale_order_detail_wx['三_3_2_3_勾选框'])
        #     elif 4 in third_info['三_漏水'][1]:
        #         self.is_click(create_sale_order_detail_wx['三_3_2_4_勾选框'])
        #     elif 5 in third_info['三_漏水'][1]:
        #         self.is_click(create_sale_order_detail_wx['三_3_2_5_勾选框'])
        #     elif 6 in third_info['三_漏水'][1]:
        #         self.is_click(create_sale_order_detail_wx['三_3_2_6_勾选框'])
        #     else:
        #         raise ValueError('传值错误')
        # else:
        #     raise ValueError('传值错误')
        # if third_info['三_协商'][0] == 1:
        #     self.is_click(create_sale_order_detail_wx['三_3_3_1_单选按钮'])
        # elif third_info['三_协商'][0] == 2:
        #     self.is_click(create_sale_order_detail_wx['三_3_3_2_单选按钮'])
        #     if third_info['三_协商'][1] == 1:
        #         self.is_click(create_sale_order_detail_wx['三_3_3_2_1_单选按钮'])
        #     elif third_info['三_协商'][2] == 2:
        #         self.is_click(create_sale_order_detail_wx['三_3_3_2_2_单选按钮'])
        #     else:
        #         raise ValueError('传值错误')
        # else:
        #     raise ValueError('传值错误')
        # if third_info['四_起泡'][0] == 1:
        #     self.is_click(create_sale_order_detail_wx['三_4_1_1_单选按钮'])
        # elif third_info['四_起泡'][0] == 2:
        #     self.is_click(create_sale_order_detail_wx['三_4_1_2_单选按钮'])
        #     self.input_text(create_sale_order_detail_wx['三_4_1_2_输入框'], third_info['四_起泡'][1])
        # else:
        #     raise ValueError('传值错误')
        # if third_info['四_承担费用'] == 1:
        #     self.is_click(create_sale_order_detail_wx['三_4_2_1_单选按钮'])
        # elif third_info['四_承担费用'] == 2:
        #     self.is_click(create_sale_order_detail_wx['三_4_2_2_单选按钮'])
        # else:
        #     raise ValueError('传值错误')

    def input_five_info(self, five_info):
        self.input_text(create_sale_order_detail_wx['五_1_3_输入框'], five_info['一'])
        if five_info['二'] == 1:
            self.is_click(create_sale_order_detail_wx['五_2_1_单选按钮'])
        elif five_info['二'] == 2:
            self.is_click(create_sale_order_detail_wx['五_2_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        deposit_list = five_info['二_1']
        for i in range(len(deposit_list)):
            deposit = deposit_list[i]
            date1_locator = 'xpath', "//input[@id='earnest_" + str(deposit_list.index(deposit)) + "_c5_2_2_1_1']"
            self.is_click(date1_locator)
            self.input_text_with_enter(date1_locator, deposit[0])
            input1_locator = 'xpath', "//input[@id='earnest_" + str(deposit_list.index(deposit)) + "_c5_2_2_1_2']"
            self.input_text(input1_locator, deposit[1])
            if deposit[2] <= 4:
                button_locator = 'xpath', "//input[@name='earnest_" + str(deposit_list.index(deposit)) \
                                 + "_c5_2_2_1_4' and @id='c52214" + str(deposit[2]) + "']"
                self.is_click(button_locator)
            else:
                raise ValueError("传值错误")
            if len(deposit_list) - deposit_list.index(deposit) != 1:
                self.is_click(create_sale_order_detail_wx['五_2_1_1_定金按钮'])
        # for value in five_info['二_1']:
        #     if five_info['二_1'].index(value) == 0:
        #         flag = 1
        #     elif five_info['二_1'].index(value) == 1:
        #         flag = 5
        #     else:
        #         break
        #     if flag == 1:  # 区别时间选择框和输入框
        #         self.is_click(create_sale_order_detail_wx['五_2_1_1_' + str(flag) + '_输入框'])
        #         self.input_text_with_enter(create_sale_order_detail_wx['五_2_1_1_' + str(flag) + '_输入框'], value[0])
        #     if flag == 5:
        #         self.input_text(create_sale_order_detail_wx['五_2_1_1_' + str(flag) + '_输入框'], value[0])
        #     self.input_text(create_sale_order_detail_wx['五_2_1_1_' + str(flag + 1) + '_输入框'], value[1])
        #     if value[2] == 1:
        #         self.is_click(create_sale_order_detail_wx['五_2_1_1_' + str(flag + 3) + '_1_单选按钮'])
        #     elif value[2] == 2:
        #         self.is_click(create_sale_order_detail_wx['五_2_1_1_' + str(flag + 3) + '_2_单选按钮'])
        #     elif value[2] == 3:
        #         self.is_click(create_sale_order_detail_wx['五_2_1_1_' + str(flag + 3) + '_3_单选按钮'])
        #     else:
        #         raise ValueError('传值错误')
        for first_pay in five_info['二_2']:
            flag = str(five_info['二_2'].index(first_pay) + 1)
            self.is_click(create_sale_order_detail_wx['五_2_2_' + flag + '_1_选择框'])
            self.__choose_value_in_special_drop_down_box(first_pay[0][0])
            if first_pay[0][0] == 1 or first_pay[0][0] == 4:
                pass
            elif first_pay[0][0] == 2 or 4 < first_pay[0][0] < 8:
                self.input_text(create_sale_order_detail_wx['五_2_2_' + flag + '_1_输入框'], first_pay[0][1])
            elif first_pay[0][0] == 3:
                self.is_click(create_sale_order_detail_wx['五_2_2_' + flag + '_1_输入框'])
                self.input_text_with_enter(create_sale_order_detail_wx['五_2_2_' + flag + '_1_输入框'], first_pay[0][1])
            else:
                raise ValueError('传值错误')
            self.input_text(create_sale_order_detail_wx['五_2_2_' + flag + '_2_输入框'], first_pay[1])
            if first_pay[2] == 1:
                self.is_click(create_sale_order_detail_wx['五_2_2_' + flag + '_4_1_单选按钮'])
            elif first_pay[2] == 2:
                self.is_click(create_sale_order_detail_wx['五_2_2_' + flag + '_4_2_单选按钮'])
            elif first_pay[2] == 3:
                self.is_click(create_sale_order_detail_wx['五_2_2_' + flag + '_4_3_单选按钮'])
            elif first_pay[2] == 4:
                self.is_click(create_sale_order_detail_wx['五_2_2_' + flag + '_4_4_单选按钮'])
            else:
                raise ValueError('传值错误')
        # if len(five_info['二_3']) == 0:
        if not five_info['二_3']:
            pass
        else:
            if five_info['二_3'][0] == 1:
                self.is_click(create_sale_order_detail_wx['五_2_3_1_1_1_单选按钮'])
            elif five_info['二_3'][0] == 2:
                self.is_click(create_sale_order_detail_wx['五_2_3_1_1_2_单选按钮'])
            elif five_info['二_3'][0] == 3:
                self.is_click(create_sale_order_detail_wx['五_2_3_1_1_3_单选按钮'])
            else:
                raise ValueError('传值错误')
            self.input_text(create_sale_order_detail_wx['五_2_3_1_2_输入框'], five_info['二_3'][1])
            self.is_click(create_sale_order_detail_wx['五_2_3_1_4_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['五_2_3_1_4_输入框'], five_info['二_3'][2])
            if five_info['二_3'][3] == 1:
                self.is_click(create_sale_order_detail_wx['五_2_3_1_5_1_单选按钮'])
            elif five_info['二_3'][3] == 2:
                self.is_click(create_sale_order_detail_wx['五_2_3_1_5_2_单选按钮'])
            else:
                raise ValueError('传值错误')
            if five_info['二_3'][4][0] == 1:
                self.is_click(create_sale_order_detail_wx['五_2_3_2_1_单选按钮'])
                self.is_click(create_sale_order_detail_wx['五_2_3_2_1_选择框'])
                if five_info['二_3'][4][1][0] == 1:
                    self.__choose_value_in_special_drop_down_box(1)
                    self.is_click(create_sale_order_detail_wx['五_2_3_2_1_输入框'])
                    self.input_text_with_enter(create_sale_order_detail_wx['五_2_3_2_1_输入框'], five_info['二_3'][4][1][1])
                elif five_info['二_3'][4][1][0] == 2:
                    self.__choose_value_in_special_drop_down_box(2)
                    self.input_text(create_sale_order_detail_wx['五_2_3_2_1_输入框'], five_info['二_3'][4][1][1])
                else:
                    raise ValueError('传值错误')
            elif five_info['二_3'][4][0] == 2:
                self.is_click(create_sale_order_detail_wx['五_2_3_2_2_单选按钮'])
                self.input_text(create_sale_order_detail_wx['五_2_3_2_2_输入框'], five_info['二_3'][4][1])
            elif five_info['二_3'][4][0] == 3:
                self.is_click(create_sale_order_detail_wx['五_2_3_2_3_单选按钮'])
            else:
                raise ValueError('传值错误')

        self.input_text(create_sale_order_detail_wx['五_2_4_1_输入框'], five_info['二_4'][0])
        self.is_click(create_sale_order_detail_wx['五_2_4_3_选择框'])
        self.__choose_value_in_special_drop_down_box(five_info['二_4'][1][0])
        if five_info['二_4'][1][0] == 1:
            pass
        elif five_info['二_4'][1][0] == 2 or five_info['二_4'][1][0] == 4:
            self.input_text(create_sale_order_detail_wx['五_2_4_3_输入框'], five_info['二_4'][1][1])
        elif five_info['二_4'][1][0] == 3:
            self.is_click(create_sale_order_detail_wx['五_2_4_3_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['五_2_4_3_输入框'], five_info['二_4'][1][1])
        else:
            raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_wx['五_2_4_4_选择框'])
        if five_info['二_4'][2] <= 5:
            self.__choose_value_in_special_drop_down_box(five_info['二_4'][2])
        else:
            raise ValueError('传值错误')
        # if five_info['二_4'][2] == 1:
        #     self.is_click(create_sale_order_detail_wx['五_2_4_4_1_单选按钮'])
        # elif five_info['二_4'][2] == 2:
        #     self.is_click(create_sale_order_detail_wx['五_2_4_4_2_单选按钮'])
        # else:
        #     raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_wx['五_2_5_1_选择框'])
        self.__choose_value_in_special_drop_down_box(five_info['二_5'][0][0])
        if five_info['二_5'][0][0] == 1:
            pass
        elif five_info['二_5'][0][0] == 2 or five_info['二_5'][0][0] == 4:
            self.input_text(create_sale_order_detail_wx['五_2_5_1_输入框'], five_info['二_5'][0][1])
        elif five_info['二_5'][0][0] == 3:
            self.is_click(create_sale_order_detail_wx['五_2_5_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['五_2_5_1_输入框'], five_info['二_5'][0][1])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_wx['五_2_5_2_输入框'], five_info['二_5'][1])
        self.is_click(create_sale_order_detail_wx['五_2_5_4_选择框'])
        self.__choose_value_in_special_drop_down_box(five_info['二_5'][2][0])
        if five_info['二_5'][2][0] == 1:
            pass
        elif five_info['二_5'][2][0] == 2 or five_info['二_5'][2][0] == 4:
            self.input_text(create_sale_order_detail_wx['五_2_5_4_输入框'], five_info['二_5'][2][1])
        elif five_info['二_5'][2][0] == 3:
            self.is_click(create_sale_order_detail_wx['五_2_5_4_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['五_2_5_4_输入框'], five_info['二_5'][2][1])
        else:
            raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_wx['五_2_5_5_选择框'])
        if five_info['二_5'][3] <= 5:
            self.__choose_value_in_special_drop_down_box(five_info['二_5'][3])
        else:
            raise ValueError('传值错误')
        # if five_info['二_5'][3] == 1:
        #     self.is_click(create_sale_order_detail_wx['五_2_5_5_1_单选按钮'])
        # elif five_info['二_5'][3] == 2:
        #     self.is_click(create_sale_order_detail_wx['五_2_5_5_2_单选按钮'])
        # else:
        #     raise ValueError('传值错误')

    def input_six_info(self, six_info):
        self.is_click(create_sale_order_detail_wx['六_1_选择框'])
        self.__choose_value_in_special_drop_down_box(six_info['网签手续日期'][0])
        if six_info['网签手续日期'][0] == 1:
            self.is_click(create_sale_order_detail_wx['六_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['六_1_输入框'], six_info['网签手续日期'][1])
        elif six_info['网签手续日期'][0] == 2:
            self.input_text(create_sale_order_detail_wx['六_1_输入框'], six_info['网签手续日期'][1])
        else:
            raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_wx['六_2_选择框'])
        self.__choose_value_in_special_drop_down_box(six_info['转移登记日期'][0])
        if six_info['转移登记日期'][0] in [1, 2, 4, 5]:
            self.input_text(create_sale_order_detail_wx['六_2_输入框'], six_info['转移登记日期'][1])
        elif six_info['转移登记日期'][0] == 3:
            self.is_click(create_sale_order_detail_wx['六_2_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['六_2_输入框'], six_info['转移登记日期'][1])
        else:
            raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_wx['六_3_选择框'])
        self.__choose_value_in_special_drop_down_box(six_info['登记手续日期'][0])
        if six_info['登记手续日期'][0] in [2, 4]:
            self.input_text(create_sale_order_detail_wx['六_3_输入框'], six_info['登记手续日期'][1])
        elif six_info['登记手续日期'][0] == 3:
            self.is_click(create_sale_order_detail_wx['六_2_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['六_3_输入框'], six_info['登记手续日期'][1])
        elif six_info['登记手续日期'][0] == 1:
            pass
        else:
            raise ValueError('传值错误')

    def input_seven_info(self, seven_info):
        self.is_click(create_sale_order_detail_wx['七_1_1_选择框'])
        self.__choose_value_in_special_drop_down_box(seven_info['一'][0])
        if seven_info['一'][0] == 1:
            self.is_click(create_sale_order_detail_wx['七_1_2_输入框'])
            self.input_text_with_enter(create_sale_order_detail_wx['七_1_2_输入框'], seven_info['一'][1])
        elif seven_info['一'][0] in [2, 3, 4, 5]:
            self.input_text(create_sale_order_detail_wx['七_1_2_输入框'], seven_info['一'][1])
        else:
            raise ValueError('传值错误')
        if seven_info['三'] == 1:
            self.is_click(create_sale_order_detail_wx['七_3_2_1_单选按钮'])
        elif seven_info['三'] == 2:
            self.is_click(create_sale_order_detail_wx['七_3_2_2_单选按钮'])
        elif seven_info['三'] == 3:
            self.is_click(create_sale_order_detail_wx['七_3_2_3_单选按钮'])
        else:
            raise ValueError('传值错误')

    def input_eight_info(self, eight_info):
        if 1 in eight_info['一_1']:
            self.is_click(create_sale_order_detail_wx['八_1_1_1_勾选框'])
        if 2 in eight_info['一_1']:
            self.is_click(create_sale_order_detail_wx['八_1_1_2_勾选框'])
        if 3 in eight_info['一_1']:
            self.is_click(create_sale_order_detail_wx['八_1_1_3_勾选框'])
        if 4 in eight_info['一_1']:
            self.is_click(create_sale_order_detail_wx['八_1_1_4_勾选框'])
        if 5 in eight_info['一_1']:
            self.is_click(create_sale_order_detail_wx['八_1_1_5_勾选框'])
        if eight_info['一_2'] == 1:
            self.is_click(create_sale_order_detail_wx['八_1_2_1_单选按钮'])
        elif eight_info['一_2'] == 2:
            self.is_click(create_sale_order_detail_wx['八_1_2_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        if eight_info['一_3'] == 1:
            self.is_click(create_sale_order_detail_wx['八_1_3_1_单选按钮'])
        elif eight_info['一_3'] == 2:
            self.is_click(create_sale_order_detail_wx['八_1_3_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        if eight_info['一_4'] == 1:
            self.is_click(create_sale_order_detail_wx['八_1_4_1_单选按钮'])
        elif eight_info['一_4'] == 2:
            self.is_click(create_sale_order_detail_wx['八_1_4_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        if eight_info['二_税费'][0] == 1:
            self.is_click(create_sale_order_detail_wx['八_2_1_1_单选按钮'])
        elif eight_info['二_税费'][0] == 2:
            self.is_click(create_sale_order_detail_wx['八_2_1_2_单选按钮'])
        elif eight_info['二_税费'][0] == 3:
            self.is_click(create_sale_order_detail_wx['八_2_1_3_单选按钮'])
        elif eight_info['二_税费'][0] == 4:
            self.is_click(create_sale_order_detail_wx['八_2_1_4_单选按钮'])
            self.input_text(create_sale_order_detail_wx['八_2_1_4_输入框'], eight_info['二_税费'][1])
        else:
            raise ValueError('传值错误')
        # if eight_info['二_新税费'] == 1:
        #     self.is_click(create_sale_order_detail_wx['八_2_2_1_单选按钮'])
        # elif eight_info['二_新税费'] == 2:
        #     self.is_click(create_sale_order_detail_wx['八_2_2_2_单选按钮'])
        # elif eight_info['二_新税费'] == 3:
        #     self.is_click(create_sale_order_detail_wx['八_2_2_3_单选按钮'])
        # else:
        #     raise ValueError('传值错误')

    def input_twelve_info(self, twelve_info):
        self.input_text(create_sale_order_detail_wx['十二_1_输入框'], twelve_info['一'])
        self.is_click(create_sale_order_detail_wx['十二_2_选择框'])
        if twelve_info['二'][0] <= 3:
            self.__choose_value_in_special_drop_down_box(twelve_info['二'][0])
            self.input_text(create_sale_order_detail_wx['十二_2_输入框'], twelve_info['二'][1])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_wx['十二_3_输入框'], twelve_info['三'])

    def input_attachment_one_info(self, attachment_one_info):
        self.input_text(create_sale_order_detail_wx['附件一_家具_书桌_数量'], attachment_one_info['书桌'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家具_餐桌_数量'], attachment_one_info['餐桌'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家具_茶几_数量'], attachment_one_info['茶几'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家具_床_数量'], attachment_one_info['床'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家具_沙发_数量'], attachment_one_info['沙发'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家具_衣柜_数量'], attachment_one_info['衣柜'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家具_床垫_数量'], attachment_one_info['床垫'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家具_椅子_数量'], attachment_one_info['椅子'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家具_梳妆台_数量'], attachment_one_info['梳妆台'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_电视机_数量'], attachment_one_info['电视机'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_空调_数量'], attachment_one_info['空调'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_冰箱_数量'], attachment_one_info['冰箱'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_洗衣机_数量'], attachment_one_info['洗衣机'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_油烟机_数量'], attachment_one_info['油烟机'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_灶台_数量'], attachment_one_info['灶台'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_微波炉_数量'], attachment_one_info['微波炉'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_电脑_数量'], attachment_one_info['电脑'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_音响_数量'], attachment_one_info['音响'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_饮水机_数量'], attachment_one_info['饮水机'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_灯具_数量'], attachment_one_info['灯具'][1])
        self.input_text(create_sale_order_detail_wx['附件一_家电_机顶盒_数量'], attachment_one_info['机顶盒'][1])

    def input_commission_confirmation_info(self, commission_confirmation_info):
        self.input_text(create_sale_order_detail_wx['佣金确认书_车位_输入框'], commission_confirmation_info['车位'])
        # if commission_confirmation_info['交易类型'] == 1:
        #     self.is_click(create_sale_order_detail_wx['佣金确认书_交易类型_出售_单选按钮'])
        # elif commission_confirmation_info['交易类型'] == 2:
        #     self.is_click(create_sale_order_detail_wx['佣金确认书_交易类型_购买_单选按钮'])
        # elif commission_confirmation_info['交易类型'] == 3:
        #     self.is_click(create_sale_order_detail_wx['佣金确认书_交易类型_转让_单选按钮'])
        # else:
        #     raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_wx['佣金确认书_佣金金额_输入框'], commission_confirmation_info['佣金金额'])
        self.is_click(create_sale_order_detail_wx['佣金确认书_支付日期_选择框'])
        self.__choose_value_in_special_drop_down_box(commission_confirmation_info['支付日期'][0])
        if commission_confirmation_info['支付日期'][0] == 2:
            self.input_text(create_sale_order_detail_wx['佣金确认书_支付日期_输入框'], commission_confirmation_info['支付日期'][1])
        elif commission_confirmation_info['支付日期'][0] == 1:
            pass
        else:
            raise ValueError('传值错误')

    def input_commission_confirmation2_info(self, commission_confirmation2_info):
        self.input_text(create_sale_order_detail_wx['佣金确认书二_车位_输入框'], commission_confirmation2_info['车位'])
        # if commission_confirmation2_info['交易类型'] == 1:
        #     self.is_click(create_sale_order_detail_wx['佣金确认书二_交易类型_出售_单选按钮'])
        # elif commission_confirmation2_info['交易类型'] == 2:
        #     self.is_click(create_sale_order_detail_wx['佣金确认书二_交易类型_购买_单选按钮'])
        # elif commission_confirmation2_info['交易类型'] == 3:
        #     self.is_click(create_sale_order_detail_wx['佣金确认书二_交易类型_转让_单选按钮'])
        # else:
        #     raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_wx['佣金确认书二_佣金金额_输入框'], commission_confirmation2_info['佣金金额'])
        self.is_click(create_sale_order_detail_wx['佣金确认书二_支付日期_选择框'])
        self.__choose_value_in_special_drop_down_box(commission_confirmation2_info['支付日期'][0])
        if commission_confirmation2_info['支付日期'][0] == 2:
            self.input_text(create_sale_order_detail_wx['佣金确认书二_支付日期_输入框'],
                            commission_confirmation2_info['支付日期'][1])
        elif commission_confirmation2_info['支付日期'][0] == 1:
            pass
        else:
            raise ValueError('传值错误')

    def input_receipt_info(self, receipt_info):
        self.is_click(create_sale_order_detail_wx['收据_日期_输入框'])
        self.input_text_with_enter(create_sale_order_detail_wx['收据_日期_输入框'], receipt_info['日期'])
        collection_details = receipt_info['收款明细']
        if 0 < len(collection_details) < 4:
            for collection in collection_details:
                self.is_click(create_sale_order_detail_wx['收据_支付日期' + str(collection_details.index(collection) + 1)
                                                          + '_输入框'])
                self.input_text_with_enter(
                    create_sale_order_detail_wx['收据_支付日期' + str(collection_details.index(collection) + 1)
                                                + '_输入框'], collection['日期'])
                self.input_text(create_sale_order_detail_wx['收据_支付金额'
                                                            + str(collection_details.index(collection) + 1)
                                                            + '_输入框'], collection['金额'])
        else:
            raise ValueError('传值错误')

    def __choose_value_in_drop_down_box(self, choose_value):
        ele_list = self.find_elements(create_sale_order_detail_wx['合同内容下拉框'])
        for ele in ele_list:
            if ele.text == choose_value:
                ele.click()
                sleep()
                break

    def __choose_value_in_special_drop_down_box(self, index=1):
        ele_list = self.find_elements(create_sale_order_detail_wx['合同内容特殊下拉框'])
        ele_list[index-1].click()
        sleep()
