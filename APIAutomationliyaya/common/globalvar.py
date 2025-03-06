#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: globalvar.py
@date: 2021/9/9 0009
"""


class GlobalVar(object):

    header = {'Content-Type': 'application/json', 'Connection': 'keep_alive'}  # 初始请求头
    clean_header = {'Content-Type': 'application/json', 'Connection': 'close'}  # 初始请求头
    city_env = {  # 城市包含的地区
        'sz': ['sz', 'ks', 'zjg'],
        'ks': ['ks'],
        'zjg': ['zjg'],
        'wx': ['wx'],
        'hz': ['tl'],
        'tl': ['tl']
    }
    house_estate_id = ''  # 楼盘id
    house_building_number_id = ''  # 楼栋id
    house_building_cell_id = ''  # 楼栋单元id
    house_location_id = ''  # 房源位置id
    sale_house_id = ''  # 买卖房源id
    sale_house_code = ''  # 买卖房源编号
    rent_house_id = ''  # 租赁房源id
    rent_house_code = ''  # 租赁房源编号
    new_house_id = ''  # 新房id
    custom_id = 'EA1F959D-AC9D-474C-8105-6F134E79CE8F'  # 客源id
    wx_custom_id = ''  # 无锡客源id
    hz_custom_id = ''  # 杭州客源id
    custom_code = 'C2109000015'  # 客源编号
    custom_name = ''  # 客源姓名
    house_verify_code = '123456'  # 房源验证超级码
    new_estate_id = ''  # 新房楼盘id
    cw_collection_account = '30090188000279443'  # 财务收款账户
    cw_collection_account_name = '苏州京日找房信息科技有限公司'  # 财务收款账户名
    cw_collection_company_name = '苏州京日找房信息科技有限公司'  # 财务收款公司
    xf_house_id = ''  # 新房源id
    xf_house_name = ''  # 新房源名称
    xf_custom_id = '68ccd9e7-4d1e-4be7-9c22-15eb83975969'  # 新房客源id
    xf_custom_code = 'X2110000031'  # 新房客源编号
    xf_custom_name = 'api自动化客源'

