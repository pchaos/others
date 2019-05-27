# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     cninfoScrabAbs
   Description :
   Author :
   date：          2019/5/10
-------------------------------------------------
   Change Activity:
                   2019/5/10:
-------------------------------------------------
"""
import csv
import math
import os
import time
import requests
import abc


class cninfoScrabBase():
    START_DATE = '2014-12-31'  # 搜索的起始日期
    END_DATE = str(time.strftime('%Y-%m-%d'))  # 默认当前提取，可设定为固定值
    OUT_DIR = '{}tmp{}2019年'.format(os.sep, os.sep)
    OUTPUT_FILENAME = '2019年度报告'
    # 板块类型：沪市：shmb；深市：szse；深主板：szmb；中小板：szzx；创业板：szcy；
    PLATE = 'szzx;'
    # 公告类型：category_scgkfx_szsh（首次公开发行及上市）、category_ndbg_szsh（年度报告）、category_bndbg_szsh（半年度报告）
    CATEGORY = 'category_ndbg_szsh;'
    URL = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3029.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    MAX_PAGESIZE = 50
    MAX_RELOAD_TIMES = 5
    RESPONSE_TIMEOUT = 10
    pass

    @classmethod
    # 参数：页面id(每页条目个数由MAX_PAGESIZE控制)，是否返回总条目数(bool)
    def get_response(page_num, return_total_count=False):
        query = {
            'stock': '',
            'searchkey': '',
            'plate': PLATE,
            'category': CATEGORY,
            'trade': '',
            'column': 'szse',  # 注意沪市为sse
            #        'columnTitle': '历史公告查询',
            'pageNum': page_num,
            'pageSize': MAX_PAGESIZE,
            'tabName': 'fulltext',
            'sortName': '',
            'sortType': '',
            'limit': '',
            'showTitle': '',
            'seDate': START_DATE + '~' + END_DATE,
        }
        result_list = []
        reloading = 0
        while True:
            #        reloading += 1
            #        if reloading > MAX_RELOAD_TIMES:
            #            return []
            #        elif reloading > 1:
            #            __sleeping(random.randint(5, 10))
            #            print('... reloading: the ' + str(reloading) + ' round ...')
            try:
                r = requests.post(URL, query, HEADER, timeout=RESPONSE_TIMEOUT)
            except Exception as e:
                print(e)
                continue
            if r.status_code == requests.codes.ok and r.text != '':
                break
        my_query = r.json()
        try:
            r.close()
        except Exception as e:
            print(e)
        if return_total_count:
            return my_query['totalRecordNum']
        else:
            for each in my_query['announcements']:
                file_link = 'http://static.cninfo.com.cn/' + str(
                    each['adjunctUrl'])
                file_name = __filter_illegal_filename(
                    str(each['secCode']) + str(each['secName']) + str(
                        each['announcementTitle']) + '.' + '(' + str(
                        each['adjunctSize']) + 'k)' +
                    file_link[-file_link[::-1].find('.') - 1:]  # 最后一项是获取文件类型后缀名
                )
                result_list.append([file_name, file_link])
            return result_list