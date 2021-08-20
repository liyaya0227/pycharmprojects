#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: createsaleorder_szpage.py
@date: 2021/7/2 0002
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

create_sale_order_detail_sz = Element('web/contract/createsaleorder_sz')


class ContractCreateSaleOrderDetailSZPage(WebPage):

    def input_contract_content(self, test_data):
        self.choose_house_administrative_region(test_data['房屋所属行政区'])
        self.input_buyer_info(test_data['房屋出卖人信息'])
        self.input_seller_info(test_data['房屋买受人信息'])
        self.input_first_info(test_data['第一条信息'])
        self.input_second_info(test_data['第二条信息'])
        self.input_third_info(test_data['第三条信息'])
        self.input_four_info(test_data['第四条信息'])
        self.input_five_info(test_data['第五条信息'])
        self.input_seven_info(test_data['第七条信息'])
        self.input_nine_info(test_data['第九条信息'])
        self.input_ten_info(test_data['第十条信息'])
        self.input_eleven_info(test_data['第十一条信息'])
        self.input_twelve_info(test_data['第十二条信息'])
        self.input_sixteen_info(test_data['第十六条信息'])
        self.input_special_info(test_data['特别告知'])
        self.input_attachment_two_info(test_data['附件二信息'])
        self.input_supplementary_agreement_info(test_data['补充协议'])
        self.input_commission_confirmation_info(test_data['房地产经纪佣金确认书一'])
        self.input_commission_confirmation2_info(test_data['房地产经纪佣金确认书二'])
        self.input_receipt_info(test_data['收据'])

    def choose_house_administrative_region(self, region_info):
        self.is_click(create_sale_order_detail_sz['房屋所属行政区选择框'])
        self.__choose_value_in_drop_down_box(region_info)

    def input_buyer_info(self, buyer_info):
        self.input_text(create_sale_order_detail_sz['房屋出卖人_姓名输入框'], buyer_info['房屋出卖人_姓名'])
        self.input_text(create_sale_order_detail_sz['房屋出卖人_英文名输入框'], buyer_info['房屋出卖人_英文名'])
        self.is_click(create_sale_order_detail_sz['房屋出卖人_性别选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出卖人_性别'])
        self.input_text(create_sale_order_detail_sz['房屋出卖人_国籍输入框'], buyer_info['房屋出卖人_国籍'])
        self.is_click(create_sale_order_detail_sz['房屋出卖人_出生日期输入框'])
        self.input_text_with_enter(create_sale_order_detail_sz['房屋出卖人_出生日期输入框'], buyer_info['房屋出卖人_出生日期'])
        self.is_click(create_sale_order_detail_sz['房屋出卖人_证件名称选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出卖人_证件名称'])
        self.input_text(create_sale_order_detail_sz['房屋出卖人_证件号码输入框'], buyer_info['房屋出卖人_证件号码'])
        self.input_text(create_sale_order_detail_sz['房屋出卖人_联系电话输入框'], buyer_info['房屋出卖人_联系电话'])
        self.input_text(create_sale_order_detail_sz['房屋出卖人_电子邮箱输入框'], buyer_info['房屋出卖人_电子邮箱'])
        self.input_text(create_sale_order_detail_sz['房屋出卖人_通讯地址输入框'], buyer_info['房屋出卖人_通讯地址'])

    def input_seller_info(self, seller_info):
        keys = seller_info.keys()
        if '房屋买受人' in keys:
            main_seller_info = seller_info['房屋买受人']
            self.input_text(create_sale_order_detail_sz['房屋买受人_姓名输入框'], main_seller_info['房屋买受人_姓名'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_英文名输入框'], main_seller_info['房屋买受人_英文名'])
            self.is_click(create_sale_order_detail_sz['房屋买受人_性别选择框'])
            self.__choose_value_in_drop_down_box(main_seller_info['房屋买受人_性别'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_国籍输入框'], main_seller_info['房屋买受人_国籍'])
            self.is_click(create_sale_order_detail_sz['房屋买受人_出生日期输入框'])
            self.input_text_with_enter(create_sale_order_detail_sz['房屋买受人_出生日期输入框'], main_seller_info['房屋买受人_出生日期'])
            self.is_click(create_sale_order_detail_sz['房屋买受人_证件名称选择框'])
            self.__choose_value_in_drop_down_box(main_seller_info['房屋买受人_证件名称'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_证件号码输入框'], main_seller_info['房屋买受人_证件号码'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_联系电话输入框'], main_seller_info['房屋买受人_联系电话'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_电子邮箱输入框'], main_seller_info['房屋买受人_电子邮箱'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_通讯地址输入框'], main_seller_info['房屋买受人_通讯地址'])
        if '共同买受人' in keys:
            common_sellers_info = seller_info['共同买受人']
            self.input_common_seller_info(common_sellers_info)

    def input_common_seller_info(self, common_sellers_info):
        for common_seller_info in common_sellers_info:
            self.is_click(create_sale_order_detail_sz['房屋买受人_添加共同买受人按钮'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_姓名输入框'], common_seller_info['共同买受人_姓名'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_英文名输入框'], common_seller_info['共同买受人_英文名'])
            self.is_click(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                      + str(common_sellers_info.index(common_seller_info) + 1)
                                                      + '_性别选择框'])
            self.__choose_value_in_drop_down_box(common_seller_info['共同买受人_性别'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_国籍输入框'], common_seller_info['共同买受人_国籍'])
            self.is_click(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                      + str(common_sellers_info.index(common_seller_info) + 1)
                                                      + '_出生日期输入框'])
            self.input_text_with_enter(
                create_sale_order_detail_sz['房屋买受人_共同买受人' + str(common_sellers_info.index(common_seller_info) + 1)
                                            + '_出生日期输入框'], common_seller_info['共同买受人_出生日期'])
            self.is_click(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                      + str(common_sellers_info.index(common_seller_info) + 1)
                                                      + '_证件名称选择框'])
            self.__choose_value_in_drop_down_box(common_seller_info['共同买受人_证件名称'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_证件号码输入框'], common_seller_info['共同买受人_证件号码'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_联系电话输入框'], common_seller_info['共同买受人_联系电话'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_电子邮箱输入框'], common_seller_info['共同买受人_电子邮箱'])
            self.input_text(create_sale_order_detail_sz['房屋买受人_共同买受人'
                                                        + str(common_sellers_info.index(common_seller_info) + 1)
                                                        + '_通讯地址输入框'], common_seller_info['共同买受人_通讯地址'])

    def input_first_info(self, first_info):
        self.is_click(create_sale_order_detail_sz['一_1_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['区'])
        self.input_text(create_sale_order_detail_sz['一_1_2_输入框'], first_info['详细地址'])
        self.input_text(create_sale_order_detail_sz['一_2_1_输入框'], first_info['房屋所有权证编号'])
        self.is_click(create_sale_order_detail_sz['一_3_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['土地使用权获得方式'])
        self.input_text(create_sale_order_detail_sz['一_3_2_输入框'], first_info['土地使用权证号'])
        self.is_click(create_sale_order_detail_sz['一_3_3_选择框'])
        if first_info['土地使用权终止日期'][0] == 1:
            self.__choose_value_in_special_drop_down_box(1)
            self.is_click(create_sale_order_detail_sz['一_3_3_输入框'])
            if first_info['土地使用权终止日期'][1] != '':
                self.input_text_with_enter(create_sale_order_detail_sz['一_3_3_输入框'], first_info['土地使用权终止日期'][1])
            else:
                raise ValueError('传值错误')
        elif first_info['土地使用权终止日期'][0] == 2:
            self.__choose_value_in_special_drop_down_box(2)
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_sz['一_4_1_输入框'], first_info['产权登记建筑面积'])
        self.is_click(create_sale_order_detail_sz['一_5_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['房屋用途'])
        self.is_click(create_sale_order_detail_sz['一_6_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['建筑结构'])
        self.is_click(create_sale_order_detail_sz['一_7_1_输入框'])
        self.input_text_with_enter(create_sale_order_detail_sz['一_7_1_输入框'], first_info['房屋建成年份'])
        self.input_text(create_sale_order_detail_sz['一_8_1_输入框'], first_info['产权登记附记内容'])

    def input_second_info(self, second_info):
        if second_info['房屋权证状况'][0] == 1:
            self.is_click(create_sale_order_detail_sz['二_1_1_单选按钮'])
        elif second_info['房屋权证状况'][0] == 2:
            self.is_click(create_sale_order_detail_sz['二_1_2_单选按钮'])
            self.input_text(create_sale_order_detail_sz['二_1_2_输入框'], second_info['房屋权证状况'][1])
        else:
            raise ValueError('传值错误')
        if second_info['房屋抵押状况'][0] == 1:
            self.is_click(create_sale_order_detail_sz['二_2_1_单选按钮'])
        elif second_info['房屋抵押状况'][0] == 2:
            self.is_click(create_sale_order_detail_sz['二_2_2_单选按钮'])
            self.is_click(create_sale_order_detail_sz['二_2_2_选择框'])
            if second_info['房屋抵押状况'][1][0] == 1:
                self.__choose_value_in_special_drop_down_box(1)
            else:
                raise ValueError('传值错误')
            self.is_click(create_sale_order_detail_sz['二_2_2_输入框'])
            self.input_text_with_enter(create_sale_order_detail_sz['二_2_2_输入框'], second_info['房屋抵押状况'][1][1])
        else:
            raise ValueError('传值错误')
        if second_info['房屋租赁状况'][0] == 1:
            self.is_click(create_sale_order_detail_sz['二_3_1_单选按钮'])
        elif second_info['房屋租赁状况'][0] == 2:
            self.is_click(create_sale_order_detail_sz['二_3_2_单选按钮'])
            self.input_text(create_sale_order_detail_sz['二_3_2_输入框'], second_info['房屋租赁状况'][1])
        else:
            raise ValueError('传值错误')
        if second_info['房屋居住权情况'][0] == 1:
            self.is_click(create_sale_order_detail_sz['二_10_1_单选按钮'])
        elif second_info['房屋居住权情况'][0] == 2:
            self.is_click(create_sale_order_detail_sz['二_10_2_单选按钮'])
            self.input_text(create_sale_order_detail_sz['二_10_2_1_输入框'], second_info['房屋居住权情况'][1][0])
            self.is_click(create_sale_order_detail_sz['二_10_2_2_选择框'])
            if second_info['房屋居住权情况'][1][1][0] <= 3:
                self.__choose_value_in_special_drop_down_box(second_info['房屋居住权情况'][1][1][0])
                self.input_text(create_sale_order_detail_sz['二_10_2_2_输入框'], second_info['房屋居住权情况'][1][1][1])
            else:
                raise ValueError('传值错误')
            if second_info['房屋居住权情况'][1][1] == 3:
                self.input_text(create_sale_order_detail_sz['二_10_2_2_选择框'], second_info['房屋居住权情况'][1][1][1])
        else:
            raise ValueError('传值错误')
        if second_info['房屋物业管理状况'] == 1:
            self.is_click(create_sale_order_detail_sz['二_4_1_单选按钮'])
        elif second_info['房屋物业管理状况'] == 2:
            self.is_click(create_sale_order_detail_sz['二_4_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        if second_info['房屋户籍状况'][0] == 1:
            self.is_click(create_sale_order_detail_sz['二_5_1_单选按钮'])
        elif second_info['房屋户籍状况'][0] == 2:
            self.is_click(create_sale_order_detail_sz['二_5_2_单选按钮'])
            self.is_click(create_sale_order_detail_sz['二_5_2_1_选择框'])
            if second_info['房屋户籍状况'][1][0] == 1:
                self.__choose_value_in_special_drop_down_box(1)
                self.input_text(create_sale_order_detail_sz['二_5_2_1_输入框'], second_info['房屋户籍状况'][1][1])
            else:
                raise ValueError('传值错误')
            self.input_text(create_sale_order_detail_sz['二_5_2_2_输入框'], second_info['房屋户籍状况'][2])
        else:
            raise ValueError('传值错误')
        if second_info['房屋维修资金状'][0] == 1:
            self.is_click(create_sale_order_detail_sz['二_6_1_单选按钮'])
            if second_info['房屋维修资金状'][1][0] == 1:
                self.is_click(create_sale_order_detail_sz['二_6_1_1_单选按钮'])
            elif second_info['房屋维修资金状'][1][0] == 2:
                self.is_click(create_sale_order_detail_sz['二_6_1_2_单选按钮'])
            else:
                raise ValueError('传值错误')
        elif second_info['房屋维修资金状'][0] == 2:
            self.is_click(create_sale_order_detail_sz['二_6_2_单选按钮'])
            if second_info['房屋维修资金状'][1][0] == 1:
                self.is_click(create_sale_order_detail_sz['二_6_2_1_单选按钮'])
            elif second_info['房屋维修资金状'][1][0] == 2:
                self.is_click(create_sale_order_detail_sz['二_6_2_2_单选按钮'])
                self.input_text(create_sale_order_detail_sz['二_6_2_2_输入框'], second_info['房屋维修资金状'][1][1])
            else:
                raise ValueError('传值错误')
        else:
            raise ValueError('传值错误')
        self.is_click(create_sale_order_detail_sz['二_8_1_输入框'])
        self.input_text_with_enter(create_sale_order_detail_sz['二_8_1_输入框'], second_info['费用已支付日期'])
        self.is_click(create_sale_order_detail_sz['二_8_2_输入框'])
        self.input_text_with_enter(create_sale_order_detail_sz['二_8_2_输入框'], second_info['费用支付开始日期'])

    def input_third_info(self, third_info):
        self.input_text(create_sale_order_detail_sz['三_1_输入框'], third_info['房屋价款'])

    def input_four_info(self, four_info):
        self.is_click(create_sale_order_detail_sz['四_单选按钮'])
        if four_info['选项'][0] == 1:
            self.is_click(create_sale_order_detail_sz['四_1_单选按钮'])
            if four_info['选项'][1][0] == 1:
                self.is_click(create_sale_order_detail_sz['四_1_1_选择框'])
                self.__choose_value_in_special_drop_down_box(1)
            else:
                raise ValueError('传值错误')
            self.is_click(create_sale_order_detail_sz['四_1_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_sz['四_1_1_输入框'], four_info['选项'][1][1])
        elif four_info['选项'][0] == 2:
            self.is_click(create_sale_order_detail_sz['四_2_单选按钮'])
            self.is_click(create_sale_order_detail_sz['四_2_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_sz['四_2_1_输入框'], four_info['选项'][1][0])
            self.input_text(create_sale_order_detail_sz['四_2_2_输入框'], four_info['选项'][1][1])
            if four_info['选项'][1][2] == 1:
                self.is_click(create_sale_order_detail_sz['四_2_4_选择框'])
                self.__choose_value_in_special_drop_down_box(four_info['选项'][1][2])
            else:
                raise ValueError('传值错误')
            self.is_click(create_sale_order_detail_sz['四_2_7_输入框'])
            self.input_text_with_enter(create_sale_order_detail_sz['四_2_7_输入框'], four_info['选项'][1][3])
        else:
            raise ValueError('传值错误')

    def input_five_info(self, five_info):
        self.input_text(create_sale_order_detail_sz['五_1_1_输入框'], five_info['逾期日期范围'])
        self.input_text(create_sale_order_detail_sz['五_1_2_输入框'], five_info['逾期支付百分比'])
        self.input_text(create_sale_order_detail_sz['五_1_3_输入框'], five_info['支付日期范围'])
        self.input_text(create_sale_order_detail_sz['五_2_2_输入框'], five_info['解除合同几日内'])
        self.input_text(create_sale_order_detail_sz['五_2_3_输入框'], five_info['支付违约金比例'])

    def input_seven_info(self, seven_info):
        self.is_click(create_sale_order_detail_sz['七_1_选择框'])
        index = seven_info['交付日期'][0]
        self.__choose_value_in_special_drop_down_box(index)
        if index == 1:
            self.is_click(create_sale_order_detail_sz['七_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_sz['七_1_输入框'], seven_info['交付日期'][1])
        else:
            self.input_text(create_sale_order_detail_sz['七_1_输入框'], seven_info['交付日期'][1])

    def input_nine_info(self, nine_info):
        if nine_info['选项'][0] == 1:
            self.is_click(create_sale_order_detail_sz['九_1_单选按钮'])
            self.input_text(create_sale_order_detail_sz['九_1_输入框'], nine_info['选项'][1])
            if nine_info['选项'][2] == 1:
                self.is_click(create_sale_order_detail_sz['九_2_1_单选按钮'])
            elif nine_info['选项'][2] == 2:
                self.is_click(create_sale_order_detail_sz['九_2_2_单选按钮'])
            else:
                raise ValueError("填值错误")
        elif nine_info['选项'][0] == 2:
            self.is_click(create_sale_order_detail_sz['九_2_单选按钮'])
            self.input_text(create_sale_order_detail_sz['九_2_输入框'],  nine_info['选项'][1])
        else:
            raise ValueError("填值错误")

    def input_ten_info(self, ten_info):
        if ten_info['选项'][0] == 1:
            self.is_click(create_sale_order_detail_sz['十_1_选择框'])
            self.__choose_value_in_special_drop_down_box(1)
            self.input_text(create_sale_order_detail_sz['十_1_输入框'], ten_info['选项'][1])
        else:
            raise ValueError("填值错误")

    def input_eleven_info(self, eleven_info):
        if eleven_info['选项'][0] == 1:
            self.is_click(create_sale_order_detail_sz['十一_1_单选按钮'])
        elif eleven_info['选项'][0] == 2:
            self.is_click(create_sale_order_detail_sz['十一_2_单选按钮'])
            self.input_text(create_sale_order_detail_sz['十一_2_输入框'], eleven_info['选项'][1])
        else:
            raise ValueError("选项填值错误")

    def input_twelve_info(self, twelve_info):
        if twelve_info['选项'][0][0] == 1:
            self.is_click(create_sale_order_detail_sz['十二_1_1_单选按钮'])
        elif twelve_info['选项'][0][0] == 2:
            self.is_click(create_sale_order_detail_sz['十二_1_2_单选按钮'])
        elif twelve_info['选项'][0][0] == 3:
            self.is_click(create_sale_order_detail_sz['十二_1_3_单选按钮'])
        elif twelve_info['选项'][0][0] == 4:
            self.is_click(create_sale_order_detail_sz['十二_1_4_单选按钮'])
            self.input_text(create_sale_order_detail_sz['十二_1_4_输入框'], twelve_info['选项'][0][1])
        else:
            raise ValueError("选项填值错误")
        if twelve_info['选项'][1] == 1:
            self.is_click(create_sale_order_detail_sz['十二_1_5_输入框'])
            self.__choose_value_in_special_drop_down_box(1)
        else:
            raise ValueError("选项填值错误")

    def input_sixteen_info(self, sixteen_info):
        if sixteen_info['选项'] == 1:
            self.is_click(create_sale_order_detail_sz['十六_1_单选按钮'])
        elif sixteen_info['选项'] == 2:
            self.is_click(create_sale_order_detail_sz['十六_2_单选按钮'])
        else:
            raise ValueError("选项填值错误")

    def input_special_info(self, special_info):
        self.input_text(create_sale_order_detail_sz['特别告知_输入框'], special_info['房产'])

    def input_attachment_two_info(self, attachment_two_info):
        if attachment_two_info['装修房或毛坯房'] == '装修房':
            self.is_click(create_sale_order_detail_sz['附件二_1_1_单选按钮'])
        elif attachment_two_info['装修房或毛坯房'] == '毛坯房':
            self.is_click(create_sale_order_detail_sz['附件二_1_2_单选按钮'])
        else:
            raise ValueError()
        if attachment_two_info['甲方或乙方'] == '甲方':
            self.is_click(create_sale_order_detail_sz['附件二_6_1_单选按钮'])
        elif attachment_two_info['甲方或乙方'] == '乙方':
            self.is_click(create_sale_order_detail_sz['附件二_6_2_单选按钮'])
        else:
            raise ValueError()

    def input_supplementary_agreement_info(self, supplementary_agreement_info):
        deposit_list = supplementary_agreement_info['定金']
        for pay in deposit_list:
            choose1_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='earnest_" \
                              + str(deposit_list.index(pay)) + "_AC_B1_1_1_1']"
            self.is_click(choose1_locator)
            date = pay['日期']
            self.__choose_value_in_special_drop_down_box(date[0])
            input1_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='earnest_" \
                             + str(deposit_list.index(pay)) + "_B1_1_1_1']"
            if date[0] == 1:
                self.is_click(input1_locator)
                self.input_text_with_enter(input1_locator, date[1])
            if date[0] != 1 and date[0] != 2:
                self.input_text(input1_locator, date[1])
            if date[0] > 6:
                raise ValueError("传参错误")
            input2_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='earnest_" \
                             + str(deposit_list.index(pay)) + "_B1_1_1_2']"
            self.input_text(input2_locator, pay['金额'])
            if pay['支付方式'] == 1:
                button1_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@name='earnest_" \
                              + str(deposit_list.index(pay)) + "_B1_1_1_4' and @id='B11142']"
                self.is_click(button1_locator)
                choose4_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='earnest_" \
                                  + str(deposit_list.index(pay)) + "_AC_B1_1_1_5']"
                self.is_click(choose4_locator)
                self.__choose_value_in_special_drop_down_box(1)
                input4_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='earnest_" \
                                 + str(deposit_list.index(pay)) + "_B1_1_1_5']"
                self.input_text(input4_locator, pay['其他'])
            elif pay['支付方式'] == 2:
                button2_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@name='earnest_" \
                              + str(deposit_list.index(pay)) + "_B1_1_1_4' and @id='B11143']"
                self.is_click(button2_locator)
            else:
                raise ValueError("传值错误")
            if len(deposit_list) - deposit_list.index(pay) != 1:
                self.is_click(create_sale_order_detail_sz['补充协议_1_1_1_定金按钮'])
        house_payment_list = supplementary_agreement_info['房款']
        for house_payment in house_payment_list:
            choose1_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='housePayment_" \
                              + str(house_payment_list.index(house_payment)) + "_AC_B1_1_1_1']"
            self.is_click(choose1_locator)
            date = house_payment['日期']
            self.__choose_value_in_special_drop_down_box(date[0])
            input1_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='housePayment_" \
                             + str(house_payment_list.index(house_payment)) + "_B1_1_1_1']"
            if date[0] == 1:
                self.is_click(input1_locator)
                self.input_text_with_enter(input1_locator, date[1])
            if date[0] != 1 and date[0] != 2:
                self.input_text(input1_locator, date[1])
            if date[0] > 6:
                raise ValueError("传参错误")
            input2_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='housePayment_" \
                             + str(house_payment_list.index(house_payment)) + "_B1_1_1_2']"
            self.input_text(input2_locator, house_payment['金额'])
            if house_payment['支付方式'] == 1:
                button1_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@name='housePayment_" \
                                  + str(house_payment_list.index(house_payment)) + "_B1_1_1_4' and @id='B11142']"
                self.is_click(button1_locator)
                choose4_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='housePayment_" \
                                  + str(house_payment_list.index(house_payment)) + "_AC_B1_1_1_5']"
                self.is_click(choose4_locator)
                self.__choose_value_in_special_drop_down_box(1)
                input4_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@id='housePayment_" \
                                 + str(house_payment_list.index(house_payment)) + "_B1_1_1_5']"
                self.input_text(input4_locator, house_payment['其他'])
            elif house_payment['支付方式'] == 2:
                button2_locator = 'xpath', "//div[@style='']//div[@id='B0']//input[@name='housePayment_" \
                                  + str(house_payment_list.index(house_payment)) + "_B1_1_1_4' and @id='B11143']"
                self.is_click(button2_locator)
            else:
                raise ValueError("传值错误")
            if len(house_payment_list) - house_payment_list.index(house_payment) != 1:
                self.is_click(create_sale_order_detail_sz['补充协议_1_1_1_房款按钮'])

        house_deposit = supplementary_agreement_info['交房保证金']
        self.is_click(create_sale_order_detail_sz['补充协议_1_5_1_选择框'])
        house_deposit_date = house_deposit['日期']
        self.__choose_value_in_special_drop_down_box(house_deposit_date[0])
        if house_deposit_date[0] == 1:
            self.is_click(create_sale_order_detail_sz['补充协议_1_5_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_sz['补充协议_1_5_1_输入框'], house_deposit_date[1])
        if house_deposit_date[0] != 1 and house_deposit_date[0] != 2:
            self.input_text(create_sale_order_detail_sz['补充协议_1_5_1_输入框'], house_deposit_date[1])
        if house_deposit_date[0] > 6:
            raise ValueError("传参错误")
        self.input_text(create_sale_order_detail_sz['补充协议_1_5_2_输入框'], house_deposit['金额'])
        if house_deposit['支付方式'] == 1:
            self.is_click(create_sale_order_detail_sz['补充协议_1_5_4_单选按钮'])
            self.is_click(create_sale_order_detail_sz['补充协议_1_5_6_选择框'])
            self.__choose_value_in_special_drop_down_box()
            self.input_text(create_sale_order_detail_sz['补充协议_1_5_6_输入框'], house_deposit['其他'])
        elif house_deposit['支付方式'] == 2:
            self.is_click(create_sale_order_detail_sz['补充协议_1_5_5_单选按钮'])
        else:
            raise ValueError("传值错误")
        resident_deposit = supplementary_agreement_info['户口迁出保证金']
        self.is_click(create_sale_order_detail_sz['补充协议_1_6_1_选择框'])
        resident_deposit_date = resident_deposit['日期']
        self.__choose_value_in_special_drop_down_box(resident_deposit_date[0])
        if resident_deposit_date[0] == 1:
            self.is_click(create_sale_order_detail_sz['补充协议_1_6_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_sz['补充协议_1_6_1_输入框'], resident_deposit_date[1])
        if resident_deposit_date[0] != 1 and resident_deposit_date[0] != 2:
            self.input_text(create_sale_order_detail_sz['补充协议_1_6_1_输入框'], resident_deposit_date[1])
        if resident_deposit_date[0] > 6:
            raise ValueError("传参错误")
        self.input_text(create_sale_order_detail_sz['补充协议_1_6_2_输入框'], resident_deposit['金额'])
        if resident_deposit['支付方式'] == 1:
            self.is_click(create_sale_order_detail_sz['补充协议_1_6_4_单选按钮'])
            self.is_click(create_sale_order_detail_sz['补充协议_1_6_6_选择框'])
            self.__choose_value_in_special_drop_down_box()
            self.input_text(create_sale_order_detail_sz['补充协议_1_6_6_输入框'], resident_deposit['其他'])
        elif resident_deposit['支付方式'] == 2:
            self.is_click(create_sale_order_detail_sz['补充协议_1_6_5_单选按钮'])
        else:
            raise ValueError("传值错误")
        self.input_text(create_sale_order_detail_sz['补充协议_1_户名_输入框'], supplementary_agreement_info['户名'])
        self.input_text(create_sale_order_detail_sz['补充协议_1_开户行_输入框'], supplementary_agreement_info['开户行'])
        self.input_text(create_sale_order_detail_sz['补充协议_1_账号_输入框'], supplementary_agreement_info['账号'])
        rent_status = supplementary_agreement_info['出租状态']
        if rent_status['是否'] == '是':
            self.is_click(create_sale_order_detail_sz['补充协议_4_1_单选按钮'])
        elif rent_status['是否'] == '否':
            self.is_click(create_sale_order_detail_sz['补充协议_4_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        taxation = supplementary_agreement_info['税费']
        if taxation['选项'] == 1:
            self.is_click(create_sale_order_detail_sz['补充协议_5_1_1_单选按钮'])
        elif taxation['选项'] == 2:
            self.is_click(create_sale_order_detail_sz['补充协议_5_1_2_单选按钮'])
        elif taxation['选项'] == 3:
            self.is_click(create_sale_order_detail_sz['补充协议_5_1_3_单选按钮'])
        elif taxation['选项'] == 4:
            self.is_click(create_sale_order_detail_sz['补充协议_5_1_4_单选按钮'])
        elif taxation['选项'] == 5:
            self.is_click(create_sale_order_detail_sz['补充协议_5_1_5_单选按钮'])
        else:
            raise ValueError('传值错误')
        if taxation['是否'] == '是':
            self.is_click(create_sale_order_detail_sz['补充协议_5_2_1_单选按钮'])
        elif taxation['是否'] == '否':
            self.is_click(create_sale_order_detail_sz['补充协议_5_2_2_单选按钮'])
        else:
            raise ValueError('传值错误')
        self.input_text(create_sale_order_detail_sz['补充协议_7_1_输入框'], supplementary_agreement_info['其他'])

    def input_commission_confirmation_info(self, commission_confirmation_info):
        self.input_text(create_sale_order_detail_sz['佣金确认书_甲方_输入框'], commission_confirmation_info['甲方'])
        # self.input_text(create_sale_order_detail_sz['佣金确认书_乙方_输入框'], commission_confirmation_info['乙方'])
        if commission_confirmation_info['车位'] == '否':
            self.is_click(create_sale_order_detail_sz['佣金确认书_车位_否_单选按钮'])
        elif commission_confirmation_info['车位'] == '是':
            self.is_click(create_sale_order_detail_sz['佣金确认书_车位_有_单选按钮'])
        else:
            raise ValueError("传值错误")
        self.input_text(create_sale_order_detail_sz['佣金确认书_佣金金额_输入框'], commission_confirmation_info['佣金金额'])
        self.is_click(create_sale_order_detail_sz['佣金确认书_支付日期_选择框'])
        self.__choose_value_in_special_drop_down_box(1)

    def input_commission_confirmation2_info(self, commission_confirmation_info):
        self.input_text(create_sale_order_detail_sz['佣金确认书二_甲方_输入框'], commission_confirmation_info['甲方'])
        # self.input_text(create_sale_order_detail_sz['佣金确认书二_乙方_输入框'], commission_confirmation_info['乙方'])
        if commission_confirmation_info['车位'] == '否':
            self.is_click(create_sale_order_detail_sz['佣金确认书二_车位_否_单选按钮'])
        elif commission_confirmation_info['车位'] == '是':
            self.is_click(create_sale_order_detail_sz['佣金确认书二_车位_有_单选按钮'])
        else:
            raise ValueError("传值错误")
        self.input_text(create_sale_order_detail_sz['佣金确认书二_佣金金额_输入框'], commission_confirmation_info['佣金金额'])
        self.is_click(create_sale_order_detail_sz['佣金确认书二_支付日期_选择框'])
        self.__choose_value_in_special_drop_down_box(1)

    def input_receipt_info(self, receipt_info):
        self.input_text(create_sale_order_detail_sz['收据_房屋出售人_输入框'], receipt_info['房屋出售人'])
        self.input_text(create_sale_order_detail_sz['收据_房屋买受人_输入框'], receipt_info['房屋买受人'])
        # self.input_text(create_sale_order_detail_sz['收据_定金_输入框'], receipt_info['定金'])
        collection_details = receipt_info['收款明细']
        if len(collection_details) < 4:
            for collection in collection_details:
                self.is_click(create_sale_order_detail_sz['收据_支付日期'
                                                          + str(collection_details.index(collection) + 1) + '_输入框'])
                self.input_text_with_enter(
                    create_sale_order_detail_sz['收据_支付日期' + str(collection_details.index(collection) + 1)
                                                + '_输入框'], collection['日期'])
                self.input_text(
                    create_sale_order_detail_sz['收据_支付金额' + str(collection_details.index(collection) + 1) + '_输入框'],
                    collection['金额'])
        else:
            raise ValueError("传值错误")

    def __choose_value_in_drop_down_box(self, choose_value):
        sleep(0.5)
        ele_list = self.find_elements(create_sale_order_detail_sz['合同内容下拉框'])
        if choose_value == '':
            ele_list[0].click()
        else:
            for ele in ele_list:
                if ele.text == choose_value:
                    ele.click()
                    return True
            raise ValueError('传值错误')

    def __choose_value_in_special_drop_down_box(self, index=1):
        sleep(0.5)
        ele_list = self.find_elements(create_sale_order_detail_sz['合同内容特殊下拉框'])
        ele_list[index-1].click()
