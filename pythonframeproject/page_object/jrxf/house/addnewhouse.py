"""
@author: lijiahui
@version: V1.0
@file: addnewhouse.py
@time: 2022/1/17
"""
from common.readelement import Element
from config.conf import cm
from page.webpage import WebPage
from utils.timeutil import sleep

addnewhouse = Element('jrxf/house/add_house')

class AddNewHouse(WebPage):
    def click_newhouse_manager_button(self):
        self.is_click(addnewhouse['新房管理菜单'], sleep_time=0.5)

    def click_estate_manager_button(self):
        self.is_click(addnewhouse['楼盘管理按钮'], sleep_time=0.5)

    def click_add_newhouse_button(self):
        self.is_click(addnewhouse['新增楼盘按钮'], sleep_time=0.5)

    def input_estate_name(self, estate_name):
        self.input_text(addnewhouse['楼盘名称输入框'], estate_name)
        sleep(0.5)

    def input_developer(self, developer):
        self.input_text(addnewhouse['开发商输入框'], developer)
        sleep(0.5)

    def select_estate_state(self, estate_state):
        self.is_click(addnewhouse['楼盘状态选择框'], sleep_time=0.5)
        self.select_item_option(estate_state)


    def input_estate_price(self, estate_price):
        self.input_text(addnewhouse['楼盘价格输入框'], estate_price)
        sleep(0.5)

    def input_opening_time(self, opening_time):
        self.input_text_with_enter(addnewhouse['开盘时间输入框'], opening_time)
        sleep(0.5)

    def input_check_out_time(self, check_out_time):
        self.input_text_with_enter(addnewhouse['交房时间输入框'], check_out_time)
        sleep(0.5)

    # def input_property_type(self, property_type):
    #     self.input_text(addnewhouse['物业类型选择框'], property_type)
    def select_property_type(self, property_type):
        self.is_click(addnewhouse['物业类型选择框'], sleep_time=0.5)
        self.select_item_option(property_type)

    def select_areas(self, city, country, trade):
        self.is_click(addnewhouse['项目行政区域市选择框'], sleep_time=0.5)
        self.select_item_option(city)
        self.is_click(addnewhouse['项目行政区域区选择框'], sleep_time=0.5)
        self.select_item_option(country)
        self.is_click(addnewhouse['项目行政区域商圈选择框'], sleep_time=0.5)
        self.select_item_option(trade)

    def input_estate_address(self, estate_address):
        self.input_text(addnewhouse['楼盘地址输入框'], estate_address)
        sleep(0.5)

    def input_sales_address(self, sales_address):
        self.input_text(addnewhouse['售楼处地址输入框'], sales_address)
        sleep(0.5)

    def input_longitude(self, longitude):
        # ele = self.find_element(addnewhouse['楼盘经度输入框'])

        self.set_element_attribute(addnewhouse['楼盘经度输入框'], 'class', 'ant-input')
        sleep(0.5)
        self.remove_element_attribute(addnewhouse['楼盘经度输入框'], 'disabled')
        self.input_text(addnewhouse['楼盘经度输入框'], longitude)

    def input_latitude(self, latitude):
        # ele = self.find_element(addnewhouse['楼盘纬度输入框'])
        self.set_element_attribute(addnewhouse['楼盘纬度输入框'], 'class', 'ant-input')
        sleep(0.5)
        self.remove_element_attribute(addnewhouse['楼盘纬度输入框'], 'disabled')
        self.input_text(addnewhouse['楼盘纬度输入框'], latitude)


    def click_ok_button(self):
        self.is_click(addnewhouse['确定按钮'])

    def click_editor_button(self):
        self.is_click(addnewhouse['编辑楼盘按钮'], sleep_time=0.5)

    def click_contract_tab(self):
        self.is_click(addnewhouse['上传合同tab'], sleep_time=0.5)

    def upload_contract(self, picture_path):
        self.send_key(addnewhouse['上传合同'], picture_path)
        self.send_key(addnewhouse['上传预售许可证'], picture_path)
        sleep(2)
        self.is_click(addnewhouse['提交审核按钮'])

    def click_estate_contract_examine_button(self):
        self.is_click(addnewhouse['楼盘合同审核按钮'], sleep_time=0.5)

    def search_estate_name_in_contract(self, estate_name):
        self.input_text(addnewhouse['合同审核楼盘搜索输入框'], estate_name)
        self.is_click(addnewhouse['合同审核楼盘搜索按钮'], sleep_time=0.5)

    def click_examine_button(self):
        self.is_click(addnewhouse['审核楼盘按钮'], sleep_time=0.5)

    def click_examine_pass_button(self):
        self.is_click(addnewhouse['审核通过按钮'], sleep_time=0.5)

    def click_examine_dialog_ok_button(self):
        self.is_click(addnewhouse['审核通过弹窗'], sleep_time=0.5)

    def click_ready_sale_tab(self):
        self.is_click(addnewhouse['待上架楼盘tab'], sleep_time=0.5)

    def click_ready_sale_editor_button(self):
        self.is_click(addnewhouse['待上架编辑楼盘按钮'], sleep_time=0.5)

    def search_estate_name(self, estate_name):
        self.input_text(addnewhouse['楼盘搜索输入框'], estate_name)
        self.is_click(addnewhouse['楼盘搜索按钮'], sleep_time=0.5)

    def input_maintain_baseinfo(self, estate_discount, advance_report_time, report_protect_time,
                                takelook_protect_time, incentive_policy, buliding_type,
                                property_rights, plot_ratio, green_rate, household_number,
                                parking_number, hydropower, property_company,
                                property_fee, heating):
        self.input_text(addnewhouse['楼盘优惠输入框'], estate_discount)
        self.input_text(addnewhouse['提前报备时间输入框'], advance_report_time)
        self.input_text(addnewhouse['报备保护时间输入框'], report_protect_time)
        self.input_text(addnewhouse['带看保护时间输入框'], takelook_protect_time)
        self.input_text(addnewhouse['激励政策输入框'], incentive_policy)
        self.is_click(addnewhouse['建筑类型选择框'], sleep_time=0.5)
        self.select_item_option(buliding_type)
        self.is_click(addnewhouse['产权年限选择框'], sleep_time=0.5)
        self.select_item_option(property_rights)
        self.input_text(addnewhouse['容积率输入框'], plot_ratio)
        self.input_text(addnewhouse['绿化率输入框'], green_rate)
        self.input_text(addnewhouse['规划户数输入框'], household_number)
        self.input_text(addnewhouse['规划车位输入框'], parking_number)
        self.is_click(addnewhouse['水电燃气选择框'], sleep_time=0.5)
        self.select_item_option(hydropower)
        self.input_text(addnewhouse['物业公司输入框'], property_company)
        self.input_text(addnewhouse['物业费输入框1'], property_fee[0])
        self.input_text(addnewhouse['物业费输入框2'], property_fee[1])
        self.is_click(addnewhouse['供暖方式选择框'], sleep_time=0.5)
        self.select_item_option(heating)

    def add_contract(self, contract_name, contract_phone):  # 新增联系人
        # target_ele = self.find_element(addnewhouse['新增联系人card_title'])
        item_option_value = contract_name + '-' + contract_phone
        # self.driver.execute_script("arguments[0].scrollIntoView();", target_ele)  # 拖动到可见的元素去
        self.is_click(addnewhouse['R新房案场选择'], sleep_time=0.5)
        self.input_text(addnewhouse['选择角色弹窗_姓名输入框'], contract_name)
        self.select_item_option(item_option_value)
        self.is_click(addnewhouse['选择角色弹窗_确定按钮'], sleep_time=0.5)
        self.is_click(addnewhouse['S新房经理选择'], sleep_time=0.5)
        self.input_text(addnewhouse['选择角色弹窗_姓名输入框'], contract_name)
        self.select_item_option(item_option_value)
        self.is_click(addnewhouse['选择角色弹窗_确定按钮'], sleep_time=0.5)
        self.is_click(addnewhouse['D新房总监选择'], sleep_time=0.5)
        self.input_text(addnewhouse['选择角色弹窗_姓名输入框'], contract_name)
        self.select_item_option(item_option_value)
        self.is_click(addnewhouse['选择角色弹窗_确定按钮'], sleep_time=0.5)

    def click_save_button(self):
        self.is_click(addnewhouse['保存按钮'])

    def click_ready_sale_examine(self):
        self.is_click(addnewhouse['上架楼盘审核按钮'], sleep_time=0.5)

    def search_ready_sale_estate_name(self, estate_name):
        self.input_text(addnewhouse['待上架楼盘搜索输入框'], estate_name)
        self.is_click(addnewhouse['待上架楼盘搜索按钮'], sleep_time=0.5)

    def click_ready_sale_examine_button(self):
        self.is_click(addnewhouse['待上架审核楼盘按钮'], sleep_time=0.5)

    def click_bound_dialog_button(self):
        self.is_click(addnewhouse['绑定代理商审核通过弹窗'], sleep_time=0.5)

    def click_coopration_eatate_tab(self):
        self.is_click(addnewhouse['合作楼盘tab'], sleep_time=0.5)

    def delete_coopration_eatate(self):
        self.is_click(addnewhouse['合作楼盘删除按钮'], sleep_time=0.5)
        self.is_click(addnewhouse['确认删除按钮'], sleep_time=0.5)

    # def select_item_option(self, option=None, index=None):
    #     if option:
    #         locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
    #                            "'ant-select-item ant-select-item-option') and @title='" + option + "'] "
    #         self.is_click(locator)
    #     else:
    #         locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
    #                            "'ant-select-item ant-select-item-option')] "
    #         options = self.find_elements(locator)
    #         options[index].click()



    def add_house_baseinfo(self, test_data):
        '''添加楼盘基础信息'''
        self.click_newhouse_manager_button()
        self.click_estate_manager_button()
        self.click_add_newhouse_button()
        self.input_estate_name(test_data['base_info']['estate_name'])
        self.input_developer(test_data['base_info']['developer'])
        self.select_estate_state(test_data['base_info']['estate_state'])
        self.input_estate_price(test_data['base_info']['estate_price'])
        self.input_opening_time(test_data['base_info']['opening_time'])
        self.input_check_out_time(test_data['base_info']['check_out_time'])
        self.select_property_type(test_data['base_info']['property_type'])
        self.select_areas(test_data['base_info']['areas'][0], test_data['base_info']['areas'][1], test_data['base_info']['areas'][2])
        self.input_estate_address(test_data['base_info']['estate_address'])
        self.input_sales_address(test_data['base_info']['sales_address'])
        self.input_longitude(test_data['base_info']['longitude'])
        self.input_latitude(test_data['base_info']['latitude'])
        self.click_ok_button()


    def editor_house_baseinfo(self, test_data):
        '''上传合同'''
        # self.click_newhouse_manager_button()
        # self.click_estate_manager_button()
        sleep(2)
        self.search_estate_name(test_data['base_info']['estate_name'])
        self.click_editor_button()
        self.click_contract_tab()
        self.upload_contract([cm.tmp_picture_file])

    def examine_contract(self, test_data):
        '''审核合同待审核楼盘'''
        # self.click_newhouse_manager_button()
        self.click_estate_contract_examine_button()
        self.search_estate_name_in_contract(test_data['base_info']['estate_name'])
        sleep(3)
        self.click_examine_button()
        self.click_examine_pass_button()
        self.click_examine_dialog_ok_button()

    def save_detail_baseinfo(self, test_data):
        '''待上架楼盘编辑基础信息'''
        # self.click_newhouse_manager_button()
        self.click_estate_manager_button()
        sleep(1)
        self.click_ready_sale_tab()
        sleep(1)
        self.search_estate_name(test_data['base_info']['estate_name'])
        sleep(2)
        self.click_ready_sale_editor_button()
        self.input_maintain_baseinfo(test_data['detail_info']['estate_discount'],
                                     test_data['detail_info']['advance_report_time'],
                                     test_data['detail_info']['report_protect_time'],
                                     test_data['detail_info']['takelook_protect_time'],
                                     test_data['detail_info']['incentive_policy'],
                                     test_data['detail_info']['buliding_type'],
                                     test_data['detail_info']['property_rights'],
                                     test_data['detail_info']['plot_ratio'],
                                     test_data['detail_info']['green_rate'],
                                     test_data['detail_info']['household_number'],
                                     test_data['detail_info']['parking_number'],
                                     test_data['detail_info']['hydropower'],
                                     test_data['detail_info']['property_company'],
                                     test_data['detail_info']['property_fee'],
                                     test_data['detail_info']['heating'])
        self.add_contract(test_data['contract']['contract_name'], test_data['contract']['contract_phone'])
        self.click_save_button()
        self.click_examine_dialog_ok_button()

    def ready_sale_examine(self, test_data):
        '''待上架楼盘审核'''
        self.click_ready_sale_examine()
        self.search_ready_sale_estate_name(test_data['base_info']['estate_name'])
        self.click_ready_sale_examine_button()
        self.click_examine_pass_button()
        self.click_bound_dialog_button()
        self.click_examine_dialog_ok_button()

    def delete_estate(self, test_data):
        '''删除楼盘'''
        # self.click_newhouse_manager_button()
        self.click_estate_manager_button()
        sleep(2)
        self.click_coopration_eatate_tab()
        self.search_estate_name(test_data['base_info']['estate_name'])
        self.delete_coopration_eatate()


