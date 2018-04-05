#coding=utf-8

import time
from bs4 import BeautifulSoup
from userAgents import *
from proxiesList import proxy
import requests
import urlparse
import json
import warnings
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


print '此次爬虫使用的代理IP是{}'.format(proxy)

'''
-------------------------------------------------------------
方法1作用：获取某个贴吧的信息
参数说明："tieba_name"是打开某个贴吧后，浏览器地址栏中的"kw="之后的汉字
-------------------------------------------------------------
'''
def get_tieba_detail_info(tieba_name):
    start_url='http://tieba.baidu.com/f'
    host_url='http://tieba.baidu.com'
    payload={'ie':'utf-8','kw':str(tieba_name)}
    # r=requests.get(start_urcl,params=payload,proxies=proxy,timeout=20)
    r=requests.get(start_url, params=payload)
    if r.status_code==200:
        time.sleep(2)
        bs = BeautifulSoup(r.text,'html5lib')
        # print "解析贴吧姓名", bs
        # 1、获取贴吧名字
        get_name = bs.find('title').text
        print "标题", get_name
        name = get_name.split('_')[0].split(' ')[-1]
        print "名字", name
        # 2、获取关注人数
        get_memNum=bs.select('span[class="card_menNum"]')[0]
        memNum=get_memNum.text
        print "关注人数", memNum
        # 3、获取帖子总数
        get_infoNum=bs.select('span[class="card_infoNum"]')[0]
        infoNum=get_infoNum.text

        # 4、获取本吧所在类别信息
        get_card_info = bs.select('div.card_info > ul > li > a')
        print "dddd", get_card_info
        # 5、获取所在频道
        channel=get_card_info[0].text.encode('utf-8')
        # 6、获取所在目录
        # dir_text=get_card_info[1].text.encode('utf-8')
        # 7、获取slogan
        get_slogan=bs.select('div.card_top.clearfix > p')
        slogan=get_slogan[0].text
        # 8、获取本吧详细信息链接——【待解决】
        get_det_link=bs.select("h4 > span > a")
        det_link=host_url+get_det_link[0].get('href')
        # 获得吧务团队、本吧会员、本吧会员的信息
        # get_bawu_detials_link(det_link)

        get_all_pages = bs.select('.pagination-default .last')[0].get('href')
        result = urlparse.urlparse(get_all_pages)
        parmas = urlparse.parse_qs(result.query, True)
        print "获取页面的总页码", parmas["pn"]
        all_pages = int(parmas["pn"][0])
        print "共计页数为：", all_pages

        #主题数 帖子数 会员数
        topic_num_param = bs.select('.red_text')
        topic_num = int(topic_num_param[0].get_text())
        invitation_num = int(topic_num_param[1].get_text())
        vip_num = int(topic_num_param[2].get_text())
        print "主题数 帖子数 会员数分别为:", topic_num, invitation_num, vip_num
        print name
        print memNum
        print infoNum
        print channel
        # print dir_text
        print slogan
        print "det_link:", det_link
    else:
        print "请求错误，请调试请求~"
        pass



'''
--------------------------------------------------------------------------
方法2说明：获取"本吧信息"中的详细信息页面中的三个模块的链接（吧务团队、吧务候选、本吧会员）
         其中"本吧详情"模块的链接就是传入的参数"detial_link"
参数说明：本参数是从方法1中的得到，是某贴吧主页的右侧"本吧信息"的"查看详情"的链接，所以本
        函数可以搭配方法1才能自动使用，否则需要手动获取"查看详情"的链接
--------------------------------------------------------------------------
'''
def get_bawu_detials_link(detial_link):
    # 获得贴吧的吧务信息——考虑整合到获取贴吧的详细信息函数中
    details_info_url='http://tieba.baidu.com/bawu2/platform/detailsInfo?word=%E4%B8%8A%E6%B5%B7%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8'
    host_url='http://tieba.baidu.com'
    # r=requests.get(details_info_url,proxies=proxy,timeout=20)
    r = requests.get(details_info_url)
    if r.status_code == 200:
        time.sleep(2)
        bs = BeautifulSoup(r.text,'html5lib')
        get_team_info_url = bs.select('div > p > a')
        # 获取吧务团队的链接
        team_info_url = host_url+get_team_info_url[1].get('href')
        # 获得吧务候选的链接
        candidate_info_url = host_url+get_team_info_url[2].get('href')
        # 获得本吧会员的链接
        member_info_url = host_url+get_team_info_url[3].get('href')

        print team_info_url
        print candidate_info_url
        print member_info_url
    else:
        print '请求错误，请调试请求！'
        pass


