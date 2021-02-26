# -*- coding: utf-8 -*-
"""登录ibm cloud，重启vps
"""
import os
import time
from dotenv import load_dotenv
# explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
from seleniumbase import BaseCase


class IBMCloudTest(BaseCase):
    """ IBM Cloud Test
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
            cls.filename = "ibmcloud"

    def login(self, user="", password=""):
        if len(password) == 0:
            raise Exception("密码不对")
        if len(user) == 0:
            raise Exception("用户名不对")
        self.assert_element('button[name="login"]')
        self.update_text("input.bx--text-input", f"{user}\n")
        self.assert_title("IBM Cloud")
        self.update_text("input.bx--password-input", f"{password}")
        self.wait_for_element_present("div.bx--password-input-wrapper", timeout=20)
        #  self.assert_text("Log in", "登录")
        self.assert_element('input[id="password"]')
        self.click("//div[2]/div[2]/div[2]/button/span")

    def test_basic(self):
        self.open("https://cloud.ibm.com/")
        time.sleep(1)
        self.assert_title("IBM Cloud")
        self.login(self.email, self.password)
        #  time.sleep(1)
        # click "Cloud Foundry apps"
        try:
            # 英文版 
            self.wait_for_element_present("link=Cloud Foundry apps", timeout=30)
            self.click("link=Cloud Foundry apps")
        except Exception as e:
            # 中文版
            self.open("https://cloud.ibm.com/resources?groups=cf-application")
        # click "..."
        self.click('svg.bx--overflow-menu__icon')
        # click "restart"
        time.sleep(2)
        # 验证存在标题
        self.assert_element('//*[@id="main-content"]/div[2]')
        #  self.wait_for_element_present("//body[@id='body']/div[5]/ul/li[2]/button/div", timeout=12)
        self.wait_for_element_present("//*[@id='body']/div[5]/ul/li[2]/button/div", timeout=15)
        self.click("//*[@id='body']/div[5]/ul/li[2]/button/div")
        time.sleep(1.2)
        self.wait_for_element_present("(//button[@type='button'])[17]", timeout=12)
        time.sleep(1.2)
        self.click("(//button[@type='button'])[17]")
        time.sleep(5)
