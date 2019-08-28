# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     genHTML
   Description :
   Author :       pchaos
   date：          2019/8/28
-------------------------------------------------
   Change Activity:
                   2019/8/28:
-------------------------------------------------
"""
__author__ = 'pchaos'

from bs4 import BeautifulSoup

flist = ["hacker.html"]
for fn in flist:
	with open('{}.ini'.format(fn), "r") as f:
		fnini = f.read()

	alist = fnini.split("\n")
	for a in alist:
		# print(a.split("||"))
		ddcit = {}
		dlist = []
		try:
			d = {"text": "", "href": ""}
			t, h = a.split("||")
			d["text"] = t
			d["href"] = h
		except Exception as e:
			pass
		dlist.append(d)

		# print(dlist.keys(), dlist.values())
		for d in dlist:
			print(d)
			print(d["text"], d["href"])