'''
-------------------------------------------------------------------------
方法3作用：获取某贴吧的吧务团队的所有人链接
         （已实现分类：吧主、小吧主、图片小编、视频小编、吧刊主编、吧刊小编）
参数说明："吧务团队"的链接，来源是由方法2获得。所以本方法需要搭配方法2才可以自动爬取信息，
        否则请自行获取"吧务团队"模块的链接。
-------------------------------------------------------------------------
'''

# 获得吧务团队信息-有错误，待修改
def get_bawu_member_link():
    team_info_url='http://tieba.baidu.com/bawu2/platform/listBawuTeamInfo?word=%C9%CF%BA%A3%B9%A4%B3%CC%BC%BC%CA%F5%B4%F3%D1%A7'
    host_url='http://tieba.baidu.com'
    # r=requests.get(team_info_url,proxies=proxy,timeout=20)
    r=requests.get(team_info_url, timeout=20)
    if r.status_code==200:
        time.sleep(2)
        bs=BeautifulSoup(r.text,'lxml')
        # 吧主的个人信息链接
        get_bazhu_link=bs.select('div.bawu_single_type.first_section > div.member_wrap.clearfix > span > a.user_name')
        bazhu_length=len(get_bazhu_link)
        # for i in range(0,bazhu_length):
        #     print   host_url+get_bazhu_link[i].get('href')

        #小吧主的个人信息——有问题！继承nth-child（2）解析错误，换解析方式？
        # get_xiaobazhu_link=bs.select('div:nth-child(2) > div.member_wrap.clearfix > span > a.user_name')
        get_xiaobazhu_link = bs.select('a.user_name')
        xiaobazhu_length=len(get_xiaobazhu_link)
        # for j in range(bazhu_length,xiaobazhu_length):
        #     print host_url+get_xiaobazhu_link[j].get('href')

        #图片小编的个人信息链接
        # get_tupianxiaobian_link=get_xiaobazhu_link
        # tupianxiaobian_link=get_tupianxiaobian_link
    else:
        print '请求错误，请修改请求！'
        pass



'''
-------------------------------------------------------------
方法4作用：获取某个贴吧，某一页的所有帖子信息（包括：标题、链接）
参数说明："tieba_name"是打开某个贴吧主页后，浏览器地址栏中"kw="后的汉字
        "page"是想要爬取的页码数
-------------------------------------------------------------
'''
def get_single_page_items_info(tieba_name, page):
    host_url = 'http://tieba.baidu.com'
    # pn=[pn for pn in range(0,6350,50)]
    payload = {'ie': 'utf-8', 'kw': str(tieba_name), 'pn': str(page)}
    # r=requests.get(host_url+'/f',params=payload,proxies=,timeout=15)
    r = requests.get(host_url+'/f', params=payload, timeout=15)
    time.sleep(2)
    if r.status_code == 200:
        bs = BeautifulSoup(r.text, 'html5lib')
        items = bs.select('div.threadlist_title.pull_left.j_th_tit > a')
        item_authors = bs.select('div.col2_right.j_threadlist_li_right > div.threadlist_lz.clearfix > div.threadlist_author.pull_right > span.tb_icon_author > span.frs-author-name-wrap > a')
        item_num = len(items)
        response_num = bs.select('div.col2_left.j_threadlist_li_left > span')
        # item_author_num=len(item_authors)
        for i in range(0, item_num-1):
            # 得到了帖子的标题
            print items[i].text
            # 回帖量
            print (int(response_num[i].text)+1)
            # 得到帖子的链接
            print host_url+'/'+items[i].get('href')
            # 帖子的楼主信息
            print item_authors[i].text
            # 楼主信息的链接
            print (host_url+item_authors[i].get('href'))
            print '\n'
    else:
        print "请求错误，请调试请求！"
        pass


'''
--------------------------------------------------------------
方法5作用：获取某个贴吧，某几页之间的所有帖子信息（包括：标题、链接）
参数说明："tieba_name"是打开某个贴吧主页后，浏览器地址栏中"kw="后的汉字
        "beginPage"是想要爬取的起始页码数
        "endPage"是想要爬取的结尾页码数
--------------------------------------------------------------
'''
def get_all_items_info(tieba_name, beginPage, endPage):
    for page in range(50*(beginPage-1), 50*endPage, 50):
        get_single_page_items_info(str(tieba_name), page)



