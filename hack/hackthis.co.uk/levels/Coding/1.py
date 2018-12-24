# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     1.py
   Description :
   Author :       pchaos
   date：          18-12-20
-------------------------------------------------
   Change Activity:
                   18-12-20:
-------------------------------------------------
"""
__author__ = 'pchaos'

import requests
import os, errno
from dotenv import load_dotenv

def getLoginEnv():
    '''
    从环境变量获取用户名、密码
    :return:
    '''

    def loadEnv(envFileName="../config.env"):
        load_dotenv(envFileName)

    username = 1
    if "username" in os.environ:
        username = os.getenv('username', 'username not set')
    else:
        print('请先 export username， password')
    if "password" in os.environ:
        password = os.getenv('password', 'password not set')

    if not isinstance(username, str):
        loadEnv()
        return getLoginEnv()
    return username, password


def auth():
    url = "https://www.hackthis.co.uk/?login"
    sess = requests.Session()
    # enter username and password
    username, password= getLoginEnv()
    data = {
        "username": username,
        "password": password,
    }
    # auth
    sess.post(url, data=data)
    return sess


def one():
    sess = auth()
    res = sess.get("https://www.hackthis.co.uk/levels/coding/1")
    html = res.content.decode("utf-8")
    start = html.find("<textarea")
    end = html.find("</textarea")
    parts = html[start:end].replace("<textarea>", "")
    items = filter(None, [i.strip() for i in parts.split(",")])
    ans = ", ".join(sorted(items))
    data = {"answer": ans}
    res = sess.post("https://www.hackthis.co.uk/levels/coding/1", data=data)
    print(res)


def two():
    sess = auth()
    res = sess.get("https://www.hackthis.co.uk/levels/coding/2")
    html = res.content.decode("utf-8")
    start = html.find("<textarea")
    end = html.find("</textarea")
    parts = html[start:end].replace("<textarea>", "")
    # items = filter(None, [str(i).strip() for i in parts.split(",")])
    txt = ""
    for i in parts.split(","):
        # print i
        try:
            txt = txt + chr(126 - int(i))
        except ValueError:
            txt = txt + " "
    txt = txt.lower()
    data = {"answer": txt}
    res = sess.post("https://www.hackthis.co.uk/levels/coding/2", data=data)
    print(res)


if __name__ in "__main__":
    one()
    # two()
