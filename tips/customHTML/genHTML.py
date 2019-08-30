# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     genHTML
   Description : 从配置ini文件中生成用户主页
   Author :       pchaos
   date：          2019/8/28
-------------------------------------------------
   Change Activity:
                   2019/8/28:
-------------------------------------------------
"""
__author__ = 'pchaos'

import os
from bs4 import BeautifulSoup
import jinja2


class genHTML():

	def __init__(self):
		self.__outputDir = '/tmp/'
		self.dlist = []
		self.__outputFilename = ""
		self.__iniFilename = ""

	@property
	def iniFilename(self):
		return self.__iniFilename

	@iniFilename.setter
	def iniFilename(self, value):
		self.__iniFilename = value

	@property
	def outputFilename(self):
		return self.__outputFilename

	@outputFilename.setter
	def outputFilename(self, value):
		if value != self.__outputFilename:
			self.__outputFilename = value
			self.iniFilename = "{}.ini".format(value)

	def getSource(self, iniFile=""):
		if iniFile == "":
			iniFile = self.iniFilename
		if not os.path.exists(inifile):
			print("文件不存在：{}".format(inifile))
			return []
		# 读取
		with open(inifile, "r") as f:
			fnini = f.read()
		dlist = []
		alist = fnini.split("\n")
		i = 0
		for a in alist:
			try:
				item = {"caption": "", "href": ""}
				t, h = a.split("||")
				item["caption"] = t
				item["href"] = h
				dlist.append(item)
				i += 1
			except Exception as e:
				print("warning !! {} 不能转换为dictionary, 使用默认{}".format(a, item))
				# 读取空行 自动填充空数据至数据个数能被5整除
				for j in range(5):
					if i % 5 > 0:
						dlist.append(item)
						i += 1
					else:
						break

		return dlist

	def genHTML(self, filename=""):
		if len(filename) == 0 and self.outputFilename == "":
			print("需要设置输出文件名! ")
			return None
		self.outputFilename = filename
		dlist = self.getSource()
		if len(dlist) == 0:
			print("文件{}无数据".format(self.outputFilename))
			return None
		templateLoader = jinja2.FileSystemLoader(searchpath="./")
		templateEnv = jinja2.Environment(loader=templateLoader)
		TEMPLATE_FILE = "template.html"
		template = templateEnv.get_template(TEMPLATE_FILE)
		outputText = template.render(title="HACKER",
		                             sites=dlist)  # this is where to put args to the template renderer

		wfile = os.path.join(self.__outputDir, filename)
		with open(wfile, "w+") as f:
			f.write(outputText)
		return wfile


if __name__ == '__main__':
	# 需要生成的文件名list。模板文件为：template.html，模板数据文件名为：需要生成的文件名+".ini"
	flist = ["hacker.html"]

	for fn in flist:
		inifile = '{}.ini'.format(fn)
		gh = genHTML()
		# gh.outputFilename = fn
		of = gh.genHTML(fn)
		print("完成 {}".format(of))
