#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: certificate.py
@date: 2021/11/19 0019
"""
from enum import Enum, unique


@unique
class CertificateNameEnum(Enum):
    Delegate = '书面委托协议'
    key = '钥匙委托凭证'
    VipDelegate = 'VIP服务委托协议'
    Room = '房产证'


@unique
class CertificateCodeEnum(Enum):
    Delegate = '3'
    VipDelegate = '0'
    Key = '2'
    Room = '1'
