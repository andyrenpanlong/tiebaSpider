#coding=utf-8

import time
from bs4 import BeautifulSoup
import requests
import urlparse
import json
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def search_all_page_url(tieba_name):
    start_url = 'http://tieba.baidu.com/f'
    payload = {'ie': 'utf-8', 'kw': str(tieba_name)}
    r = requests.get(start_url, params=payload)
    all_pages = ''
    if r.status_code == 200:
        time.sleep(5)
        bs = BeautifulSoup(r.text, 'html5lib')
        get_all_pages = bs.select('.pagination-default .last')[0].get('href')
        result = urlparse.urlparse(get_all_pages)
        parmas = urlparse.parse_qs(result.query, True)
        print "获取页面的总页码", parmas["pn"]
        all_pages = int(parmas["pn"][0])
        print "共计页数为：", all_pages
    else:
        print "页面信息获取失败"
        pass
    return all_pages

# 获取某条贴吧信息的所有帖子链接
def get_which_all_linkUrl(all_pages, tieba_name):
    dataArr = []
    start_url = 'http://tieba.baidu.com/f'
    host_url = 'http://tieba.baidu.com'
    # for page in range(0, all_pages, 50):
    for page in range(850, all_pages, 50):
        print page
        payload = {'ie': 'utf-8', 'kw': str(tieba_name), 'pn': page}
        res = requests.get(start_url, params=payload, timeout=20)
        print "当前页码为：", page, payload
        if res.status_code == 200:
            bs = BeautifulSoup(res.text, 'html5lib')
            get_which_all_links = bs.select("#thread_list .j_thread_list")
            for i in range(0, len(get_which_all_links), 1):
                dataSet = get_which_all_links[i]['data-field']
                tie_href = get_which_all_links[i].select('.threadlist_title .j_th_tit')[0]['href']
                title = get_which_all_links[i].select('.threadlist_title .j_th_tit')[0].get('title')
                msgData = json.JSONDecoder().decode(dataSet)
                msgData['tie_href'] = host_url + tie_href
                msgData['title'] = str(title)
                print "444", dataSet
                single_data_save_mysql(msgData)
                dataArr.append(msgData)
        else:
            print "请求出错"
            pass
        # print dataArr
    return dataArr


def single_data_save_mysql(dataObj):
    print "55555", dataObj
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "200888", "longgetest", charset="utf8mb4")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute('SET CHARACTER SET utf8mb4')
    cursor.execute('SET character_set_connection=utf8mb4')

    if (dataObj['is_membertop'] == None or (not dataObj.has_key("is_membertop"))):
        dataObj['is_membertop'] = ''

    if (not dataObj.has_key("is_multi_forum") or dataObj['is_multi_forum'] == None):
        dataObj['is_multi_forum'] = ''

    if (not dataObj.has_key("tie_href") or dataObj['tie_href'] == None):
        dataObj['tie_href'] = ''

    if (not dataObj.has_key("vid") or dataObj['vid'] == None):
        dataObj['vid'] = ''

    if (not dataObj.has_key("reply_num") or dataObj['reply_num'] == None):
        dataObj['reply_num'] = ''

    if (not dataObj.has_key("is_good") or dataObj['is_good'] == None):
        dataObj['is_good'] = ''

    if (not dataObj.has_key("is_top") or dataObj['is_top'] == None):
        dataObj['is_top'] = ''

    if (not dataObj.has_key("is_protal") or dataObj['is_protal'] == None):
        dataObj['is_protal'] = ''

    if (not dataObj.has_key("author_name") or dataObj['author_name'] == None):
        dataObj['author_name'] = ''

    if (not dataObj.has_key("frs_tpoint") or dataObj['frs_tpoint'] == None):
        dataObj['frs_tpoint'] = ''

    if (not dataObj.has_key("is_bakan") or dataObj['is_bakan'] == None):
        dataObj['is_bakan'] = ''

    if (not dataObj.has_key("title") or dataObj['title'] == None):
        dataObj['title'] = ''

    if (not dataObj.has_key("first_post_id") or dataObj['first_post_id'] == None):
        dataObj['first_post_id'] = ''

#    print "3435345:", dataObj
#     names = []
#     vals = []
#     for i in dataObj:
#         names.append(i)
#         va = ''
#         if (isinstance(dataObj[i],int)):
#             va = str(dataObj[i])
#         else:
#             va = dataObj[i]
#         vals.append(va)
#     print "ddddd", names, ",".join(names)
#     print "eeeee", vals, ",".join(vals)
#     sql = "INSERT INTO TieBaList("
#     sql += ",".join(names)
#     sql += ") VALUES ("
#     sql += ",".join(vals)
#     sql += ")"
    sql = """INSERT INTO TieBaList (user_id, author_name, first_post_id, reply_num, tie_href, title) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % (dataObj['id'], dataObj['author_name'], dataObj['first_post_id'], dataObj['reply_num'], dataObj['tie_href'], dataObj['title'])


    # sql = """INSERT INTO TieBaList(user_id,
    #          is_membertop, is_multi_forum, vid, tie_href, reply_num,
    #          is_good, is_top, is_protal,
    #          frs_tpoint, is_bakan, author_name, title, first_post_id)
    #          VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
    #        % (dataObj["id"], dataObj["is_membertop"], dataObj["is_multi_forum"], dataObj["vid"],
    #           dataObj["tie_href"], dataObj["reply_num"], dataObj["is_good"],
    #           dataObj["is_top"], dataObj["is_protal"], dataObj["frs_tpoint"], dataObj["is_bakan"], dataObj["author_name"],
    #           dataObj["title"], dataObj["first_post_id"])
    # sql = """INSERT INTO TieBaList(user_id,
    #          is_membertop, is_multi_forum, vid, tie_href, reply_num,
    #          is_good, is_top, is_protal,
    #          frs_tpoint, is_bakan, author_name, title, first_post_id)
    #          VALUES ('4933031972', 'None', 'None', '', 'http://tieba.baidu.com/p/4933031972', '68', 'None', 'True', 'None', 'None', 'None', '爆机人脉，没有人脉你和谁谈单', '【公告】暂行吧规-发帖尺度规定', '102370371223')"""
    # sql = """INSERT INTO TieBaList(user_id,
    #              is_membertop, is_multi_forum, vid, tie_href, reply_num,
    #              is_good, is_top, is_protal,
    #              frs_tpoint, is_bakan, author_name, title, first_post_id)
    #              VALUES ('4933031972', 'None', 'None', '', 'http://tieba.baidu.com/p/4933031972', '68', 'None', 'True', 'None', 'None', 'None', '爆机人脉，没有人脉你和谁谈单👿', '【公告】暂行吧规-发帖尺度规定', '102370371223')"""

    print sql
    try:
       # 执行sql语句
       cursor.execute(sql)
       print "234234232"
       # 提交到数据库执行
       db.commit()
    except(IOError, ZeroDivisionError), e:
       # Rollback in case there is any error
       print "数据库执行出错：", e
       # Rollback in case there is any error
       db.rollback()

    # 关闭数据库连接
    db.close()






all_pages = search_all_page_url("智能家居吧")
arr = get_which_all_linkUrl(all_pages, "智能家居吧")
# tiebalist_save_to_mysql(arr)

