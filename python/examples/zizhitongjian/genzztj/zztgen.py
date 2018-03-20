# -*- coding: utf-8 -*-
from os import path as path

from bs4 import BeautifulSoup
import tempfile
import logging
# from io import StringIO
import os.path as path
import os
import requests
# from PIL import Image
from time import sleep
import re
from jinja2 import Environment, FileSystemLoader
import json

# logging.basicConfig(
# level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d]
# %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
maindir = 'zztj'

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S')


class BASEGEN(object):
    """
    抓取网页基础类
    """

    thepath = None
    imagePath = 'img'
    imageMinSize = 1024 * 1
    myAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
    contentList = []

    def __init__(self, mainUrl, fileformat='json'):
        """

        :param mainUrl:
        :param fileformat: 可选 'json', 'html', 'csv'
        """
        if mainUrl is not None:
            self.mainUrl = mainUrl
        else:
            raise Exception('Input Error', 'Input must not be None!')

        self.thepath = os.path.join(tempfile.gettempdir(), '%s' % maindir)
        # 创建保存文件目录
        self.getFilePath('a', self.thepath)
        self.getFilePath('a', os.path.join(self.thepath, self.imagePath))
        self.getFilePath('a', self.thepath)

        if fileformat == 'json':
            # 当前目录
            currpath = os.getcwd()
            if type(mainUrl) == str:
                self.contentList.extend(self.loadjsonfile(self.getFilePath(mainUrl, currpath)))
            else:
                for url in mainUrl:
                    self.contentList += self.loadjsonfile(self.getFilePath(url, currpath))

    def loadjsonfile(self, filename):
        """
        读取json文件到contentList
        :param filename:
        :return: a list
        """
        with open(filename, 'r') as f:
            data = f.read()
        return json.loads(data)

    def getUserAgent(self, agent='Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'):
        user_agent = {'User-agent': agent}
        return user_agent

    def getFilePath(self, filename, folder='./zztj'):
        """
        判断目录foleder是否存在，不存在则创建目录，并切换为创建的目录
        :param folder:
        :return:
        """
        if not path.exists(folder):
            os.mkdir(folder)
            os.chdir(folder)
        return path.join(folder, filename)


