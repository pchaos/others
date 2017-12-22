#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author: Sky
# Time: 2017/7/16 09:57
# File: GetChinaDomainFroCensys.py
# https://threathunter.org/topic/596aebf1dff9e14c40b6193f

import requests
import json


class Attract(object):
    def __init__(self):
        self.runNum = 0
        self.results = []

    # 模块信息
    Info = {
        "name": "GetChinaDomainFroCensys",
        "author": "@iiusky",
        "create_time": "2017年07月07日",
        "description": "使用Censys API在查找中国域名",
        "API_ID": "appid",
        "Secret": "Secret",
        "API_URL": "https://www.censys.io/api/v1"
    }

    def __search(self, ):
        """
        Censys核心运行模块,如果有分页内容，就进行分页循环取，否则只取第一页
        如果运行中出错，则重新开始运行
        """
        try:
            jsonContent = self.__getRes()
            if jsonContent['metadata']['pages'] > 1:
                for page in range(2, jsonContent['metadata']['pages'] + 1):
                    self.__contentResolve(self.__getRes(page=page))
            else:
                self.__contentResolve(self.__getRes())

        except Exception as e:
            print(e)
            self.results = []
            if self.runNum < 3:
                self.runNum += 1
                self.__search()

    def __contentResolve(self, jsonContent):
        """
        :param jsonContent: json格式
        """
        for item in range(len(jsonContent['results'])):
            self.results.append(jsonContent['results'][item]['domain'])

    def __getRes(self, page=1):
        """
        获取网页包内容
        :param page: int(default=1)
        :return: json
        """
        query = {
            'query': 'location.country: China',
            'page': page,
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        res = requests.post(self.Info['API_URL'] + "/search/websites",
                            auth=(self.Info['API_ID'], self.Info['Secret']), json=query, headers=headers)
        if res.status_code == 200 and res.json()['status'] == 'ok':
            return res.json()

    def run(self):
        """
        运行该模块,并返回一个去重后的列表
        :return: list
        """
        self.__search()
        return list(set(self.results))


if __name__ == '__main__':
    print(json.dumps(Attract().run()))
