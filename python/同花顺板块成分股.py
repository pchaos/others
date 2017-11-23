#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 19:41:44 2017

@author: Mr.ZeroW

同花顺板块成分股
https://www.ricequant.com/community/topic/4443/
"""
import urllib.request
from lxml import etree
import pandas as pd
import time

#爬取板块名称以及代码并且存在文件
with urllib.request.urlopen('http://q.10jqka.com.cn/gn/') as f:
    text = f.read().decode('gb2312')

html = etree.HTML(text)

gnbk = html.xpath('/html/body/div[2]/div[1]/div//div//div//a')
thsgnbk = []
for i in range(len(gnbk)):
    thsgnbk.append((gnbk[i].text))
    
#板块代码
bkcode = html.xpath('/html/body/div[2]/div[1]/div//div//div//a/@href')
bkcode = list(map(lambda x : x.split('/')[-2], bkcode))
data = {'Name': thsgnbk}

#存储
gnbk = pd.DataFrame(data, index = bkcode)
gnbk.to_csv('gnbk.csv')

print('板块名称以及代码已爬取，存储文件名：gnbk.csv')
#导入板块名称和代码
data = pd.read_csv('gnbk.csv')
#建立数据框，四列【板块id, 板块name, 成分股id, 成分股name】

bk_id = []
bk_name = []
s_id = []
s_name = []
iCount = 1
print('爬取开始！')
start = time.time()
for i in range(len(data)):

    bk_code = str(data.iloc[i, 0])
    name = str(data.iloc[i, 1])
    url = 'http://q.10jqka.com.cn/gn/detail/code/' + bk_code + '/'
    print('%d: %s' %(iCount, name))
    iCount += 1
    
    with urllib.request.urlopen(url) as f:
        text = f.read().decode('GBK', 'ignore')

    #得出板块成分股有多少页
    html = etree.HTML(text)
    
    result = html.xpath('//*[@id="m-page"]/span/text()')
    try:
        page = int(result[0].split('/')[-1])
        for j in range(page):
            page_n = str(j + 1)
            curl = 'http://q.10jqka.com.cn/gn/detail/order/desc/page/' + page_n+ '/ajax/1/code/' + bk_code
            with urllib.request.urlopen(curl) as f:
                text = f.read().decode('GBK')
            html = etree.HTML(text)
            #成分股代码
            stock_code = html.xpath('/html/body/table/tbody/tr/td[2]/a/text()')
            #成分股名称
            stock_name = html.xpath('/html/body/table/tbody/tr/td[3]/a/text()')
            s_id += stock_code
            s_name += stock_name
            bk_id.extend([bk_code]* len(stock_code))
            bk_name.extend([name]* len(stock_name))
            
    except IndexError as e:
        curl = url
        with urllib.request.urlopen(curl) as f:
            text = f.read().decode('GBK')
        html = etree.HTML(text)
        #成分股代码
        stock_code = html.xpath('//*[@id="maincont"]/table/tbody/tr/td[2]/a/text()')
        #成分股名称
        stock_name = html.xpath('//*[@id="maincont"]/table/tbody/tr/td[3]/a/text()')   
        s_id += stock_code
        s_name += stock_name
        bk_id.extend([bk_code]* len(stock_code))
        bk_name.extend([name]* len(stock_name))
        
    
data_dict = dict(BK_ID = bk_id, BK_NAME = bk_name, S_ID = s_id, S_NAME = s_name)
cdata = pd.DataFrame(data_dict)
cdata.to_csv('chengfengu.csv')
end = time.time()
print('爬取结束！！\n开始时间：%s\n结束时间：%s\n'%(time.ctime(end), time.ctime(start)))
