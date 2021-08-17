#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_more.py
@time: 2021/08/10
"""
import allure
import pytest
from page_object.house.detailpage import HouseDetailPage
from page_object.house.tablepage import HouseTablePage
from utils.logger import log


@allure.feature("测试房源详情页面相关功能")
class TestHouseDetail(object):

    # json_file_path = cm.test_data_dir + "/test_sale/test_house/test_add.json"
    # test_data = get_data(json_file_path)
    @allure.story("查看房源基本信息")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['买卖', '租赁'])
    def test_view_basic_information(self, web_driver, flag):
        driver = web_driver
        house_detail = HouseDetailPage(driver)
        account_name = house_detail.get_account_name()
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(account_name, flag)
        print('test_view_basic_information', num)
        if int(num) > 0:
            house_detail.enter_house_detail(flag)
            house_detail.view_basic_information()
            res = house_detail.is_view_success()
            assert res
        else:
            log.error('当前维护人没有{flag}房源'.format(flag = flag))
            assert False

    @allure.story("维护人提交修改房源状态审核，商圈经理驳回审核")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['买卖', '租赁'])
    def test_modify_house_state(self, web_driver, flag):
        driver = web_driver
        house_detail = HouseDetailPage(driver)
        account_name = house_detail.get_account_name()
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(account_name, flag)
        if int(num) > 0:  # 判断当前用户的房源数量
            house_no = house_detail.enter_house_detail(flag)[0]
            res = house_detail.verify_can_modify()
            # print('test_view_basic_information', res)
            if res:  # 校验当前房源是否支持修改状态
                log.error(f'存在待审核的{flag}记录，不允许再次修改'.format(flag = flag))
                assert False
            else:
                house_detail.submit_modify_state_application()
                res1 = house_detail.is_submit_success()
                if res1:  # 校验修改房源状态审核是否提交成功
                    res2 = house_detail.is_get_application_success('商圈经理', house_no)
                    if res2:  # 校验商圈经理是否收到审核申请
                        res3 = house_detail.is_reject_application_sucess()
                        if res3 == False:  # 校验商圈经理是否驳回审核成功
                            log.error(f'商圈经理驳回{flag}审核失败'.format(flag = flag))
                            assert False
                        assert res3
                    else:
                        log.error(f'商圈经理未收到修改{flag}房源状态申请'.format(flag = flag))
                        assert False
                else:
                    log.error(f'提交修改{flag}房源状态审核失败'.format(flag = flag))
                    assert False
        else:
            log.error('当前维护人没有{flag}房源'.format(flag = flag))
            assert False

    @allure.story("修改房源价格-从调整价格进入")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['买卖', '租赁'])
    def test_modify_house_price(self, web_driver, flag):
        driver = web_driver
        house_detail = HouseDetailPage(driver)
        account_name = house_detail.get_account_name()
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(account_name, flag)
        if int(num) > 0:
            house_no, initial_price, house_area, init_maintainer_name= house_detail.enter_house_detail(flag)
            is_equel, is_submit, final_price = house_detail.is_modify_house_price_success(initial_price)
            if is_equel == False:  # 校验弹窗页面的房源价格与详情页面的房源价格是否一致
                log.error(f'调价弹窗页面的{flag}房源价格与详情页面的房源价格不一致'.format(flag = flag))
            if is_submit:  # 校验调价是否提交成功
                if flag == '买卖':
                    is_equel2, is_equel3 = house_detail.is_correct(final_price, house_area, flag)
                    res = house_detail.is_record_correct(initial_price, final_price, flag)
                    if is_equel2 and is_equel3:  # 校验详情页面的房价和单价是否更新
                        assert True
                    else:
                        log.error(f'详情页面{flag}房源价格或单价更新失败'.format(flag=flag))
                        assert False
                    if res:  # 校验调价记录是否更新
                        assert True
                    else:
                        log.error(f'{flag}调价记录更新失败'.format(flag=flag))
                elif flag == '租赁':
                    is_equel2 = house_detail.is_correct(final_price, house_area, flag)
                    res = house_detail.is_record_correct(initial_price, final_price, flag)
                    if is_equel2: # 校验详情页面的房价和单价是否更新
                        assert True
                    else:
                        log.error(f'详情页面{flag}房源价格或单价更新失败'.format(flag=flag))
                        assert False
                    if res:  # 校验调价记录是否更新
                        assert True
                    else:
                        log.error(f'{flag}调价记录更新失败'.format(flag=flag))
            else:
                log.error(f'{flag}调价确定失败'.format(flag = flag))
                assert False
        else:
            log.error(f'当前维护人没有{flag}房源'.format(flag = flag))
            assert False

    @allure.story("修改房源价格-从房源基础信息进入")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['买卖', '租赁'])
    def test_modify_price_by_information(self, web_driver, flag):
        driver = web_driver
        house_detail = HouseDetailPage(driver)
        account_name = house_detail.get_account_name()
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(account_name, flag)
        if int(num) > 0:
            house_no, initial_price, house_area ,init_maintainer_name= house_detail.enter_house_detail(flag)
            is_submit, final_price = house_detail.is_modify_success_by_information()
            if is_submit:  # 校验编辑详情是否确定成功
                if flag == '买卖':
                    is_equel2, is_equel3 = house_detail.is_correct(final_price, house_area, flag)
                    res = house_detail.is_record_correct(initial_price, final_price, flag)
                    is_update = house_detail.is_log_update(account_name)
                    if is_equel2 and is_equel3:  # 校验详情页面的房价和单价是否更新
                        assert True
                    else:
                        log.error('详情页面{flag}房源价格或单价更新失败'.format(flag = flag))
                        assert False
                    if res:  # 校验调价记录是否更新
                        assert True
                    else:
                        log.error('{flag}调价记录更新失败'.format(flag = flag))
                    if is_update:  # 校验操作日志是否更新
                        house_detail.click_blank_area()
                        assert is_update
                    else:
                        house_detail.click_blank_area()
                        log.error(f'{flag}操作日志更新失败'.format(flag = flag))
                        assert False
                elif flag == '租赁':
                    is_equel2 = house_detail.is_correct(final_price, house_area, flag)
                    res = house_detail.is_record_correct(initial_price, final_price, flag)
                    is_update = house_detail.is_log_update(account_name)
                    if is_equel2:  # 校验详情页面的房价和单价是否更新
                        assert True
                    else:
                        log.error(f'详情页面{flag}房源价格或单价更新失败'.format(flag = flag))
                        assert False
                    if res:  # 校验调价记录是否更新
                        assert True
                    else:
                        log.error(f'{flag}调价记录更新失败'.format(flag = flag))
                    if is_update:  # 校验操作日志是否更新
                        house_detail.click_blank_area()
                        assert is_update
                    else:
                        house_detail.click_blank_area()
                        log.error(f'{flag}操作日志更新失败'.format(flag = flag))
                        assert False
            else:
                log.error(f'编辑详情页面{flag}房源价格提交失败'.format(flag = flag))
                assert False
        else:
            log.error(f'当前维护人没有{flag}房源'.format(flag = flag))
            assert False

    @allure.story("举报房源并驳回举报")
    @pytest.mark.run(order=2)  # 保证在新增房源用例后执行
    @pytest.mark.parametrize('flag', ['买卖', '租赁'])
    def test_report_house(self, web_driver, flag):
        driver = web_driver
        house_detail = HouseDetailPage(driver)
        account_name = house_detail.get_account_name()
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(account_name, flag)
        if int(num) > 0:
            house_no = house_detail.enter_house_detail(flag)[0]
            res = house_detail.verify_can_report()
            if res:  # 校验当前房源是否支持举报
                log.error(f'存在待审核的{flag}记录，不允许再次举报'.format(flag = flag))
                assert False
            else:
                res = house_detail.report_house()
                if res:  # 校验举报房源是否确认成功
                    house_detail.is_get_report('平台品管', house_no)
                    if res:  # 校验平台品管是否收到举报房源申请
                        res = house_detail.reject_report()
                        assert res  # 校验是否驳回成功
                    else:
                        log.error(f'品管未收到{flag}举报申请'.format(flag = flag))
                        assert False
                else:
                    log.error(f'举报{flag}房源确认失败'.format(flag = flag))
                    assert False

    @allure.story("更换当前房源的维护人")
    @pytest.mark.run(order=3)  # 保证调整价格等用例执行结束后再执行更换房源维护人用例
    @pytest.mark.parametrize('flag', ['买卖', '租赁'])
    def test_replace_maintainer(self, web_driver, flag):
        driver = web_driver
        house_detail = HouseDetailPage(driver)
        account_name = house_detail.get_account_name()
        house_detail.change_role('经纪人')
        num = house_detail.get_house_num(account_name, flag)
        if int(num) > 0:
            house_no, initial_price, house_area, init_maintainer_name = house_detail.enter_house_detail(flag)
            res = house_detail.replace_maintainer(init_maintainer_name)
            assert res








if __name__ == '__main__':
    pytest.main(['-q', 'test_more.py'])
