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
            inifile = '{}.ini'.format(fn)
            gh = genTABHTML()
            # gh.outputFilename = fn
            gh.outputFilename = "test"
            gh.iniFilename = inifile
            try:
                templateFile = "customHTML/template.tab.table.html"
                of, render = gh.genHTML(None,
                                        # of, render = gh.genHTML("a{}".format(fn),
                                        title=fn.split(".")[0],
                                        prettify=False,
                                        template=templateFile)
            except Exception as e:
                templateFile = "template.tab.table.html"
                of, render = gh.genHTML(None,
                                        # of, render = gh.genHTML("a{}".format(fn),
                                        title=fn.split(".")[0],
                                        prettify=False,
                                        template=templateFile)
            print("输出文件完成 {}".format(of))
            # print(render)
            self.assertTrue(len(render) > 100)
            renderList.append(render)
        print(renderList)
        # main
        inifile = '{}.ini'.format(flist[0])
        gh = genTABHTML()
        # gh.outputFilename = fn
        gh.iniFilename = inifile
        try:
            templateFile = "template.tab.html"
            render = gh.renders(renderList,
                                prettify=True,
                                # template="customHTML/template.tab.html",
                                template=templateFile,
                                title="Main")
        except Exception as e:
            templateFile = "customHTML/template.tab.html"
            render = gh.renders(renderList,
                                prettify=True,
                                # template="customHTML/template.tab.html",
                                template=templateFile,
                                title="Main")
        saveText = ""
        for r in render:
            saveText += r
        gh.save('main.htm', saveText)
        print("输出文件完成 {}".format(render))


if __name__ == '__main__':
    unittest.main()
