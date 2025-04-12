# -*- coding=utf-8 -*-

"""
sbase record test_url_directory.py --url=http://192.168.124.80:5344/%E6%95%99%E8%82%B2/%E7%BC%96%E7%A8%8B%E5%BC%80%E5%8F%91 --gui
"""
import time

from bs4 import BeautifulSoup as bs
from seleniumbase import BaseCase

BaseCase.main(__name__, __file__)


class RecorderTest(BaseCase):
    def setUp(self, masterqa_mode=False):
        # 目录显示区
        self.selector = ['//*[@id="root"]/div[2]/div/div[1]', "a"]  #  爬取所有链接

        return super().setUp(masterqa_mode)

    def tearDown(self):
        self.selector = None
        return super().tearDown()

    def test_recording(self):
        url = "http://192.168.124.80:5344/教育/编程开发"
        data = []
        self.open("http://192.168.124.80:5344/教育/编程开发")
        self.maximize_window()
        self.get_elements(url, self.selector[0], None, data=data)
        self.click('p[title="00-【计算机基础197GB】"]')
        self.click('p[title="Git从入门到精通"]')
        self.click('p[title="01-课程导读.mp4"]')

    def get_content(self, url):
        """
        递归爬取网页，构建节点数据

        Args:
            url: 当前页面的 URL
            selector: 选择器的 XPath 表达式
            parent_id: 父节点在 nodes 表中的 ID
            data: 存储节点数据的列表
        """

        self.get(url)

        # 获取页面源代码
        html_content = self.get_page_source()
        return html_content

    def get_elements(self, url, selector, parent_id, data):
        """
        递归爬取网页，构建节点数据

        Args:
            url: 当前页面的 URL
            selector: 选择器的 XPath 表达式
            parent_id: 父节点在 nodes 表中的 ID
            data: 存储节点数据的列表
        """

        # 获取页面源代码
        self.open(url)
        time.sleep(1)
        # html_content = self.get_content(url=url)

        # 解析 HTML
        # soup = bs(html_content, 'html.parser')
        # elements = soup.select_one(selector)
        # for element in elements:
        #     title = element.text.strip()
        #     data.append({'title': title, 'parent_id': parent_id})
        #     self.get_elements(element.get('href'), selector, len(data) - 1, data)
        # reeturn data

        # self.wait_for_element_visibile(selector)
        elem = self.find_element(selector)
        if elem is None:
            return
        # print(f'{elem.parent.find_elements(".size")[2].parent.find_element(".name").text =}')
        title = elem.text.strip()
        search_str = "名称\n大小\n修改时间\n"
        if search_str in title:
            title = title.replace(search_str, "")

        print(title)
        ls = title.split("\n")
        breakpoint()
        data.append({'title': title, 'parent_id': parent_id})
        self.get_elements(elem.get('href'), selector, len(data) - 1, data)
        return datm
