# coding = utf-8
''' 巨潮资讯网-爬取公告对应的下载地址

'''
import csv
import math
import os
import time
import requests
import re
import pandas as pd

START_DATE = '1990-01-01'  # 搜索的起始日期
END_DATE = str(time.strftime('%Y-%m-%d'))  # 默认当前提取，可设定为固定值
OUT_DIR = '{}tmp{}2019年'.format(os.sep, os.sep)
OUTPUT_FILENAME = '2019年度报告'
# 板块类型：沪市：shmb；深市：szse；深主板：szmb；中小板：szzx；创业板：szcy；
PLATE = 'szse;'
# 公告类型：category_scgkfx_szsh（首次公开发行及上市）、category_ndbg_szsh（年度报告）、category_bndbg_szsh（半年度报告）
# CATEGORY = 'category_ndbg_szsh;'
CATEGORY = ''

url = 'http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum=1'
# http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum=1&pageSize=500
url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
MAX_PAGESIZE = 50
MAX_RELOAD_TIMES = 5
RESPONSE_TIMEOUT = 10


def standardize_dir(dir_str):
    # assert (os.path.exists(dir_str)), 'Such directory \"' + str(dir_str) + '\" does not exists!'
    if not os.path.exists(dir_str):
        os.makedirs(dir_str)
    if dir_str[len(dir_str) - 1] != os.sep:
        return dir_str + os.sep
    else:
        return dir_str


# 参数：页面id(每页条目个数由MAX_PAGESIZE控制)，是否返回总条目数(bool)
def get_response(url, page_num, return_total_count=False, stock_code=''):
    query = {
        'stock': stock_code,
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
            r = requests.post(url, query, HEADER, timeout=RESPONSE_TIMEOUT)
        except Exception as e:
            print(e)
            time.sleep(0.5)
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
            announcementId = str(each['announcementId'])
            file_link = 'http://static.cninfo.com.cn/' + str(each['adjunctUrl'])
            # 其他格式匹配. 如2016-12-24与2016/12/24的日期格式.
            date_reg_exp = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}')
            mat = re.search(date_reg_exp, each['adjunctUrl'])
            if mat:
                # 发布日期
                aDate = mat.group(0)
            else:
                aDate = ''
            aDate = '-{}'.format(aDate.replace('-', ''))
            file_name = __filter_illegal_filename(
                str(each['secCode']) + str(each['secName'])
                + aDate
                + str(each['announcementTitle']) + '(' + str(
                    each['adjunctSize']) + 'k)' +
                file_link[-file_link[::-1].find('.') - 1:]  # 最后一项是获取文件类型后缀名
            )
            # if len(file_name) > 100:
            #     file_name = __filter_illegal_filename(
            #         str(each['secCode']) + str(each['secName'])
            #         + aDate
            #         + str(each['announcementTitle'])
            #         + file_link[-file_link[::-1].find('.') - 1:]  # 最后一项是获取文件类型后缀名
            #     )
            result_list.append([announcementId, file_name, file_link])
        return result_list


def __log_error(err_msg):
    err_msg = str(err_msg)
    print(err_msg)
    with open(error_log, 'a', encoding='gb18030') as err_writer:
        err_writer.write(err_msg + '\n')


def __filter_illegal_filename(filename):
    illegal_char = {
        ' ': '',
        '*': '',
        '/': '-',
        '\\': '-',
        ':': '-',
        '?': '-',
        '"': '',
        '<': '',
        '>': '',
        '|': '',
        '－': '-',
        '—': '-',
        '（': '(',
        '）': ')',
        'Ａ': 'A',
        'Ｂ': 'B',
        'Ｈ': 'H',
        '，': ',',
        '。': '.',
        '：': '-',
        '！': '_',
        '？': '-',
        '“': '"',
        '”': '"',
        '‘': '',
        '’': '',
        '《': '_',
        '》': ''
    }
    for item in illegal_char.items():
        filename = filename.replace(item[0], item[1])
    return filename


def read_zxg(fname='zxg.txt'):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if not fname.find(os.sep) > -1:
        fname = os.path.join(dir_path, fname)
    resultList = []
    if os.path.isfile(fname):
        with open(fname, 'r', encoding='UTF-8') as zxg:
            alist = zxg.readlines()
    for a in alist:
        resultList.append(a[0:6])
    return resultList

