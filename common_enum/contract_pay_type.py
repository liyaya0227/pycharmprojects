#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: pay_type.py
@date: 2021/10/21 0021
"""
from enum import Enum, unique


@unique
class ContractPayTypeEnum(Enum):

    FullPayment = 'full_payment'
    CommercialLoan = 'commercial_loan'
