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

	def getRealFileName(self, filename):
		fx1 = os.path.exists(os.path.join(os.path.realpath("./"), filename))
		fx2 = os.path.exists(
			os.path.join(os.path.realpath("./customHTML"), filename))
		if ((not fx1 and not fx2) or len(filename) == 0):
			print(
				"文件不存在：{}".format(
					os.path.join(os.path.realpath("./"), filename)))
			return None
		# 读取
		if fx1:
			filename = os.path.join(os.path.realpath("./"), filename)
		else:
			if fx2:
				filename = os.path.join(os.path.realpath("./customHTML"),
				                        filename)
		return filename

	def getSource(self, iniFile=""):
		if iniFile == "":
			iniFile = self.iniFilename
		iniFile = self.getRealFileName(iniFile)

		with open(iniFile, "r") as f:
			fnini = f.read()
		dlist = []
		alist = fnini.split("\n")
		i = 0
		for a in alist:
			try:
				item = {"caption": "", "href": ""}
				t, h = a.split("||")
				if t.startswith(";"):
					# 该行为注释
					continue
				item["caption"] = t
				item["href"] = h
				lh, lt = len(h), len(t)
				if (lh + lt) > 0 and (lh == 0 or lt == 0):
					# 非空行，转换后其中一个长度为零
					print("warning !! {} 不能转换为dictionary, 忽略".format(a))
					continue
				dlist.append(item)
				i += 1
			except Exception as e:
				print("warning !! 空行, 使用默认 {}".format(item))
				# 读取空行 自动填充空数据至数据个数能被5整除
				for j in range(5):
					if i % 5 > 0:
						dlist.append(item)
						i += 1
					else:
						break
		# 最终添加的元素长度排成五列
		item = {"caption": "", "href": ""}
		while len(dlist) % 5 > 0:
			dlist.append(item)
		return dlist

	def genHTML(self, outputFilename=None, title="", prettify=True,
	            template="template.html"):
		filename = "" if outputFilename is None else outputFilename
		if len(filename) == 0 and self.outputFilename == "":
			print("需要设置输出文件名! ")
			return None, None
		else:
			if len(filename) > 0:
				self.__outputFilename = filename
		dlist = self.getSource()
		if len(dlist) == 0:
			print("文件{}无数据".format(self.outputFilename))
			return None, None
		if title == "":
			title = self.capitalize_first_last_letters(filename.split(".")[0])
		render = self.renders(dlist, prettify, template, title)
		return self.save(outputFilename, render)

	def save(self, outputFilename=None, render=""):
		if outputFilename is not None:
			wfile = os.path.join(self.__outputDir, outputFilename)
			with open(wfile, "w+") as f:
				f.write(render)
			return wfile, render
		else:
			if self.outputFilename is not None:
				return self.save(self.outputFilename, render)
			else:
				# 不写到文件
				return None, render

	def renders(self, dlist, prettify, template, title):
		templateLoader = jinja2.FileSystemLoader(searchpath="./")
		templateEnv = jinja2.Environment(loader=templateLoader)
		# template = self.getRealFileName(template)
		template = templateEnv.get_template(template)

		render = template.render(title=title,
		                         sites=dlist)  # this is where to put args to the template renderer
		if prettify:
			# 美化显示
			soup = BeautifulSoup(render, "lxml")
			render = soup.prettify()
		return render

	@classmethod
	def capitalize_first_last_letters(cls, str1):
		# 首字符大写
		return str1.capitalize()


if __name__ == '__main__':
	# 需要生成的文件名list。模板文件为：template.html，模板数据文件名为：需要生成的文件名+".ini"
	flist = ["main.htm", "main_tech.htm", "hacker.html"]

	for fn in flist:
		inifile = '{}.ini'.format(fn)
		gh = genHTML()
		# gh.outputFilename = fn
		gh.iniFilename = inifile
		of, _ = gh.genHTML(fn)
		print("完成 {}".format(of))
