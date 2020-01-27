# -*- coding: utf-8 -*-
"""
下载selenium
https://pypi.org/project/selenium/
Chrome: 	https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge: 	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox: 	https://github.com/mozilla/geckodriver/releases
Safari: 	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

@Time    : 2020/1/27 下午12:53

@File    : testsenium.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import time
from selenium import webdriver


class testSELENIUM(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Firefox()

    def tearDown(self) :
        self.browser.quit()

    def test_selenium27(self):
        # 多窗口之间切换
        # 原文链接：https: // blog.csdn.net / u011541946 / article / details / 70132672
        driver = self.browser

        driver.maximize_window()
        driver.get('http://news.baidu.com')
        time.sleep(1)

        news_link = driver.find_element_by_xpath("//*[@id='pane-news']/div/ul/li[1]/strong/a")
        page1_title_string = news_link.text  # 得到页面A新闻标题
        news_link.click()  # 点击新闻链接
        time.sleep(1)
        handles = driver.window_handles

        for handle in handles:  # 切换窗口（切换到搜狗）
            if handle != driver.current_window_handle:
                print('switch to second window', handle)
                driver.close()  # 关闭第一个窗口
                driver.switch_to.window(handle)  # 切换到第二个窗口
        page2_title_string = driver.title
        # page2_title_string = driver.find_element_by_tag_name("title").parent.title

        try:
            assert page1_title_string in page2_title_string  # 判断页面B标题是否包含页面A标题
            print('Test Pass.')
        except Exception as e:
            print('Test Fail')


if __name__ == '__main__':
    unittest.main()
