# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     genIni
   Description :  将HTML文件转换成网址ini文件
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
		outputFile = '{}.ini'.format(fn)
		with open(outputFile, "w+") as fw:
			blankLine = False # 判断是否重复输出空行多个空行输出只输出一行空行
			for a in soup.find_all('a', href=True):
				print(a['href'], a.text)
				if len(a['href']) > 5:
					fw.write("{}{}{}\n".format(a.text, "||", a['href']))
					blankLine = False
				else:
					if not blankLine:
						fw.write("\n")
						blankLine = True
		print("输出文件:{}".format(outputFile))