# -*- coding: utf-8 -*-
"""登录racknerd cloud，重启vps
"""
import os
import time
from dotenv import load_dotenv
# explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
from seleniumbase import BaseCase

class RACKNERDTest(BaseCase):
    """ RACKNERD Cloud Test
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
        cls.restarturl = "https://my.racknerd.com/clientarea.php"

    def login(self, user="", password=""):
        if len(password) == 0:
            raise Exception("密码不对")
        if len(user) == 0:
            raise Exception("用户名不对")
        # 根据登录界面修改下面变量
        loginusername = "username"
        loginid = "inputEmail"
        loginpasswordid = "inputPassword"

        self.assert_element(f'input[name="{loginusername}"]')
        self._print("input username")
        #  self.update_text(f"input#{loginid}", f"{user}\n")
        self.type(f"#{loginid}", f"{user}")
        self._print("input password")
        #  self.update_text(f"input#{loginpasswordid}", f"{password}")
        self.type(f"input#{loginpasswordid}", f"{password}")
        self.wait_for_element_present("#login", timeout=20)
        #  self.assert_text("Log in", "登录")
        self.assert_element(f'input[id="{loginpasswordid}"]')
        self.click("#login")

    def restarting(self, isRestart=0):
        if isRestart > 0:
            try:
                self.open(self.restarturl)
                # logined
                self.assert_text("Welcome Back")
                self.wait_for_element_present('div[class="list-group"]', timeout=5)
                # click Manage Product
                #  self.click('div[class="list-group"]')
                self._print(f"Active Products/Services")
                self.click('//*[@id="ClientAreaHomePagePanels-Active_Products_Services-0"]')
                self._print(f"Manage Product")
                self.assert_text("Manage Product")
                self._print(f"Ready to restart vps")
                # reboot
                self.wait_for_element_present('span[id="displayreboot"]', timeout=18)
                self.click('//*[@id="displayreboot"]/a')
                self.wait_for_element_present('div[class="modal-content"]', timeout=5)
                # confirm
                time.sleep(3)
                self.click('input[type="button"]')
            except Exception as e:
                self._print(e.args)
                url="https://my.racknerd.com/clientarea.php?action=productdetails&amp;id=39227&amp;serveraction=custom&amp;a=reboot"
                self.open(url)
            self._print("restarting!!")
        else:
            self._print("no need restart!")

    def test_basic(self):
        url="https://my.racknerd.com/index.php"
        url="https://my.racknerd.com"
        url2=self.restarturl
        try:
            self.open(url)
            #  self.asscert_text("VPS")
            self.wait_for_element_present('a[href="#"]', timeout=5)
        except Exception as e:
            self._print("url timeout.")
            time.sleep(3)
        finally:
            self.open(url2)
            self._print(f"open {url2}")
            time.sleep(1)
            #  self.wait_for_element_present('a[href="/services/vps"]', timeout=10)

        self.assert_element('a[href="#"]')
        self._print("prepare login")
        self.login(self.email, self.password)
        #  time.sleep(1)
        # click "Cloud Foundry apps"
        try:
            # active Services
            css='div[class="panel-heading"]'
            self.wait_for_element_present(css, timeout=8)
            self.click(css)
        except Exception as e:
            self._print(e.args)
            self.open(url2)
        # click "..."
        self._print(f"prepare to restart")
        self.restarting(self.isRestart)
        time.sleep(5)

    def login_to_swag_labs(self):
        """ Login to Swag Labs and verify that login was successful. """
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce")
        self.click('input[type="submit"]')
        self.open("https://my.racknerd.com/index.php?rp=/login")
        self.type("#inputEmail", "123")
        self.sleep(5)

    def atest_A_LOGIN(self):
        """ This test checks standard login for the Swag Labs store. """
        self.login_to_swag_labs()
        self.assert_element("#inventory_container")
        self.assert_element('div:contains("Sauce Labs Backpack")')