class ZZTGEN(BASEGEN):
    '''
    通过本地json文件，产生html
    '''
    indexTitle = '《资治通鉴》'
    copyRight = '本文摘自www.sbkk88.com，整理： chaos，感谢： xxxx, mail: drifthua # gmail . com'

    # 图片最小尺寸，小与最小尺寸时，需要重新下载，大于该尺寸的图片不会重新自动下载

    def getTemplate(self, tplName='', templatesFolder='templates'):
        '''
        tplName 模版名称
        templatesFolder 模版路径 默认路径为：templates
        '''
        if len(tplName) == 0:
            tplName = 'index.html'
        # with open(file, 'r') as f:
        #     s = f.read()
        # todo 判断是否有templatesFolder目录
        env = Environment(loader=FileSystemLoader(templatesFolder))
        tpl = env.get_template(tplName)
        return tpl

    def getTitle(self, soup):
        '''
        取得标题
        '''
        global tilesContain
        # 从html格式中取得标题
        tt = soup.title.text.split('_')
        # ['教你炒股票30：缠中说禅理论的绝对性', 'ajiao99999', '新浪博客']
        if len(tt) > 0:
            return tt[0]
        # 从文章正文取得标题
        titles = tilesContain
        for a in soup.findAll('h2', {'class': 'titName SG_txta'}):
            for b in titles:
                matchObj = re.search(b, str(a))
                if matchObj:
                    return a.text
        return None

    def getTitle2(self, soup):
        '''
        取得副标题
        '''
        # 文章标题
        # t= soup.findAll('div', {'class': 'articalTitle'}).
        # if t is None:
        #     t = soup.findAll('div', {'class': 'BNE_title'})
        # 文章时间
        t2 = None
        for a in soup.findAll('span', {'class': 'SG_txtc'}):
            if a.parent.name == 'div':
                if t2 is None:
                    t2 = a
                else:
                    t2.append(a)

        # 标签 分类
        for b in soup.findAll('div', {'class': 'articalTag'}):
            if b.parent.name == 'div':
                if t2 is None:
                    t2 = b
                else:
                    t2.append(b)
        if len(soup.findAll('div', {'class': 'articalTag'})) == 0:
            for b in soup.findAll('div', {'class': 'tagbox'}):
                if b.parent.name == 'div':
                    if t2 is None:
                        t2 = b
                    else:
                        t2.append(b)
        return t2

    def getArticle_comment_list(self, soup):
        '''
        取得评论
        '''
        # 从文章正文取得标题
        al = None
        for a in soup.findAll('ul', {'class': 'com_list'}):
            if al is None:
                al = a
            else:
                al.append(a)
        return al

    def getMainBody(self, soup):
        '''
        三种情况获取博文主内容
        :param soup:
        :return:
        '''
        for b in soup.findAll('div', {'id': 'sina_keyword_ad_area2'}):
            return b

        for b in soup.findAll('div', {'class': 'BNE_main'}):
            matchObj = re.search("内容区", str(b))
            if matchObj:
                # for a in soup.findAll('div', {'class': 'BNE_cont'}):
                return b
        for b in soup.findAll('div', {'id': 'articlebody'}):
            return b

    def _delTag(self, body, delTAG, defaultTAG='div'):
        for a in body.findAll(defaultTAG, {'class': delTAG}):
            a.string = ""
            del a['class']
            logging.debug("_delTag: {0}".format(a))
        return body

    def _alterBottom(self, body, alterTag):
        '''
        改变底部链接为本地链接
        '''
        for a in body.findAll('div', {'class': alterTag}):
            for b in a.findAll('a'):
                # 改变href标签
                b['href'] = b.text + ".html"
            for b in a.findAll('span'):
                for comment in b:
                    fixed_text = comment.replace("\xa0", "")
                    fixed_text = fixed_text.replace(">", "")
                    fixed_text = fixed_text.replace("<", "")
                    comment.replace_with(fixed_text + "  ")
            logging.debug("_alterBottom a:{0}".format(a))
        return body

    def cleanrubbish(self, body):
        # del title
        # body = _delTag(body, 'articalTitle')
        # # del 标签
        body = self._delTag(body, 'c')
        body = self._delTag(body, 'dashang')
        body = self._delTag(body, 'banner960Ad1 mt5')
        body = self._delTag(body, 'mingzhuPage')
        body = self._delTag(body, 'turnBoxzz')
        body = self._delTag(body, 'img2', defaultTAG='span')
        body = self._delTag(body, 'titName SG_txta', defaultTAG='h2')
        # body = _delTag(body, 'articalfrontback SG_j_linedot1 clearfix')
        body = self._delTag(body, 'h1_tit', defaultTAG='h1')

        # 赠金笔
        body = self._delTag(body, 'shareUp')

        body = self._delTag(body, 'lk_a lka_last', defaultTAG='a')
        body = self._alterBottom(body, 'articalfrontback articalfrontback2 clearfix')
        return body

    def getImage(self, url, name=None, folder='./', sleeptime=8):
        file = path.join(folder, name)
        logging.debug('filename: {0} '.format(file))
        if not os.path.exists(file):
            with open(file, 'wb') as f:
                r = requests.get(url, stream=True,
                                 headers=self.getUserAgent(), timeout=12)
                if r.ok:
                    # for block in r.iter_content(1024):
                    for block in r.iter_content(2048):
                        if not block:
                            break
                        f.write(block)
            logging.debug('sleep: {0}'.format(sleeptime))
            sleep(sleeptime)
        else:
            statinfo = os.stat(file)
            if statinfo.st_size < self.imageMinSize:
                os.remove(file)
                self.getImage(url, name, '', sleeptime)

    def getImages(self, body, title, sleeptime=8, searchTitle=None):
        i = 0
        if searchTitle is None:
            searchTitle = title
        for a in body.findAll('img', {'title': searchTitle}):
            i += 1
            try:
                url = a['real_src']
                # getImage(url, title + str(i) + '.jpg')
                filename = os.path.join(self.imagePath, title + str(i))
                self.getImage(url, filename, self.thepath, sleeptime)
                a['real_src'] = filename
                a['src'] = filename
                # 鼠标点击链接
                a.parent['href'] = filename
                logging.debug('getImages:{0}'.format(a))
                logging.debug(a.parent)
                logging.debug(url)
                logging.debug(filename)
            except Exception as exception:
                logging.error('Error {0}'.format(exception))
                logging.info('exception: {0}'.format(a))
                i -= 1
        return body

    def _getTitleTag(self, tagName, tagStr='', fontSize=12):
        soup = BeautifulSoup("p", 'lxml')
        soup['align'] = "center"
        bb = soup.p
        bb.string = ""
        new_tag = soup.new_tag("p")
        new_tag['align'] = "center"
        new_tag['style'] = "font-size: {0}px;".format(fontSize)
        new_tag.name = tagName
        new_tag.string = tagStr
        return new_tag

    def getlocalarticle(self, url, folder='./', charset='utf-8'):
        """
        从本地获取文章
        :param url:
        :param folder:
        :param charset:
        :return:
        """
        for a in self.contentList:
            if url == a.get('link'):
                soup = BeautifulSoup(a.get('desc'), 'lxml')
                title = a.get('title')
                title2 = " "
                article_comment_list = " "
                body = soup.find('div', {'id': 'f_article'})
                if body is None:
                    return title
                body = self.cleanrubbish(body)
                body.title = title
                # 处理两种图片识别格式
                # body = self.getImages(body, title, self.delaySecond)
                # body = self.getImages(body, title + '_', self.delaySecond, '')

                self.saveToFile(self.getFilePath(title, folder),
                                self.alterArticalContents(body, title, title2, article_comment_list, self.copyRight),
                                charset)
                return title

    def getarticle(self, url, folder='./', charset='utf-8'):
        '''
        保存新浪博客网址（url）对应的图片及文字到指定目录（folder)
        '''
        logging.debug('getarticle: {0}'.format(url))
        r = requests.get(url, headers=self.getUserAgent())
        if r.ok:
            soup = BeautifulSoup(r.content, 'lxml')
            title = self.getTitle(soup)
            title2 = self.getTitle2(soup)
            article_comment_list = self.getArticle_comment_list(soup)
            body = self.getMainBody(soup)
            if body is None:
                return title
            body = self.cleanrubbish(body)
            body.title = title
            # 处理两种图片识别格式
            body = self.getImages(body, title, self.delaySecond)
            body = self.getImages(body, title + '_', self.delaySecond, '')

            self.saveToFile(self.getFilePath(title, folder),
                            self.alterArticalContents(body, title, title2, article_comment_list, self.copyRight),
                            charset)
            return title
        else:
            logging.Error('Requests Error: {0}'.format(url))
        return ""

    def getlocalarticleList(self, order=-1):
        """
        获取本地链接list
        :param order:
        :return:
        """
        if self.contentList is not None:
            r = ''
            for a in self.contentList:
                r += '<a href="' + a.get('link') + '">' + a.get('title') + '</a>'
            if len(r) > 0:
                soup = BeautifulSoup(r, 'lxml')
                body = soup.findAll('a')
                # 倒序
                if order == -1:
                    return body[::-1]
                else:
                    return body

    def getarticleList(self, url=None, order=-1):
        '''
        获取链接list，当order = -1时，返回倒序列表
        '''
        articleList = []
        if url is None:
            # 本地链接
            articleList.extend(self.getlocalarticleList(order))
            return articleList

        if type(url) == str:
            articleList.extend(self.getSingleArticleList(url, order))
        elif type(url) == list:
            for a in url:
                articleList += self.getSingleArticleList(a, order)
        for a in articleList:
            {'''
            todo 不知道为什么会有新浪首页的链接，待查
            剔除类似无用链接：  <a href="http://news.sina.com.cn/" target="_blank">
            <img align="absmiddle" class="SG_icon SG_icon107" height="18" src="http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif" title="已推荐到新闻中心，点击查看更多精彩内容" width="18"/>
            </a>
            '''}
            try:
                if a.img.get('class') is not None:
                    articleList.remove(a)
            except:
                pass
        return articleList

    def getSingleArticleList(self, url=None, order=-1):
        if url is not None:
            r = requests.get(url, headers=self.getUserAgent(self.myAgent), stream=True)
            if r.ok:
                soup = BeautifulSoup(r.content, 'lxml')
                body = soup.find('div', {'class': 'articleList'})
                #        body = body.findAll('span', {'class': 'atc_title'})
                body = body.findAll('a')
                # 倒序
                if order == -1:
                    return body[::-1]
                else:
                    return body
        else:
            pass

    def saveToFile(self, filename='', text=None, charset='utf-8'):
        '''
        保存soup到文件filename中
        '''
        # todo 判断filename是否有后缀
        file_ext = ".html"
        filename = filename + file_ext

        with open(filename, "w") as text_file:
            text_file.write("{0}".format(text))
        logging.info('saved file: {0} '.format(filename))

    def alterMainIndex(self, alist, title, remark):
        '''
        修整index.html
        '''
        template = self.getTemplate('', 'genzztj/templates')
        return template.render(title=title, atc_titles=alist, remark=remark)

    def alterArticalContents(self, articalContents=None, title="", title2="", article_comment_list='', remark=""):
        '''
        修整article.html
        '''
        template = self.getTemplate('article.htm', 'genzztj/templates')
        return template.render(articalContents=articalContents, title=title, title2=title2,
                               article_comment_list=article_comment_list, remark=remark)

    def getMainPath(self):
        self.thepath = os.path.join(tempfile.gettempdir(), maindir)
        return self.thepath

    # 下载目录
    # thepath = os.path.join(tempfile.gettempdir(), 'guweiling')
    # 下载图片后等待时间，否则可能被屏蔽
    delaySecond = 0.05

    # 缠论108课标题
    tilesContain = ["上证大底的必然性", '', '']

    saveCharset = 'GB2312'


if __name__ == '__main__':
    None
