#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: role_type.py
@date: 2021/11/12 0012
"""
from enum import Enum, unique


@unique
class RoleTypeEnum(Enum):

    SuperAdmin = '超级管理员'
    PrimaryAgent = '初级经纪人'
    BusinessManager = '商圈经理'
    SurveyPerson = '实勘人'
