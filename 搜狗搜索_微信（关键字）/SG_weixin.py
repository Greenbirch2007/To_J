#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def get_first_page():

    url = 'https://www.sogou.com/'
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="weixinch"]').click()  #选择微信


    driver.find_element_by_xpath('//*[@id="query"]').clear()
    driver.find_element_by_xpath('//*[@id="query"]').send_keys("赴日IT") # 输入搜索的关键字
    driver.find_element_by_xpath('//*[@id="searchForm"]/div/input[3]').click()  #点击搜索
    html = driver.page_source

    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,12):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="sogou_next"]').click()
        time.sleep(1)
        html = driver.page_source
        return html



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    weixinHao = selector.xpath('//div[@class="s-p"]/a/text()')
    article_link = selector.xpath("//h3/a/@href")
    for i1,i2 in zip(weixinHao,article_link):
        big_list.append((i1,i2))
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='To_J',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into To_J_weixin (weixinHao,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass





if __name__ == '__main__':
    html = get_first_page()
    content =   parse_html(html)
    insertDB(content)
    while True:
        html = next_page()
        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())
        time.sleep(1)


# #
# create table To_J_weixin(
# id int not null primary key auto_increment,
# weixinHao varchar(20),
# link text
# ) engine=InnoDB  charset=utf8;