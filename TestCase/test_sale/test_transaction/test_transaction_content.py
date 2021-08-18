#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_transaction_content.py
@date: 2021/7/22 0022
"""

import pytest
import allure
from config.conf import cm
from decimal import Decimal
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_data
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.house.addpage import HouseAddPage
from page_object.house.tablepage import HouseTablePage
from page_object.house.detailpage import HouseDetailPage
from page_object.customer.detailpage import CustomerDetailPage
from page_object.customer.tablepage import CustomerTablePage
from page_object.achievement.detailpage import AchievementDetailPage
from page_object.achievement.tablepage import AchievementTablePage
from page_object.contract.createorderpage import ContractCreateOrderPage
from page_object.contract.detailpage import ContractDetailPage
from page_object.contract.previewpage import ContractPreviewPage
from page_object.contract.tablepage import ContractTablePage
from page_object.transaction.tablepage import TransactionTablePage
from page_object.transaction.detailpage import TransactionDetailPage

house_info = {}
customer_info = {}


@allure.feature("测试权证单据内容模块")
class TestTransactionOrderContent(object):

    json_file_path = cm.test_data_dir + "/test_sale/test_transaction/test_transaction_order_content_" \
                     + ini.environment + ".json"
    test_data = get_data(json_file_path)
    house_data = test_data['房源信息']
    customer_data = test_data['客源信息']
    house_key_info_data = test_data['房源重点信息']
    full_payment_contract_data = test_data['全款合同信息']
    commercial_loan_contract_data = test_data['商贷合同信息']
    house_data['楼盘'] = ini.house_community_name
    house_data['楼栋'] = ini.house_building_id
    house_data['门牌号'] = ini.house_doorplate
    customer_data['电话号'] = ini.custom_telephone

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_info
        global customer_info

        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_add = HouseAddPage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_detail = CustomerDetailPage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        if house_table.get_house_code_by_db(flag='买卖') == '':  # 判断房源是否存在，不存在则新增
            house_table.click_add_house_button()
            house_add.choose_sale_radio()
            house_add.choose_estate_name(ini.house_community_name)  # 填写物业地址信息
            house_add.choose_building_id(ini.house_building_id)
            house_add.choose_building_cell(ini.house_building_cell)
            house_add.choose_floor(ini.house_floor)
            house_add.choose_doorplate(ini.house_doorplate)
            house_add.click_next_button()
            house_add.input_owner_info_and_house_info(self.house_data, '买卖')
        main_upview.clear_all_title()
        main_leftview.click_all_house_label()
        house_code = house_table.get_house_code_by_db(flag='买卖')
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_reset_button()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_info = house_detail.get_address_dialog_house_property_address()
        house_info['house_code'] = house_code
        house_info['house_type'] = house_detail.get_house_type()
        house_info['orientations'] = house_detail.get_orientations()
        house_info['floor'] = house_detail.get_floor_dialog_house_floor()
        house_info['inspect_type'] = house_detail.get_inspect_type()
        house_info['house_state'] = house_detail.get_house_state()
        assert house_info != {}
        log.info('获取房源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        if customer_table.get_customer_table_count() == 1:
            if '二手住宅' not in customer_table.get_customer_detailed_requirements_by_row(1):
                customer_table.go_customer_detail_by_row(1)
                customer_detail.click_invalid_customer_button()
                customer_detail.choose_invalid_customer_type('其他原因')
                customer_detail.input_invalid_customer_reason('自动化测试需要')
                customer_detail.click_dialog_confirm_button()
                main_upview.clear_all_title()
                main_leftview.click_my_customer_label()
                customer_table.add_customer(test_data=self.customer_data)
        else:
            customer_table.add_customer(test_data=self.customer_data)
        customer_info['customer_code'] = customer_table.get_customer_code_by_row(1)
        customer_info['customer_name'] = customer_table.get_customer_name_by_row(1)
        assert customer_info != {}
        log.info('获取客源信息，新建合同校验需要')
        main_upview.clear_all_title()

    @allure.story("测试全款购买合同，查看权证单显示数据用例")
    @pytest.mark.sale
    @pytest.mark.transaction
    @pytest.mark.run(order=41)
    # @pytest.mark.dependency()
    # @pytest.mark.flaky(reruns=5, reruns_delay=2)
    @pytest.mark.parametrize("contract_data", full_payment_contract_data)
    def test_001(self, web_driver, contract_data):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_create_order = ContractCreateOrderPage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        achievement_table = AchievementTablePage(web_driver)
        achievement_detail = AchievementDetailPage(web_driver)
        transaction_table = TransactionTablePage(web_driver)
        transaction_detail = TransactionDetailPage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_reset_button()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_info['house_code'])
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_key_info = house_detail.get_house_key_info()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_create_order_button()
        contract_create_order.input_house_code(house_info['house_code'])
        contract_create_order.click_get_house_info_button()
        contract_create_order.verify_house_info(house_info)
        contract_create_order.click_verify_house_button()
        log.info('房源信息校验通过')
        contract_create_order.input_customer_code(customer_info['customer_code'])
        contract_create_order.click_get_customer_info_button()
        assert contract_create_order.get_customer_name() == customer_info['customer_name']
        contract_create_order.click_next_step_button()
        if ini.environment == 'sz' or ini.environment == 'ks':
            contract_create_order.choose_district_contract()
            contract_create_order.click_confirm_button_in_dialog()
        contract_create_order.input_contract_content(contract_data, '买卖')
        contract_create_order.click_submit_button()
        main_topview.close_notification()
        log.info('合同创建成功')
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_house_code_search(house_info['house_code'])
        contract_table.input_customer_code_search(customer_info['customer_code'])
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        contract_code = contract_details['contract_code']
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_go_examine_button()  # 经纪人提交审核
        contract_detail.click_confirm_button()
        main_leftview.change_role('商圈经理')  # 商圈经理审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.pass_examine_by_row(1)
        main_leftview.change_role('合同法务')  # 法务审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.legal_examine_by_row(1)
        contract_preview.click_pass_button()
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_preview_button()
        contract_preview.click_signature_button()  # 签章
        main_topview.close_notification()
        contract_preview.click_print_with_sign_button()  # 打印
        contract_preview.cancel_print()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract()
        contract_detail.upload_two_sign_contract()  # 经纪人签约时间
        contract_detail.upload_pictures([cm.tmp_picture_file])  # 经纪人上传主体合同
        contract_info = contract_detail.get_contract_info()
        contract_detail.click_submit_button()
        contract_detail.click_report_achievement_button()  # 经纪人提交业绩审核
        achievement_detail.click_submit_button()
        main_leftview.change_role('商圈经理')  # 商圈经理业绩审核
        main_leftview.click_achievement_label()
        achievement_table.click_achievement_examine_tab()
        achievement_table.click_to_examine_tab()
        achievement_table.input_contract_code_search(contract_code)
        achievement_table.click_search_button()
        achievement_table.click_pass_examine_button_by_row(1)
        contract_table.update_agency_fee(contract_code)  # 数据库修改代理费
        main_leftview.change_role('权证专员')  # 权证专员过户
        main_leftview.click_on_way_order_label()
        transaction_table.click_contract_code_tab()
        transaction_table.input_search_text(contract_code)
        transaction_table.click_search_button()
        transaction_table.go_to_transaction_detail_by_row(1)
        transaction_detail.complete_transfer_house()
        transaction_detail.close_case()  # 权证专员结案
        main_topview.close_notification()
        transaction_detail.show_sensitive_info()  # 显示敏感信息
        transaction_info = transaction_detail.get_transaction_info()
        transaction_fund_info = transaction_detail.get_fund_info()
        transaction_buyer_info = transaction_detail.get_buyer_info()
        transaction_seller_info = transaction_detail.get_seller_info()
        transaction_house_info = transaction_detail.get_house_info()
        transaction_management = ''  # 权证单内容的校验
        if ini.environment == 'ks':
            if contract_data['第四条信息']['支付方式'][0] == 1:
                transaction_management = '全款'
            if contract_data['第四条信息']['支付方式'][0] == 2:
                transaction_management = '商贷'
        if ini.environment == 'wx':
            if contract_data['第五条信息']['二'] == 1:
                transaction_management = '全款'
            if contract_data['第五条信息']['二'] == 2:
                transaction_management = '商贷'
        else:
            if contract_data['第四条信息']['选项'][0] == 1:
                transaction_management = '全款'
            if contract_data['第四条信息']['选项'][0] == 2:
                transaction_management = '商贷'
        assert transaction_info['交易管理'] == transaction_management
        assert transaction_info['交易编号'] == contract_code.replace('HE', 'QZ')
        assert transaction_info['合同编号'] == contract_code
        assert transaction_info['创建日期'] == contract_info['create_time']
        assert transaction_info['签约日期'] == contract_info['sign_time']
        if ini.environment == 'ks':
            assert transaction_info['合同约定办理资金托管日期'] == '-'
        elif ini.environment == 'wx':
            if contract_data['第五条信息']['二_2'][0][0][0] == 1:
                assert transaction_info['合同约定办理资金托管日期'] == '办理权属转移登记前'
            if contract_data['第五条信息']['二_2'][0][0][0] == 2:
                assert transaction_info['合同约定办理资金托管日期'] == '办理权属转移登记后' + contract_data['第五条信息']['二_2'][0][0][1] + '日内'
            if contract_data['第五条信息']['二_2'][0][0][0] == 3:
                assert transaction_info['合同约定办理资金托管日期'] == \
                       contract_data['第五条信息']['二_2'][0][0][1].split('-')[0] + '年' \
                       + contract_data['第五条信息']['二_2'][0][0][1].split('-')[1] + '月' \
                       + contract_data['第五条信息']['二_2'][0][0][1].split('-')[2] + '日' + '前'
            if contract_data['第五条信息']['二_2'][0][0][0] == 4:
                assert transaction_info['合同约定办理资金托管日期'] == '本合同签订当日'
            if contract_data['第五条信息']['二_2'][0][0][0] == 5:
                assert transaction_info['合同约定办理资金托管日期'] == '本合同签订后' + contract_data['第五条信息']['二_2'][0][0][1] + '日内'
            if contract_data['第五条信息']['二_2'][0][0][0] == 6:
                assert transaction_info['合同约定办理资金托管日期'] == '办理网签手续后' + contract_data['第五条信息']['二_2'][0][0][1] + '日内'
            if contract_data['第五条信息']['二_2'][0][0][0] == 6:
                assert transaction_info['合同约定办理资金托管日期'] == '办理资金托管手续后' + contract_data['第五条信息']['二_2'][0][0][1] + '日内'
        else:
            if transaction_info['交易管理'] == '全款':
                assert transaction_info['合同约定办理资金托管日期'] == \
                       contract_data['第四条信息']['选项'][1][1].split('-')[0] + '年' \
                       + contract_data['第四条信息']['选项'][1][1].split('-')[1] + '月' \
                       + contract_data['第四条信息']['选项'][1][1].split('-')[2] + '日'
            if transaction_info['交易管理'] == '商贷':
                assert transaction_info['合同约定办理资金托管日期'] == \
                       contract_data['第四条信息']['选项'][1][0].split('-')[0] + '年' \
                       + contract_data['第四条信息']['选项'][1][0].split('-')[1] + '月' \
                       + contract_data['第四条信息']['选项'][1][0].split('-')[2] + '日'
        if transaction_info['交易管理'] == '商贷':
            if ini.environment == 'sz':
                assert transaction_info['合同约定贷款审批通过日期'] == \
                       contract_data['第四条信息']['选项'][1][3].split('-')[0] + '年' \
                       + contract_data['第四条信息']['选项'][1][3].split('-')[1] + '月' \
                       + contract_data['第四条信息']['选项'][1][3].split('-')[2] + '日'
            else:
                assert transaction_info['合同约定贷款审批通过日期'] == '-'
        assert transaction_info['备注'] == '-'
        deposit = Decimal('0')
        if ini.environment == 'wx':
            for item in contract_data['第五条信息']['二_1']:
                deposit = deposit + Decimal(item[1])
            house_payment = Decimal(contract_data['第五条信息']['一'])
            # house_delivery_payment = Decimal('0')
            register_transfer_payment = Decimal(contract_data['第五条信息']['二_4'][0])
            property_delivery_payment = Decimal(contract_data['第五条信息']['二_5'][1])
            first_payment = Decimal('0')
            for item in contract_data['第五条信息']['二_2']:
                first_payment = first_payment + Decimal(item[1])
            if transaction_info['交易管理'] == '全款':
                assert Decimal(transaction_fund_info['成交总价'][:-1]) == deposit + first_payment + \
                       property_delivery_payment + register_transfer_payment
            if transaction_info['交易管理'] == '商贷':
                assert Decimal(transaction_fund_info['成交总价'][:-1]) == deposit + first_payment + \
                       Decimal(contract_data['第五条信息']['二_3'][1]) + property_delivery_payment + register_transfer_payment
            assert Decimal(transaction_fund_info['网签价'][:-1]) == house_payment
            assert Decimal(transaction_fund_info['首期款总额'][:-1]) == deposit + first_payment + register_transfer_payment \
                   + property_delivery_payment
            assert Decimal(transaction_fund_info['定金总额'][:-1]) == deposit
            assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == first_payment
            assert Decimal(transaction_fund_info['购房款/首付款（第一笔）'][:-1]) == Decimal(contract_data['第五条信息']['二_2'][0][1])
            if transaction_info['交易管理'] == '商贷':
                assert Decimal(transaction_fund_info['拟贷款金额'][:-1]) == Decimal(contract_data['第五条信息']['二_3'][1])
            # assert Decimal(transaction_fund_info['交房保证金'][:-1]) == house_delivery_payment
            assert Decimal(transaction_fund_info['户口迁出保证金'][:-1]) == register_transfer_payment
            assert Decimal(transaction_fund_info['物业交割保证金'][:-1]) == property_delivery_payment
        else:
            house_money = Decimal('0')
            if ini.environment == 'sz':
                for item in contract_data['补充协议']['定金']:
                    deposit = deposit + Decimal(item['金额'])
                for item in contract_data['补充协议']['房款']:
                    house_money = house_money + Decimal(item['金额'])
            if ini.environment == 'ks':
                for item in contract_data['补充协议']['首期款支付分期']:
                    deposit = deposit + Decimal(item['金额'])
            house_payment = Decimal(contract_data['第三条信息']['房屋价款'])
            house_delivery_payment = Decimal(contract_data['补充协议']['交房保证金']['金额'])
            register_transfer_payment = Decimal(contract_data['补充协议']['户口迁出保证金']['金额'])
            assert Decimal(transaction_fund_info['成交总价'][:-1]) == house_payment + deposit + house_delivery_payment \
                   + register_transfer_payment + house_money
            assert Decimal(transaction_fund_info['网签价'][:-1]) == house_payment
            assert Decimal(transaction_fund_info['首期款总额'][:-1]) == deposit + house_delivery_payment \
                   + register_transfer_payment + house_money
            if ini.environment == 'ks':
                assert Decimal(transaction_fund_info['定金总额'][:-1]) == \
                       Decimal(contract_data['第四条信息']['购房定金'])
            else:
                assert Decimal(transaction_fund_info['定金总额'][:-1]) == deposit
            if transaction_info['交易管理'] == '全款':
                if ini.environment == 'ks':
                    if contract_data['第四条信息']['支付方式'][1] == 1:
                        assert transaction_fund_info['首付款总金额'] == '无'
                    if contract_data['第四条信息']['支付方式'][1] == 2:
                        assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == \
                               Decimal(self.full_payment_contract_data2['第四条信息']['支付方式'][2][2])
                if ini.environment == 'sz':
                    assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == house_payment + house_delivery_payment \
                           + register_transfer_payment + house_money
                assert Decimal(transaction_fund_info['购房款/首付款（第一笔）'][:-1]) == house_payment
            if transaction_info['交易管理'] == '商贷':
                if ini.environment == 'ks':
                    assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == \
                           Decimal(contract_data['第四条信息']['支付方式'][2][1])
                    assert Decimal(transaction_fund_info['购房款/首付款（第一笔）'][:-1]) == \
                           Decimal(contract_data['第四条信息']['支付方式'][2][1])
                    assert Decimal(transaction_fund_info['拟贷款金额'][:-1]) == \
                           Decimal(contract_data['第四条信息']['支付方式'][3][0])
                if ini.environment == 'ks':
                    assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == Decimal(
                        contract_data['第四条信息']['选项'][1][1])
                    assert Decimal(transaction_fund_info['购房款/首付款（第一笔）'][:-1]) == deposit + house_delivery_payment \
                           + register_transfer_payment + house_money
                    assert Decimal(transaction_fund_info['拟贷款金额'][:-1]) == house_payment \
                           - Decimal(contract_data['第四条信息']['选项'][1][1])
            assert Decimal(transaction_fund_info['交房保证金'][:-1]) == house_delivery_payment
            assert Decimal(transaction_fund_info['户口迁出保证金'][:-1]) == register_transfer_payment
        assert transaction_buyer_info['姓名'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_姓名']
        assert transaction_buyer_info['性质'] == '-'
        assert transaction_buyer_info['性别'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_性别']
        assert transaction_buyer_info['国籍'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_国籍']
        assert transaction_buyer_info['证件类型'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_证件名称']
        assert transaction_buyer_info['证件号码'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_证件号码']
        assert transaction_buyer_info['联系电话'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_联系电话']
        assert transaction_buyer_info['其他联系方式'] == '--'
        assert transaction_buyer_info['户籍'] == '--'
        assert transaction_buyer_info['婚姻状况'] == '--'
        assert transaction_buyer_info['买方家庭住房套数'] == '--'
        assert transaction_seller_info['姓名'] == contract_data['房屋出卖人信息']['房屋出卖人_姓名']
        assert transaction_seller_info['性质'] == '-'
        assert transaction_seller_info['性别'] == contract_data['房屋出卖人信息']['房屋出卖人_性别']
        assert transaction_seller_info['国籍'] == contract_data['房屋出卖人信息']['房屋出卖人_国籍']
        assert transaction_seller_info['证件类型'] == contract_data['房屋出卖人信息']['房屋出卖人_证件名称']
        assert transaction_seller_info['证件号码'] == contract_data['房屋出卖人信息']['房屋出卖人_证件号码']
        assert transaction_seller_info['联系电话'] == contract_data['房屋出卖人信息']['房屋出卖人_联系电话']
        assert transaction_seller_info['其他联系方式'] == '--'
        assert transaction_seller_info['婚姻状况'] == '--'
        assert transaction_house_info['房源编号'] == house_info['house_code']
        if ini.environment == 'ks':
            assert transaction_house_info['规划用途'] == '-'
            assert transaction_house_info['建筑面积'] == contract_data['第一条信息']['产权登记面积'] + 'm²'
            assert transaction_house_info['建成年代'] == '-'
            assert transaction_house_info['共有权证号'] == '-'
        elif ini.environment == 'wx':
            if contract_data['第一条信息']['三'][0] == 1:
                assert transaction_house_info['规划用途'] == '住宅'
            if contract_data['第一条信息']['三'][0] == 2:
                assert transaction_house_info['规划用途'] == '公寓'
            if contract_data['第一条信息']['三'][0] == 3:
                assert transaction_house_info['规划用途'] == '别墅'
            if contract_data['第一条信息']['三'][0] == 4:
                assert transaction_house_info['规划用途'] == '办公'
            if contract_data['第一条信息']['三'][0] == 5:
                assert transaction_house_info['规划用途'] == '商业'
            if contract_data['第一条信息']['三'][0] == 6:
                assert transaction_house_info['规划用途'] == '工业'
            if contract_data['第一条信息']['三'][0] == 7:
                assert transaction_house_info['规划用途'] == '其他' + contract_data['第一条信息']['三'][1]
            assert transaction_house_info['建筑面积'] == contract_data['第一条信息']['建筑面积'] + 'm²'
            assert transaction_house_info['建成年代'] == '-'
            if contract_data['第二条信息']['一_持证方式'][1] == "":
                assert transaction_house_info['共有权证号'] == "-"
            else:
                assert transaction_house_info['共有权证号'] == contract_data['第二条信息']['一_持证方式'][1]
        else:
            assert transaction_house_info['规划用途'] == contract_data['第一条信息']['房屋用途']
            assert transaction_house_info['建筑面积'] == contract_data['第一条信息']['产权登记建筑面积'] + 'm²'
            assert transaction_house_info['建成年代'] == contract_data['第一条信息']['房屋建成年份']
            if contract_data['第二条信息']['房屋权证状况'][0] == 1:
                assert transaction_house_info['共有权证号'] == '-'
            if contract_data['第二条信息']['房屋权证状况'][0] == 2:
                assert transaction_house_info['共有权证号'] == contract_data['第二条信息']['房屋权证状况'][1]
        if ini.environment == 'wx':
            if contract_data['第一条信息']['四'][0] == 1:
                assert transaction_house_info['房屋性质'] == '商品房'
            if contract_data['第一条信息']['四'][0] == 2:
                assert transaction_house_info['房屋性质'] == '房改房'
            if contract_data['第一条信息']['四'][0] == 3:
                assert transaction_house_info['房屋性质'] == '安置房'
            if contract_data['第一条信息']['四'][0] == 4:
                assert transaction_house_info['房屋性质'] == '向社会公开销售的经济适用住房'
            if contract_data['第一条信息']['四'][0] == 5:
                assert transaction_house_info['房屋性质'] == '其他房屋' + contract_data['第一条信息']['四'][1]
        else:
            assert transaction_house_info['房屋性质'] == '-'
        assert transaction_house_info['楼盘名称'] == house_info['estate_name']
        if ini.environment == 'wx':
            if contract_data['第二条信息']['一_权属状况'][0] == 1:
                assert transaction_house_info['房本类型'] == '不动产权证'
            if contract_data['第二条信息']['一_权属状况'][0] == 2:
                assert transaction_house_info['房本类型'] == '房屋所有权证'
            assert transaction_house_info['产权证号'] == contract_data['第二条信息']['一_权属状况'][1]
        else:
            assert transaction_house_info['房本类型'] == '-'
            assert transaction_house_info['产权证号'] == contract_data['第一条信息']['房屋所有权证编号']
        if house_key_info['house_state'] == '-':
            house_key_info['house_state'] = '--'
        assert transaction_house_info['房屋现状'] == house_key_info['house_state']
        assert transaction_house_info['物业地址'] == house_info['estate_name'] + house_info['building_name'] + '-' + \
               house_info['unit_name'] + '-' + house_info['floor'] + '-' + house_info['door_name']
        if ini.environment == 'wx':
            assert transaction_house_info['行政区域'] == '-'
        else:
            assert transaction_house_info['行政区域'] == contract_data['第一条信息']['区']
        if ini.environment == 'wx':
            if contract_data['第二条信息']['三'][0] == 1:
                assert transaction_house_info['是否有抵押'] == '无抵押'
                assert transaction_house_info['合同约定的注销抵押日期'] == '-'
            if contract_data['第二条信息']['三'][0] == 2:
                assert transaction_house_info['是否有抵押'] == '有抵押'
                assert transaction_house_info['合同约定的注销抵押日期'] == \
                       contract_data['第二条信息']['三'][2][1].split('-')[0] + '年' \
                       + contract_data['第二条信息']['三'][2][1].split('-')[1] + '月' \
                       + contract_data['第二条信息']['三'][2][1].split('-')[2] + '日'
        else:
            if contract_data['第二条信息']['房屋抵押状况'][0] == 1:
                assert transaction_house_info['是否有抵押'] == '无抵押'
                assert transaction_house_info['合同约定的注销抵押日期'] == '-'
            if contract_data['第二条信息']['房屋抵押状况'][0] == 2:
                assert transaction_house_info['是否有抵押'] == '有抵押'
                assert transaction_house_info['合同约定的注销抵押日期'] == \
                       contract_data['第二条信息']['房屋抵押状况'][1][1].split('-')[0] + '年' \
                       + contract_data['第二条信息']['房屋抵押状况'][1][1].split('-')[1] + '月' \
                       + contract_data['第二条信息']['房屋抵押状况'][1][1].split('-')[2] + '日'
        if house_key_info['is_unique'] == '不唯一':
            assert transaction_house_info['是否唯一'] == '否'
        if house_key_info['is_unique'] == '唯一':
            assert transaction_house_info['是否唯一'] == '是'
        if house_key_info['is_unique'] == '-':
            assert transaction_house_info['是否唯一'] == '-'
        assert transaction_house_info['产证年限'] == house_key_info['house_property_limit']
        assert transaction_house_info['是否限售房'] == '--'

    @allure.story("测试商贷购买合同，查看权证单显示数据用例")
    @pytest.mark.sale
    @pytest.mark.transaction
    @pytest.mark.run(order=41)
    # @pytest.mark.dependency()
    # @pytest.mark.flaky(reruns=5, reruns_delay=2)
    @pytest.mark.parametrize("contract_data", commercial_loan_contract_data)
    def test_002(self, web_driver, contract_data):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_create_order = ContractCreateOrderPage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        achievement_table = AchievementTablePage(web_driver)
        achievement_detail = AchievementDetailPage(web_driver)
        transaction_table = TransactionTablePage(web_driver)
        transaction_detail = TransactionDetailPage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_reset_button()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_info['house_code'])
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.edit_house_key_info(self.house_key_info_data)
        main_upview.clear_all_title()
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_reset_button()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_info['house_code'])
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_key_info = house_detail.get_house_key_info()
        house_info['inspect_type'] = house_detail.get_inspect_type()
        house_info['house_state'] = house_detail.get_house_state()
        house_info['has_pledge'] = house_detail.get_has_pledge()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_create_order_button()
        contract_create_order.input_house_code(house_info['house_code'])
        contract_create_order.click_get_house_info_button()
        contract_create_order.verify_house_info(house_info)
        contract_create_order.click_verify_house_button()
        log.info('房源信息校验通过')
        contract_create_order.input_customer_code(customer_info['customer_code'])
        contract_create_order.click_get_customer_info_button()
        assert contract_create_order.get_customer_name() == customer_info['customer_name']
        contract_create_order.click_next_step_button()
        if ini.environment == 'sz' or ini.environment == 'ks':
            contract_create_order.choose_district_contract()
            contract_create_order.click_confirm_button_in_dialog()
        contract_create_order.input_contract_content(contract_data, '买卖')
        contract_create_order.click_submit_button()
        main_topview.close_notification()
        log.info('合同创建成功')
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_house_code_search(house_info['house_code'])
        contract_table.input_customer_code_search(customer_info['customer_code'])
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        contract_code = contract_details['contract_code']
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_go_examine_button()  # 经纪人提交审核
        contract_detail.click_confirm_button()
        main_leftview.change_role('商圈经理')  # 商圈经理审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.pass_examine_by_row(1)
        main_leftview.change_role('合同法务')  # 法务审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.legal_examine_by_row(1)
        contract_preview.click_pass_button()
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_preview_button()
        contract_preview.click_signature_button()  # 签章
        main_topview.close_notification()
        contract_preview.click_print_with_sign_button()  # 打印
        contract_preview.cancel_print()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract()
        contract_detail.upload_two_sign_contract()  # 经纪人签约时间
        contract_detail.upload_pictures([cm.tmp_picture_file])  # 经纪人上传主体合同
        contract_info = contract_detail.get_contract_info()
        contract_detail.click_submit_button()
        contract_detail.click_report_achievement_button()  # 经纪人提交业绩审核
        achievement_detail.click_submit_button()
        main_leftview.change_role('商圈经理')  # 商圈经理业绩审核
        main_leftview.click_achievement_label()
        achievement_table.click_achievement_examine_tab()
        achievement_table.click_to_examine_tab()
        achievement_table.input_contract_code_search(contract_code)
        achievement_table.click_search_button()
        achievement_table.click_pass_examine_button_by_row(1)
        contract_table.update_agency_fee(contract_code)  # 数据库修改代理费
        main_leftview.change_role('权证专员')  # 权证专员过户
        main_leftview.click_on_way_order_label()
        transaction_table.click_contract_code_tab()
        transaction_table.input_search_text(contract_code)
        transaction_table.click_search_button()
        transaction_table.go_to_transaction_detail_by_row(1)
        transaction_detail.complete_transfer_house()
        transaction_detail.close_case()  # 权证专员结案
        main_topview.close_notification()
        transaction_detail.show_sensitive_info()  # 显示敏感信息
        transaction_info = transaction_detail.get_transaction_info()
        transaction_fund_info = transaction_detail.get_fund_info()
        transaction_buyer_info = transaction_detail.get_buyer_info()
        transaction_buyer_share_person_info = transaction_detail.get_buyer_share_person()
        transaction_seller_info = transaction_detail.get_seller_info()
        transaction_house_info = transaction_detail.get_house_info()
        transaction_management = ''  # 权证单内容的校验
        if ini.environment == 'ks':
            if contract_data['第四条信息']['支付方式'][0] == 1:
                transaction_management = '全款'
            if contract_data['第四条信息']['支付方式'][0] == 2:
                transaction_management = '商贷'
        if ini.environment == 'wx':
            if contract_data['第五条信息']['二'] == 1:
                transaction_management = '全款'
            if contract_data['第五条信息']['二'] == 2:
                transaction_management = '商贷'
        else:
            if contract_data['第四条信息']['选项'][0] == 1:
                transaction_management = '全款'
            if contract_data['第四条信息']['选项'][0] == 2:
                transaction_management = '商贷'
        assert transaction_info['交易管理'] == transaction_management
        assert transaction_info['交易编号'] == contract_code.replace('HE', 'QZ')
        assert transaction_info['合同编号'] == contract_code
        assert transaction_info['创建日期'] == contract_info['create_time']
        assert transaction_info['签约日期'] == contract_info['sign_time']
        if ini.environment == 'ks':
            assert transaction_info['合同约定办理资金托管日期'] == '-'
        elif ini.environment == 'wx':
            if contract_data['第五条信息']['二_2'][0][0][0] == 1:
                assert transaction_info['合同约定办理资金托管日期'] == '办理权属转移登记前'
            if contract_data['第五条信息']['二_2'][0][0][0] == 2:
                assert transaction_info['合同约定办理资金托管日期'] == '办理权属转移登记后' + contract_data['第五条信息']['二_2'][0][0][1] + '日内'
            if contract_data['第五条信息']['二_2'][0][0][0] == 3:
                assert transaction_info['合同约定办理资金托管日期'] == \
                       contract_data['第五条信息']['二_2'][0][0][1].split('-')[0] + '年' \
                       + contract_data['第五条信息']['二_2'][0][0][1].split('-')[1] + '月' \
                       + contract_data['第五条信息']['二_2'][0][0][1].split('-')[2] + '日' + '前'
            if contract_data['第五条信息']['二_2'][0][0][0] == 4:
                assert transaction_info['合同约定办理资金托管日期'] == '本合同签订当日'
            if contract_data['第五条信息']['二_2'][0][0][0] == 5:
                assert transaction_info['合同约定办理资金托管日期'] == '本合同签订后' + contract_data['第五条信息']['二_2'][0][0][1] + '日内'
            if contract_data['第五条信息']['二_2'][0][0][0] == 6:
                assert transaction_info['合同约定办理资金托管日期'] == '办理网签手续后' + contract_data['第五条信息']['二_2'][0][0][1] + '日内'
            if contract_data['第五条信息']['二_2'][0][0][0] == 6:
                assert transaction_info['合同约定办理资金托管日期'] == '办理资金托管手续后' + contract_data['第五条信息']['二_2'][0][0][1] + '日内'
        else:
            if transaction_info['交易管理'] == '全款':
                assert transaction_info['合同约定办理资金托管日期'] == \
                       contract_data['第四条信息']['选项'][1][1].split('-')[0] + '年' \
                       + contract_data['第四条信息']['选项'][1][1].split('-')[1] + '月' \
                       + contract_data['第四条信息']['选项'][1][1].split('-')[2] + '日'
            if transaction_info['交易管理'] == '商贷':
                assert transaction_info['合同约定办理资金托管日期'] == \
                       contract_data['第四条信息']['选项'][1][0].split('-')[0] + '年' \
                       + contract_data['第四条信息']['选项'][1][0].split('-')[1] + '月' \
                       + contract_data['第四条信息']['选项'][1][0].split('-')[2] + '日'
        if transaction_info['交易管理'] == '商贷':
            if ini.environment == 'sz':
                assert transaction_info['合同约定贷款审批通过日期'] == \
                       contract_data['第四条信息']['选项'][1][3].split('-')[0] + '年' \
                       + contract_data['第四条信息']['选项'][1][3].split('-')[1] + '月' \
                       + contract_data['第四条信息']['选项'][1][3].split('-')[2] + '日'
            else:
                assert transaction_info['合同约定贷款审批通过日期'] == '-'
        assert transaction_info['备注'] == '-'
        deposit = Decimal('0')
        if ini.environment == 'wx':
            for item in contract_data['第五条信息']['二_1']:
                deposit = deposit + Decimal(item[1])
            house_payment = Decimal(contract_data['第五条信息']['一'])
            # house_delivery_payment = Decimal('0')
            register_transfer_payment = Decimal(contract_data['第五条信息']['二_4'][0])
            property_delivery_payment = Decimal(contract_data['第五条信息']['二_5'][1])
            first_payment = Decimal('0')
            for item in contract_data['第五条信息']['二_2']:
                first_payment = first_payment + Decimal(item[1])
            if transaction_info['交易管理'] == '全款':
                assert Decimal(transaction_fund_info['成交总价'][:-1]) == deposit + first_payment + \
                       property_delivery_payment + register_transfer_payment
            if transaction_info['交易管理'] == '商贷':
                assert Decimal(transaction_fund_info['成交总价'][:-1]) == deposit + first_payment + \
                       Decimal(contract_data['第五条信息']['二_3'][1]) + property_delivery_payment + register_transfer_payment
            assert Decimal(transaction_fund_info['网签价'][:-1]) == house_payment
            assert Decimal(transaction_fund_info['首期款总额'][:-1]) == deposit + first_payment + register_transfer_payment \
                   + property_delivery_payment
            assert Decimal(transaction_fund_info['定金总额'][:-1]) == deposit
            assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == first_payment
            assert Decimal(transaction_fund_info['购房款/首付款（第一笔）'][:-1]) == Decimal(contract_data['第五条信息']['二_2'][0][1])
            if transaction_info['交易管理'] == '商贷':
                assert Decimal(transaction_fund_info['拟贷款金额'][:-1]) == Decimal(contract_data['第五条信息']['二_3'][1])
            # assert Decimal(transaction_fund_info['交房保证金'][:-1]) == house_delivery_payment
            assert Decimal(transaction_fund_info['户口迁出保证金'][:-1]) == register_transfer_payment
            assert Decimal(transaction_fund_info['物业交割保证金'][:-1]) == property_delivery_payment
        else:
            house_money = Decimal('0')
            if ini.environment == 'sz':
                for item in contract_data['补充协议']['定金']:
                    deposit = deposit + Decimal(item['金额'])
                for item in contract_data['补充协议']['房款']:
                    house_money = house_money + Decimal(item['金额'])
            if ini.environment == 'ks':
                for item in contract_data['补充协议']['首期款支付分期']:
                    deposit = deposit + Decimal(item['金额'])
            house_payment = Decimal(contract_data['第三条信息']['房屋价款'])
            house_delivery_payment = Decimal(contract_data['补充协议']['交房保证金']['金额'])
            register_transfer_payment = Decimal(contract_data['补充协议']['户口迁出保证金']['金额'])
            assert Decimal(transaction_fund_info['成交总价'][:-1]) == house_payment + deposit + house_delivery_payment \
                   + register_transfer_payment + house_money
            assert Decimal(transaction_fund_info['网签价'][:-1]) == house_payment
            assert Decimal(transaction_fund_info['首期款总额'][:-1]) == deposit + house_delivery_payment \
                   + register_transfer_payment + house_money
            if ini.environment == 'ks':
                assert Decimal(transaction_fund_info['定金总额'][:-1]) == \
                       Decimal(contract_data['第四条信息']['购房定金'])
            else:
                assert Decimal(transaction_fund_info['定金总额'][:-1]) == deposit
            if transaction_info['交易管理'] == '全款':
                if ini.environment == 'ks':
                    if contract_data['第四条信息']['支付方式'][1] == 1:
                        assert transaction_fund_info['首付款总金额'] == '无'
                    if contract_data['第四条信息']['支付方式'][1] == 2:
                        assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == \
                               Decimal(self.full_payment_contract_data2['第四条信息']['支付方式'][2][2])
                if ini.environment == 'sz':
                    assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == house_payment + house_delivery_payment \
                           + register_transfer_payment + house_money
                assert Decimal(transaction_fund_info['购房款/首付款（第一笔）'][:-1]) == house_payment
            if transaction_info['交易管理'] == '商贷':
                if ini.environment == 'ks':
                    assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == \
                           Decimal(contract_data['第四条信息']['支付方式'][2][1])
                    assert Decimal(transaction_fund_info['购房款/首付款（第一笔）'][:-1]) == \
                           Decimal(contract_data['第四条信息']['支付方式'][2][1])
                    assert Decimal(transaction_fund_info['拟贷款金额'][:-1]) == \
                           Decimal(contract_data['第四条信息']['支付方式'][3][0])
                if ini.environment == 'ks':
                    assert Decimal(transaction_fund_info['首付款总金额'][:-1]) == Decimal(
                        contract_data['第四条信息']['选项'][1][1])
                    assert Decimal(transaction_fund_info['购房款/首付款（第一笔）'][:-1]) == deposit + house_delivery_payment \
                           + register_transfer_payment + house_money
                    assert Decimal(transaction_fund_info['拟贷款金额'][:-1]) == house_payment \
                           - Decimal(contract_data['第四条信息']['选项'][1][1])
            assert Decimal(transaction_fund_info['交房保证金'][:-1]) == house_delivery_payment
            assert Decimal(transaction_fund_info['户口迁出保证金'][:-1]) == register_transfer_payment
        assert transaction_buyer_info['姓名'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_姓名']
        assert transaction_buyer_info['性质'] == '-'
        assert transaction_buyer_info['性别'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_性别']
        assert transaction_buyer_info['国籍'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_国籍']
        assert transaction_buyer_info['证件类型'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_证件名称']
        assert transaction_buyer_info['证件号码'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_证件号码']
        assert transaction_buyer_info['联系电话'] == contract_data['房屋买受人信息']['房屋买受人']['房屋买受人_联系电话']
        assert transaction_buyer_info['其他联系方式'] == '--'
        assert transaction_buyer_info['户籍'] == '--'
        assert transaction_buyer_info['婚姻状况'] == '--'
        assert transaction_buyer_info['买方家庭住房套数'] == '--'
        assert transaction_buyer_share_person_info['姓名'] == \
               contract_data['房屋买受人信息']['共同买受人'][0]['共同买受人_姓名']
        assert transaction_buyer_share_person_info['性质'] == '-'
        assert transaction_buyer_share_person_info['性别'] == \
               contract_data['房屋买受人信息']['共同买受人'][0]['共同买受人_性别']
        assert transaction_buyer_share_person_info['国籍'] == \
               contract_data['房屋买受人信息']['共同买受人'][0]['共同买受人_国籍']
        assert transaction_buyer_share_person_info['证件类型'] == \
               contract_data['房屋买受人信息']['共同买受人'][0]['共同买受人_证件名称']
        assert transaction_buyer_share_person_info['证件号码'] == \
               contract_data['房屋买受人信息']['共同买受人'][0]['共同买受人_证件号码']
        assert transaction_buyer_share_person_info['联系电话'] == \
               contract_data['房屋买受人信息']['共同买受人'][0]['共同买受人_联系电话']
        assert transaction_buyer_share_person_info['其他联系方式'] == '--'
        assert transaction_buyer_share_person_info['户籍'] == '--'
        assert transaction_buyer_share_person_info['婚姻状况'] == '--'
        assert transaction_buyer_share_person_info['买方家庭住房套数'] == '--'
        assert transaction_seller_info['姓名'] == contract_data['房屋出卖人信息']['房屋出卖人_姓名']
        assert transaction_seller_info['性质'] == '-'
        assert transaction_seller_info['性别'] == contract_data['房屋出卖人信息']['房屋出卖人_性别']
        assert transaction_seller_info['国籍'] == contract_data['房屋出卖人信息']['房屋出卖人_国籍']
        assert transaction_seller_info['证件类型'] == contract_data['房屋出卖人信息']['房屋出卖人_证件名称']
        assert transaction_seller_info['证件号码'] == contract_data['房屋出卖人信息']['房屋出卖人_证件号码']
        assert transaction_seller_info['联系电话'] == contract_data['房屋出卖人信息']['房屋出卖人_联系电话']
        assert transaction_seller_info['其他联系方式'] == '--'
        assert transaction_seller_info['婚姻状况'] == '--'
        assert transaction_house_info['房源编号'] == house_info['house_code']
        if ini.environment == 'ks':
            assert transaction_house_info['规划用途'] == '-'
            assert transaction_house_info['建筑面积'] == contract_data['第一条信息']['产权登记面积'] + 'm²'
            assert transaction_house_info['建成年代'] == '-'
            assert transaction_house_info['共有权证号'] == '-'
        elif ini.environment == 'wx':
            if contract_data['第一条信息']['三'][0] == 1:
                assert transaction_house_info['规划用途'] == '住宅'
            if contract_data['第一条信息']['三'][0] == 2:
                assert transaction_house_info['规划用途'] == '公寓'
            if contract_data['第一条信息']['三'][0] == 3:
                assert transaction_house_info['规划用途'] == '别墅'
            if contract_data['第一条信息']['三'][0] == 4:
                assert transaction_house_info['规划用途'] == '办公'
            if contract_data['第一条信息']['三'][0] == 5:
                assert transaction_house_info['规划用途'] == '商业'
            if contract_data['第一条信息']['三'][0] == 6:
                assert transaction_house_info['规划用途'] == '工业'
            if contract_data['第一条信息']['三'][0] == 7:
                assert transaction_house_info['规划用途'] == '其他' + contract_data['第一条信息']['三'][1]
            assert transaction_house_info['建筑面积'] == contract_data['第一条信息']['建筑面积'] + 'm²'
            assert transaction_house_info['建成年代'] == '-'
            assert transaction_house_info['共有权证号'] == contract_data['第二条信息']['一_持证方式'][1]
        else:
            assert transaction_house_info['规划用途'] == contract_data['第一条信息']['房屋用途']
            assert transaction_house_info['建筑面积'] == contract_data['第一条信息']['产权登记建筑面积'] + 'm²'
            assert transaction_house_info['建成年代'] == contract_data['第一条信息']['房屋建成年份']
            if contract_data['第二条信息']['房屋权证状况'][0] == 1:
                assert transaction_house_info['共有权证号'] == '-'
            if contract_data['第二条信息']['房屋权证状况'][0] == 2:
                assert transaction_house_info['共有权证号'] == contract_data['第二条信息']['房屋权证状况'][1]
        if ini.environment == 'wx':
            if contract_data['第一条信息']['四'][0] == 1:
                assert transaction_house_info['房屋性质'] == '商品房'
            if contract_data['第一条信息']['四'][0] == 2:
                assert transaction_house_info['房屋性质'] == '房改房'
            if contract_data['第一条信息']['四'][0] == 3:
                assert transaction_house_info['房屋性质'] == '安置房'
            if contract_data['第一条信息']['四'][0] == 4:
                assert transaction_house_info['房屋性质'] == '向社会公开销售的经济适用住房'
            if contract_data['第一条信息']['四'][0] == 5:
                assert transaction_house_info['房屋性质'] == '其他房屋' + contract_data['第一条信息']['四'][1]
        else:
            assert transaction_house_info['房屋性质'] == '-'
        assert transaction_house_info['楼盘名称'] == house_info['estate_name']
        if ini.environment == 'wx':
            if contract_data['第二条信息']['一_权属状况'][0] == 1:
                assert transaction_house_info['房本类型'] == '不动产权证'
            if contract_data['第二条信息']['一_权属状况'][0] == 2:
                assert transaction_house_info['房本类型'] == '房屋所有权证'
            assert transaction_house_info['产权证号'] == contract_data['第二条信息']['一_权属状况'][1]
        else:
            assert transaction_house_info['房本类型'] == '-'
            assert transaction_house_info['产权证号'] == contract_data['第一条信息']['房屋所有权证编号']
        if house_key_info['house_state'] == '-':
            house_key_info['house_state'] = '--'
        assert transaction_house_info['房屋现状'] == house_key_info['house_state']
        assert transaction_house_info['物业地址'] == house_info['estate_name'] + house_info['building_name'] + '-' + \
               house_info['unit_name'] + '-' + house_info['floor'] + '-' + house_info['door_name']
        if ini.environment == 'wx':
            assert transaction_house_info['行政区域'] == '-'
        else:
            assert transaction_house_info['行政区域'] == contract_data['第一条信息']['区']
        if ini.environment == 'wx':
            if contract_data['第二条信息']['三'][0] == 1:
                assert transaction_house_info['是否有抵押'] == '无抵押'
                assert transaction_house_info['合同约定的注销抵押日期'] == '-'
            if contract_data['第二条信息']['三'][0] == 2:
                assert transaction_house_info['是否有抵押'] == '有抵押'
                assert transaction_house_info['合同约定的注销抵押日期'] == \
                       contract_data['第二条信息']['三'][1][1].split('-')[0] + '年' \
                       + contract_data['第二条信息']['三'][1][1].split('-')[1] + '月' \
                       + contract_data['第二条信息']['三'][1][1].split('-')[2] + '日'
        else:
            if contract_data['第二条信息']['房屋抵押状况'][0] == 1:
                assert transaction_house_info['是否有抵押'] == '无抵押'
                assert transaction_house_info['合同约定的注销抵押日期'] == '-'
            if contract_data['第二条信息']['房屋抵押状况'][0] == 2:
                assert transaction_house_info['是否有抵押'] == '有抵押'
                assert transaction_house_info['合同约定的注销抵押日期'] == \
                       contract_data['第二条信息']['房屋抵押状况'][1][1].split('-')[0] + '年' \
                       + contract_data['第二条信息']['房屋抵押状况'][1][1].split('-')[1] + '月' \
                       + contract_data['第二条信息']['房屋抵押状况'][1][1].split('-')[2] + '日'
        if house_key_info['is_unique'] == '不唯一':
            assert transaction_house_info['是否唯一'] == '否'
        if house_key_info['is_unique'] == '唯一':
            assert transaction_house_info['是否唯一'] == '是'
        if house_key_info['is_unique'] == '-':
            assert transaction_house_info['是否唯一'] == '-'
        assert transaction_house_info['产证年限'] == house_key_info['house_property_limit']
        assert transaction_house_info['是否限售房'] == '--'
