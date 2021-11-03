#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/10/14 0013
"""
from page.webpage import WebPage
from common.readelement import Element

detail = Element('jrcw/web/settlement/detail')


class SettlementDetailPage(WebPage):

    def get_settlement_code(self):
        """获取结算单据号"""
        return self.get_element_text(detail['结算单据号标签'])

    def get_project_code(self):
        """获取项目结算单据号"""
        return self.get_element_text(detail['项目结算单据号标签'])

    def get_version(self):
        """获取版本号"""
        return self.get_element_text(detail['版本号标签'])

    def get_reconciliation_status(self):
        """获取对账状态"""
        return self.get_element_text(detail['对账状态标签'])

    def get_order_detail(self):
        """获取结算详情_订单明细"""
        return {
            'order_code': self.get_element_text(detail['订单明细_订单编号标签']),
            'expect_settlement_time': self.get_element_text(detail['订单明细_预计结算时间标签'])[7:],
            'version': self.get_element_text(detail['订单明细_版本号标签'])[4:],
            'product_name': self.get_element_text(detail['订单明细_产品名称标签'])[5:],
            'order_time': self.get_element_text(detail['订单明细_下单时间标签'])[5:],
            'business_type': self.get_element_text(detail['订单明细_款项类型标签']),
            'create_time': self.get_element_text(detail['订单明细_结算单创建时间标签'])[8:],
            'fee_type': self.get_element_text(detail['订单明细_结算类型标签']),
            'settlement_model': self.get_element_text(detail['订单明细_结算模式标签']),
            'settlement_shop': self.get_element_text(detail['订单明细_结算门店/商户标签'])[8:],
            'settlement_city': self.get_element_text(detail['订单明细_结算城市标签'])[5:]
        }

    def settlement__detail(self):
        """获取结算明细"""
        return {
            'fee_type': self.get_element_text(detail['结算明细_结算类型单元格']),
            'version': self.get_element_text(detail['结算明细_结算版本号单元格']),
            'settlement_money': self.get_element_text(detail['结算明细_结算金额单元格']),
            'service_charge': self.get_element_text(detail['结算明细_手续费单元格']),
            'settlement_shop': self.get_element_text(detail['结算明细_结算门店/商户单元格']),
            'settlement_company': self.get_element_text(detail['结算明细_结算公司单元格'])
        }

    def settlement_history_version(self):
        """获取销售单历史版本信息"""
        def __get_table_column_by_name(name):
            """获取列表头的列数"""
            table_header_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlementdetail')]" \
                                            "//span[text()='结算单历史版本']/ancestor::div[@class='detail ivu-row']" \
                                            "//div[@class='ivu-table-header']//table/thead/tr/th//span"
            return self.find_elements(table_header_locator).index(name)
        table_data = []
        table_row_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlementdetail')]" \
                                     "//span[text()='结算单历史版本']/ancestor::div[@class='detail ivu-row']" \
                                     "//div[@class='ivu-table-body']/table/tr"
        for i in range(len(self.find_elements(table_row_locator))):
            fee_type_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlementdetail')]" \
                                         "//span[text()='结算单历史版本']/ancestor::div[@class='detail ivu-row']" \
                                         "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                               + __get_table_column_by_name('结算类型') + "]//span"
            version_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlementdetail')]" \
                                       "//span[text()='结算单历史版本']/ancestor::div[@class='detail ivu-row']" \
                                       "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                              + __get_table_column_by_name('结算版本号') + "]/div/div"
            settlement_money_locator = 'xpath', "//div[@class='ivu-layout']" \
                                                "//div[contains(@class, 'settlementdetail')]" \
                                                "//span[text()='结算单历史版本']/ancestor::div[@class='detail ivu-row']" \
                                                "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                       + __get_table_column_by_name('结算金额') + "]/div/div"
            service_charge_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlementdetail')]" \
                                              "//span[text()='结算单历史版本']/ancestor::div[@class='detail ivu-row']" \
                                              "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                     + __get_table_column_by_name('手续费') + "]/div/div"
            settlement_shop_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlementdetail')]" \
                                               "//span[text()='结算单历史版本']/ancestor::div[@class='detail ivu-row']" \
                                               "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                      + __get_table_column_by_name('结算门店/商户') + "]//p"
            settlement_company_locator = 'xpath', "//div[@class='ivu-layout']" \
                                                  "//div[contains(@class, 'settlementdetail')]" \
                                                  "//span[text()='结算单历史版本']/ancestor::div[@class='detail ivu-row']" \
                                                  "//div[@class='ivu-table-body']/table/tr[" + str(i) + "]/td[" \
                                         + __get_table_column_by_name('结算公司') + "]//p"
            row_data = {
                'fee_type': self.get_element_text(fee_type_locator),
                'version': self.get_element_text(version_locator),
                'settlement_money': self.get_element_text(settlement_money_locator)[1:],
                'service_charge': self.get_element_text(service_charge_locator)[1:],
                'settlement_shop': self.get_element_text(settlement_shop_locator),
                'settlement_company': self.get_element_text(settlement_company_locator)
            }
            table_data.append(row_data)
        return table_data
