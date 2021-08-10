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
    conn = pymssql.connect(server=ini.database_server, user=ini.database_account, password=ini.database_password,
                           database=ini.database_name, charset='utf8')
    try:
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
    conn = pymssql.connect(server=ini.database_server, user=ini.database_account, password=ini.database_password,
                           database=ini.database_name, charset='utf8')
    try:
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
    result = select_sql("select id from estate_new_base_info where [name]='" + ini.house_community_name + "'")
    print(str(result[0][0]))
    result1 = select_sql("select house_code from trade_house where location_estate_id='" + str(result[0][0]) + "' "
                         "and location_building_number='1' and location_building_cell='1' and location_floor='1' "
                         "and location_doorplate='1002' and is_valid='1' and [status]='0'")
    print(result1[0][0])
