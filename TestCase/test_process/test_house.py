# -*- coding:utf-8 -*-
import pytest
import allure
from utils.logger import log
from config.conf import cm
from page_object.main.maintopviewpage import MainTopViewPage
from page_object.main.mianleftviewpage import MainLeftViewPage
from page_object.main.mainrightviewpage import MainRightViewPage
from page_object.main.invalidhousepage import InvalidHousePage
from page_object.house.housetablepage import HouseTablePage
from page_object.house.houseaddpage import HouseAddPage
from page_object.house.housedatailpage import HouseDetailPage
from page_object.house.keyentrustmentcertificatepage import KeyEntrustmentCertificatePage

import re


@allure.feature("测试房源模块")
class TestHouse(object):

    community_name = '自动化测试楼盘'
    building_id = '1'
    building_cell = '1'
    floor = '1'
    doorplate = '102'
    house_owner_name = 'ceshi'
    house_owner_phone = '18112591866'
    house_types = ['2', '2', '2', '1']
    area = '120'
    orientations = ['南']
    sale_price = '200'
    inspect_type = '下班后可看'
    photographer = 'A1经纪人18400000000'
    exploration_time = ['明天', '16:00-17:00']
    appointment_instructions = '预约实勘，请留意'

    @pytest.fixture(scope="class", autouse=True)
    def close_topview(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_topview.click_close_button()
        main_leftview = MainLeftViewPage(web_driver)
        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()

    @allure.story("测试新增房源，查看搜索结果用例")
    # @pytest.mark.skip
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        house_table = HouseTablePage(web_driver)
        invalid_house_page = InvalidHousePage(web_driver)
        house_add = HouseAddPage(web_driver)

        house_table.click_add_house_button()
        house_add.choose_sale_radio()
        house_add.input_community_name(self.community_name)
        house_add.input_building_id(self.building_id)
        house_add.input_building_cell(self.building_cell)
        house_add.input_floor(self.floor)
        house_add.input_doorplate(self.doorplate)
        house_add.choose_sale_radio()
        house_add.click_next_button()
        content = main_topview.find_notification_content()
        if content != '':
            log.info('房源已存在')
            house_code = re.search(r"房源编号(\d+?)，", content).group(1)
            main_leftview.click_all_house_label()
            house_table.clear_filter()
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row()
            house_detail.click_invalid_house_button()
            house_detail.input_invalid_reason("测试需要")
            house_detail.click_invalid_reason_confirm_button()
            content = main_topview.find_notification_content()
            if content == '错误':
                log.info('无效申请已提交')
                house_detail.click_invalid_reason_cancel_button()
            main_leftview.change_role('超级管理员')
            main_rightview.click_invalid_house()
            invalid_house_page.click_pass_by_housecode(house_code)
            invalid_house_page.click_invalid_house_confirm_button()
            content = main_topview.find_notification_content()
            if content != '成功':
                invalid_house_page.click_pass_by_housecode(house_code)
                invalid_house_page.click_invalid_house_confirm_button()
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_add_house_button()
            house_add.choose_rent_radio()
            house_add.input_community_name(self.community_name)
            house_add.input_building_id(self.building_id)
            house_add.input_building_cell(self.building_cell)
            house_add.input_floor(self.floor)
            house_add.input_doorplate(self.doorplate)
            house_add.choose_sale_radio()
            house_add.click_next_button()
        log.info('填写物业地址成功')
        house_add.input_house_owner_name(self.house_owner_name)
        house_add.input_house_owner_phone(self.house_owner_phone)
        log.info('填写业主信息成功')
        house_add.choose_house_type(self.house_types)
        house_add.input_area(self.area)
        house_add.choose_orientations(self.orientations)
        house_add.input_sale_price(self.sale_price)
        house_add.choose_inspect_type(self.inspect_type)
        house_add.click_add_button()
        log.info('填写房源信息成功')
        main_leftview.click_all_house_label()
        house_table.input_community_name_search(self.community_name)
        house_table.input_building_id_search(self.building_id)
        house_table.input_doorplate_search(self.doorplate)
        house_table.click_search_button()
        assert house_table.get_house_table_count() == 1
        log.info('搜索结果正确')

    @allure.story("测试房源预约实勘用例")
    # @pytest.mark.skip
    @pytest.mark.dependency(depends=['test_001'], scope='class')
    def test_002(self, web_driver):
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_reset_button()
        house_table.clear_filter()
        house_table.input_community_name_search(self.community_name)
        house_table.input_building_id_search(self.building_id)
        house_table.input_doorplate_search(self.doorplate)
        house_table.click_search_button()
        house_table.go_house_detail_by_row()
        house_detail.click_exploration_button()
        house_detail.choose_normal_exploration()
        house_detail.choose_photographer(self.photographer)
        house_detail.choose_exploration_time(self.exploration_time)
        house_detail.input_appointment_instructions(self.appointment_instructions)
        house_detail.click_exploration_confirm_button()
        log.info('预约实勘申请已提交')

    @allure.story("测试房源上传协议用例")
    @pytest.mark.skip
    @pytest.mark.dependency(depends=['test_001'], scope='class')
    def test_003(self, web_driver):
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        house_table.clear_filter()
        house_table.go_house_detail_by_row()
        house_detail.expand_certificates_info()
        house_detail.click_key_entrustment_certificate_upload_button()
        key_entrustment_certificate = KeyEntrustmentCertificatePage(web_driver)
        key_entrustment_certificate.input_agreement_number("")
        key_entrustment_certificate.input_key_type(["密码钥匙", "123456"])
        key_entrustment_certificate.input_shop_space("shops pace")
        key_entrustment_certificate.input_remark("remark")
        key_entrustment_certificate.upload_picture(cm.tmp_picture)
        key_entrustment_certificate.click_save_button()
        log.info('钥匙委托凭证已上传')


if __name__ == '__main__':
    pytest.main(['D:/PythonProject/UIAutomation/ui/TestCase/test_process/test_house.py'])
