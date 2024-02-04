# -*- coding: utf-8 -*-
# Created: 2024-01-23 18:05:55
# Last Modified: 2024-01-23 19:18:46
"""
https://www.jianshu.com/p/9de3be54abc1
"""

import requests
from bs4 import BeautifulSoup

url = "https://path.dirts.cn/tH0c47D2P"
url = "https://path.dirts.cn/suda/server/front/business/path"
head = """
fetch("https://path.dirts.cn/suda/server/front/business/path", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-AU;q=0.7,zh-TW;q=0.6",
    "authorization": "1ee2464b7a750097c77eb427969e4d4c",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://path.dirts.cn/tH0c47D2P",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
});
"""
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml')
    print(response.content)
    print(soup.contents)
    print(soup.a)
