#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "200888", "longgetest", charset="utf8")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 设置编码格式
# cursor.execute('SET NAMES utf8;')
# cursor.execute('SET CHARACTER SET utf8;')
# cursor.execute('SET character_set_connection=utf8;')

cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS TieBaList")

# 创建数据表SQL语句
sql = """CREATE TABLE TieBaList (\
         id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,\
         user_id  CHAR(30),\
         first_post_id CHAR (50),\
         tie_href CHAR(200),\
         author_name VARCHAR (100) CHARACTER SET utf8mb4,\
         title VARCHAR (100) CHARACTER SET utf8mb4,\
         is_membertop  CHAR(30),\
         is_multi_forum  CHAR(30),\
         vid CHAR(50),\
         reply_num CHAR (20),\
         is_good  CHAR(20),\
         is_top CHAR(20),\
         is_protal CHAR(20),\
         frs_tpoint CHAR(50),\
         is_bakan CHAR(20))"""

cursor.execute(sql)

# 关闭数据库连接
db.close()