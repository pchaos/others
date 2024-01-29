"""
 python -m pytest new_recording.py -q -s --gui
 Last Modified: 2024-01-29 01:45:44
"""
import time

from bs4 import BeautifulSoup as bs
from seleniumbase import BaseCase

BaseCase.main(__name__, __file__)


class RecorderTest(BaseCase):
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
