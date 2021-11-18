#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: city_name.py
@date: 2021/10/18 0018
"""
from enum import Enum, unique


@unique
class CityNameEnum(Enum):

    sz = '苏州'
    ks = '昆山'
    zjg = '张家港'
    wx = '无锡'
    hz = '桐庐'
