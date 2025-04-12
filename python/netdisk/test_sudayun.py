"""
 pytest test_sudayun.py
 pytest test_sudayun.py::RecorderTest::test_recording_recurse
 Last Modified: 2024-05-04 15:48:41

self.driver.get_cookies()=[{'domain': '.path.dirts.cn', 'httpOnly': False, 'name': 'Hm_lpvt_0e42d925d22019079151233bdd075179', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1706862023'}, {'domain': '.path.dirts.cn', 'expiry': 1738398023, 'httpOnly': False, 'name': 'Hm_lvt_0e42d925d22019079151233bdd075179', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1706862023'}]

"""

import time
from html import unescape
from urllib.request import unquote

# import pytest
from bs4 import BeautifulSoup as bs
from seleniumbase import BaseCase

# BaseCase.main(__name__, __file__)


class RecorderTest(BaseCase):

    def setUp(self, masterqa_mode=False):
        super().setUp(masterqa_mode)
        self.open("https://path.dirts.cn/th0c47d2p")

    def tearDown(self):
        return super().tearDown()

    def test_recording(self):
        self.open("https://path.dirts.cn/th0c47d2p")

        html = self.get_page_source()
        # print(html)
        soup = bs(html, "lxml")
        # print(f"{soup.prettify()=}")
        ls = soup.find_all('div', class_='text-link list-item')
        print(type(ls))
        print(f"{ls=}")
        ls1 = soup.find_all('div', class_='text-link')
        self.assertTrue(len(ls) > 0, f"length must not be zero!!")
        self.assertTrue(ls == ls1, "text-link and list-item not equal ")
        # ls = ls[0].find_all_next("span", class_="ml8")
        ls = ls[0].find_all_next("span", class_="flex1")
        print(f"{ls=}")

        for line in ls:
            print(f"{line.find(string=True)=}")
            click_string = line.find(string=True)
            self.click(f"span:contains('{click_string}')")
            time.sleep(1.5)
            self.go_back()

        self.click('span:contains("教育一区")')
        self.click('span:contains("----其他平台精品课程---")')
        self.click('span:contains("0.1.课文课里的写作密码")')
        self.click('span:contains("【完结】课文的写作密码1年级下册")')
        self.click('span:contains("0.1.课文课里的写作密码")')

    def test_recording_recurse(self):
        self.open("https://path.dirts.cn/th0c47d2p")
        #
        url = "https://path.dirts.cn/tH0c47D2P?i=8274&dir=/%E6%95%99%E8%82%B2%E4%B8%80%E5%8C%BA/----%E5%85%B6%E4%BB%96%E5%B9%B3%E5%8F%B0%E7%B2%BE%E5%93%81%E8%AF%BE%E7%A8%8B---/04.%E5%B0%8F%E8%8B%97"
        # url = "https://path.dirts.cn/tH0c47D2P?i=3632&dir=/%E6%95%99%E8%82%B2%E4%B8%80%E5%8C%BA/----%E5%85%B6%E4%BB%96%E5%B9%B3%E5%8F%B0%E7%B2%BE%E5%93%81%E8%AF%BE%E7%A8%8B---/04.%E5%B0%8F%E8%8B%97"
        print(f"url:{unescape(unquote(url))}")
        # 可点击和不可点击链接
        self.main_dirs(url)

    def test_cookies(self):
        """
        pytest test_sudayun.py::RecorderTest::test_cookies
        self.driver.get_cookies()=[{'domain': '.path.dirts.cn', 'httpOnly': False, 'name': 'Hm_lpvt_0e42d925d22019079151233bdd075179', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1708185825'}, {'domain': '.path.dirts.cn', 'expiry': 1739721825, 'httpOnly': False, 'name': 'Hm_lvt_0e42d925d22019079151233bdd075179', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1708185825'}]
        """
        self.open("https://path.dirts.cn/th0c47d2p")
        print(f"{self.driver.get_cookies()=}")
        self.cookie = self.driver.get_cookies()[0]
        # /教育一区
        self.open("https://path.dirts.cn/tH0c47D2P?i=8274&dir=/%E6%95%99%E8%82%B2%E4%B8%80%E5%8C%BA")
        print(f"教育一区 {self.driver.get_cookies()=}")

    def dirs(self, click_string=""):
        self.click(f"span.ml8.flex1:contains('{click_string}')")
        print(f"click span.ml8.flex1:{click_string}")
        # check click is done
        time.sleep(1.5)
        self.wait_for_element_visible(f"span:contains('{click_string}')")
        html = self.get_page_source()
        # print(html)
        soup = bs(html, "lxml")
        print(f"{soup.prettify()=}")
        # class="text-link list-item" 包含可点击链接
        # class="list-item" 包含不可点击链接
        ls = soup.find_all('div', class_='text-link list-item')
        print(f"{type(ls)=}")
        print(f"{ls=}")
        if len(ls) > 0:
            self.assertTrue(len(ls) > 0, f"length must not be zero!!{ls=}")
            # ls = ls[0].find_all_next("span", class_="ml8")
            ls = ls[0].find_all_next("span", class_="flex1")
            print(f"{ls=}")

            for line in ls:
                print(f"{line.find(string=True)=}")
                click_string = line.find(string=True)
                self.dirs(click_string)
                time.sleep(1.0)
                org_url = self.get_current_url()
                self.go_back()
                if org_url == self.get_current_url():
                    break
        else:
            # todo 已到达目录底层
            # self.go_back()
            # time.sleep(1.0)
            print(f"{click_string} done!")
            pass

    def main_dirs(self, url=""):
        """
        self.driver.get_cookies()[0]["name"]
        self.driver.get_cookies()[0]["value"]
        """
        response = self.open(url)

        print(f"opening {url=}")
        print(f"{self.driver.get_cookies()=}")
        self.cookie = self.driver.get_cookies()[0]

        parrent_url = self.get_current_url()
        print(f"parrent_url:{unescape(unquote(parrent_url))}")
        time.sleep(5)
        html = self.get_page_source()
        # print(html)
        soup = bs(html, "lxml")
        # print(f"{soup.prettify()=}")
        ls = soup.find_all('div', class_='text-link list-item')
        print(type(ls))
        print(f"{ls=}")
        ls1 = soup.find_all('div', class_='text-link')
        self.assertTrue(len(ls) > 0, f"length must not be zero!!")
        self.assertTrue(ls == ls1, "text-link and list-item not equal ")
        # ls = ls[0].find_all_next("span", class_="ml8")
        ls_detail = ls[0].find_all_next("span", class_="flex1")
        print(f"{ls_detail=}")

        for line in ls_detail:
            print(f"{line.find(string=True)=}")
            click_string = line.find(string=True)
            self.dirs(click_string)
            if self.get_current_url() == parrent_url:
                break
            else:
                self.go_back()
            # self.click(f"span:contains('{click_string}')")
            time.sleep(1.5)
            # self.go_back()
