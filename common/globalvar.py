#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: globalvar.py
@date: 2021/9/28 0028
"""


class GlobalVar(object):

    city_env = {  # 城市包含的地区
        'sz': ['sz', 'ks', 'zjg'],
        'ks': ['ks'],
        'zjg': ['zjg'],
        'wx': ['wx'],
        'hz': ['tl'],
        'tl': ['tl']
    }
    house_verify_code = 'mNI1CcUn'  # 房源验证超级码
    house_code = ''
    customer_code = ''
    customer_name = ''
    house_info = {}
    sale_house_id = ''  # 买卖房源id
    sale_house_code = ''  # 买卖房源编号
    rent_house_id = ''  # 租赁房源id
    rent_house_code = ''  # 租赁房源编号
    new_house_id = ''  # 新房id