'''
-------------------------------------------------------------
方法6作用:获取某一篇帖子某一页的所有的楼层评论、评论者所使用的设备信息、评论时间
参数说明："item_link"帖子的链接
        "page"页码数
-------------------------------------------------------------
'''
# 获取每一篇帖子的某一页详细信息以及楼层评论
def get_single_judgement_info(item_link, page):
    payload = {'pn': str(page)}
    # r=requests.get(item_link,proxies=proxy,timeout=15,params=payload)
    page_content = []
    r = requests.get(item_link, params=payload, timeout=15)
    time.sleep(2)
    if r.status_code == 200:
        bs = BeautifulSoup(r.text, 'html5lib')
        # 得到回复内容
        contents = bs.select('#j_p_postlist .l_post')
        for i in range(0, len(contents), 1):
            page_content.append(contents[i]['data-field'])
    else:
        print "请求错误，请调试请求！"
    divide_author_content(page_content)
    return page_content



'''
--------------------------------------------------------------------
方法7作用:获取某一篇帖子某几页之间的所有的楼层评论、评论者所使用的设备信息、评论时间
参数说明："beginPage"起始页码
        "endPage"结尾页码
--------------------------------------------------------------------
'''

# 获取某个帖子某页之前的所有楼层评论
def get_all_judgement_info(item_link, beginPage, endPage):
    for page in range(beginPage, endPage+1, 1):
        get_single_judgement_info(item_link, page)


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
                msgData['title'] = title
                single_data_save_mysql(msgData)
                dataArr.append(msgData)
        else:
            print "请求出错"
            pass
        # print dataArr
    return dataArr


def single_data_save_mysql(dataObj):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "200888", "iocommunet", charset="utf8mb4")
    # db = MySQLdb.connect("localhost", "root", "200888", "iocommunet")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')

    print "基地：", dataObj
    sql = """INSERT INTO TieBaList(user_id,
             is_membertop, is_multi_forum, vid, tie_href, reply_num,
             is_good, is_top, is_protal,
             frs_tpoint, is_bakan, author_name, title, first_post_id)
             VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
           % (dataObj["id"], dataObj["is_membertop"], dataObj["is_multi_forum"], dataObj["vid"],
              dataObj["tie_href"], dataObj["reply_num"], dataObj["is_good"],
              dataObj["is_top"], dataObj["is_protal"], dataObj["frs_tpoint"], dataObj["is_bakan"], dataObj["author_name"],
              dataObj["title"], dataObj["first_post_id"])

    # sql = """INSERT INTO TieBaList(user_id,
    #             is_membertop, is_multi_forum, vid, tie_href, reply_num,
    #             is_good, is_top, is_protal,
    #             frs_tpoint, is_bakan, first_post_id)
    #             VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
    #       % (dataObj["id"], dataObj["is_membertop"], dataObj["is_multi_forum"], dataObj["vid"],
    #          dataObj["tie_href"], dataObj["reply_num"], dataObj["is_good"],
    #          dataObj["is_top"], dataObj["is_protal"], dataObj["frs_tpoint"],
    #          dataObj["is_bakan"], dataObj["first_post_id"])
    print "888 :", sql

    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except(IOError, ZeroDivisionError), e:
       # Rollback in case there is any error
       print "数据库执行出错：", e
       # Rollback in case there is any error
       db.rollback()

    # 关闭数据库连接
    db.close()


# item_link = 'http://tieba.baidu.com/p/4372736094'
# beginPage = 1
# endPage = 2
# get_all_judgement_info(item_link, beginPage, endPage)

# get_which_all_linkUrl("智能家居吧")



#贴吧链接存入数据库
def tiebalist_save_to_mysql(dataArr):
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "200888", "iocommunet", charset="utf8mb4")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')

    # 如果数据表已经存在使用 execute() 方法删除表。
    # cursor.execute("DROP TABLE IF EXISTS TieBaList")

    # 创建数据表SQL语句
    sql = """CREATE TABLE TieBaList (
             id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
             user_id  CHAR (20),
             is_membertop  CHAR(20),
             is_multi_forum  CHAR(20),
             vid CHAR(20),
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

    # cursor.execute(sql)
    for value in dataArr:
        print "555:", value
        # SQL 插入语句isinstance(s, unicode) 用来判断是否为unicode
        sql2 = """INSERT INTO TieBaList(user_id,
                 is_membertop, is_multi_forum, vid, tie_href, reply_num,
                 is_good, is_top, is_protal,
                 frs_tpoint, is_bakan, author_name, title, first_post_id)
                 VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
               % (value["id"], value["is_membertop"], value["is_multi_forum"], value["vid"],
                  value["tie_href"], value["reply_num"],  value["is_good"],
                  value["is_top"], value["is_protal"], value["frs_tpoint"], value["is_bakan"], value["author_name"], value["title"], value["first_post_id"])
        print "sadad:", sql2
        try:
            # 执行sql语句
            cursor.execute(sql2)
            # 提交到数据库执行
            db.commit()
        except(IOError, ZeroDivisionError), e:
            # Rollback in case there is any error
            print "数据库执行出错：", e
            db.rollback()
    # 关闭数据库连接
    db.close()


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

