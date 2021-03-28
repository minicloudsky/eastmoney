#!/usr/bin/env python
# coding=utf-8
import pymysql

host = 'db'
port = 3306
user = 'root'
password = 'root'
db = 'eastmoney'

def init_database():
    conn = pymysql.connect(host=host, port=port, user=user, password=password,db='mysql')
    cursor = conn.cursor()
    cursor.execute("create database if not exists  {}".format(db))
    conn.commit()
    print("finish create database {}".format(cursor.fetchall()))
    update_permission_sql = """
    ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
    """
    cursor.execute(update_permission_sql)
    conn.commit()
    print("finish update permissions {}".format(cursor.fetchall()))

if __name__ == '__main__':
    init_database()

