# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_genTABHTML
   Description :  tab css style test
   Author :       pchaos
   date：          2019/9/9
-------------------------------------------------
   Change Activity:
                   2019/9/9:
-------------------------------------------------
"""
from unittest import TestCase
from .genTabHTML import genTABHTML


class TestGenTABHTML(TestCase):
	def test_genHTML(self):
		# 需要生成的文件名list。模板文件为：template.html，模板数据文件名为：需要生成的文件名+".ini"
		flist = ["main.htm", "main_tech.htm", "hacker.html"]

		# inifile = '{}.ini'.format(flist[0])
		inifile = '{}.ini'.format(flist[0])
		for fn in flist:
			gh = genTABHTML()
			# gh.outputFilename = fn
			gh.iniFilename = inifile
			of, render = gh.genHTML("a{}".format(fn),
			                        prettify=False,
			                        template="customHTML/template.tab.table.html")
			print("完成 {}".format(of))
			print(render)
			self.assertTrue(len(render) > 100)