# 从数据库查询全部文章链接
def search_all_url():
    urls = []
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "200888", "iocommunet")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM TieBaList"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            urls.append(row[5])
    except:
        print "Error: unable to fecth data"

    # 关闭数据库连接
    db.close()
    return urls


# 存储作者信息到作者表
def save_to_author(dataObj):
    if(not dataObj.has_key("name_u")):
        dataObj['name_u'] = ''

    if(not dataObj.has_key("user_sex")):
        dataObj['user_sex'] = ''

    if (not dataObj.has_key("portrait")):
        dataObj['portrait'] = ''

    if (not dataObj.has_key("is_like")):
        dataObj['is_like'] = ''

    if (not dataObj.has_key("level_id")):
        dataObj['level_id'] = ''

    if (not dataObj.has_key("level_name")):
        dataObj['level_name'] = ''

    if (not dataObj.has_key("cur_score")):
        dataObj['cur_score'] = ''

    if (not dataObj.has_key("bawu")):
        dataObj['bawu'] = ''

    if (not dataObj.has_key("user_id")):
        dataObj['user_id'] = ''
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "200888", "iocommunet")
    db.set_character_set('utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    #设置编码格式
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    sql = """INSERT INTO author(user_id, user_name, name_u, user_sex, portrait, is_like, level_id, level_name, cur_score, bawu)
             VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (dataObj['user_id'], dataObj['user_name'], dataObj['name_u'], dataObj['user_sex'], dataObj['user_sex'], dataObj['portrait'], dataObj['is_like'], dataObj['level_id'], dataObj['level_name'], dataObj['bawu'])
    print "sql:", sql
    try:
        # 执行SQL语句
        cursor.execute(sql)
        db.commit()
        print "执行完毕"
    except(IOError, ZeroDivisionError), e:
        # Rollback in case there is any error
        print "数据库执行出错：", e
        pass

    # 关闭数据库连接
    db.close()

def save_to_content(dataObj):
    if (not dataObj.has_key("user_sex")):
        dataObj['user_sex'] = ''
    if (not dataObj.has_key("forum_id")):
        dataObj['forum_id'] = ''
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "200888", "iocommunet")
    db.set_character_set('utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    #设置编码格式
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    print dataObj
    sql = """INSERT INTO content(post_id, is_anonym, forum_id, thread_id, user_sex, post_no, type, comment_num, post_index)
             VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (dataObj['post_id'], dataObj['is_anonym'], dataObj['forum_id'], dataObj['thread_id'], dataObj['user_sex'],dataObj['post_no'], dataObj['type'], dataObj['comment_num'], dataObj['post_index'])
    try:
        # 执行SQL语句
        cursor.execute(sql)
        db.commit()
        print "执行完毕"
    except(IOError, ZeroDivisionError), e:
        # Rollback in case there is any error
        print "数据库执行出错：", e

    # 关闭数据库连接
    db.close()

def divide_author_content(msgArr):
    for content in msgArr:
        msgData = json.JSONDecoder().decode(content)
        save_to_author(msgData['author'])
        save_to_content(msgData['content'])

def save_content_to_page(value):
    db = MySQLdb.connect("localhost", "root", "200888", "iocommunet")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print "数据库链接成功"
    # cursor.execute('SET NAMES utf8;')
    # cursor.execute('SET CHARACTER SET utf8mb4;')
    # cursor.execute('SET character_set_connection=utf8mb4;')

    sql = """INSERT INTO page(user_id, post_id, text)
                 VALUES ('%s', '%s', '%s')""" % (value['user_id'], value['post_id'], value['text'])

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except(IOError, ZeroDivisionError), e:
        # Rollback in case there is any error
        print "数据库执行出错：", e
        # Rollback in case there is any error
        db.rollback()

    # 关闭数据库连接
    db.close()






# all_pages = search_all_page_url("智能家居吧")
# arr = get_which_all_linkUrl(all_pages, "智能家居吧")
# tiebalist_save_to_mysql(arr)

def getTieZiPage(urlLink):
    r = requests.get(urlLink)
    all_pages = ''
    if r.status_code == 200:
        time.sleep(5)
        bs = BeautifulSoup(r.text, 'html5lib')
        all_pages = bs.select('.l_reply_num')[0].select('.red')[1].text or '1'
    else:
        print "页面信息获取失败"
    return int(all_pages)

arr = search_all_url()
print len(arr)

for i in range(0, len(arr), 1):
    print "aa：", arr[i]
    endPage = getTieZiPage(arr[i])
    get_all_judgement_info(arr[i], 1, endPage+1)
