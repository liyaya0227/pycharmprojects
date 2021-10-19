#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/10/13 0013
"""
from page.webpage import WebPage
from common.readelement import Element

detail = Element('jrcw/web/sale/detail')


class SaleDetailPage(WebPage):

    def get_sale_code(self):
        """获取销售单据号"""
        return self.element_text(detail['销售单据号标签'])

    def get_sale_info(self):
        """获取销售单信息"""
        return {
            'sale_code': self.element_text(detail['销售单信息_销售单据号标签']),
            'project_type': self.element_text(detail['销售单信息_项目类型标签']),
            'pay_status': self.element_text(detail['销售单信息_付款状态标签']),
            'project_code': self.element_text(detail['销售单信息_项目单据号标签']),
            'sign_city': self.element_text(detail['销售单信息_签约城市标签']),
            'version': self.element_text(detail['销售单信息_版本号标签']),
            'receivable_money': self.element_text(detail['销售单信息_应收金额标签'])[1:].replace(',', ),
            'order_code': self.element_text(detail['销售单信息_订单编号标签']),
            'create_time': self.element_text(detail['销售单信息_创建日期标签']),
            'received_money': self.element_text(detail['销售单信息_已收金额标签'])[1:].replace(',', ),
            'product_info': self.element_text(detail['销售单信息_产品信息标签']),
            'order_time': self.element_text(detail['销售单信息_下单日期标签']),
            'uncollected_money': self.element_text(detail['销售单信息_待收金额标签'])[1:].replace(',', ),
            'create_person': self.element_text(detail['销售单信息_创建人标签'])
        }

    def sale_detail(self):
        """获取销售单明细"""
        return {
            'platform_fee': self.element_text(detail['销售单明细_平台费标签']),
            'brand_fee': self.element_text(detail['销售单明细_品牌费标签']),
            'shop_fee': self.element_text(detail['销售单明细_门店代理费标签'])
        }

    def sale_history_version(self):
        """获取销售单历史版本信息"""
        def __get_table_column_by_name(name):
            """获取列表头的列数"""
            table_header_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                            "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]"\
                                            "//div[@class='ivu-table-header']//table/thead/tr/th//span"
            return self.find_elements(table_header_locator).index(name)
        table_data = []
        table_row_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                     "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                     "//div[@class='ivu-table-body']/table/tr"
        for i in range(len(self.find_elements(table_row_locator))):
            sale_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                         "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                         "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                + __get_table_column_by_name('销售单号') + "]//span"
            version_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                       "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                       "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                              + __get_table_column_by_name('版本号') + "]//span"
            create_time_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                           "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                           "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                  + __get_table_column_by_name('创建时间') + "]//span"
            create_person_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                             "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                             "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                    + __get_table_column_by_name('创建人') + "]//span"
            shop_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                    "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                    "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                           + __get_table_column_by_name('门店/商户') + "]//span"
            shop_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                         "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                         "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                + __get_table_column_by_name('门店/商户编号') + "]//span"
            company_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                       "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                       "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                              + __get_table_column_by_name('公司') + "]//span"
            receivable_money_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'saledetail')]" \
                                                "//div[text()='销售单历史版本']/parent::div/div[contains(@class,'detail')]" \
                                                "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                       + __get_table_column_by_name('应收金额') + "]//span"
            row_data = {
                'sale_code': self.element_text(sale_code_locator),
                'version': self.element_text(version_locator),
                'create_time': self.element_text(create_time_locator),
                'create_person': self.element_text(create_person_locator),
                'store': self.element_text(shop_locator),
                'shop_code': self.element_text(shop_code_locator),
                'company': self.element_text(company_locator),
                'receivable_money': self.element_text(receivable_money_locator)
            }
            table_data.append(row_data)
        return table_data
