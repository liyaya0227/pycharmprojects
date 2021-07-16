#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: createsaleorder_kspage.py
@date: 2021/7/2 0002
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

create_sale_order_detail_ks = Element('contract/createsaleorder_ks')


class ContractCreateSaleOrderDetailKSPage(WebPage):

    def input_contract_content(self, test_data):
        self.input_buyer_info(test_data['房屋出租方信息'])
        self.input_seller_info(test_data['房屋承租方信息'])
        self.input_first_info(test_data['第一条信息'])
        self.input_second_info(test_data['第二条信息'])
        self.input_third_info(test_data['第三条信息'])
        self.input_four_info(test_data['第四条信息'])
        self.input_five_info(test_data['第五条信息'])
        self.input_six_info(test_data['第六条信息'])
        self.input_ten_info(test_data['第十条信息'])
        self.input_eleven_info(test_data['第十一条信息'])
        self.input_twelve_info(test_data['第十二条信息'])
        self.input_thirteen_info(test_data['第十三条信息'])
        self.input_attachment_two_info(test_data['附件二信息'])
        self.input_supplementary_agreement_info(test_data['补充协议'])
        self.input_commission_confirmation_info(test_data['房地产经纪佣金确认书'])
        self.input_commission_confirmation2_info(test_data['房地产经纪佣金确认书'])
        self.input_receipt_info(test_data['收据'])

    def input_buyer_info(self, buyer_info):
        self.input_text(create_sale_order_detail_ks['房屋出租方_姓名输入框'], buyer_info['房屋出租方_姓名'])
        self.input_text(create_sale_order_detail_ks['房屋出租方_英文名输入框'], buyer_info['房屋出租方_英文名'])
        self.is_click(create_sale_order_detail_ks['房屋出租方_性别选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出租方_性别'])
        self.input_text(create_sale_order_detail_ks['房屋出租方_国籍输入框'], buyer_info['房屋出租方_国籍'])
        self.is_click(create_sale_order_detail_ks['房屋出租方_出生日期输入框'])
        self.input_text_with_enter(create_sale_order_detail_ks['房屋出租方_出生日期输入框'], buyer_info['房屋出租方_出生日期'])
        self.is_click(create_sale_order_detail_ks['房屋出租方_证件名称选择框'])
        self.__choose_value_in_drop_down_box(buyer_info['房屋出租方_证件名称'])
        self.input_text(create_sale_order_detail_ks['房屋出租方_证件号码输入框'], buyer_info['房屋出租方_证件号码'])
        self.input_text(create_sale_order_detail_ks['房屋出租方_联系电话输入框'], buyer_info['房屋出租方_联系电话'])
        self.input_text(create_sale_order_detail_ks['房屋出租方_电子邮箱输入框'], buyer_info['房屋出租方_电子邮箱'])
        self.input_text(create_sale_order_detail_ks['房屋出租方_通讯地址输入框'], buyer_info['房屋出租方_通讯地址'])

    def input_seller_info(self, seller_info):
        self.input_text(create_sale_order_detail_ks['房屋承租方_姓名输入框'], seller_info['房屋承租方_姓名'])
        self.input_text(create_sale_order_detail_ks['房屋承租方_英文名输入框'], seller_info['房屋承租方_英文名'])
        self.is_click(create_sale_order_detail_ks['房屋承租方_性别选择框'])
        self.__choose_value_in_drop_down_box(seller_info['房屋承租方_性别'])
        self.input_text(create_sale_order_detail_ks['房屋承租方_国籍输入框'], seller_info['房屋承租方_国籍'])
        self.is_click(create_sale_order_detail_ks['房屋承租方_出生日期输入框'])
        self.input_text_with_enter(create_sale_order_detail_ks['房屋承租方_出生日期输入框'], seller_info['房屋承租方_出生日期'])
        self.is_click(create_sale_order_detail_ks['房屋承租方_证件名称选择框'])
        self.__choose_value_in_drop_down_box(seller_info['房屋承租方_证件名称'])
        self.input_text(create_sale_order_detail_ks['房屋承租方_证件号码输入框'], seller_info['房屋承租方_证件号码'])
        self.input_text(create_sale_order_detail_ks['房屋承租方_联系电话输入框'], seller_info['房屋承租方_联系电话'])
        self.input_text(create_sale_order_detail_ks['房屋承租方_电子邮箱输入框'], seller_info['房屋承租方_电子邮箱'])
        self.input_text(create_sale_order_detail_ks['房屋承租方_通讯地址输入框'], seller_info['房屋承租方_通讯地址'])

    def input_first_info(self, first_info):
        self.is_click(create_sale_order_detail_ks['一_1_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['区'])
        self.input_text(create_sale_order_detail_ks['一_1_2_输入框'], first_info['详细地址'])
        self.input_text(create_sale_order_detail_ks['一_2_1_输入框'], first_info['房屋所有权证编号'])
        self.input_text(create_sale_order_detail_ks['一_3_1_输入框'], first_info['土地使用权证编号'])
        self.is_click(create_sale_order_detail_ks['一_4_1_输入框'])
        self.input_text_with_enter(create_sale_order_detail_ks['一_4_1_输入框'], first_info['土地使用权终止日期'])
        self.input_text(create_sale_order_detail_ks['一_5_1_输入框'], first_info['产权登记面积'])
        self.is_click(create_sale_order_detail_ks['一_6_1_选择框'])
        self.__choose_value_in_drop_down_box(first_info['房屋性质'])
        self.input_text(create_sale_order_detail_ks['一_7_1_输入框'], first_info['产权登记附记内容'])

    def input_second_info(self, second_info):
        if second_info['权证状况'][0] == 1:
            self.is_click(create_sale_order_detail_ks['二_1_1_单选按钮'])
        elif second_info['权证状况'][0] == 2:
            self.is_click(create_sale_order_detail_ks['二_1_2_单选按钮'])
        else:
            raise ValueError("选项填值错误")
        if second_info['抵押状况'][0] == 1:
            self.is_click(create_sale_order_detail_ks['二_2_1_单选按钮'])
        elif second_info['抵押状况'][0] == 2:
            self.is_click(create_sale_order_detail_ks['二_2_2_单选按钮'])
        else:
            raise ValueError("选项填值错误")
        if second_info['租赁状况'][0] == 1:
            self.is_click(create_sale_order_detail_ks['二_3_1_单选按钮'])
        elif second_info['租赁状况'][0] == 2:
            self.is_click(create_sale_order_detail_ks['二_3_2_单选按钮'])
        else:
            raise ValueError("选项填值错误")
        if second_info['物业管理状况'][0] == 1:
            self.is_click(create_sale_order_detail_ks['二_4_1_单选按钮'])
        elif second_info['物业管理状况'][0] == 2:
            self.is_click(create_sale_order_detail_ks['二_4_2_单选按钮'])
        else:
            raise ValueError("选项填值错误")

    def input_third_info(self, third_info):
        self.input_text(create_sale_order_detail_ks['三_小写_输入框'], third_info['人民币小写'])

    def input_four_info(self, four_info):
        self.is_click(create_sale_order_detail_ks['四_1_1_输入框'])
        self.input_text_with_enter(create_sale_order_detail_ks['四_1_1_输入框'], four_info['支付日期'])
        self.input_text(create_sale_order_detail_ks['四_1_2_输入框'], four_info['购房定金'])
        if four_info['支付方式'][0] == 1:
            self.is_click(create_sale_order_detail_ks['四_2_1_单选按钮'])
            if four_info['支付方式'][1] == 1:
                self.is_click(create_sale_order_detail_ks['四_2_1_1_单选按钮'])
                value = four_info['支付方式'][2]
                self.is_click(create_sale_order_detail_ks['四_2_1_2_选择框'])
                self.__choose_value_in_special_drop_down_box(value[0])
                self.input_text(create_sale_order_detail_ks['四_2_1_2_输入框'], value[1])

    def input_five_info(self, five_info):
        self.input_text(create_sale_order_detail_ks['五_1_1_输入框'], five_info['逾期日期范围'])
        self.input_text(create_sale_order_detail_ks['五_1_2_输入框'], five_info['逾期支付百分比'])
        self.input_text(create_sale_order_detail_ks['五_2_2_输入框'], five_info['支付日期范围'])
        self.input_text(create_sale_order_detail_ks['五_2_3_输入框'], five_info['支付违约金比例'])
        self.input_text(create_sale_order_detail_ks['五_2_4_输入框'], five_info['支付违约金倍数'])

    def input_six_info(self, six_info):
        self.is_click(create_sale_order_detail_ks['六_1_1_选择框'])
        index = six_info['腾空房屋'][0]
        self.__choose_value_in_special_drop_down_box(index)
        if index == 1:
            self.is_click(create_sale_order_detail_ks['六_1_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_ks['六_1_1_输入框'], six_info['腾空房屋'][1])
        else:
            self.input_text(create_sale_order_detail_ks['六_1_1_输入框'], six_info['腾空房屋'][1])
        if 1 in six_info['条约']:
            self.is_click(create_sale_order_detail_ks['六_2_1_勾选框'])
        if 2 in six_info['条约']:
            self.is_click(create_sale_order_detail_ks['六_2_2_勾选框'])
        if 3 in six_info['条约']:
            self.is_click(create_sale_order_detail_ks['六_2_3_勾选框'])
        if six_info['其他'] != "":
            self.is_click(create_sale_order_detail_ks['六_2_4_勾选框'])
            self.input_text(create_sale_order_detail_ks['六_2_4_勾选框'], six_info['其他'])

    def input_ten_info(self, ten_info):
        self.input_text(create_sale_order_detail_ks['十_1_输入框'], ten_info['日期'])
        self.input_text(create_sale_order_detail_ks['十_2_输入框'], ten_info['违约金'])

    def input_eleven_info(self, eleven_info):
        self.input_text(create_sale_order_detail_ks['十一_1_输入框'], eleven_info['日期'])

    def input_twelve_info(self, twelve_info):
        self.input_text(create_sale_order_detail_ks['十二_1_1_输入框'], twelve_info['性质类型'])
        if twelve_info['处理方式'][0] == 1:
            self.is_click(create_sale_order_detail_ks['十二_2_1_单选按钮'])
        elif twelve_info['处理方式'][0] == 2:
            self.is_click(create_sale_order_detail_ks['十二_2_2_单选按钮'])
            self.input_text(create_sale_order_detail_ks['十二_2_2_输入框'], twelve_info['处理方式'][1])
        else:
            raise ValueError("选项填值错误")

    def input_thirteen_info(self, thirteen_info):
        if 1 in thirteen_info['选项']:
            self.is_click(create_sale_order_detail_ks['十三_1_1_单选按钮'])
        elif 2 in thirteen_info['选项']:
            self.is_click(create_sale_order_detail_ks['十三_1_2_单选按钮'])
        elif 3 in thirteen_info['选项']:
            self.is_click(create_sale_order_detail_ks['十三_1_3_单选按钮'])
        else:
            raise ValueError("填入的值不对")
        if thirteen_info['其他'] != "":
            self.is_click(create_sale_order_detail_ks['十三_1_4_单选按钮'])
            self.input_text(create_sale_order_detail_ks['十三_2_2_输入框'], thirteen_info['其他'])

    def input_fourteen_info(self, sixteen_info):
        self.input_text(create_sale_order_detail_ks['十四_2_2_输入框'], sixteen_info['日期'])

    def input_attachment_two_info(self, attachment_two_info):
        if attachment_two_info['1'][0] == 1:
            self.is_click(create_sale_order_detail_ks['附件二_1_1_单选按钮'])
            self.input_text(create_sale_order_detail_ks['附件二_1_1_输入框'], attachment_two_info['1'][1])
        elif attachment_two_info['1'][0] == 2:
            self.is_click(create_sale_order_detail_ks['附件二_1_2_单选按钮'])
            self.is_click(create_sale_order_detail_ks['附件二_1_2_输入框'])
            self.input_text_with_enter(create_sale_order_detail_ks['附件二_1_2_输入框'], attachment_two_info['1'][1])
        else:
            raise ValueError()
        if attachment_two_info['3'][0] == 1:
            self.is_click(create_sale_order_detail_ks['附件二_3_1_单选按钮'])
            if attachment_two_info['3'][1] == 1:
                self.is_click(create_sale_order_detail_ks['附件二_3_1_1_单选按钮'])
            elif attachment_two_info['3'][1] == 2:
                self.is_click(create_sale_order_detail_ks['附件二_3_1_2_单选按钮'])
            else:
                raise ValueError("填入的值不对")
        elif attachment_two_info['3'][0] == 2:
            self.is_click(create_sale_order_detail_ks['附件二_3_2_单选按钮'])
            if attachment_two_info['3'][1] == 1:
                self.is_click(create_sale_order_detail_ks['附件二_3_2_1_单选按钮'])
            elif attachment_two_info['3'][1] == 2:
                self.is_click(create_sale_order_detail_ks['附件二_3_2_2_单选按钮'])
            else:
                raise ValueError("填入的值不对")
        else:
            raise ValueError("填入的值不对")
        self.input_text(create_sale_order_detail_ks['附件二_4_1_输入框'], attachment_two_info['4'])
        if attachment_two_info['7'] == 1:
            self.is_click(create_sale_order_detail_ks['附件二_7_1_单选按钮'])
        elif attachment_two_info['7'] == 2:
            self.is_click(create_sale_order_detail_ks['附件二_7_2_单选按钮'])
        else:
            raise ValueError("填入的值不对")
        if attachment_two_info['8'][0] == 1:
            self.is_click(create_sale_order_detail_ks['附件二_8_1_1_单选按钮'])
        elif attachment_two_info['8'][0] == 2:
            self.is_click(create_sale_order_detail_ks['附件二_8_1_2_单选按钮'])
        else:
            raise ValueError("填入的值不对")
        if attachment_two_info['8'][1] == 1:
            self.is_click(create_sale_order_detail_ks['附件二_8_2_1_单选按钮'])
        elif attachment_two_info['8'][1] == 2:
            self.is_click(create_sale_order_detail_ks['附件二_8_2_2_单选按钮'])
        else:
            raise ValueError("填入的值不对")
        if attachment_two_info['8'][2] == 1:
            self.is_click(create_sale_order_detail_ks['附件二_8_3_1_单选按钮'])
        elif attachment_two_info['8'][2] == 2:
            self.is_click(create_sale_order_detail_ks['附件二_8_3_2_单选按钮'])
        else:
            raise ValueError("填入的值不对")
        self.input_text(create_sale_order_detail_ks['附件二_10_1_输入框'], attachment_two_info['10'])

    def input_supplementary_agreement_info(self, supplementary_agreement_info):
        pay_list = supplementary_agreement_info['首期款支付分期']
        for pay in pay_list:
            self.is_click(create_sale_order_detail_ks['补充协议_1_1_1_选择框'])
            date = pay['日期']
            self.__choose_value_in_special_drop_down_box(date[0])
            if date[0] != 2:
                self.is_click(create_sale_order_detail_ks['补充协议_1_1_1_输入框'])
                self.input_text_with_enter(create_sale_order_detail_ks['补充协议_1_1_1_输入框'], date[1])
            if date[0] > 6:
                raise ValueError("传参错误")
            self.input_text(create_sale_order_detail_ks['补充协议_1_1_2_输入框'], pay['金额'])
            if pay['支付方式'] == 1:
                self.is_click(create_sale_order_detail_ks['补充协议_1_1_3_单选按钮'])
            elif pay['支付方式'] == 2:
                self.is_click(create_sale_order_detail_ks['补充协议_1_1_4_单选按钮'])
            elif pay['支付方式'] == 3:
                self.is_click(create_sale_order_detail_ks['补充协议_1_1_5_单选按钮'])
            else:
                raise ValueError("传值错误")
            self.is_click(create_sale_order_detail_ks['补充协议_1_1_6_选择框'])
            self.__choose_value_in_special_drop_down_box()
            self.input_text(create_sale_order_detail_ks['补充协议_1_1_6_输入框'], pay['其他'])
        house_deposit = supplementary_agreement_info['户口迁出保证金']
        self.is_click(create_sale_order_detail_ks['补充协议_1_5_1_选择框'])
        house_deposit_date = house_deposit['日期']
        self.__choose_value_in_special_drop_down_box(house_deposit_date[0])
        if house_deposit_date[0] != 2:
            self.is_click(create_sale_order_detail_ks['补充协议_1_5_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_ks['补充协议_1_5_1_输入框'], house_deposit_date[1])
        if house_deposit_date[0] > 6:
            raise ValueError("传参错误")
        self.input_text(create_sale_order_detail_ks['补充协议_1_5_2_输入框'], house_deposit['金额'])
        if house_deposit['支付方式'] == 1:
            self.is_click(create_sale_order_detail_ks['补充协议_1_5_3_单选按钮'])
        elif house_deposit['支付方式'] == 2:
            self.is_click(create_sale_order_detail_ks['补充协议_1_5_4_单选按钮'])
        elif house_deposit['支付方式'] == 3:
            self.is_click(create_sale_order_detail_ks['补充协议_1_5_5_单选按钮'])
        else:
            raise ValueError("传值错误")
        self.is_click(create_sale_order_detail_ks['补充协议_1_5_6_选择框'])
        self.__choose_value_in_special_drop_down_box()
        self.input_text(create_sale_order_detail_ks['补充协议_1_5_6_输入框'], house_deposit['其他'])
        resident_deposit = supplementary_agreement_info['户口迁出保证金']
        self.is_click(create_sale_order_detail_ks['补充协议_1_6_1_选择框'])
        resident_deposit_date = resident_deposit['日期']
        self.__choose_value_in_special_drop_down_box(resident_deposit_date[0])
        if resident_deposit_date[0] != 2:
            self.is_click(create_sale_order_detail_ks['补充协议_1_6_1_输入框'])
            self.input_text_with_enter(create_sale_order_detail_ks['补充协议_1_6_1_输入框'], resident_deposit_date[1])
        if resident_deposit_date[0] > 6:
            raise ValueError("传参错误")
        self.input_text(create_sale_order_detail_ks['补充协议_1_6_2_输入框'], resident_deposit['金额'])
        if resident_deposit['支付方式'] == 1:
            self.is_click(create_sale_order_detail_ks['补充协议_1_6_3_单选按钮'])
        elif resident_deposit['支付方式'] == 2:
            self.is_click(create_sale_order_detail_ks['补充协议_1_6_4_单选按钮'])
        elif resident_deposit['支付方式'] == 3:
            self.is_click(create_sale_order_detail_ks['补充协议_1_6_5_单选按钮'])
        else:
            raise ValueError("传值错误")
        self.is_click(create_sale_order_detail_ks['补充协议_1_6_6_选择框'])
        self.__choose_value_in_special_drop_down_box()
        self.input_text(create_sale_order_detail_ks['补充协议_1_6_6_输入框'], house_deposit['其他'])
        self.input_text(create_sale_order_detail_ks['补充协议_6_1_输入框'], supplementary_agreement_info['其他'])

    def input_commission_confirmation_info(self, commission_confirmation_info):
        self.input_text(create_sale_order_detail_ks['佣金确认书_车位_输入框'], commission_confirmation_info['车位'])
        self.input_text(create_sale_order_detail_ks['佣金确认书_佣金金额_输入框'], commission_confirmation_info['佣金金额'])
        self.is_click(create_sale_order_detail_ks['佣金确认书_支付日期_选择框'])
        self.__choose_value_in_special_drop_down_box(commission_confirmation_info['支付日期'][0])
        if commission_confirmation_info['支付日期'][0] == 2:
            self.input_text(create_sale_order_detail_ks['佣金确认书_支付日期_输入框'], commission_confirmation_info['支付日期'][1])

    def input_commission_confirmation2_info(self, commission_confirmation_info):
        self.input_text(create_sale_order_detail_ks['佣金确认书二_车位_输入框'], commission_confirmation_info['车位'])
        self.input_text(create_sale_order_detail_ks['佣金确认书二_佣金金额_输入框'], commission_confirmation_info['佣金金额'])
        self.is_click(create_sale_order_detail_ks['佣金确认书二_支付日期_选择框'])
        self.__choose_value_in_special_drop_down_box(commission_confirmation_info['支付日期'][0])
        if commission_confirmation_info['支付日期'][0] == 2:
            self.input_text(create_sale_order_detail_ks['佣金确认书二_支付日期_输入框'], commission_confirmation_info['支付日期'][1])

    def input_receipt_info(self, receipt_info):
        collection_details = receipt_info['收款明细']
        for collection in collection_details:
            self.is_click(create_sale_order_detail_ks['收据_支付日期' + str(collection_details.index(collection) + 1)
                                                      + '_输入框'])
            self.input_text_with_enter(create_sale_order_detail_ks['收据_支付日期'
                                                                   + str(collection_details.index(collection) + 1)
                                                                   + '_输入框'], collection['日期'])
            self.input_text(create_sale_order_detail_ks['收据_支付金额' + str(collection_details.index(collection) + 1)
                                                        + '_输入框'], collection['金额'])

    def __choose_value_in_drop_down_box(self, choose_value):
        ele_list = self.find_elements(create_sale_order_detail_ks['合同内容下拉框'])
        for ele in ele_list:
            if ele.text == choose_value:
                ele.click()
                sleep()
                break

    def __choose_value_in_special_drop_down_box(self, index=1):
        ele_list = self.find_elements(create_sale_order_detail_ks['合同内容特殊下拉框'])
        ele_list[index-1].click()
        sleep()