def read_zxg_filter(fname='zxgFilter.txt'):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if not fname.find(os.sep) > -1:
        fname = os.path.join(dir_path, fname)
    resultList = []
    if os.path.isfile(fname):
        with open(fname, 'r', encoding='UTF-8') as zxg:
            alist = zxg.readlines()
    for a in alist:
        if a.strip() > '':
            resultList.append(a.strip())
    return resultList


def get_cninfo(stockCode='', df=pd.DataFrame()):
    if stockCode[0] == '6':
        PLATE = 'shmb;'
    else:
        # 板块类型：沪市：shmb；深市：szse；深主板：szmb；中小板：szzx；创业板：szcy；
        PLATE = 'szse;'
    # 获取记录数、页数
    item_count = get_response(url, 1, True, stock_code=stockCode)
    assert (item_count != []), 'Please restart this script!'
    begin_pg = 1
    end_pg = int(math.ceil(item_count / MAX_PAGESIZE))
    print(
        'Page count: ' + str(end_pg) + '; item count: ' + str(item_count) + '.')
    time.sleep(0.5)
    resultList = []
    # 逐页抓取
    for i in range(begin_pg, end_pg + 1):
        row = get_response(url, i, stock_code=stockCode)
        if not row:
            __log_error('Failed to fetch page #' + str(i) +
                        ': exceeding max reloading times (' + str(
                MAX_RELOAD_TIMES) + ').')
            continue
        else:
            resultList.extend(row)
            last_item = i * MAX_PAGESIZE if i < end_pg else item_count
            print('Page ' + str(i) + '/' + str(
                end_pg) + ' fetched, it contains items: ('
                  + str(1 + (i - 1) * MAX_PAGESIZE) + '-'
                  + str(last_item) + ')/' + str(item_count) + '.')
            if len(df) > 0:
                # 是否已经下载过
                rowdf = pd.DataFrame(row)
                common = rowdf.merge(df, on=[1, 2])
                adf = rowdf[~rowdf.isin(common)].dropna()
                if len(rowdf) > len(adf):
                    # 有下载过的目录
                    break
        time.sleep(0.35)

    return resultList


def save_cninfo():
    codeList = read_zxg()
    # 初始化重要变量
    error_log = standardize_dir(OUT_DIR) + 'error.log'
    output_csv_file = get_output_csv_file()
    try:
        df = pd.read_csv(output_csv_file, header=None, usecols=[0, 1, 2, 3])
    except Exception as e:
        df = pd.DataFrame()
    # 原始长度
    orglen = len(df)
    adf = pd.DataFrame()
    for code in codeList:
        print(code)
        if len(code) != 6:
            print('股票代码长度错误：{} 长度：{}'.format(code, len(code)))
            continue
        alist = get_cninfo(stockCode=code, df=df)
        sublist = read_zxg_filter()
        for a in alist:
            if any(re.findall('|'.join(sublist), a[1])):
                a.append(1)
            else:
                a.append(0)
        # print(pd.DataFrame(alist))
        adf = pd.concat([adf, pd.DataFrame(alist)], ignore_index=True)
    # 新公告放在前面
    df = pd.concat([adf, df], ignore_index=True)
    df.drop_duplicates(subset=[1, 2], keep="last", inplace=True)
    df.sort_values(by =[1], ascending=False, inplace=True)
    if len(df) != orglen:
        df.to_csv(output_csv_file, index=False, header=False)
        print('{} saved.'.format(output_csv_file))


def get_output_csv_file():
    # 若本目录有OUTPUT_FILENAME，则优先使用本目录文件
    out_dir = os.path.dirname(os.path.abspath(__file__))
    filename = '{}.csv'.format(os.path.join(out_dir, OUTPUT_FILENAME))
    if os.path.exists(filename):
        return filename
    out_dir = standardize_dir(OUT_DIR)
    filename = '{}.csv'.format(os.path.join(out_dir, OUTPUT_FILENAME))
    return filename


if __name__ == '__main__' and __package__ is None:
    save_cninfo()
