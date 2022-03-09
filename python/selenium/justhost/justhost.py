# -*- coding: utf-8 -*-
"""登录justhost cloud，重启vps
"""
import os
import time
from dotenv import load_dotenv
# explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
from seleniumbase import BaseCase

#  import pytest


#  @pytest.mark.marker_test_suite
class JUSTHOSTTest(BaseCase):
    """ JUSTHOST Cloud Test
    """
    @classmethod
    def setUpClass(cls):

        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=True)

        cls.email = os.getenv("EMAIL")
        cls.password = os.getenv("PASSWORD")
        cls.isProxy = int(os.getenv("PROXY"))  # 是否用proxy
        cls.isRestart = int(os.getenv("RESTART"))  # 是否用重启vps
        cls.headless = bool(int(os.getenv("HEADLESS")))
        if cls.headless:
            print("headless mode")
        try:
            cls.filename = os.path.splitext(os.path.basename(__file__))[0]
        except Exception as e:
            cls.filename = "justhost"

    def login(self, user="", password=""):
        if len(password) == 0:
            raise Exception("密码不对")
        if len(user) == 0:
            raise Exception("用户名不对")
        self.assert_element('input[name="login"]')
        self.update_text("input#login", f"{user}\n")
        #  self.assert_title("IBM Cloud")
        self.update_text("input#password", f"{password}")
        self.wait_for_element_present(
            "#loginForm > div.jFormWrapperContainer > ul > li.nextLi > button",
            timeout=20)
        #  self.assert_text("Log in", "登录")
        self.assert_element('input[id="password"]')
        self.click(
            "#loginForm > div.jFormWrapperContainer > ul > li.nextLi > button")

    def restarting(self, isRestart=0):
        self._print(f"prepare to restart")
        if isRestart > 0:
            try:
                self.open("https://justhost.ru/tickets")
                self.open("https://justhost.ru/billing/active")
                self.assert_text("ID")
                #  self.assert_text("div#formActiveServices")
                #  self._print(f"formActiveServices exists")
                self.wait_for_element_present('a[href="/tickets"]', timeout=35)
                # click control
                self.click('a:contains("управление")')
                self._print(f"click control")
                self.assert_text("VPS kvm", timeout=5)
                self._print(f"Ready to restart vps")
                url = self.get_current_url()
                url=f'https://justhost.ru/vps_service/vpsReset/{url.split("/")[-1]}'
                self._print(f"open {url}")
                #  self.click('a:contains("Перезагрузить сервер")', timeout =30)
                self.open(url)
                #  self.click('tr.status-2[strong]')
                #  restart =driver.find_elements_by_link_text("Перезагрузите сервер")
                #  restart=driver.find_elements_by_class_name("ui-corner-all");
                restart = self.find_elements("a.ui-corner-all")
                self._print(f"{restart=}")
            except Exception as e:
                # english version
                self._print(e.args)
                restart = self.find_elements("Restart server")
            if isinstance(restart, list):
                for i in restart:
                    self._print(f"'{i.text}'")
                    if i.text == 'Перезапустить сервер':
                        self._print(f"found '{i.text}' and restart server")
                        i.click()
                        time.sleep(2)
                        break
            self._print("restarting!!")

    #  @pytest.mark.marker1
    def test_basic(self):
        url = "https://justhost.ru/billing/active"
        try:
            self.open("https://justhost.ru/")
            #  self.asscert_text("VPS")
            self.wait_for_element_present('a[href="/optimal-plan/"]',
                                          timeout=5)
        except Exception as e:
            self._print("url timeout.")
            time.sleep(3)
        finally:
            self.open(url)
            self._print(f"open {url}")
            time.sleep(1)
            #  self.wait_for_element_present('a[href="/services/vps"]', timeout=10)

        self.assert_element('a[href="https://justhost.ru/services/vps"]')
        #  self.assert_title("IBM Cloud")
        self.login(self.email, self.password)
        #  time.sleep(1)
        # click "Cloud Foundry apps"
        try:
            #active Services
            css = 'a[href="/billing/active"]'
            self.wait_for_element_present(css, timeout=5)
            self.click(css)
        except Exception as e:
            self._print(e.args)
            self.open(url)
        # click "..."
        self._print(f"prepare to restart")
        self.restarting(self.isRestart)
        time.sleep(5)

    def atest_D(self):
        self.open("https://xkcd.com/2021/")
        self.assert_text("Software Development", "div#ctitle")
        print("ok")

    def atest_google_tour(self):
        self.open('https://google.com')
        self.wait_for_element('input[title="Search"]')

        self.create_tour(theme="dark")
        self.add_tour_step("Welcome to Google!", title="SeleniumBase Tours")
        self.add_tour_step("Type in your query here.", 'input[title="Search"]')
        self.play_tour()

        self.highlight_type('input[title="Search"]', "Google")
        self.wait_for_element('[role="listbox"]')  # Wait for autocomplete

        self.create_tour(theme="light")
        self.add_tour_step("Then click to search.", '[value="Google Search"]')
        self.add_tour_step("Or press [ENTER] after entry.", '[title="Search"]')
        self.play_tour()
