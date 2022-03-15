# -*- coding: utf-8 -*-
"""登录racknerd cloud，重启vps
https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py
"""
import os
import random
import time
# explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only

import numpy as np
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from seleniumbase import BaseCase

delays = 95


def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


class presearchTest(BaseCase):
    """ presearch Cloud Test
    """
    @classmethod
    def setUpClass(cls):

        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=True)

        cls.email = os.getenv("EMAIL")
        cls.password = os.getenv("PASSWORD")
        try:
            cls.filename = os.path.splitext(os.path.basename(__file__))[0]
        except Exception as e:
            cls.filename = "presearch"
        cls.restarturl = "https://www.presearch.org/"
        cls.all_keys = [
            "username", "password", "country", "income", "funny",
            "tdx function"
        ]
        cls.user_data_dir = os.getenv('chromeuserdatadir')

    def get_google_keywords(self):
        # List Of 1000 Most Searched Words On Google
        url = "https://www.mondovo.com/keywords/most-searched-words-on-google"
        self._print(f"get {url}")
        self.open(url)
        elems = self.wait_for_element_present(f'table[class="top-100"',
                                              timeout=8)
        self.press_down_arrow(times=5)
        if elems:
            #  soup = bs4.BeautifulSoup(self.get_beautiful_soup().text)
            soup = self.get_beautiful_soup()
            self._print(f"{type(soup)}")
            table = soup.find('table')
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                #  self._print(f"{cols=}")
                if len(cols) > 1:
                    self.all_keys.append(cols[1])
        self._print(self.all_keys)
        return self.all_keys

    def get_weibo_keywors(
        self, url="https://s.weibo.com/top/summary?cate=socialevent"):
        self.open(url)
        self.wait_for_element_present(f'tr[class="thead_tr"', timeout=8)
        self.press_down_arrow(times=8)
        elems = self.find_elements(".td-02")
        for elem in elems:
            #  self._print(elem)
            self._print(elem.text)
            self.all_keys.append(elem.text.replace("#", ""))
        return self.all_keys

    def prepare(self):
        self.get_google_keywords()

        self.get_weibo_keywors()
        url = "https://s.weibo.com/top/summary?cate=entrank"
        self.get_weibo_keywors(url)
        url = "https://s.weibo.com/top/summary?cate=realtimehot"
        self.get_weibo_keywors(url)
        url = "https://s.weibo.com/top/summary?cate=total&key=friends"
        self.get_weibo_keywors(url)
        self._print(self.all_keys)

    def login(self, user="", password=""):
        if len(password) == 0:
            raise Exception("密码不对")
        if len(user) == 0:
            raise Exception("用户名不对")
        # 根据登录界面修改下面变量
        loginusername = "email"
        loginid = "inputEmail"
        loginpasswordid = "inputPassword"
        loginpasswordname = "password"

        self.assert_element(f'input[name="{loginusername}"]')
        self._print("type username")
        #  self.update_text(f"input#{loginid}", f"{user}\n")
        #  self.type(f"#{loginid}", f"{user}")
        self.type(f'input[name="{loginusername}"]', f"{user}")
        self._print("type password")
        #  self.update_text(f"input#{loginpasswordid}", f"{password}")
        #  self.type(f"input#{loginpasswordid}", f"{password}")
        self.type(f'input[name="{loginpasswordname}"]', f"{password}")
        remember_check = '//*[@id="login-form"]/form/div[3]/div[1]/div[1]/div/label/input'
        self.select_if_unselected(remember_check)
        recaptcha = '#recaptcha-anchor'
        if self.is_element_present(recaptcha):
            self._print("check recaptcha")
            self.click(recaptcha)
        inputchar = input(
            "Enter your Username and Password Menually then enter 1: ")
        if inputchar.lower() == "q":
            exit(3)
        #  print
        #  input("Enter your Username and Password Menually then enter 1: "))

        # login button
        login_button = '#login-form'
        if self.is_element_present(login_button):
            self.click(login_button)
        self.wait_for_element_present("//*/div/span[2]")

    def random_down(self, counts=12, ischinese=False):
        if not ischinese:
            for _ in range(int(random.random() * counts)):
                # 随机选择可选搜索内容
                self.send_keys(self.get_search_selector(), Keys.ARROW_DOWN)
                #  self.find_element_by_id("search").send_keys(Keys.ARROW_DOWN)
                #  time.sleep(0.05)
                time.sleep(random.random() / 9)

    def get_search_selector(self):
        if self.is_element_present("#search"):
            selector = "#search"
        else:
            # <input class="w-full h-12 pr-20 focus:outline-none pl-4 font-light dark:bg-background-dark300 dark:text-gray-50 text-sm sm:text-base" x-ref="searchInput" placeholder="What are you looking for today?" type="text" autocomplete="off" name="q" value="consol print pretty">
            selector = 'input[name="q"]'
        return selector

    def delay_sendkey(self, key=""):
        # 减慢搜索输入速度
        print(f"send_keys ", end="|")
        selector = self.get_search_selector()
        for k in key:
            self.send_keys(selector, k)
            #  self.find_element_by_id("search").send_keys(k)
            time.sleep(random.random() / 2)
            print(f"{k}", end="")
            #  self._print(f"{k}")
        self._print("")

        if len(key) > 1:
            time.sleep(random.random() * 5)
            # 非汉字搜索，随机获取关键字
            self.random_down(
                ischinese=is_chinese(key[1 if len(key) > 1 else 0]))
            self.send_keys(selector, Keys.ENTER)
        elif len(key) == 0:
            # 清空输入框
            time.sleep(random.random() / 2)
            self.clear(selector)

    def close_all_new_windows(self, old_windows_handles=None):
        # close new presearch windwos
        multi_window = self.driver.window_handles
        try:
            for window in multi_window:
                if window not in old_windows_handles:
                    try:
                        self.switch_to_window(window)
                        self._print(f"window:{window}")
                        time.sleep(0.5)
                        self.driver.close()
                    except Exception as e:
                        raise e
        except Exception as e:
            raise e

    def after_login(self, searchcounts=10):
        #  searchcounts = 10
        self.get("https://presearch.org")
        # 随机产生搜索次数
        searchcounts += int(
            round(random.random() * 2 * (-1 if random.random() > 0.5 else 1),
                  0))
        for i in range(searchcounts):
            time.sleep(1)
            search_key = random.choice(self.all_keys)
            self._print(search_key)
            time.sleep(random.random() * 15)
            try:
                #  self.find_element_by_id("search").send_keys(search_key)
                #  if self.get_search_selector() != "#search":
                #  self.open(self.restarturl)
                #  self._print(f"current search input:{self.get_search_selector()}")
                #  self._print(f"current url {self.get_current_url()}")
                self.delay_sendkey(search_key)
                #  self.send_keys("#search", Keys.ENTER)
                #  self.find_element_by_id("search").send_keys(Keys.ENTER)
            except Exception as e:
                self._print(e.args)
                self.switch_to_window(self.driver.window_handles[-1])
                time.sleep(2)
                self.get("https://presearch.org")
                self._print(f"{i}/{searchcounts} ... on Exception")
                #  self.find_element_by_id("search").send_keys(search_key)
                self.delay_sendkey(search_key)
                #  time.sleep(random.random() * 4)
                #  self.random_down(ischinese=is_chinese(
                #  search_key[1 if len(search_key) > 1 else 0]))
                #  self.send_keys("#search", Keys.ENTER)
                #  self.find_element_by_id("search").send_keys(Keys.ENTER)

            else:
                pass
            #  actions.send_keys(search_key)
            #  actions.send_keys(Keys.ENTER)
            #  actions.perform()
            prev_search_key = search_key
            time.sleep(4)
            time.sleep(random.random() * 15)
            delayseconds = random.random() * int(delays)
            self._print(
                f"delay {np.round(delayseconds, 2)} seconds ... {i}/{searchcounts}"
            )
            time.sleep(delayseconds)
            #  self.go_back()
            self.bring_active_window_to_front()
            #  self.switch_to_window(self.driver.window_handles[-2])
            self.delay_sendkey()

        self._print(f"Done ... {searchcounts=}")

    def test_basic(self):
        #  self._print(f"self.driver:{dir(self.driver)}")
        old_window = self.driver.window_handles
        self.open_new_tab()
        self.prepare()

        url = "https://www.presearch.org/"
        url2 = self.restarturl
        need_login_str = 'div:contains("Register or Login")'
        try:
            self.open(url)
            if self.is_element_present(need_login_str):
                self._print(f"click {need_login_str}")
                self.click(need_login_str)
            #  self.wait_for_element_present('div[class="tw-relative tw-flex-1"]',
            # <span class="bg-presearch-alternative text-white font-normal px-2 ml-2 rounded-md hidden md:block" style="font-size:10px; padding-top:2px; padding-bottom:2px">PRE</span>
            self.wait_for_element_present('span:contains("PRE")', timeout=3)
        except Exception as e:
            self._print(f"url timeout.{e.args}")
            login_elem = self.is_element_present(selector=need_login_str)
            if login_elem:
                #  login_elem.click()
                self.open("https://www.presearch.org/login?signin")
                #  result=self.click(need_login_str)
                #  self._print(f"click {result=} {login_elem=} {login_elem.text}")
                self._print(f"prepare login {self.email} {self.password}")
                self.login(user=self.email, password=self.password)

            self.wait_for_element_present('//*/div/span[2]',
                                          By.XPATH,
                                          timeout=10)

        # PRE
        self.assert_element('//*/div/span[2]', By.XPATH)
        #  time.sleep(1)
        try:
            # loginned
            self.wait_for_element_present(need_login_str, timeout=5)
            self.click(need_login_str)
        except Exception as e:
            self._print(e.args)
            self.open(url2)
        # click "..."
        self._print(f"prepare to presearch")
        try:
            #  self.after_login(10)
            self.after_login(10)
        except Exception as e:
            self._print(e.args)
        finally:
            self.close_all_new_windows(old_window)
        #  self.restarting(self.isRestart)
        time.sleep(5)
