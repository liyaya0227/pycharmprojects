#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: trade_certificate_type.py
@date: 2021/10/11 0017
"""
from enum import Enum, unique


@unique
class TradeCertificateTypeEnum(Enum):

    tradeHouseVipDelegateInfoVO = 'VIP服务委托协议'
    tradeHouseRoomInfoVO = '房产证'
    keyInfoVO = '钥匙委托凭证'
    tradeHouseDelegateInfoVO = '书面委托协议'
    tradeHouseTaxInfoVO = '契税票'
    tradeHouseContractInfoVO = '原始购房合同'
    tradeHouseIdentityInfoVO = '身份证明'
