#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: createsaleorder_hzpage.py
@date: 2021/8/20 0002
"""
import datetime
from utils.timeutil import sleep, dt_strftime, dt_strftime_with_delta
from page.webpage import WebPage
from common.readelement import Element

create_sale_order_detail_hz = Element('jrgj/web/contract/createsaleorder_hz')


class ContractCreateSaleOrderDetailHZPage(WebPage):

    def input_contract_content(self, test_data):
        """填写合同信息"""
        self.choose_house_administrative_region(test_data['房屋所属行政区'])
        self.input_buyer_info(test_data['房屋出卖人信息'])
        self.input_seller_info(test_data['房屋买受人信息'])
        self.input_first_info(test_data['第一条信息'])
        self.input_second_info(test_data['第二条信息'])
        self.input_third_info(test_data['第三条信息'])
        self.input_four_info(test_data['第四条信息'])
        self.input_five_info(test_data['第五条信息'])
        self.input_seven_info(test_data['第七条信息'])
        self.input_eight_info(test_data['第八条信息'])
        self.input_nine_info(test_data['第九条信息'])
        self.input_ten_info(test_data['第十条信息'])
        self.input_attachment_one_info(test_data['附件一信息'])
        self.input_supplementary_agreement_info(test_data['补充协议'])
        self.input_commission_confirmation_info(test_data['房地产经纪佣金确认书一'])
        self.input_commission_confirmation2_info(test_data['房地产经纪佣金确认书二'])

    def choose_house_administrative_region(self, region_info):
        """填写行政区信息"""
        self.click_element(create_sale_order_detail_hz['房屋所属行政区选择框'])
        self.__choose_value_in_drop_down_box(region_info)

    def input_buyer_info(self, buyer_info):
        """填写房屋出卖人信息"""
        self.input_text(create_sale_order_detail_hz['房屋出卖人_姓名输入框'], buyer_info['房屋出卖人_姓名'])
        self.input_text(create_sale_order_detail_hz['房屋出卖人_英文名输入框'], buyer_info['房屋出卖人_英文名'])
        self.click_element(create_sale_order_detail_hz['房屋出卖人_性别选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出卖人_性别'])
        self.input_text(create_sale_order_detail_hz['房屋出卖人_国籍输入框'], buyer_info['房屋出卖人_国籍'])
        self.click_element(create_sale_order_detail_hz['房屋出卖人_出生日期输入框'])
        self.input_text_with_enter(create_sale_order_detail_hz['房屋出卖人_出生日期输入框'], buyer_info['房屋出卖人_出生日期'])
        self.click_element(create_sale_order_detail_hz['房屋出卖人_证件名称选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出卖人_证件名称'])
        self.input_text(create_sale_order_detail_hz['房屋出卖人_证件号码输入框'], buyer_info['房屋出卖人_证件号码'])
        self.input_text(create_sale_order_detail_hz['房屋出卖人_联系电话输入框'], buyer_info['房屋出卖人_联系电话'])
        self.input_text(create_sale_order_detail_hz['房屋出卖人_电子邮箱输入框'], buyer_info['房屋出卖人_电子邮箱'])
        self.input_text(create_sale_order_detail_hz['房屋出卖人_通讯地址输入框'], buyer_info['房屋出卖人_通讯地址'])

    def input_seller_info(self, seller_info):
        """填写房屋买受人信息"""
        keys = seller_info.keys()
        if '房屋买受人' in keys:
            main_seller_info = seller_info['房屋买受人']
            self.input_text(create_sale_order_detail_hz['房屋买受人_姓名输入框'], main_seller_info['房屋买受人_姓名'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_英文名输入框'], main_seller_info['房屋买受人_英文名'])
            self.click_element(create_sale_order_detail_hz['房屋买受人_性别选择框'])
            self.__choose_value_in_drop_down_box(main_seller_info['房屋买受人_性别'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_国籍输入框'], main_seller_info['房屋买受人_国籍'])
            self.click_element(create_sale_order_detail_hz['房屋买受人_出生日期输入框'])
            self.input_text_with_enter(create_sale_order_detail_hz['房屋买受人_出生日期输入框'], main_seller_info['房屋买受人_出生日期'])
            self.click_element(create_sale_order_detail_hz['房屋买受人_证件名称选择框'])
            self.__choose_value_in_drop_down_box(main_seller_info['房屋买受人_证件名称'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_证件号码输入框'], main_seller_info['房屋买受人_证件号码'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_联系电话输入框'], main_seller_info['房屋买受人_联系电话'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_电子邮箱输入框'], main_seller_info['房屋买受人_电子邮箱'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_通讯地址输入框'], main_seller_info['房屋买受人_通讯地址'])
        if '共同买受人' in keys:
            common_sellers_info = seller_info['共同买受人']
            self.input_common_seller_info(common_sellers_info)

    def input_common_seller_info(self, common_sellers_info):
        """填写共同买受人信息"""
        for common_seller_info in common_sellers_info:
            self.click_element(create_sale_order_detail_hz['房屋买受人_添加共同买受人按钮'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_姓名输入框'], common_seller_info['共同买受人_姓名'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_英文名输入框'], common_seller_info['共同买受人_英文名'])
            self.click_element(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                           + str(common_sellers_info.index(common_seller_info) + 1)
                                                           + '_性别选择框'])
            self.__choose_value_in_drop_down_box(common_seller_info['共同买受人_性别'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_国籍输入框'], common_seller_info['共同买受人_国籍'])
            self.click_element(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                           + str(common_sellers_info.index(common_seller_info) + 1)
                                                           + '_出生日期输入框'])
            self.input_text_with_enter(
                create_sale_order_detail_hz['房屋买受人_共同买受人' + str(common_sellers_info.index(common_seller_info) + 1)
                                            + '_出生日期输入框'], common_seller_info['共同买受人_出生日期'])
            self.click_element(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                           + str(common_sellers_info.index(common_seller_info) + 1)
                                                           + '_证件名称选择框'])
            self.__choose_value_in_drop_down_box(common_seller_info['共同买受人_证件名称'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_证件号码输入框'], common_seller_info['共同买受人_证件号码'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_联系电话输入框'], common_seller_info['共同买受人_联系电话'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_电子邮箱输入框'], common_seller_info['共同买受人_电子邮箱'])
            self.input_text(create_sale_order_detail_hz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_通讯地址输入框'], common_seller_info['共同买受人_通讯地址'])

    def input_first_info(self, first_info):
        """填写第一条信息"""
        self.input_text(create_sale_order_detail_hz['一_1_输入框'], first_info['一'])
        self.click_element(create_sale_order_detail_hz['一_2_选择框'])
        self.__choose_value_in_drop_down_box(first_info['二'])
        self.input_text(create_sale_order_detail_hz['一_3_输入框'], first_info['三'])
        self.click_element(create_sale_order_detail_hz['一_4_选择框'])
        self.__choose_value_in_drop_down_box(first_info['四'])
        self.input_text(create_sale_order_detail_hz['一_5_输入框'], first_info['五'])
        self.input_text(create_sale_order_detail_hz['一_6_1_输入框'], first_info['六'][0])
        self.click_element(create_sale_order_detail_hz['一_6_2_选择框'])
        self.__choose_value_in_drop_down_box(first_info['六'][1])
        self.input_text(create_sale_order_detail_hz['一_6_3_输入框'], self.date_handle(first_info['六'][2]), enter=True)
        self.input_text(create_sale_order_detail_hz['一_6_4_输入框'], self.date_handle(first_info['六'][3]), enter=True)
        self.input_text(create_sale_order_detail_hz['一_7_输入框'], first_info['七'])

    def input_second_info(self, second_info):
        """填写第二条信息"""
        if second_info['一'][0] == 1:
            self.click_element(create_sale_order_detail_hz['二_1_1_单选按钮'])
        elif second_info['一'][0] == 2:
            self.click_element(create_sale_order_detail_hz['二_1_2_单选按钮'])
            self.input_text(create_sale_order_detail_hz['二_1_2_1_输入框'], second_info['一'][1])
        else:
            raise ValueError('传值错误')
        if second_info['二'][0] == 1:
            self.click_element(create_sale_order_detail_hz['二_2_1_单选按钮'])
        elif second_info['二'][0] == 2:
            self.click_element(create_sale_order_detail_hz['二_2_2_单选按钮'])
            self.input_text(create_sale_order_detail_hz['二_2_2_1_输入框'], second_info['二'][1])
            if second_info['二'][2][0] == 1:
                self.click_element(create_sale_order_detail_hz['二_2_2_2_选择框'])
                self.__choose_value_in_drop_down_box(1)
            else:
                raise ValueError('传值错误')
            self.input_text(create_sale_order_detail_hz['二_2_2_2_输入框'], self.date_handle(second_info['二'][2][1]),
                            enter=True)
            self.input_text(create_sale_order_detail_hz['二_2_2_3_输入框'], second_info['二'][3])
            if second_info['二'][4][0] == 1:
                self.click_element(create_sale_order_detail_hz['二_2_2_4_1_单选按钮'])
            elif second_info['二'][4][0] == 2:
                self.click_element(create_sale_order_detail_hz['二_2_2_4_2_单选按钮'])
                if second_info['二'][4][1][0] <= 2:
                    self.click_element(create_sale_order_detail_hz['二_2_2_4_2_1_选择框'])
                    self.__choose_index_in_drop_down_box(second_info['二'][4][1][0])
                    if second_info['二'][4][1][0] == 2:
                        self.input_text(create_sale_order_detail_hz['二_2_2_4_2_1_输入框'],
                                        self.date_handle(second_info['二'][4][1][1]), enter=True)
                else:
                    raise ValueError('传值错误')
            else:
                raise ValueError('传值错误')
        else:
            raise ValueError('传值错误')
        if second_info['三'][0] == 1:
            self.click_element(create_sale_order_detail_hz['二_3_1_单选按钮'])
        elif second_info['三'][0] == 2:
            self.click_element(create_sale_order_detail_hz['二_3_2_单选按钮'])
            self.input_text(create_sale_order_detail_hz['二_3_2_1_输入框'], second_info['三'][1])
        else:
            raise ValueError('传值错误')
        if second_info['四'][0] == 1:
            self.click_element(create_sale_order_detail_hz['二_4_1_单选按钮'])
            if second_info['四'][1][0] <= 2:
                self.click_element(create_sale_order_detail_hz['二_4_1_1_选择框'])
                self.__choose_index_in_drop_down_box(second_info['四'][1][0])
                if second_info['四'][1][0] == 1:
                    self.input_text(create_sale_order_detail_hz['二_4_1_1_输入框'],
                                    self.date_handle(second_info['四'][1][1]), enter=True)
            else:
                raise ValueError('传值错误')
        elif second_info['四'][0] == 2:
            self.click_element(create_sale_order_detail_hz['二_4_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        if second_info['五'][0] == 1:
            self.click_element(create_sale_order_detail_hz['二_5_1_单选按钮'])
        elif second_info['五'][0] == 2:
            self.click_element(create_sale_order_detail_hz['二_5_2_单选按钮'])
            if second_info['五'][1][0] <= 4:
                self.click_element(create_sale_order_detail_hz['二_5_2_1_选择框'])
                self.__choose_index_in_drop_down_box(second_info['五'][1][0])
                if second_info['五'][1][0] == 1:
                    self.input_text(create_sale_order_detail_hz['二_5_2_1_输入框'],
                                    self.date_handle(second_info['五'][1][0]), enter=True)
                if second_info['五'][1][0] == 4:
                    self.input_text(create_sale_order_detail_hz['二_5_2_1_输入框'], second_info['五'][1][1])
            else:
                raise ValueError('传值错误')
            self.input_text(create_sale_order_detail_hz['二_5_2_2_输入框'], second_info['五'][2])
        else:
            raise ValueError('传值错误')
        if second_info['六'][0] == 1:
            self.click_element(create_sale_order_detail_hz['二_6_1_单选按钮'])
            if second_info['六'][1] == 1:
                self.click_element(create_sale_order_detail_hz['二_6_1_1_单选按钮'])
            elif second_info['六'][1] == 2:
                self.click_element(create_sale_order_detail_hz['二_6_1_2_单选按钮'])
            else:
                raise ValueError('传值错误')
        elif second_info['六'][0] == 2:
            self.click_element(create_sale_order_detail_hz['二_6_2_单选按钮'])
            if second_info['六'][1] == 1:
                self.click_element(create_sale_order_detail_hz['二_6_2_1_单选按钮'])
            elif second_info['六'][1] == 2:
                self.click_element(create_sale_order_detail_hz['二_6_2_2_单选按钮'])
                self.input_text(create_sale_order_detail_hz['二_6_2_2_1_输入框'], second_info['六'][2])
            else:
                raise ValueError('传值错误')
        else:
            raise ValueError('传值错误')
        if second_info['七'][0] == 1:
            self.click_element(create_sale_order_detail_hz['二_7_1_单选按钮'])
        elif second_info['七'][0] == 2:
            self.click_element(create_sale_order_detail_hz['二_7_2_单选按钮'])
            self.input_text(create_sale_order_detail_hz['二_7_2_1_输入框'], second_info['七'][1])
            if second_info['七'][2] == 1:
                self.click_element(create_sale_order_detail_hz['二_7_2_2_1_单选按钮'])
            elif second_info['七'][2] == 2:
                self.click_element(create_sale_order_detail_hz['二_7_2_2_2_单选按钮'])
            elif second_info['七'][2] == 3:
                self.click_element(create_sale_order_detail_hz['二_7_2_2_3_单选按钮'])
                self.input_text(create_sale_order_detail_hz['二_7_2_2_3_输入框'], second_info['七'][3])
            else:
                raise ValueError('传值错误')
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['二_9_1_输入框'], self.date_handle(second_info['九'][0]), enter=True)
        self.input_text(create_sale_order_detail_hz['二_9_2_输入框'], self.date_handle(second_info['九'][1]), enter=True)

    def input_third_info(self, third_info):
        """填写第三条信息"""
        self.input_text(create_sale_order_detail_hz['三_1_输入框'], third_info)

    def input_four_info(self, four_info):
        """填写第四条信息"""
        if four_info['支付方式'] == 1:
            self.click_element(create_sale_order_detail_hz['四_1_单选按钮'])
            self.input_text(create_sale_order_detail_hz['四_1_1_输入框'], self.date_handle(four_info['一次性付款'][0]),
                            enter=True)
            self.input_text(create_sale_order_detail_hz['四_1_2_输入框'], four_info['一次性付款'][1])
            if four_info['一次性付款'][2] <= 3:
                self.click_element(create_sale_order_detail_hz['四_1_4_选择框'])
                self.__choose_index_in_drop_down_box(four_info['一次性付款'][2])
            else:
                raise ValueError('传值错误')
        elif four_info['支付方式'] == 2:
            self.click_element(create_sale_order_detail_hz['四_2_单选按钮'])
            self.input_text(create_sale_order_detail_hz['四_2_1_1_输入框'],
                            self.date_handle(four_info['贷款付款']['一'][0]), enter=True)
            self.input_text(create_sale_order_detail_hz['四_2_1_2_输入框'], four_info['贷款付款']['一'][1])
            if four_info['贷款付款'][2] <= 3:
                self.click_element(create_sale_order_detail_hz['四_2_1_4_选择框'])
                self.__choose_index_in_drop_down_box(four_info['贷款付款']['一'][2])
            else:
                raise ValueError('传值错误')
            self.input_text(create_sale_order_detail_hz['四_2_2_输入框'], self.date_handle(four_info['贷款付款']['二']),
                            enter=True)
            if four_info['贷款付款']['四'][0] == 1:
                self.click_element(create_sale_order_detail_hz['四_2_4_1_单选按钮'])
                self.input_text(create_sale_order_detail_hz['四_2_4_1_输入框'], four_info['贷款付款']['四'][1])
            elif four_info['贷款付款']['四'][0] == 2:
                self.click_element(create_sale_order_detail_hz['四_2_4_2_单选按钮'])
                self.input_text(create_sale_order_detail_hz['四_2_4_2_输入框'], four_info['贷款付款']['四'][1])
            else:
                raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['四_3_输入框'], four_info['结尾'])

    def input_five_info(self, five_info):
        """填写第五条信息"""
        self.input_text(create_sale_order_detail_hz['五_1_输入框'], self.date_handle(five_info['一_1']), enter=True)
        if five_info['一_2'][0] <= 3:
            self.click_element(create_sale_order_detail_hz['五_2_选择框'])
            self.__choose_index_in_drop_down_box(five_info['一_2'][0])
            if five_info['一_2'][0] == 3:
                self.input_text(create_sale_order_detail_hz['五_2_输入框'], five_info['一_2'][1])
        else:
            raise ValueError('传值错误')

    def input_seven_info(self, seven_info):
        """填写第七条信息"""
        if seven_info[0] <= 3:
            self.click_element(create_sale_order_detail_hz['七_1_选择框'])
            self.__choose_index_in_drop_down_box(seven_info[0])
            if seven_info[0] == 1:
                self.input_text(create_sale_order_detail_hz['七_1_输入框'], self.date_handle(seven_info[1]), enter=True)
            else:
                self.input_text(create_sale_order_detail_hz['七_1_输入框'], seven_info[1])
        else:
            raise ValueError('传值错误')

    def input_nine_info(self, nine_info):
        """填写第九条信息"""
        if nine_info[0] == 1:
            self.click_element(create_sale_order_detail_hz['九_1_单选按钮'])
        elif nine_info[0] == 2:
            self.click_element(create_sale_order_detail_hz['九_2_单选按钮'])
            self.input_text(create_sale_order_detail_hz['九_2_输入框'], nine_info[1])
        else:
            raise ValueError('传值错误')

    def input_eight_info(self, eight_info):
        """填写第八条信息"""
        if eight_info[0] == 1:
            self.click_element(create_sale_order_detail_hz['八_1_单选按钮'])
            self.input_text(create_sale_order_detail_hz['八_2_1_输入框'], eight_info[1])
            if eight_info[2] == 1:
                self.click_element(create_sale_order_detail_hz['八_1_2_1_单选按钮'])
            if eight_info[2] == 2:
                self.click_element(create_sale_order_detail_hz['八_1_2_2_单选按钮'])
            else:
                raise ValueError('传值错误')
            self.input_text(create_sale_order_detail_hz['八_1_3_输入框'], eight_info[3])
        elif eight_info[0] == 2:
            self.click_element(create_sale_order_detail_hz['八_2_单选按钮'])
            self.input_text(create_sale_order_detail_hz['八_2_1_输入框'], eight_info[1])
        else:
            raise ValueError('传值错误')

    def input_ten_info(self, ten_info):
        """填写第十条信息"""
        if ten_info['1_一'][0] == 1:
            self.click_element(create_sale_order_detail_hz['十_1_1_1_1_单选按钮'])
        elif ten_info['1_一'][0] == 2:
            self.click_element(create_sale_order_detail_hz['十_1_1_1_2_单选按钮'])
        elif ten_info['1_一'][0] == 3:
            self.click_element(create_sale_order_detail_hz['十_1_1_1_3_单选按钮'])
        elif ten_info['1_一'][0] == 4:
            self.click_element(create_sale_order_detail_hz['十_1_1_1_4_单选按钮'])
        elif ten_info['1_一'][0] == 5:
            self.click_element(create_sale_order_detail_hz['十_1_1_1_5_单选按钮'])
        else:
            raise ValueError('传值错误')
        if ten_info['1_二'] == 1:
            self.click_element(create_sale_order_detail_hz['十_1_1_2_1_单选按钮'])
        elif ten_info['1_二'] == 2:
            self.click_element(create_sale_order_detail_hz['十_1_1_2_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['十_1_2_输入框'], ten_info['1_二'])
        if ten_info['1_三'][0] == 1:
            self.click_element(create_sale_order_detail_hz['十_1_3_1_单选按钮'])
        elif ten_info['1_三'][0] == 2:
            self.click_element(create_sale_order_detail_hz['十_1_3_2_单选按钮'])
        elif ten_info['1_三'][0] == 3:
            self.click_element(create_sale_order_detail_hz['十_1_3_3_单选按钮'])
        elif ten_info['1_三'][0] == 4:
            self.click_element(create_sale_order_detail_hz['十_1_3_4_单选按钮'])
            self.input_text(create_sale_order_detail_hz['十_1_3_4_输入框'], ten_info['1_三'][1])
        else:
            raise ValueError('传值错误')
        if ten_info['1_四'][0] <= 2:
            self.click_element(create_sale_order_detail_hz['十_1_4_选择框'])
            self.__choose_index_in_drop_down_box(ten_info['1_四'][0])
            if ten_info['1_四'][0] == 2:
                self.input_text(create_sale_order_detail_hz['十_1_4_输入框'], ten_info['1_四'][1])
        else:
            raise ValueError('传值错误')

    def input_attachment_one_info(self, attachment_one_info):
        """填写附件一"""
        self.input_text(create_sale_order_detail_hz['附录一_1_1_输入框'], attachment_one_info['供水'])
        self.input_text(create_sale_order_detail_hz['附录一_1_2_输入框'], attachment_one_info['供电'])
        self.input_text(create_sale_order_detail_hz['附录一_1_3_输入框'], attachment_one_info['供燃气'])
        self.input_text(create_sale_order_detail_hz['附录一_1_4_1_输入框'], attachment_one_info['空调'][0])
        self.input_text(create_sale_order_detail_hz['附录一_1_4_2_输入框'], attachment_one_info['空调'][1])
        self.input_text(create_sale_order_detail_hz['附录一_1_4_3_输入框'], attachment_one_info['空调'][2])
        self.input_text(create_sale_order_detail_hz['附录一_1_5_输入框'], attachment_one_info['电视馈线'])
        self.input_text(create_sale_order_detail_hz['附录一_1_6_输入框'], attachment_one_info['电话'])
        self.input_text(create_sale_order_detail_hz['附录一_1_7_输入框'], attachment_one_info['互联网接入方式'])
        self.input_text(create_sale_order_detail_hz['附录一_1_8_输入框'], attachment_one_info['其他'])
        if attachment_one_info['三'][0] == 1:
            self.click_element(create_sale_order_detail_hz['附录一_3_1_1_单选按钮'])
        elif attachment_one_info['三'][0] == 2:
            self.click_element(create_sale_order_detail_hz['附录一_3_1_2_单选按钮'])
        elif attachment_one_info['三'][0] == 3:
            self.click_element(create_sale_order_detail_hz['附录一_3_1_3_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['附录一_3_2_输入框'], attachment_one_info['三'][1])
        self.input_text(create_sale_order_detail_hz['附录一_4_输入框'], attachment_one_info['四'])

    def input_supplementary_agreement_info(self, supplementary_agreement_info):
        """填写补充协议"""
        deposit_list = supplementary_agreement_info['一_定金']
        for m in range(len(deposit_list)):
            if deposit_list[m]['日期'][0] <= 6:
                choose1_locator = 'xpath', "//input[@id='earnest_" + str(m) + "_ac_b1_1_1']"
                self.click_element(choose1_locator)
                self.__choose_index_in_drop_down_box(deposit_list[m]['日期'][0])
                if deposit_list[m]['日期'][0] != 2:
                    input1_locator = 'xpath', "//input[@id='earnest_" + str(m) + "_b1_1_1']"
                    if deposit_list[m]['日期'][0] == 1:
                        self.input_text(input1_locator, self.date_handle(deposit_list[m]['日期'][1]), enter=True)
                    else:
                        self.input_text(input1_locator, deposit_list[m]['日期'][1])
            else:
                raise ValueError('传值错误')
            input2_locator = 'xpath', "//input[@id='earnest_" + str(m) + "_b1_1_2']"
            self.input_text(input2_locator, deposit_list[m]['金额'])
            if len(deposit_list) - m != 1:
                self.click_element(create_sale_order_detail_hz['补充协议_添加定金按钮'])
        house_payment_list = supplementary_agreement_info['一_房款']
        for n in range(len(house_payment_list)):
            if house_payment_list[n]['日期'][0] <= 6:
                choose1_locator = 'xpath', "//input[@id='housePayment_" + str(n) + "_ac_b1_1_1']"
                self.click_element(choose1_locator)
                self.__choose_index_in_drop_down_box(house_payment_list[n]['日期'][0])
                if house_payment_list[n]['日期'][0] != 2:
                    input1_locator = 'xpath', "//input[@id='housePayment_" + str(n) + "_b1_1_1']"
                    if house_payment_list[n]['日期'][0] == 1:
                        self.input_text(input1_locator, self.date_handle(house_payment_list[n]['日期'][1]), enter=True)
                    else:
                        self.input_text(input1_locator, house_payment_list[n]['日期'][1])
            else:
                raise ValueError('传值错误')
            input2_locator = 'xpath', "//input[@id='housePayment_" + str(n) + "_b1_1_2']"
            self.input_text(input2_locator, house_payment_list[n]['金额'])
            if len(house_payment_list) - n != 1:
                self.click_element(create_sale_order_detail_hz['补充协议_添加房款按钮'])
        if supplementary_agreement_info['一_交房保证金']['日期'][0] <= 6:
            self.click_element(create_sale_order_detail_hz['补充协议_1_3_1_选择框'])
            self.__choose_index_in_drop_down_box(supplementary_agreement_info['一_交房保证金']['日期'][0])
            if supplementary_agreement_info['一_交房保证金']['日期'][0] != 2:
                if supplementary_agreement_info['一_交房保证金']['日期'][0] == 1:
                    self.input_text(create_sale_order_detail_hz['补充协议_1_3_1_输入框'],
                                    self.date_handle(supplementary_agreement_info['一_交房保证金']['日期'][1]), enter=True)
                else:
                    self.input_text(create_sale_order_detail_hz['补充协议_1_3_1_输入框'],
                                    supplementary_agreement_info['一_交房保证金']['日期'][1])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['补充协议_1_3_2_输入框'], supplementary_agreement_info['一_交房保证金']['金额'])
        if supplementary_agreement_info['一_户口迁出保证金']['日期'][0] <= 6:
            self.click_element(create_sale_order_detail_hz['补充协议_1_4_1_选择框'])
            self.__choose_index_in_drop_down_box(supplementary_agreement_info['一_户口迁出保证金']['日期'][0])
            if supplementary_agreement_info['一_户口迁出保证金']['日期'][0] != 2:
                if supplementary_agreement_info['一_户口迁出保证金']['日期'][0] == 1:
                    self.input_text(create_sale_order_detail_hz['补充协议_1_4_1_输入框'],
                                    self.date_handle(supplementary_agreement_info['一_户口迁出保证金']['日期'][1]), enter=True)
                else:
                    self.input_text(create_sale_order_detail_hz['补充协议_1_4_1_输入框'],
                                    supplementary_agreement_info['一_户口迁出保证金']['日期'][1])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['补充协议_1_4_2_输入框'], supplementary_agreement_info['一_户口迁出保证金']['金额'])
        self.input_text(create_sale_order_detail_hz['补充协议_1_5_1_输入框'], supplementary_agreement_info['一_户名'])
        self.input_text(create_sale_order_detail_hz['补充协议_1_5_2_输入框'], supplementary_agreement_info['一_开户行'])
        self.input_text(create_sale_order_detail_hz['补充协议_1_5_3_输入框'], supplementary_agreement_info['一_账号'])
        if supplementary_agreement_info['三'][0] == 1:
            self.click_element(create_sale_order_detail_hz['补充协议_3_1_单选按钮'])
            self.input_text(create_sale_order_detail_hz['补充协议_3_1_1_输入框'], supplementary_agreement_info['三'][1])
            self.input_text(create_sale_order_detail_hz['补充协议_3_1_3_输入框'],
                            self.date_handle(supplementary_agreement_info['三'][2]), enter=True)
            self.input_text(create_sale_order_detail_hz['补充协议_3_1_4_输入框'],
                            self.date_handle(supplementary_agreement_info['三'][3]), enter=True)
            if supplementary_agreement_info['三'][4][0] == 1:
                self.click_element(create_sale_order_detail_hz['补充协议_3_1_5_1_1__输入框'])
                self.input_text(create_sale_order_detail_hz['补充协议_3_1_5_1_1__输入框'],
                                self.date_handle(supplementary_agreement_info['三'][4][1]), enter=True)
                if supplementary_agreement_info['三'][4][2] <= 3:
                    self.click_element(create_sale_order_detail_hz['补充协议_3_1_5_1_2__选择框'])
                    self.__choose_index_in_drop_down_box(supplementary_agreement_info['三'][4][2])
                    if supplementary_agreement_info['三'][4][2][0] == 1:
                        self.input_text(create_sale_order_detail_hz['补充协议_3_1_5_1_2__输入框'],
                                        self.date_handle(supplementary_agreement_info['三'][4][2][1]), enter=True)
                    if supplementary_agreement_info['三'][4][2][0] == 2:
                        self.input_text(create_sale_order_detail_hz['补充协议_3_1_5_1_2__输入框'],
                                        supplementary_agreement_info['三'][4][2][1])
                else:
                    raise ValueError('传值错误')
            elif supplementary_agreement_info['三'][4][0] == 2:
                self.click_element(create_sale_order_detail_hz['补充协议_3_1_5_2_单选按钮'])
                self.input_text(create_sale_order_detail_hz['补充协议_3_1_5_2_1_输入框'],
                                self.date_handle(supplementary_agreement_info['三'][4][1]), enter=True)
            else:
                raise ValueError('传值错误')
        elif supplementary_agreement_info['三'][0] == 2:
            self.click_element(create_sale_order_detail_hz['补充协议_3_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['补充协议_5_输入框'], supplementary_agreement_info['五'])

    def input_commission_confirmation_info(self, commission_confirmation_info):
        """填写第一份佣金确认书"""
        if commission_confirmation_info['车位'][0] == 1:
            self.click_element(create_sale_order_detail_hz['佣金确认书_车位_1_单选按钮'])
            self.input_text(create_sale_order_detail_hz['佣金确认书_车位_1_输入框'], commission_confirmation_info['车位'][1])
        elif commission_confirmation_info['车位'][0] == 1:
            self.click_element(create_sale_order_detail_hz['佣金确认书_车位_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['佣金确认书_佣金金额_输入框'], commission_confirmation_info['佣金金额'])
        if commission_confirmation_info['支付日期'][0] <= 2:
            self.click_element(create_sale_order_detail_hz['佣金确认书_支付日期_选择框'])
            self.__choose_index_in_drop_down_box(commission_confirmation_info['支付日期'][0])
            if commission_confirmation_info['支付日期'][0] == 2:
                self.input_text(create_sale_order_detail_hz['佣金确认书_支付日期_输入框'], commission_confirmation_info['支付日期'][1])
        else:
            raise ValueError('传值错误')

    def input_commission_confirmation2_info(self, commission_confirmation2_info):
        """填写第二份佣金确认书"""
        if commission_confirmation2_info['车位'][0] == 1:
            self.click_element(create_sale_order_detail_hz['佣金确认书二_车位_1_单选按钮'])
            self.input_text(create_sale_order_detail_hz['佣金确认书二_车位_1_输入框'], commission_confirmation2_info['车位'][1])
        elif commission_confirmation2_info['车位'][0] == 1:
            self.click_element(create_sale_order_detail_hz['佣金确认书二_车位_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_hz['佣金确认书二_佣金金额_输入框'], commission_confirmation2_info['佣金金额'])
        if commission_confirmation2_info['支付日期'][0] <= 2:
            self.click_element(create_sale_order_detail_hz['佣金确认书二_支付日期_选择框'])
            self.__choose_index_in_drop_down_box(commission_confirmation2_info['支付日期'][0])
            if commission_confirmation2_info['支付日期'][0] == 2:
                self.input_text(create_sale_order_detail_hz['佣金确认书二_支付日期_输入框'],
                                commission_confirmation2_info['支付日期'][1])
        else:
            raise ValueError('传值错误')

    def __choose_value_in_drop_down_box(self, choose_value):
        """下拉框内容选择"""
        sleep(0.5)
        ele_list = self.find_elements(create_sale_order_detail_hz['合同内容下拉框'])
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
        self.click_element(locator)

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
