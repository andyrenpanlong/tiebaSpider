#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "200888", "iocommunet")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS content")

# 创建数据表SQL语句
sql = """CREATE TABLE content (
         post_id  CHAR(20) NOT NULL,
         is_anonym CHAR(10),
         open_id CHAR(100),  
         open_type CHAR(1),
         date CHAR(100),
         vote_crypt CHAR(10),
         post_no CHAR(10),
         type CHAR(20),
         content VARCHAR(10000),
         comment_num CHAR(20),
         ptype CHAR(20),
         is_saveface CHAR(20),
         props CHAR(20),
         post_index CHAR(20),
         forum_id CHAR (20),
         thread_id CHAR (20),
         user_sex CHAR (10),
         pb_tpoint CHAR(20))"""

cursor.execute(sql)

# 关闭数据库连接
db.close()