#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: mysql.py
@time: 2021/08/18
"""
#连接sqlserve
import pymssql
#连接mysql
import pymysql
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


def select_my_sql(sql):
    db_info = {
        "host": ini.xf_database_server,
        "port": int(ini.xf_database_port),
        "user": ini.xf_database_account,
        "password": ini.xf_database_password,
        "db": ini.xf_database_name,
        "charset": "utf8",
    }
    conn = pymysql.connect(**db_info)
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
    house_detail = select_my_sql("SELECT * FROM `new_house` where new_house_name = 'leaya测试新房楼盘002'")
    print(house_detail)

