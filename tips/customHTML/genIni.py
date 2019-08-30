# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     genIni
   Description :
   Author :       pchaos
   date：          2019/8/30
-------------------------------------------------
   Change Activity:
                   2019/8/30:
-------------------------------------------------
"""
from bs4 import BeautifulSoup

flist = ["hacker.html"]
for fn in flist:
	with open(fn, "r") as f:

		contents = f.read()

		soup = BeautifulSoup(contents, 'lxml')
		with open('{}.ini'.format(fn), "w+") as fw:
			for a in soup.find_all('a', href=True):
				print(a['href'], a.text)
				fw.write("{}{}{}\n".format(a.text, "||", a['href']))