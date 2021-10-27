#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: databaseutil.py
@date: 2021/10/18 0018
"""
import pymssql
import pymysql
from common.readconfig import ini


class DataBaseUtil(object):

    def __init__(self, db_type, database_name):
        if db_type == 'SQL Server':
            db_info = {
                'server': ini.database_server,
                'user': ini.database_account,
                'password': ini.database_password,
                'database': database_name,
                'charset': 'utf8'
            }
            self.conn = pymssql.connect(**db_info)
        elif db_type == 'My SQL':
            db_info = {
                'host': ini.mysql_database_host,
                'port': int(ini.mysql_database_port),
                'user': ini.mysql_database_account,
                'password': ini.mysql_database_password,
                'database': database_name,
                'charset': 'utf8'
            }
            self.conn = pymysql.connect(**db_info)

        elif db_type == 'Xf My SQL':
            db_info = {
                'host': ini.xf_database_host,
                'port': int(ini.mysql_database_port),
                'user': ini.xf_database_account,
                'password': ini.xf_database_password,
                'database': database_name,
                'charset': 'utf8'
            }
            self.conn = pymysql.connect(**db_info)
        else:
            raise ValueError('传值错误')

    def select_sql(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            col = cursor.description
            fields = []
            for i in range(len(col)):
                fields.append(col[i][0])
            fc = cursor.fetchall()
            return fc
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.conn.close()

    def update_sql(self, sql):
        try:
            cursor = self.conn.cursor()
            count = cursor.execute(sql)
            self.conn.commit()
            return count
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.conn.close()
