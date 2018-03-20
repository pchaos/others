# -*- coding: utf-8 -*-
"""
Created on 2016-10-28

@author: chaos
"""
from unittest import TestCase

import sys
import os
import tempfile

from genzztj.zztgen import ZZTGEN
import logging

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class TestZZTGEN(TestCase):
    '''
    测试谷为陵的博客： http://blog.sina.com.cn/s/articlelist_1414927881_0_1.html

    '''
    # todo 第一次运行测试的时候总是会报错。
    theTarget = None
    mainurl = None

    def setUp(self):
        self.mainurl = ['zztj.json']
        self.theTarget = ZZTGEN(self.mainurl)
        #如果存在index文件，则先删除
        fn = self.theTarget.getFilePath('index', self.theTarget.getMainPath()) + '.html'
        if os.path.isfile(fn):
            os.remove(fn)

    def tearDown(self):
        self.theTarget = None

    def test_getUserAgent(self):
        ag = self.theTarget.getUserAgent()
        self.assertFalse(ag is None, "can't  get user agent")

    def test_getTemplate(self):
        self.fail()

    def test_getFilePath(self):
        self.fail()

    def test_getTitle(self):
        self.fail()

    def test_getMainBody(self):
        self.fail()

    def test_cleanrubbish(self):
        self.fail()

    def test_getImage(self):
        '''
        博客
        :return:
        '''
        # 本次抓取没有图片
        self.fail()

    def test__getTitleTag(self):
        self.fail()

    def test_getarticle(self):
        '''
        测试获取所有博文

        :return:
        '''

        def getFilelist(path='./'):
            """
            目录对应的文件列表，不包含目录
            :param path:
            :return: 返回目录对应的文件列表
            """
            from os import listdir
            from os.path import isfile, join

            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            return onlyfiles

        urlStartnum = 0
        articleStartnum = 0
        thepath = os.path.join(tempfile.gettempdir(), 'zztj')
        articleList = self.theTarget.getarticleList()
        for a in articleList[articleStartnum::]:
            logging.info('articleList: {0}'.format(a.text))
            saveCharset = 'GB2312'
            # if (len(a['href']) > len('http://blog.sina.com.cn/s/')) and (len(a['href']) > len('http://blog.sina.com.cn/lm/finance/')):
            title = self.theTarget.getlocalarticle(a['href'], thepath, saveCharset)
            file_ext = ".html"
            b = a
            b['href'] = title + file_ext
            for comment in b:
                fixed_text = comment.replace(comment, title)
                comment.replace_with(fixed_text)
            logging.info('change href: {0}'.format(b))
            # else:
            #
            #     a = None

        self.assertEqual(len(articleList), len(getFilelist(thepath)),
            'test fail,articleList:{0}, saveFile:{1}'.format(len(articleList),len(getFilelist(thepath))))

        # 保存index文件
        indexfn = self.theTarget.getFilePath('index', self.theTarget.getMainPath())
        self.theTarget.saveToFile(indexfn,
                                  self.theTarget.alterMainIndex(articleList, self.theTarget.indexTitle, self.theTarget.copyRight))

    def test_getarticleList(self):
        # method one
        articleList = []
        for a in self.mainurl:
            articleList.extend(self.theTarget.getarticleList(a))
        log.debug('test_getarticleList:{0}'.format(articleList))
        self.assertFalse(articleList is None, 'articleList is None')
        # method two
        articleList1 = self.theTarget.getarticleList(self.mainurl)
        self.assertTrue(articleList1 == articleList, 'articleList not equals!')
        log.debug(articleList1)

    def test_saveToFile(self):
        # 保存index.html
        articleList = self.theTarget.getarticleList(self.mainurl)
        fn = self.theTarget.getFilePath('index', self.theTarget.getMainPath())
        self.theTarget.saveToFile(fn,
                                  self.theTarget.alterMainIndex(articleList, self.theTarget.indexTitle, self.theTarget.copyRight))
        fn = fn + '.html'
        self.assertTrue(os.path.isfile(fn),
                                   'file Not Exits:{0}'.format(fn))

    def test_alterMainIndex(self):
        self.fail()

    def test_alterArticalContents(self):
        self.fail()

    def test_all(self):
        a=1
