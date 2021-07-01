#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: sqlutil.py
@time: 2021/06/25
"""
import pymssql
from common.readconfig import ini


def update_sql(sql):
    try:
        conn = pymssql.connect(server=ini.database_server, user=ini.database_account, password=ini.database_password,
                               database=ini.database_name, charset='utf8')
        cursor = conn.cursor()
        count = cursor.execute(sql)
        conn.commit()
        return count
    except Exception as ex:
        conn.rollback()
        raise ex
    finally:
        conn.close()


def select_sql(sql):
    try:
        conn = pymssql.connect(server=ini.database_server, user=ini.database_account, password=ini.database_password,
                               database=ini.database_name, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(sql)
        col = cursor.description
        fields = []
        for i in range(len(col)):
            fields.append(col[i][0])
        fc = cursor.fetchall()
        return fc
    except Exception as ex:
        conn.rollback()
        raise ex
    finally:
        conn.close()


if __name__ == '__main__':
    result = select_sql("select * from dbo.contract_order")

