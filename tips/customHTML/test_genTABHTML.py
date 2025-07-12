# -*- coding: utf-8 -*-
"""
File Name：     test_genTABHTML
Description :  tab css style test
Author :       pchaos
Last Modified: 2025-07-12 22:03:58
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
        flist = ["main.htm", "main_tech.htm", "tech_hardware.html", "hacker.html"]

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
    def setUp(self) -> None:
        self.flist = [
            "k6.html",
            "k6A.html",
            "k9.html",
            "k0.html",
            "k12.html",
        ]

    def test_genHTML(self):
        # 需要生成的文件名list。模板文件为：template.html，模板数据文件名为：需要生成的文件名+".ini"
        flist = self.flist
        renderList = []
        for fn in flist:
            if ".ini" in fn:
                inifile = "{}".format(fn)
            else:
                inifile = "{}.ini".format(fn)
            gh = genTABHTML()
            gh.outputFilename = "test"
            gh.iniFilename = inifile
            gh.numPerLine = 4
            try:
                templateFile = "customHTML/template.tab.table.html"
                of, render = gh.genHTML(
                    None, title=fn.split(".")[0], prettify=False, template=templateFile, numPerLine=gh.numPerLine
                )
            except Exception as e:
                templateFile = "template.tab.table.html"
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
        # print("输出文件完成 {}".format(render))
        print(f"{flist} saved in index.html")

    def test_genHTML_phone(self):
        # 需要生成的文件名list。模板文件为：template.html，模板数据文件名为：需要生成的文件名+".ini"
        flist = self.flist
        renderList = []
        for fn in flist:
            if fn.endswith(".ini"):
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
            render = gh.renders(renderList, prettify=True, template=templateFile, title="K12教育")
        except Exception as e:
            templateFile = "customHTML/template.tab.script.phone.html"
            print(f"{e} something error with {inifile}")
            time.sleep(1)
            render = gh.renders(renderList, prettify=True, template=templateFile, title="K12教育")
        saveText = ""
        for r in render:
            saveText += r
        gh.save("index_phone.html", saveText)
        # print("输出文件完成 {}".format(render))
        print(f"{flist} saved in index_phone.html")


class TestUnGenHTML(TestCase):
    """从 HTML 文件中提取 URL 和文本

    pytest -v -s test_genTABHTML.py::TestUnGenHTML > /tmp/url.txt
    """

    def test_unGenHTML(self):
        from bs4 import BeautifulSoup

        # 读取 HTML 文件
        with open('/tmp/index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 提取所有链接及其文本
            url_text_pairs = []
            for link in soup.find_all('a'):
                url = link.get('href')
                text = link.text.strip()
                url_text_pairs.append((text, url))

            # 打印提取的 URL 和对应文本
            for text, url in url_text_pairs:
                print(f'{text}||URL: {url}')


if __name__ == "__main__":
    unittest.main()
