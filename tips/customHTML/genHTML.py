# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     genHTML
   Description : 从配置ini文件中生成
   Author :       pchaos
   date：          2019/8/28
-------------------------------------------------
   Change Activity:
                   2019/8/28:
-------------------------------------------------
"""
__author__ = 'pchaos'

from bs4 import BeautifulSoup
import jinja2

dlist = []
flist = ["hacker.html"]
for fn in flist:
	with open('{}.ini'.format(fn), "r") as f:
		fnini = f.read()

	alist = fnini.split("\n")
	for a in alist:
		# print(a.split("||"))
		ddict = {}

		try:
			item = {"caption": "", "href": ""}
			t, h = a.split("||")
			item["caption"] = t
			item["href"] = h
		except Exception as e:
			pass
		ddict.update(dlist)
		dlist.append(item)

		# print(dlist.keys(), dlist.values())
		# for item in dlist:
		# 	print(item)
		# 	print(item["caption"], item["href"])

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(title="HACKER", sites=dlist)  # this is where to put args to the template renderer

with open('/tmp/{}'.format(fn), "w+") as f:
	f.write(outputText)
