#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "200888", "iocommunet")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS page")

# 创建数据表SQL语句
sql = """CREATE TABLE page (
         id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
         user_id  CHAR(20) NOT NULL,
         post_id CHAR(20),
         text VARCHAR (10000))"""



cursor.execute(sql)

# 关闭数据库连接
db.close()