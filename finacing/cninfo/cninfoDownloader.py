# coding = utf-8
# __author__='Lilly'
# description:下载csv中列出的pdf年报

import csv
import os
import time
import re
import requests
from os import sys, path

# __file__ should be defined in this case
PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(PARENT_DIR)
from cninfo.cninfoScrab import get_output_csv_file, read_zxg, standardize_dir

# 每个文件最多出错几次
MAX_COUNT = 3
DST_DIR = '/tmp/report/'
# LIST_FILE = '/tmp/2019年/201农业上市企业信息_20020206-20180417.csv'
LIST_FILE = get_output_csv_file()


def download_anance():
    global DST_DIR
    standardize_dir(DST_DIR)
    assert (os.path.exists(
        DST_DIR)), 'No such destination directory \"' + DST_DIR + '\"!'
    assert (
        os.path.exists(LIST_FILE)), 'No such list file \"' + LIST_FILE + '\"!'
    if DST_DIR[len(DST_DIR) - 1] != '/':
        DST_DIR += '/'
    # 读取待下载文件列表
    with open(LIST_FILE, 'r') as csv_in:
        reader = csv.reader(csv_in)
        for each in enumerate(reader):
            download_count = 1
            download_token = False
            downloaded = False
            url = each[1][2]
            fname = adjustFileName(each[1][1])
            if int(each[1][3]) > 0 and canDownload(fname):
                # 下载标志 并且满足下载条件
                pass
            else:
                continue
            ind = each[0] + 1
            while download_count <= MAX_COUNT:
                try:
                    if os.path.exists(os.path.join(DST_DIR, fname)):
                        # 已经保存过
                        downloaded = True
                        break
                    download_count += 1
                    r = requests.get(url)
                    download_token = True
                    break
                except:
                    # 下载失败则报错误
                    print(
                        str(ind) + '::' + str(download_count) + ':\"' +
                        fname + '\" failed!')
                    download_token = False
                    time.sleep(2)
            if downloaded:
                # 已经保存过
                print(
                    str(ind) + ': already \"' + fname + '\" downloaded before.')
                continue
            if download_token:
                # 下载成功则保存
                with open(os.path.join(DST_DIR, fname), 'wb') as file:
                    file.write(r.content)
                    print(str(ind) + ': \"' + fname + '\" downloaded.')
            else:
                # 彻底下载失败则记录日志
                with open(DST_DIR + 'error.log', 'a') as log_file:
                    log_file.write(
                        time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(
                            time.time())) + 'Failed to download\"' +
                        fname + '\"\n')
                    print('...' + str(
                        ind) + ':\"' + fname + '\" finally failed ...')


def adjustFileName(filename):
    flen = len(filename)
    maxlen = 100
    if flen < maxlen:
        return filename
    else:
        # print('{} 长度： {}'.format(len(fname), fname))
        fsur = filename[-filename[::-1].find('.') - 1:]
        return filename[:(maxlen - len(fsur))] + fsur.lower()


def canDownload(filename):
    reg_exp = re.compile(r'\d{8}')
    mat = re.findall(reg_exp, filename)
    if mat:
        if len(mat) > 0:
            # 大于2017年
            if mat[0] > '20170101':
                return True
    # 首次公开发行股票
    reg_exp = re.compile('首次公开发行股票')
    mat = re.findall(reg_exp, filename)
    if mat:
        if len(mat) > 0:
            return True
    return False
