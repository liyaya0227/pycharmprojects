#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_report_data.py
@date: 2021/8/23 0023
"""

import pytest
import allure
import random
import string
from decimal import *
from random import randint
from config.conf import cm
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_data
from utils.timeutil import dt_strftime, dt_strftime_with_delta
from page_object.web.login.loginpage import LoginPage
from page_object.web.agreement.listpage import AgreementListPage
from page_object.web.main.certificateexaminepage import CertificateExaminePage
from page_object.web.main.rightviewpage import MainRightViewPage
from page_object.web.main.topviewpage import MainTopViewPage
from page_object.web.main.upviewpage import MainUpViewPage
from page_object.web.main.leftviewpage import MainLeftViewPage
from page_object.web.house.addpage import HouseAddPage
from page_object.web.house.tablepage import HouseTablePage
from page_object.web.house.detailpage import HouseDetailPage
from page_object.web.customer.detailpage import CustomerDetailPage
from page_object.web.customer.tablepage import CustomerTablePage
from page_object.web.achievement.detailpage import AchievementDetailPage
from page_object.web.achievement.tablepage import AchievementTablePage
from page_object.web.contract.createorderpage import ContractCreateOrderPage
from page_object.web.contract.detailpage import ContractDetailPage
from page_object.web.contract.previewpage import ContractPreviewPage
from page_object.web.contract.tablepage import ContractTablePage
from page_object.web.transaction.tablepage import TransactionTablePage
from page_object.web.transaction.detailpage import TransactionDetailPage
from page_object.web.contractreport.tablepage import ContractReportTablePage
from page_object.web.receivedachievementreport.tablepage import ReceivedAchievementReportTablePage
from page_object.web.paymentflow.tablepage import PaymentFlowTablePage
from page_object.web.finance.tablepage import FinanceTablePage
from page_object.web.shopsplitaccountreport.tablepage import ShopBrandDataReportTablePage
from page_object.web.brandsplitaccountreport.tablepage import BrandSplitAccountReportTablePage
from page_object.web.financereport.tablepage import FinanceReportTablePage
from page_object.web.surveysplitaccountreport.tablepage import SurveySplitAccountReportTablePage
from page_object.web.finance.detailpage import FinanceDetailPage
from page_object.web.survey.tablepage import SurveyTablePage
from page_object.web.survey.detailpage import SurveyDetailPage
from page_object.web.user.tablepage import UserTablePage
from page_object.web.shop.tablepage import ShopTablePage
from page_object.web.shop.detailpage import ShopDetailPage
from page_object.app.login.loginpage import AppLoginPage
from page_object.app.main.mainpage import AppMainPage
from page_object.app.mine.minepage import AppMinePage
from page_object.app.order.tablepage import AppOrderTablePage
from page_object.app.order.detailpage import AppOrderDetailPage

role_info = {}
contract_info = {}


@allure.feature("测试报表数据模块")
class TestReportData(object):

    json_file_path = cm.test_data_dir + "/test_sale/test_report/test_report_data_" + ini.environment + ".json"
    test_data = get_data(json_file_path)
    house_data = test_data['房源信息']
    customer_data = test_data['客源信息']
    agreement_data = test_data['协议信息']
    survey_data = test_data['实勘信息']
    contract_data = test_data['合同信息']
    customer_partner_data = test_data['客源合作人信息']

    house_data['楼盘'] = ini.house_community_name
    house_data['楼栋'] = ini.house_building_id
    house_data['门牌号'] = ini.house_doorplate
    customer_data['电话号'] = ini.custom_telephone

    @pytest.fixture(scope="class", autouse=True)
    def test_prepare(self, web_driver, android_driver):
        global contract_info
        global role_info

        login = LoginPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_add = HouseAddPage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_detail = CustomerDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)
        certificate_examine = CertificateExaminePage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_create_order = ContractCreateOrderPage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        achievement_table = AchievementTablePage(web_driver)
        achievement_detail = AchievementDetailPage(web_driver)
        transaction_table = TransactionTablePage(web_driver)
        transaction_detail = TransactionDetailPage(web_driver)
        survey_table = SurveyTablePage(web_driver)
        survey_detail = SurveyDetailPage(web_driver)
        finance_detail = FinanceDetailPage(web_driver)
        shop_brand_data_report = ShopBrandDataReportTablePage(web_driver)
        survey_split_account_report = SurveySplitAccountReportTablePage(web_driver)
        user_table = UserTablePage(web_driver)
        shop_table = ShopTablePage(web_driver)
        shop_detail = ShopDetailPage(web_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)
        app_login = AppLoginPage(android_driver)
        app_order_table = AppOrderTablePage(android_driver)
        app_order_detail = AppOrderDetailPage(android_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        if house_table.get_house_code_by_db(flag='买卖') == '':  # 判断房源是否存在，不存在则新增
            house_table.click_add_house_button()
            house_add.choose_sale_radio()
            house_add.choose_estate_name(ini.house_community_name)
            house_add.choose_building_id(ini.house_building_id)
            house_add.choose_building_cell(ini.house_building_cell)
            house_add.choose_floor(ini.house_floor)
            house_add.choose_doorplate(ini.house_doorplate)
            house_add.click_next_button()
            house_add.input_owner_info_and_house_info(self.house_data, '买卖')
            main_topview.close_notification()
            main_upview.clear_all_title()
            main_leftview.click_all_house_label()
        house_code = house_table.get_house_code_by_db(flag='买卖')
        # 更新房源创建时间
        house_table.update_house_create_time_by_db(house_code, dt_strftime_with_delta(-8, "%Y-%m-%d %H:%M:%S"))
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        contract_info['房源编号'] = house_code
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(row=1)
        house_info = house_detail.get_address_dialog_house_property_address()
        house_info['house_code'] = house_code
        house_info['house_type'] = house_detail.get_house_type()
        house_info['orientations'] = house_detail.get_orientations()
        house_info['floor'] = house_detail.get_floor_dialog_house_floor()
        house_info['inspect_type'] = house_detail.get_inspect_type()
        house_info['house_state'] = house_detail.get_house_state()
        assert house_info != {}
        log.info('获取房源信息，新建合同校验需要')
        main_leftview.log_out()  # 上传协议
        login.log_in(self.agreement_data['协议人信息']['电话'], self.agreement_data['协议人信息']['密码'])  # 切换其他门店经纪人账号上传协议
        main_leftview.change_role('经纪人')
        main_leftview.click_agreement_list_label()
        if ini.environment != 'wx':
            agreement_list.input_agreement_name_search('一般委托书')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            written_entrustment_agreement_number = agreement_list.get_written_entrustment_agreement_number()
            self.agreement_data['written_entrustment_agreement']['委托协议编号'] = written_entrustment_agreement_number
            agreement_list.input_agreement_name_search('钥匙托管协议')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            key_entrustment_certificate_number = agreement_list.get_key_entrustment_certificate_number()
            self.agreement_data['key_entrustment_certificate']['协议编号'] = key_entrustment_certificate_number
            agreement_list.input_agreement_name_search('房屋出售委托协议VIP版')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            vip_service_entrustment_agreement_number = agreement_list.get_vip_service_entrustment_agreement_number()
            self.agreement_data['vip_service_entrustment_agreement']['委托协议编号'] = \
                vip_service_entrustment_agreement_number
        else:
            agreement_list.input_agreement_name_search('限时委托代理销售协议')
            agreement_list.click_query_button()
            agreement_list.click_download_button_by_row(1)
            written_entrustment_agreement_number = agreement_list.get_written_entrustment_agreement_number()
            self.agreement_data['written_entrustment_agreement']['委托协议编号'] = written_entrustment_agreement_number
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.expand_certificates_info()
        if house_detail.check_upload_written_entrustment_agreement() != '未上传':
            house_detail.delete_written_entrustment_agreement()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_written_entrustment_agreement(self.agreement_data['written_entrustment_agreement'])
        main_topview.close_notification()
        log.info('书面委托协议已上传')
        if ini.environment != 'wx':
            house_detail.expand_certificates_info()
            if house_detail.check_upload_key_entrustment_certificate() != '未上传':
                house_detail.delete_key_entrustment_certificate()
                assert main_topview.find_notification_content() == '操作成功'
                house_detail.page_refresh()
                house_detail.expand_certificates_info()
            house_detail.upload_key_entrustment_certificate(self.agreement_data['key_entrustment_certificate'])
            main_topview.close_notification()
            log.info('钥匙委托凭证已上传')
            # house_detail.expand_certificates_info()
            # if house_detail.check_upload_vip_service_entrustment_agreement() != '未上传':
            #     house_detail.delete_vip_service_entrustment_agreement()
            #     assert main_topview.find_notification_content() == '操作成功'
            #     house_detail.page_refresh()
            #     house_detail.expand_certificates_info()
            # house_detail.upload_vip_service_entrustment_agreement(
            #     self.agreement_data['vip_service_entrustment_agreement'])
            # main_topview.close_notification()
            # log.info('VIP服务委托协议已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_deed_tax_invoice() != '未上传':
            house_detail.delete_deed_tax_invoice()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_deed_tax_invoice_information(self.agreement_data['deed_tax_invoice_information'])
        main_topview.close_notification()
        log.info('契税票已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_owner_identification_information() != '未上传':
            house_detail.delete_owner_identification_information()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_owner_identification_information(self.agreement_data['owner_identification_information'])
        main_topview.close_notification()
        log.info('身份证明已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_original_purchase_contract_information() != '未上传':
            house_detail.delete_original_purchase_contract_information()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_original_purchase_contract_information(
            self.agreement_data['original_purchase_contract_information'])
        main_topview.close_notification()
        log.info('原始购房合同已上传')
        house_detail.expand_certificates_info()
        if house_detail.check_upload_property_ownership_certificate() != '未上传':
            house_detail.delete_property_ownership_certificate()
            assert main_topview.find_notification_content() == '操作成功'
            house_detail.page_refresh()
            house_detail.expand_certificates_info()
        house_detail.upload_property_ownership_certificate(self.agreement_data['property_ownership_certificate'])
        main_topview.close_notification()
        log.info('房产证已上传')
        main_leftview.log_out()
        login.log_in(ini.user_account, ini.user_password)
        main_leftview.change_role('赋能经理')
        main_rightview.click_certificate_examine()
        certificate_examine.pass_written_entrustment_agreement_examine(house_code)
        house_detail.update_approval_records_update_time_by_db(house_code,
                                                               dt_strftime_with_delta(-2, "%Y-%m-%d %H:%M:%S"),
                                                               '书面委托协议', flag='买卖')
        if ini.environment != 'wx':
            certificate_examine.pass_key_entrustment_certificate_examine(house_code)
            house_detail.update_approval_records_update_time_by_db(house_code,
                                                                   dt_strftime_with_delta(-2, "%Y-%m-%d %H:%M:%S"),
                                                                   '钥匙委托凭证', flag='买卖')
            certificate_examine.pass_vip_service_entrustment_agreement_examine(house_code)
            house_detail.update_approval_records_update_time_by_db(house_code,
                                                                   dt_strftime_with_delta(-2, "%Y-%m-%d %H:%M:%S"),
                                                                   'VIP服务委托协议', flag='买卖')
        certificate_examine.pass_property_ownership_certificate_examine(house_code)
        main_leftview.change_role('经纪人')  # 上传实勘
        main_leftview.click_all_house_label()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        if house_detail.check_survey_status() == '已预约':
            log.info('未预约实勘，进行实勘预约')  # 须优化实勘已上传的情况
            main_leftview.change_role('超级管理员')
            main_leftview.click_survey_management_label()
            survey_table.input_house_code_search(house_code)
            survey_table.click_search_button()
            survey_person_phone = survey_table.get_survey_person_phone_by_row(1)
            main_leftview.log_out()
            login.log_in(survey_person_phone, 'Autotest1')  # 切换其他门店经纪人账号预约实勘
            main_leftview.change_role('实勘人员')
            main_leftview.click_survey_management_label()
            survey_table.input_house_code_search(house_code)
            survey_table.click_search_button()
            survey_table.click_back_order_button_by_row(1)
            survey_table.back_order_dialog_choose_reason('其他')
            survey_table.back_order_dialog_click_back_order_button()
        elif house_detail.check_survey_status() == '已上传':
            main_leftview.change_role('超级管理员')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
            house_detail.click_delete_survey_button()
            house_detail.dialog_click_confirm_button()
        else:
            pass
        main_leftview.log_out()
        login.log_in(self.survey_data['实勘人电话'], self.survey_data['实勘人密码'])  # 切换其他门店经纪人账号预约实勘
        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.click_survey_appointment_button()
        house_detail.dialog_choose_normal_survey()
        house_detail.dialog_choose_photographer(self.survey_data['实勘部姓名'])
        house_detail.dialog_choose_exploration_time(self.survey_data['预约实勘时间'])
        house_detail.dialog_input_appointment_instructions(self.survey_data['预约说明'])
        house_detail.dialog_click_confirm_button()
        main_upview.clear_all_title()
        if not app_login.check_login_page():
            app_main.close_top_view()
            app_main.click_mine_button()
            app_mine.log_out()
        app_login.log_in(self.survey_data['实勘部电话'], self.survey_data['实勘部密码'])
        app_main.click_mine_button()
        if '实勘人员' not in app_mine.get_user_role():
            app_mine.click_change_role_button()
            app_mine.change_role_choose_role('实勘人员')
            app_mine.change_role_click_confirm_button()
        app_main.click_order_button()
        app_order_table.click_search_button()
        app_order_table.input_search_content(house_code)
        if self.survey_data['预约实勘时间'][0] == '今天':
            date = dt_strftime("%d %m %Y")
        elif self.survey_data['预约实勘时间'][0] == '明天':
            date = dt_strftime_with_delta(1, "%d %m %Y")
        else:
            raise '传值错误'
        app_order_table.choose_date(date)
        app_order_table.go_order_detail_by_index(1)
        app_order_detail.click_start_shot_button()
        app_order_detail.click_end_shot_button()
        main_leftview.log_out()
        login.log_in(self.survey_data['实勘部电话'], self.survey_data['实勘部密码'])
        main_leftview.change_role('实勘人员')
        survey_part_info = {"品牌": main_rightview.get_login_person_brand(),
                            "姓名": self.survey_data['实勘部姓名'],
                            "店组": main_rightview.get_login_person_shop_group(),
                            "电话": self.survey_data['实勘部电话']}
        main_leftview.click_survey_management_label()
        survey_table.click_reset_button()
        survey_table.input_house_code_search(house_code)
        survey_table.click_search_button()
        survey_table.click_upload_survey_button_by_row(1)
        upload_pictures = [cm.tmp_picture_file, cm.tmp_picture_file]
        survey_detail.upload_picture(upload_pictures)
        survey_detail.set_title_picture_by_index(randint(1, len(upload_pictures)))
        survey_detail.click_save_button()
        house_detail.update_survey_claim_create_time_by_db(house_code, dt_strftime_with_delta(-3, "%Y-%m-%d %H:%M:%S"))
        main_leftview.log_out()
        login.log_in(ini.user_account, ini.user_password)
        main_leftview.change_role('经纪人')
        deal_person_info = {"品牌": main_rightview.get_login_person_brand(),
                            "姓名": main_rightview.get_login_person_name(),
                            "店组": main_rightview.get_login_person_shop_group(),
                            "电话": main_rightview.get_login_person_phone()}
        main_leftview.click_all_house_label()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        role_info = house_detail.get_all_valid_role_info()
        role_info['实勘部'] = survey_part_info
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()  # 获取客源信息
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
        customer_code = customer_table.get_customer_code_by_row(1)
        assert customer_code != ''
        log.info('获取客源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_create_order_button()
        contract_create_order.input_house_code(house_info['house_code'])
        contract_create_order.click_get_house_info_button()
        contract_create_order.verify_house_info(house_info)
        contract_create_order.click_verify_house_button()
        log.info('房源信息校验通过')
        contract_create_order.input_customer_code(customer_code)
        contract_create_order.click_get_customer_info_button()
        contract_create_order.click_next_step_button()
        if ini.environment == 'sz' or ini.environment == 'ks':
            contract_create_order.choose_district_contract()
            contract_create_order.click_confirm_button_in_dialog()
        contract_create_order.input_contract_content(self.contract_data, '买卖')
        contract_create_order.click_submit_button()
        main_topview.close_notification()
        log.info('合同创建成功')
        role_info['房源成交人'] = deal_person_info
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_house_code_search(house_info['house_code'])
        contract_table.input_customer_code_search(customer_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        contract_code = contract_details['contract_code']
        contract_info['合同编号'] = contract_code
        contract_info['物业地址'] = contract_details['house_address']
        contract_info['代理费'] = contract_details['agency_fee']
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_go_examine_button()  # 经纪人提交审核
        contract_detail.click_confirm_button()
        main_leftview.change_role('商圈经理')  # 商圈经理审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.pass_examine_by_row(1)
        main_leftview.change_role('合同法务')  # 法务审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.legal_examine_by_row(1)
        contract_preview.click_pass_button()
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
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
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract()
        contract_detail.upload_two_sign_contract()  # 经纪人签约时间
        main_topview.close_notification()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract()
        contract_detail.upload_pictures([cm.tmp_picture_file])  # 经纪人上传主体合同
        contract_detail.click_submit_button()
        contract_detail.click_report_achievement_button()  # 经纪人提交业绩审核
        achievement_detail.add_customer_partner([self.customer_partner_data])
        achievement_detail.click_submit_button()
        role_info['客源合作人'] = self.customer_partner_data
        main_leftview.change_role('商圈经理')  # 商圈经理业绩审核
        main_leftview.click_achievement_label()
        achievement_table.click_achievement_examine_tab()
        achievement_table.click_to_examine_tab()
        achievement_table.input_contract_code_search(contract_code)
        achievement_table.click_search_button()
        achievement_table.click_pass_examine_button_by_row(1)
        main_topview.close_notification()
        main_leftview.change_role('超级管理员')  # 线下付款
        contract_info['收款人'] = main_rightview.get_login_person_name()
        all_pay_info = {}
        payers = ['业主', '客户']
        for n in range(len(payers)):
            pay_info = {}
            main_leftview.click_contract_management_label()
            contract_table.click_sale_contract_tab()
            contract_table.input_contract_code_search(contract_code)
            contract_table.click_search_button()
            contract_table.contract_offline_collection_by_row(1)
            if contract_table.offline_collection_dialog_get_pay_money_by_payer(payers[n]) == '0.00':
                contract_table.dialog_click_cancel_button()
                continue
            contract_table.offline_collection_dialog_choose_payer(payers[n])
            contract_table.offline_collection_dialog_input_payer_time(
                dt_strftime_with_delta(-(len(payers)-n), '%Y-%m-%d %H:%M:%S'))
            contract_table.offline_collection_dialog_input_bank_serial(
                "".join(map(lambda x: random.choice(string.digits), range(8))))
            contract_table.offline_collection_dialog_upload_bank_receipt([cm.tmp_picture_file])
            pay_info['支付金额'] = payers[n]
            pay_info['支付金额'] = str(Decimal(contract_table.offline_collection_dialog_get_pay_money())
                                   .quantize(Decimal('0.00')))
            contract_table.dialog_click_confirm_button()
            main_upview.clear_all_title()
            main_leftview.click_contract_management_label()
            contract_table.input_contract_code_search(contract_code)
            contract_table.click_search_button()
            contract_table.go_contract_detail_by_row(row=1)
            contract_detail.click_finance_detail_tab()
            finance_detail.refresh()
            first_row_data = finance_detail.get_table_row_data(1)
            pay_info['收款ID'] = first_row_data['收款ID']
            pay_info['支付时间'] = first_row_data['付款时间']
            main_upview.clear_all_title()
            all_pay_info[str(n+1)] = pay_info
        contract_info['支付信息'] = all_pay_info
        main_leftview.change_role('权证专员')  # 权证专员过户
        main_leftview.click_on_way_order_label()
        transaction_table.click_contract_code_tab()
        transaction_table.input_search_text(contract_code)
        transaction_table.click_search_button()
        transaction_table.go_to_transaction_detail_by_row(1)
        transaction_detail.complete_transfer_house()
        transaction_detail.close_case()  # 权证专员结案
        main_topview.close_notification()
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_info['合同价格'] = contract_detail.get_contract_price()
        contract_info['盖章时间'] = contract_detail.get_last_seal_time()
        contract_info['签约时间'] = contract_detail.get_sign_time()
        contract_detail.click_achievement_detail_tab()
        contract_info['审核时间'] = achievement_detail.get_examine_time()
        main_leftview.change_role('超级管理员')  # 打款
        main_leftview.click_shop_split_account_data_table_label()
        shop_brand_data_report.click_wait_split_account_tab()
        shop_brand_data_report.input_contract_code_search(contract_code)
        shop_brand_data_report.clear_pay_time_search()
        shop_brand_data_report.click_search_button()
        shop_brand_data_report.pay_money_all_table()
        main_upview.clear_all_title()
        main_leftview.click_brand_rebate_data_table_label()
        shop_brand_data_report.click_wait_rebate_commission_tab()
        shop_brand_data_report.input_contract_code_search(contract_code)
        shop_brand_data_report.clear_pay_time_search()
        shop_brand_data_report.click_search_button()
        shop_brand_data_report.pay_money_all_table()
        main_leftview.click_survey_department_split_account_label()
        survey_split_account_report.click_wait_split_account_tab()
        survey_split_account_report.input_contract_code_search(contract_code)
        survey_split_account_report.clear_pay_time_search()
        survey_split_account_report.click_search_button()
        survey_split_account_report.pay_money_all_table()
        main_upview.clear_all_title()
        main_leftview.change_role('超级管理员')  # 获取角色相关信息
        sum_other_proportion = Decimal('0')
        for key, value in role_info.items():
            main_leftview.click_user_management_label()
            user_table.input_phone_search(value['电话'])
            user_table.click_search_button()
            shop_info = user_table.get_shop_info_by_row(1)
            if '客源合作人' in key:
                role_info[key]['店组'] = user_table.get_shop_group_info_by_row(1)
            role_info[key]['门店'] = shop_info['门店名']
            main_leftview.click_shop_management_label()
            shop_table.input_shop_name_search(shop_info['门店名'])
            shop_table.click_search_button()
            role_info[key]['公司'] = shop_table.get_company_by_shop_code(shop_info['门店号'])
            if '客源合作人' in key:
                role_info[key]['品牌'] = shop_table.get_brand_by_shop_code(shop_info['门店号'])
            shop_table.edit_shop_info_by_shop_code(shop_info['门店号'])
            role_info[key]['大区'] = shop_detail.get_region()
            role_info[key]['OD'] = shop_detail.get_od_name()
            role_info[key]['商圈'] = shop_detail.get_district()
            role_info[key]['OM'] = shop_detail.get_om_name()
            if key == '房源录入人':
                role_info[key]['比例'] = '10'
            elif key == '房源维护人':
                role_info[key]['比例'] = '15'
            elif key == '房源委托人':
                if ini.environment != 'wx':
                    role_info[key]['比例'] = '5'
                elif ini.environment == 'wx':
                    role_info[key]['比例'] = '2'
            elif key == '房源钥匙人':
                role_info[key]['比例'] = '5'
            elif key == '房源VIP服务人':
                role_info[key]['比例'] = '10'
            elif key == '房源实勘人':
                role_info[key]['比例'] = '2'
            elif key == '实勘部':
                role_info[key]['比例'] = '3'
            if key != '房源成交人':
                sum_other_proportion = sum_other_proportion + Decimal(role_info[key]['比例'])
            main_upview.clear_all_title()
        role_info['房源成交人']['比例'] = str(Decimal('100') - sum_other_proportion)

    @pytest.fixture(scope="function", autouse=True)
    def after_function_handle(self, web_driver):
        main_upview = MainUpViewPage(web_driver)

        yield
        main_upview.clear_all_title()

    @allure.story("测试合同业绩详情列表数据用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_001(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        achievement_detail = AchievementDetailPage(web_driver)

        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(contract_info['合同编号'])
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(row=1)
        contract_detail.click_achievement_detail_tab()
        proportion_table_data = achievement_detail.get_proportion_table_data()
        for row_data in proportion_table_data:
            pytest.assume(Decimal(row_data['分配比例']).quantize(Decimal('0.00')) ==
                          Decimal(role_info[row_data['角色类型']]['比例']).quantize(Decimal('0.00')))
            pytest.assume(row_data['角色人'] == role_info[row_data['角色类型']]['姓名'])
            pytest.assume(row_data['角色人店组'] == role_info[row_data['角色类型']]['店组'])
            # pytest.assume(row_data['商圈经理'] == role_info[row_data['角色类型']]['商圈经理'])
            pytest.assume(row_data['加盟商'] == role_info[row_data['角色类型']]['公司'])
        achievement_detail.click_receivable_achievement_tab()
        receivable_achievement_table_data = achievement_detail.get_achievement_table_data()
        for row_data in receivable_achievement_table_data:
            pytest.assume(row_data['结算月'] == contract_info['盖章时间'].split('-')[0] + contract_info['盖章时间'].split('-')[1])
            pytest.assume(row_data['业务类型'] == '二手买卖')
            pytest.assume(row_data['费用项'] == '居间代理费')
            pytest.assume(Decimal(row_data['分配比例'].split('%')[0]).quantize(Decimal('0.00')) ==
                          Decimal(role_info[row_data['角色类型']]['比例']).quantize(Decimal('0.00')))
            pytest.assume(row_data['角色人'] == role_info[row_data['角色类型']]['姓名'])
            pytest.assume(row_data['角色人店组'] == role_info[row_data['角色类型']]['店组'])
            # pytest.assume(row_data['商圈经理'] == role_info[row_data['角色类型']]['商圈经理'])
            if ini.environment == 'sz' or ini.environment == 'ks':
                pytest.assume(Decimal(row_data['业绩额']).quantize(Decimal('0.00')) ==
                              ((Decimal(contract_info['代理费']) - Decimal('500')) * Decimal('0.92')
                               * Decimal(row_data['分配比例'].split('%')[0]) / Decimal('100')
                               * Decimal('0.998')).quantize(Decimal('0.00'), ROUND_DOWN))
            elif ini.environment == 'wx':
                pytest.assume(Decimal(row_data['业绩额']).quantize(Decimal('0.00')) ==
                              ((Decimal(contract_info['代理费'])) * Decimal('0.92')
                               * Decimal(row_data['分配比例'].split('%')[0]) / Decimal('100') * Decimal('0.998'))
                              .quantize(Decimal('0.00'), ROUND_DOWN))
            elif ini.environment == 'hz':
                pytest.assume(Decimal(row_data['业绩额']).quantize(Decimal('0.00')) ==
                              ((Decimal(contract_info['代理费'])) * Decimal('0.92')
                               * Decimal(row_data['分配比例'].split('%')[0]) / Decimal('100') * Decimal('0.994'))
                              .quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(row_data['加盟商'] == role_info[row_data['角色类型']]['公司'])
        achievement_detail.click_received_achievement_tab()
        received_achievement_table_data = achievement_detail.get_achievement_table_data()
        for row_data in received_achievement_table_data:
            pytest.assume(row_data['结算月'] == contract_info['盖章时间'].split('-')[0] + contract_info['盖章时间'].split('-')[1])
            pytest.assume(row_data['业务类型'] == '二手买卖')
            pytest.assume(row_data['费用项'] == '居间代理费')
            pytest.assume(Decimal(row_data['分配比例']).quantize(Decimal('0.00')) ==
                          Decimal(role_info[row_data['角色类型']]['比例']).quantize(Decimal('0.00')))
            pytest.assume(row_data['角色人'] == role_info[row_data['角色类型']]['姓名'])
            pytest.assume(row_data['角色人店组'] == role_info[row_data['角色类型']]['店组'])
            # pytest.assume(row_data['商圈经理'] == role_info[row_data['角色类型']]['商圈经理'])
            pay_money = Decimal('0.00')
            for key, value in contract_info['支付信息'].items():
                pay_money = pay_money + Decimal(value['支付金额'])
            if ini.environment == 'sz' or ini.environment == 'ks':
                pytest.assume(Decimal(row_data['业绩额']).quantize(Decimal('0.00')) == ((pay_money - Decimal('500'))
                              * Decimal('0.92') * Decimal(row_data['分配比例']) / Decimal('100'))
                              .quantize(Decimal('0.00'), ROUND_DOWN))
            else:
                pytest.assume(Decimal(row_data['业绩额']).quantize(Decimal('0.00')) ==
                              (pay_money * Decimal('0.92') * Decimal(row_data['分配比例']) / Decimal('100'))
                              .quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(row_data['加盟商'] == role_info[row_data['角色类型']]['公司'])

    @allure.story("测试合同报表数据用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_002(self, web_driver):
        contract_report = ContractReportTablePage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)

        main_leftview.click_contract_report_label()
        contract_report.input_contract_code_search(contract_info['合同编号'])
        contract_report.click_search_button()
        table_row_data = contract_report.get_table_row_data(row=1)
        pytest.assume(table_row_data['合同信息'][0] == contract_info['合同编号'])
        pytest.assume(table_row_data['合同信息'][1] == contract_info['房源编号'])
        pytest.assume(table_row_data['合同信息'][2] == ini.house_community_name + ini.house_building_id + '-'
                      + ini.house_building_cell + '-' + ini.house_doorplate)
        pytest.assume(table_row_data['合同信息'][3] == '已完结')
        pytest.assume(table_row_data['交易类型'] == '二手买卖')
        pytest.assume(Decimal(table_row_data['合同价格']).quantize(Decimal('0.00')) ==
                      Decimal(contract_info['合同价格']).quantize(Decimal('0.00')))
        pytest.assume(Decimal(table_row_data['应收佣金']).quantize(Decimal('0.00')) ==
                      Decimal(contract_info['代理费']).quantize(Decimal('0.00')))
        pay_money = Decimal('0.00')
        for key, value in contract_info['支付信息'].items():
            pay_money = pay_money + Decimal(value['支付金额'])
        pytest.assume(Decimal(table_row_data['已收佣金']) == pay_money.quantize(Decimal('0.00'), ROUND_DOWN))
        pytest.assume(Decimal(table_row_data['未收佣金']) ==
                      Decimal(table_row_data['应收佣金']) - Decimal(table_row_data['已收佣金']))
        table_role_list = table_row_data['角色类型-占比-门店-角色人']
        for table_role in table_role_list:
            table_role_info = table_role.split('-')
            pytest.assume(table_role_info[1] ==
                          str(Decimal(role_info[table_role_info[0]]['比例']).quantize(Decimal('0.00'))) + "%")
            pytest.assume(table_role_info[2] == role_info[table_role_info[0]]['门店'])
            pytest.assume(table_role_info[3] == role_info[table_role_info[0]]['姓名'])
            pytest.assume(
                Decimal(table_row_data['业绩金额'][table_role_list.index(table_role)]).quantize(Decimal('0.00')) ==
                (Decimal(table_row_data['已收佣金'].replace(',', '')) * Decimal('0.92')
                 * Decimal(role_info[table_role_info[0]]['比例']) / Decimal('100')).quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(
                table_row_data['大区OD/小区OM'][table_role_list.index(table_role)].split('/')[0].replace(' ', '') ==
                role_info[table_role_info[0]]['大区'] + role_info[table_role_info[0]]['OD'])
            pytest.assume(
                table_row_data['大区OD/小区OM'][table_role_list.index(table_role)].split('/')[1].replace(' ', '') ==
                role_info[table_role_info[0]]['商圈'] + role_info[table_role_info[0]]['OM'])

    @allure.story("测试实收业绩报表数据用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_003(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        received_achievement_report = ReceivedAchievementReportTablePage(web_driver)

        main_leftview.click_received_achievement_report_label()
        received_achievement_report.input_contract_code_search(contract_info['合同编号'])
        received_achievement_report.click_search_button()
        table_data = received_achievement_report.get_table_data()
        pay_money_info = []
        pay_time_info = []
        for key, value in contract_info['支付信息'].items():
            pay_money_info.append(value['支付金额'])
            pay_time_info.append(value['支付时间'])
        for row_data in table_data:
            pytest.assume(row_data['合同信息'][0] == contract_info['合同编号'])
            pytest.assume(row_data['合同信息'][1] == ini.house_community_name + '-' + ini.house_building_id + '-'
                          + ini.house_building_cell + '-' + ini.house_doorplate)
            pytest.assume(row_data['合同信息'][2] == '已完结')
            pytest.assume(row_data['交易类型'] == '买卖')
            pytest.assume(str(Decimal(row_data['付款金额']).quantize(Decimal('0.00'))) in pay_money_info)
            pytest.assume(row_data['付款时间'] in pay_time_info)
            pytest.assume(row_data['角色人'] == role_info[row_data['角色类型']]['姓名'])
            pytest.assume(Decimal(row_data['实收业绩']).quantize(Decimal('0.00')) ==
                          (Decimal(row_data['付款金额']) * Decimal('0.92') * Decimal(row_data['业绩比例']) / Decimal('100'))
                          .quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(Decimal(row_data['业绩比例']).quantize(Decimal('0.00')) ==
                          Decimal(role_info[row_data['角色类型']]['比例']).quantize(Decimal('0.00')))
            # pytest.assume(row_data['分账时间'] == '')
            pytest.assume(row_data['门店/店组'] == role_info[row_data['角色类型']]['门店'] + '/'
                          + role_info[row_data['角色类型']]['店组'])
            pytest.assume(row_data['大区/小区'] == role_info[row_data['角色类型']]['大区'] + '/'
                          + role_info[row_data['角色类型']]['商圈'])
            if role_info[row_data['角色类型']]['OM'] == '':
                role_info[row_data['角色类型']]['OM'] = '--'
            pytest.assume(row_data['OM'] == role_info[row_data['角色类型']]['OM'])
            if role_info[row_data['角色类型']]['OD'] == '':
                role_info[row_data['角色类型']]['OD'] = '--'
            pytest.assume(row_data['OD'] == role_info[row_data['角色类型']]['OD'])
            pytest.assume(row_data['分账状态'] == '已分账')
            pytest.assume(row_data['业绩审核时间'] == contract_info['审核时间'])
            pytest.assume(row_data['公司'] == role_info[row_data['角色类型']]['公司'])

    @allure.story("测试流水报表数据用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_004(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        payment_flow = PaymentFlowTablePage(web_driver)

        main_leftview.click_payment_flow_label()
        payment_flow.input_contract_code_search(contract_info['合同编号'])
        payment_flow.click_search_button()
        table_data = payment_flow.get_table_data()
        pay_money_info = []
        pay_time_info = []
        for key, value in contract_info['支付信息'].items():
            pay_money_info.append(value['支付金额'])
            pay_time_info.append(value['支付时间'])
        for row_data in table_data:
            pytest.assume(row_data['合同信息'][0] == contract_info['合同编号'])
            pytest.assume(row_data['合同信息'][1] == ini.house_community_name + ini.house_building_id + '-'
                          + ini.house_building_cell + '-' + ini.house_doorplate)
            pytest.assume(row_data['合同信息'][2] == '已完结')
            pytest.assume(row_data['交易类型'] == '二手买卖')
            pytest.assume(row_data['付款金额'] in pay_money_info)
            pytest.assume(row_data['佣金'] == row_data['付款金额'])
            if ini.environment == 'wx' or ini.environment == 'hz':
                pytest.assume(row_data['权证费'] == '0.00')
            else:
                pytest.assume(row_data['权证费'] == '500.00')
            pytest.assume(row_data['收款人'] == contract_info['收款人'])
            pytest.assume(row_data['支付时间'] in pay_time_info)
            pytest.assume(row_data['成交人'] == role_info['房源成交人']['姓名'])
            pytest.assume(row_data['支付渠道'] == '线下支付')
            pytest.assume(row_data['门店/店组'] == role_info['房源成交人']['门店'] + '/' + role_info['房源成交人']['店组'])
            pytest.assume(row_data['大区/小区'] == role_info['房源成交人']['大区'] + '/' + role_info['房源成交人']['商圈'])
            if role_info['房源成交人']['OM'] == '' or role_info['房源成交人']['OM'] == '--':
                role_info['房源成交人']['OM'] = '-'
            pytest.assume(row_data['OM'] == role_info['房源成交人']['OM'])
            if role_info['房源成交人']['OD'] == '' or role_info['房源成交人']['OD'] == '--':
                role_info['房源成交人']['OD'] = '-'
            pytest.assume(row_data['OD'] == role_info['房源成交人']['OD'])

    @allure.story("测试财务数据用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_005(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        finance = FinanceTablePage(web_driver)

        main_leftview.click_finance_label()
        finance.click_receivable_table_tab()
        finance.input_contract_code_search(contract_info['合同编号'])
        finance.click_search_button()
        receivable_table_data = finance.get_table_data(flag='应收列表')
        pay_money_info = []
        pay_time_info = []
        pay_money = Decimal('0.00')
        pay_info = {}
        for key, value in contract_info['支付信息'].items():
            pay_money_info.append(value['支付金额'])
            pay_money = pay_money + Decimal(value['支付金额'])
            pay_time_info.append(value['支付时间'])
            pay_info[value['收款ID']] = value['支付金额']
        for row_data in receivable_table_data:
            pytest.assume('回佣率100%' in row_data['应收ID'])
            pytest.assume(row_data['合同编号'] == contract_info['合同编号'])
            pytest.assume(row_data['费用类型'] == '居间代理费')
            pytest.assume(row_data['业务类型'] == '二手买卖')
            pytest.assume(row_data['签约人'] == role_info['房源成交人']['姓名'])
            pytest.assume(row_data['签约店组'] == role_info['房源成交人']['店组'])
            pytest.assume(Decimal(row_data['应收款']).quantize(Decimal('0.00')) ==
                          Decimal(contract_info['代理费']).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['已收款']).quantize(Decimal('0.00'), ROUND_DOWN) ==
                          pay_money.quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(row_data['待收款'] == str(Decimal(row_data['应收款']) - Decimal(row_data['已收款'])))
            pytest.assume(row_data['操作时间'] == contract_info['盖章时间'])  # 盖章时间
        finance.click_agent_achievement_table_tab()
        finance.input_contract_code_search(contract_info['合同编号'])
        finance.click_search_button()
        agent_achievement_table_data = finance.get_table_data(flag='经纪人业绩报表')
        for row_data in agent_achievement_table_data:
            pytest.assume(row_data['合同编号'] == contract_info['合同编号'])
            pytest.assume(row_data['业务类型'] == '二手买卖')
            sum_proportion = Decimal('0')
            for role in row_data['角色类型']:
                pytest.assume(row_data['角色人'] == role_info[role]['姓名'])
                pytest.assume(row_data['角色比例'][row_data['角色类型'].index(role)] == role_info[role]['比例'] + '%')
                sum_proportion = sum_proportion + Decimal(role_info[role]['比例'])
            pytest.assume(Decimal(row_data['协议总价']).quantize(Decimal('0.00')) ==
                          Decimal(contract_info['代理费']).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['付款金额']).quantize(Decimal('0.00')) == pay_money.quantize(Decimal('0.00')))
            pytest.assume(row_data['待付款金额'] == str(Decimal(row_data['协议总价']) - Decimal(row_data['付款金额'])))
            if ini.environment == 'sz' or ini.environment == 'ks':
                pytest.assume(Decimal(row_data['应收业绩']).quantize(Decimal('0.00'), ROUND_DOWN) ==
                              ((Decimal(row_data['协议总价']) - Decimal('500')) * sum_proportion / Decimal('100')
                               * Decimal('0.92') * Decimal('0.998')).quantize(Decimal('0.00'), ROUND_DOWN))
            elif ini.environment == 'wx':
                pytest.assume(Decimal(row_data['应收业绩']).quantize(Decimal('0.00'), ROUND_DOWN) ==
                              (Decimal(row_data['协议总价']) * sum_proportion / Decimal('100') * Decimal('0.92')
                               * Decimal('0.998')).quantize(Decimal('0.00'), ROUND_DOWN))
            elif ini.environment == 'wx':
                pytest.assume(Decimal(row_data['应收业绩']).quantize(Decimal('0.00'), ROUND_DOWN) ==
                              (Decimal(row_data['协议总价']) * sum_proportion / Decimal('100') * Decimal('0.92')
                               * Decimal('0.994')).quantize(Decimal('0.00'), ROUND_DOWN))
            if ini.environment == 'sz' or ini.environment == 'ks':
                pytest.assume(Decimal(row_data['实收业绩']).quantize(Decimal('0.00'), ROUND_DOWN) ==
                              ((Decimal(row_data['协议总价']) - Decimal('500')) * sum_proportion / Decimal('100')
                               * Decimal('0.92')).quantize(Decimal('0.00'), ROUND_DOWN))
            else:
                pytest.assume(Decimal(row_data['实收业绩']).quantize(Decimal('0.00'), ROUND_DOWN) ==
                              (Decimal(row_data['协议总价']) * sum_proportion / Decimal('100') * Decimal('0.92'))
                              .quantize(Decimal('0.00'), ROUND_DOWN))
        finance.click_split_account_data_table_tab()
        finance.input_contract_code_search(contract_info['合同编号'])
        finance.clear_split_account_time()
        finance.click_search_button()
        split_account_data_table_data = finance.get_table_data(flag='分账数据表')
        split_account_company_shop_name = []
        for key, value in role_info.items():
            if '科恒发' in value['公司']:
                continue
            if value['公司'] + '' + value['门店'] not in split_account_company_shop_name:
                split_account_company_shop_name.append(value['公司'] + '-' + value['门店'])
        split_account_company_shop_info = {}
        for company_shop_name in split_account_company_shop_name:
            proportion = Decimal('0')
            for key, value in role_info.items():
                if '科恒发' in value['公司']:
                    continue
                if value['公司'] + '-' + value['门店'] == company_shop_name:
                    proportion = proportion + Decimal(value['比例'])
            split_account_company_shop_info[company_shop_name] = proportion
        for row_data in split_account_data_table_data:
            pytest.assume(row_data['合同编号'] == contract_info['合同编号'])
            pytest.assume(row_data['实收ID'] in pay_info.keys())
            pytest.assume(row_data['科目'] == '居间代理费')
            pytest.assume(row_data['成交公司-门店'] == role_info['房源成交人']['公司'] + '-' + role_info['房源成交人']['门店'])
            pytest.assume(row_data['分账公司-门店'] in split_account_company_shop_name)
            pytest.assume(row_data['付款时间'] in pay_time_info)
            pytest.assume(Decimal(row_data['付款金额']).quantize(Decimal('0.00')) ==
                          Decimal(pay_info[row_data['实收ID']]).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['应收金额']).quantize(Decimal('0.00')) ==
                          Decimal(contract_info['代理费']).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['分账金额']).quantize(Decimal('0.00')) ==
                          (Decimal(row_data['付款金额']) * Decimal(split_account_company_shop_info[row_data['分账公司-门店']])
                          / Decimal('100') * Decimal('0.92')).quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(row_data['入账金额'] == row_data['分账金额'])
            # pytest.assume(row_data['分账时间'] in split_account_company_shop_name)
            pytest.assume(row_data['分账状态'] == '已分账')

    @allure.story("测试门店分账数据表用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_006(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        shop_brand_data_report = ShopBrandDataReportTablePage(web_driver)

        main_leftview.click_shop_split_account_data_table_label()
        shop_brand_data_report.click_complete_split_account_tab()
        shop_brand_data_report.input_contract_code_search(contract_info['合同编号'])
        shop_brand_data_report.clear_split_account_time_search()
        shop_brand_data_report.clear_pay_time_search()
        shop_brand_data_report.click_search_button()
        table_data = shop_brand_data_report.get_table_data(flag='分账完成')
        split_account_company_shop_name = []
        for key, value in role_info.items():
            if '科恒发' in value['公司']:
                continue
            if value['公司'] + '-' + value['门店'] not in split_account_company_shop_name:
                split_account_company_shop_name.append(value['公司'] + '-' + value['门店'])
        split_account_company_shop_info = {}
        for company_shop_name in split_account_company_shop_name:
            proportion = Decimal('0')
            for key, value in role_info.items():
                if '科恒发' in value['公司']:
                    continue
                if value['公司'] + '-' + value['门店'] == company_shop_name:
                    proportion = proportion + Decimal(value['比例'])
            split_account_company_shop_info[company_shop_name] = str(proportion)
        pay_money_info = []
        pay_time_info = []
        pay_info = {}
        for key, value in contract_info['支付信息'].items():
            pay_money_info.append(value['支付金额'])
            pay_time_info.append(value['支付时间'])
            pay_info[value['收款ID']] = value['支付金额']
        for row_data in table_data:
            pytest.assume(row_data['合同编号'] == contract_info['合同编号'])
            pytest.assume(row_data['实收ID'] in pay_info.keys())
            if row_data['分账公司-门店'] == row_data['成交公司-门店']:
                pytest.assume(row_data['科目'] == '成交门店服务费')
            else:
                pytest.assume(row_data['科目'] == '合作门店服务费')
            pytest.assume(row_data['成交公司-门店'] == role_info['房源成交人']['公司'] + '-' + role_info['房源成交人']['门店'])
            pytest.assume(row_data['分账公司-门店'] in split_account_company_shop_name)
            pytest.assume(row_data['付款时间'] in pay_time_info)
            pytest.assume(Decimal(row_data['付款金额']).quantize(Decimal('0.00')) ==
                          Decimal(pay_info[row_data['实收ID']]).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['应收金额']).quantize(Decimal('0.00')) ==
                          Decimal(contract_info['代理费']).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['应分账金额']).quantize(Decimal('0.00'), ROUND_DOWN)
                          == (Decimal(row_data['应收金额']) * Decimal(split_account_company_shop_info[row_data['分账公司-门店']])
                          / Decimal('100') * Decimal('0.92')).quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(Decimal(row_data['实分账金额']).quantize(Decimal('0.00'), ROUND_DOWN)
                          == (Decimal(row_data['付款金额']) * Decimal(split_account_company_shop_info[row_data['分账公司-门店']])
                              / Decimal('100') * Decimal('0.92')).quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(row_data['入账金额'] == row_data['实分账金额'])
            # pytest.assume(row_data['分账时间'] == '')
            pytest.assume(row_data['分账状态'] == '已分账')

    @allure.story("测试品牌返佣数据表用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_007(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        shop_brand_data_report = ShopBrandDataReportTablePage(web_driver)

        main_leftview.click_brand_rebate_data_table_label()
        shop_brand_data_report.click_complete_rebate_commission_tab()
        shop_brand_data_report.input_contract_code_search(contract_info['合同编号'])
        shop_brand_data_report.clear_rebate_time_search()
        shop_brand_data_report.clear_pay_time_search()
        shop_brand_data_report.click_search_button()
        table_data = shop_brand_data_report.get_table_data(flag='返佣完成')
        rebate_commission_company_name = []
        for key, value in role_info.items():
            if value['公司'] not in rebate_commission_company_name:
                rebate_commission_company_name.append(value['公司'])
        company_proportion_info = {}
        for company_name in rebate_commission_company_name:
            proportion = Decimal('0')
            for key, value in role_info.items():
                if value['公司'] == company_name:
                    proportion = proportion + Decimal(value['比例'])
            company_proportion_info[company_name] = str(proportion)
        pay_money_info = []
        pay_time_info = []
        pay_info = {}
        for key, value in contract_info['支付信息'].items():
            pay_money_info.append(value['支付金额'])
            pay_time_info.append(value['支付时间'])
            pay_info[value['收款ID']] = value['支付金额']
        for row_data in table_data:
            pytest.assume(row_data['合同编号'] == contract_info['合同编号'])
            pytest.assume(row_data['实收ID'] in pay_info.keys())
            if row_data['分账公司'] == role_info['房源成交人']['公司']:
                pytest.assume(row_data['科目'] == '成交门店服务费')
            else:
                pytest.assume(row_data['科目'] == '合作门店服务费')
            pytest.assume(row_data['成交公司-门店'] == role_info['房源成交人']['公司'] + '-' + role_info['房源成交人']['门店'])
            pytest.assume(row_data['分账公司'] in rebate_commission_company_name)
            pytest.assume(row_data['付款时间'] in pay_time_info)
            pytest.assume(Decimal(row_data['付款金额']).quantize(Decimal('0.00')) ==
                          Decimal(pay_info[row_data['实收ID']]).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['返佣金额']).quantize(Decimal('0.00'), ROUND_DOWN)
                          == (Decimal(row_data['付款金额']) * Decimal(company_proportion_info[row_data['分账公司']])
                              / Decimal('100') * Decimal('0.05')).quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(row_data['返佣状态'] == '返佣完成')
            pytest.assume(row_data['返佣入账金额'] == row_data['返佣金额'])
            # pytest.assume(row_data['返佣时间'] == '')

    @allure.story("测试品牌返佣分账数据表用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_008(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        brand_split_account_report = BrandSplitAccountReportTablePage(web_driver)

        main_leftview.click_brand_rebate_split_account_data_table_label()
        brand_split_account_report.input_contract_code_search(contract_info['合同编号'])
        brand_split_account_report.clear_split_account_time_search()
        brand_split_account_report.click_search_button()
        table_data = brand_split_account_report.get_table_data()
        rebate_commission_company_name = []
        for key, value in role_info.items():
            if value['公司'] not in rebate_commission_company_name:
                rebate_commission_company_name.append(value['公司'])
        company_proportion_info = {}
        for company_name in rebate_commission_company_name:
            proportion = Decimal('0')
            for key, value in role_info.items():
                if value['公司'] == company_name:
                    proportion = proportion + Decimal(value['比例'])
            company_proportion_info[company_name] = str(proportion)
        pay_money_info = []
        pay_time_info = []
        pay_info = {}
        for key, value in contract_info['支付信息'].items():
            pay_money_info.append(value['支付金额'])
            pay_time_info.append(value['支付时间'])
            pay_info[value['收款ID']] = value['支付金额']
        for row_data in table_data:
            pytest.assume(row_data['合同编号'] == contract_info['合同编号'])
            pytest.assume(row_data['实收ID'] in pay_info.keys())
            if row_data['分账公司'] == role_info['房源成交人']['公司']:
                pytest.assume(row_data['科目'] == '成交门店服务费')
            else:
                pytest.assume(row_data['科目'] == '合作门店服务费')
            pytest.assume(row_data['成交公司-门店'] == role_info['房源成交人']['公司'] + '-' + role_info['房源成交人']['门店'])
            pytest.assume(row_data['分账公司'] in rebate_commission_company_name)
            pytest.assume(row_data['付款时间'] in pay_time_info)
            pytest.assume(Decimal(row_data['付款金额']).quantize(Decimal('0.00')) ==
                          Decimal(pay_info[row_data['实收ID']]).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['返佣金额']).quantize(Decimal('0.00'), ROUND_DOWN)
                          == (Decimal(row_data['付款金额']) * Decimal(company_proportion_info[row_data['分账公司']])
                              / Decimal('100') * Decimal('0.05')).quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(row_data['返佣状态'] == '返佣完成')
            pytest.assume(row_data['返佣入账金额'] == row_data['返佣金额'])
            # pytest.assume(row_data['返佣时间'] == '')

    @allure.story("测试财务报表用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_009(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        finance_report = FinanceReportTablePage(web_driver)

        main_leftview.click_finance_report_label()
        finance_report.click_paid_label()
        finance_report.input_contract_code_search(contract_info['合同编号'])
        finance_report.click_search_button()
        table_data = finance_report.get_table_data(flag='已支付')
        pay_money_info = []
        pay_time_info = []
        for key, value in contract_info['支付信息'].items():
            pay_money_info.append(value['支付金额'])
            pay_time_info.append(value['支付时间'].split(' ')[0])
        for row_data in table_data:
            pytest.assume(row_data['合同信息'][0] == contract_info['物业地址'])
            pytest.assume(row_data['合同信息'][1] == contract_info['合同编号'])
            pytest.assume(row_data['合同信息'][2] == contract_info['签约时间'])
            pytest.assume(row_data['交易类型'] == '二手买卖')
            pytest.assume(Decimal(row_data['应收佣金']).quantize(Decimal('0.00')) ==
                          Decimal(contract_info['代理费']).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['权证费']).quantize(Decimal('0.00')) == Decimal('0.00'))
            pytest.assume(str(Decimal(row_data['付款金额']).quantize(Decimal('0.00'))) in pay_money_info)
            pytest.assume(row_data['付款时间'] in pay_time_info)
            pytest.assume(row_data['结算月'] == contract_info['盖章时间'].split('-')[0] + '-'
                          + contract_info['盖章时间'].split('-')[1])
            for role in row_data['角色类型']:
                pytest.assume(
                    Decimal(row_data['分配比例'][row_data['角色类型'].index(role)].split(' %')[0]).quantize(Decimal('0.00')) ==
                    Decimal(role_info[role]['比例']).quantize(Decimal('0.00')))
                pytest.assume(Decimal(row_data['业绩额'][row_data['角色类型'].index(role)]).quantize(Decimal('0.00')) ==
                              (Decimal(row_data['应收佣金']) * Decimal('0.92') * Decimal(role_info[role]['比例'])
                              / Decimal('100')).quantize(Decimal('0.00'), ROUND_DOWN))
                pytest.assume(row_data['角色人'][row_data['角色类型'].index(role)] == role_info[role]['姓名'])
                pytest.assume(row_data['角色人门店'][row_data['角色类型'].index(role)] == role_info[role]['门店'])
                pytest.assume(row_data['角色人店组'][row_data['角色类型'].index(role)] == role_info[role]['店组'])
                # pytest.assume(row_data['商圈经理'][row_data['角色类型'].index(role)] == '')
                pytest.assume(row_data['加盟商'][row_data['角色类型'].index(role)] == role_info[role]['公司'])
                pytest.assume(Decimal(row_data['实分账'][row_data['角色类型'].index(role)]).quantize(Decimal('0.00')) ==
                              (Decimal(row_data['付款金额']) * Decimal('0.92') * Decimal(role_info[role]['比例'])
                               / Decimal('100')).quantize(Decimal('0.00'), ROUND_DOWN))
                pytest.assume(Decimal(row_data['手续费'][row_data['角色类型'].index(role)]).quantize(Decimal('0.00')) ==
                              Decimal('0.00'))
                # pytest.assume(row_data['分账时间'][row_data['角色类型'].index(role)] == '')
                pytest.assume(row_data['结算情况'][row_data['角色类型'].index(role)] == '已打款')

    @allure.story("测试实勘部业绩分账已完成报表用例")
    @pytest.mark.sale
    @pytest.mark.report
    @pytest.mark.run(order=51)
    @pytest.mark.skipif(ini.environment == 'sz' or ini.environment == 'ks', reason='苏州暂不支持')
    def test_010(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        survey_split_account_report = SurveySplitAccountReportTablePage(web_driver)

        main_leftview.click_survey_department_split_account_label()
        survey_split_account_report.click_complete_split_account_tab()
        survey_split_account_report.input_contract_code_search(contract_info['合同编号'])
        survey_split_account_report.clear_split_account_time_search()
        survey_split_account_report.clear_pay_time_search()
        survey_split_account_report.click_search_button()
        table_data = survey_split_account_report.get_table_data(flag='分账完成')
        split_account_company_shop_name = []
        for key, value in role_info.items():
            if '科恒发' in value['公司']:
                if value['公司'] + '-' + value['门店'] not in split_account_company_shop_name:
                    split_account_company_shop_name.append(value['公司'] + '-' + value['门店'])
        split_account_company_shop_info = {}
        for company_shop_name in split_account_company_shop_name:
            proportion = Decimal('0')
            for key, value in role_info.items():
                if '科恒发' in value['公司']:
                    if value['公司'] + '-' + value['门店'] == company_shop_name:
                        proportion = proportion + Decimal(value['比例'])
            split_account_company_shop_info[company_shop_name] = str(proportion)
        pay_money_info = []
        pay_time_info = []
        pay_info = {}
        for key, value in contract_info['支付信息'].items():
            pay_money_info.append(value['支付金额'])
            pay_time_info.append(value['支付时间'])
            pay_info[value['收款ID']] = value['支付金额']
        for row_data in table_data:
            pytest.assume(row_data['合同编号'] == contract_info['合同编号'])
            pytest.assume(row_data['实收ID'] in pay_info.keys())
            pytest.assume(row_data['科目'] == '合作门店服务费')
            pytest.assume(row_data['成交公司-门店'] == role_info['房源成交人']['公司'] + '-' + role_info['房源成交人']['门店'])
            pytest.assume(row_data['分账公司-门店'] in split_account_company_shop_name)
            pytest.assume(row_data['付款时间'] in pay_time_info)
            pytest.assume(Decimal(row_data['付款金额']).quantize(Decimal('0.00')) ==
                          Decimal(pay_info[row_data['实收ID']]).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['应收金额']).quantize(Decimal('0.00')) ==
                          Decimal(contract_info['代理费']).quantize(Decimal('0.00')))
            pytest.assume(Decimal(row_data['应分账金额']).quantize(Decimal('0.00')) ==
                          (Decimal(row_data['应收金额']) * Decimal('0.92') *
                           Decimal(split_account_company_shop_info[row_data['分账公司-门店']]) / Decimal('100'))
                          .quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(Decimal(row_data['实分账金额']).quantize(Decimal('0.00')) ==
                          (Decimal(row_data['付款金额']) * Decimal('0.92') *
                          Decimal(split_account_company_shop_info[row_data['分账公司-门店']]) / Decimal('100'))
                          .quantize(Decimal('0.00'), ROUND_DOWN))
            pytest.assume(row_data['入账金额'] == row_data['实分账金额'])
            # pytest.assume(row_data['分账时间'] == '')
            pytest.assume(row_data['分账状态'] == '已分账')
