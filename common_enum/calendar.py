#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: calendar.py
@date: 2021/11/12 0012
"""
from enum import Enum, unique


@unique
class CalendarNameEnum(Enum):

    January = '一月'
    February = '二月'
    March = '三月'
    April = '四月'
    May = '五月'
    June = '六月'
    July = '七月'
    August = '八月'
    September = '九月'
    October = '十月'
    November = '十一月'
    December = '十二月'


@unique
class CalendarCodeEnum(Enum):

    January = '01'
    February = '02'
    March = '03'
    April = '04'
    May = '05'
    June = '06'
    July = '07'
    August = '08'
    September = '09'
    October = '10'
    November = '11'
    December = '12'
