#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "200888", "iocommunet", charset="utf8mb4")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 设置编码格式
# cursor.execute('SET NAMES utf8;')
# cursor.execute('SET CHARACTER SET utf8;')
# cursor.execute('SET character_set_connection=utf8;')

cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8mb4;')
cursor.execute('SET character_set_connection=utf8mb4;')

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS TieBaList")

# 创建数据表SQL语句
sql = """CREATE TABLE TieBaList (
         id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
         user_id  CHAR (100),
         is_membertop  CHAR(20),
         is_multi_forum  CHAR(20),
         vid CHAR(100),
         tie_href CHAR(100),
         reply_num  INT,
         is_good  CHAR(50),
         is_top CHAR(50),
         is_protal CHAR(50),
         frs_tpoint CHAR(50),
         is_bakan CHAR(50),
         author_name CHAR (70),
         title CHAR (100),
         first_post_id CHAR (30))"""


cursor.execute(sql)

# 关闭数据库连接
db.close()