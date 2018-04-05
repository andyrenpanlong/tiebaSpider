#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "200888", "iocommunet")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS author")

# 创建数据表SQL语句
sql = """CREATE TABLE author (
         id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
         user_id  CHAR(20) NOT NULL ,
         user_name  CHAR(100),
         name_u CHAR(100),
         user_sex CHAR(1),
         portrait CHAR(100),
         is_like CHAR(10),
         level_id CHAR(10),
         level_name CHAR(20),
         cur_score CHAR(20),
         bawu CHAR(20),
         props CHAR(20))"""

# sql = """CREATE TABLE author (
#          user_name  CHAR(100),
#          user_id  CHAR(20) NOT NULL,
#          props CHAR(20));"""

cursor.execute(sql)

# 关闭数据库连接
db.close()