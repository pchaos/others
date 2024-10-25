# -*- coding: utf-8 -*-
"""
   File Name：     test_genTABHTML
   Description :  tab css style test
   Author :       pchaos
   Last Modified: 2024-10-25 17:22:43
   date：          2019/9/9
"""
import time

try:
    from rich import print
except Exception as e:
    print(f"Not found package : rich. Please using pip install:\npip install rich")

import unittest
from unittest import TestCase

from .genTabHTML import genTABHTML


class TestGenTABHTML(TestCase):
    def test_genHTML(self):
        # 需要生成的文件名list。模板文件为：template.html，模板数据文件名为：需要生成的文件名+".ini"
        flist = ["main.htm", "main_tech.htm", "hacker.html"]

        # inifile = '{}.ini'.format(flist[0])
        renderList = []
        for fn in flist:
            inifile = "{}.ini".format(fn)
            gh = genTABHTML()
            # gh.outputFilename = fn
            gh.outputFilename = "test"
            gh.iniFilename = inifile
            try:
                templateFile = "customHTML/template.tab.table.html"
                of, render = gh.genHTML(None, title=fn.split(".")[0], prettify=False, template=templateFile)
            except Exception as e:
                templateFile = "template.tab.table.html"
                print(f"{e} something error with {inifile}")
                time.sleep(1)
                of, render = gh.genHTML(None, title=fn.split(".")[0], prettify=False, template=templateFile)
            print("输出文件完成 {}".format(of))
            # print(render)
            self.assertTrue(len(render) > 100)
            renderList.append(render)
        print(renderList)
        # main
        inifile = "{}.ini".format(flist[0])
        gh = genTABHTML()
        # gh.outputFilename = fn
        gh.iniFilename = inifile
        try:
            templateFile = "template.tab.html"
            render = gh.renders(renderList, prettify=True, template=templateFile, title="Main")
        except Exception as e:
            templateFile = "customHTML/template.tab.html"
            print(f"{e} something error with {inifile}")
            time.sleep(1)
            render = gh.renders(renderList, prettify=True, template=templateFile, title="Main")
        saveText = ""
        for r in render:
            saveText += r
        gh.save("main.htm", saveText)
        print("输出文件完成 {}".format(render))
        print(f"{flist} saved in main.htm")


class TestGenPchaosGitIo(TestCase):
    def test_genHTML(self):
        # 需要生成的文件名list。模板文件为：template.html，模板数据文件名为：需要生成的文件名+".ini"
        flist = [
            "k15.index.html",
            "xiaoxue_enhanced.html",
        ]

        renderList = []
        for fn in flist:
            if ".ini" in fn:
                inifile = "{}".format(fn)
            else:
                inifile = "{}.ini".format(fn)
            gh = genTABHTML()
            gh.outputFilename = "test"
            gh.iniFilename = inifile
            gh.numPerLine = 5
            try:
                templateFile = "customHTML/template.tab.table.html"
                of, render = gh.genHTML(None, title=fn.split(".")[0], prettify=False, template=templateFile)
            except Exception as e:
                templateFile = "template.tab.table.html"
                print(f"{e} something error with {inifile}")
                time.sleep(1)
                of, render = gh.genHTML(None, title=fn.split(".")[0], prettify=False, template=templateFile)
            print("输出文件完成 {}".format(of))
            # print(render)
            self.assertTrue(len(render) > 100)
            renderList.append(render)

        print(f"{len(renderList)=}")
        gh = genTABHTML()
        gh.iniFilename = inifile
        try:
            templateFile = "template.tab.script.html"
            render = gh.renders(renderList, prettify=True, template=templateFile, title="Education")
        except Exception as e:
            templateFile = "customHTML/template.tab.script.html"
            print(f"{e} something error with {inifile}")
            time.sleep(1)
            render = gh.renders(renderList, prettify=True, template=templateFile, title="Education")
        saveText = ""
        for r in render:
            saveText += r
        gh.save("index.html", saveText)
        print("输出文件完成 {}".format(render))
        print(f"{flist} saved in main.htm")

    def test_genHTML_phone(self):
        # 需要生成的文件名list。模板文件为：template.html，模板数据文件名为：需要生成的文件名+".ini"
        flist = [
            "k15.index.html",
            "xiaoxue_enhanced.html",
        ]

        renderList = []
        for fn in flist:
            if ".ini" in fn:
                inifile = "{}".format(fn)
            else:
                inifile = "{}.ini".format(fn)
            gh = genTABHTML()
            gh.outputFilename = "test_phone"
            gh.iniFilename = inifile
            gh.numPerLine = 2
            try:
                templateFile = "customHTML/template.tab.table.phone.html"
                of, render = gh.genHTML(
                    None, title=fn.split(".")[0], prettify=False, template=templateFile, numPerLine=gh.numPerLine
                )
            except Exception as e:
                templateFile = "template.tab.table.phone.html"
                print(f"{e} something error with {inifile}")
                time.sleep(1)
                of, render = gh.genHTML(
                    None, title=fn.split(".")[0], prettify=False, template=templateFile, numPerLine=gh.numPerLine
                )
            print("输出文件完成 {}".format(of))
            # print(render)
            self.assertTrue(len(render) > 100)
            renderList.append(render)

        print(f"{len(renderList)=}")
        gh = genTABHTML()
        gh.iniFilename = inifile
        try:
            templateFile = "template.tab.script.phone.html"
            render = gh.renders(renderList, prettify=True, template=templateFile, title="K15教育")
        except Exception as e:
            templateFile = "customHTML/template.tab.script.phone.html"
            print(f"{e} something error with {inifile}")
            time.sleep(1)
            render = gh.renders(renderList, prettify=True, template=templateFile, title="K15教育")
        saveText = ""
        for r in render:
            saveText += r
        gh.save("index_phone.html", saveText)
        print("输出文件完成 {}".format(render))
        print(f"{flist} saved in main.htm")


if __name__ == "__main__":
    unittest.main()
