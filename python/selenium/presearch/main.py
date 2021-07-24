#   coding: utf-8
#   Copyright (c) 2021.
#   Version : 0.0.1
#   Script Author : Sushen Biswas
#
#   Sushen Biswas Github Link : https://github.com/sushen

# This is Masud Rana, Does the task like this?

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('username')
PASSWORD = os.getenv('password')
chromeuserdatadir = os.getenv('chromeuserdatadir')

# TODO: 3 Make a Long List of keyword
all_keys = [
    "username", "password", "country", "income", "funny", "tdx function"
]
# 热搜
url = "https://s.weibo.com/top/summary?cate=realtimehot"
df = pd.read_html(url)
for i in range(len(df[0])):
    all_keys.append(df[0]["关键词"][i].split()[0])
print(all_keys)

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")
chrome_options.add_argument(f"--user-data-dir={chromeuserdatadir}")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--incognito")

#  driver = webdriver.Chrome("./chromedriver.exe", chrome_options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)
#  chrome_options.add_argument("user-data-dir=chrome-data")
driver.implicitly_wait(25)  # seconds
# What will be searched

actions = ActionChains(driver)

# Time waiting for page
waiting_for_page = 13

driver.get("https://presearch.org")
time.sleep(2)
driver.get("https://www.presearch.org")

# TODO: 2 Make a login strong system in environment veriable
try:
    # already login
    #  el = driver.find_element_by_xpath('//*[@id="Home"]/div[1]/div/div[3]/a[1]')
    #  el = driver.find_element_by_class_name('hidden-xs.nav-reward-balance')
    el=driver.find_element_by_xpath('//*[@id="main-nav"]/ul/li[5]')
    if "Login"  in el.text:
        raise Exception("not login!")
    else:
        print("already logined")
except Exception as e:
    driver.get("https://presearch.org/external-login?")
    el = driver.find_element_by_xpath(
        '//*[@id="login-form"]/form/div[2]/div/input')
    el.send_keys(PASSWORD)
    el = driver.find_element_by_xpath(
        '//*[@id="login-form"]/form/div[1]/input')
    el.send_keys(USERNAME)
    print(input("Enter your Username and Password Menually then enter 1: "))
driver.get("https://presearch.org")
# print(input("Enter your Username and Password Menually then enter 1: "))
driver.find_element_by_id("search").send_keys(random.choice(all_keys))
driver.find_element_by_id("search").send_keys(Keys.ENTER)
# print(input("Enter your Username and Password Menually then enter 1: "))
time.sleep(4)

#  actions.send_keys(Keys.TAB * 10)
#  actions.send_keys(Keys.TAB * 3)
#  search_key = random.choice(all_keys)
#  actions.send_keys(search_key)
#  actions.send_keys(Keys.ENTER)
#  actions.perform()
#  time.sleep(20)
#  prev_search_key = search_key

for i in range(5):
    driver.back()
    time.sleep(4)
    search_key = random.choice(all_keys)
    print(search_key)
    time.sleep(random.random()*15)
    try:
        driver.find_element_by_id("search").send_keys(search_key)
        time.sleep(random.random()*10)
        driver.find_element_by_id("search").send_keys(Keys.ENTER)
    except Exception as e:
        driver.get("https://presearch.org")
        print("on Exception")
        driver.find_element_by_id("search").send_keys(search_key)
        time.sleep(random.random()*10)
        driver.find_element_by_id("search").send_keys(Keys.ENTER)

    else:
        pass
    #  actions.send_keys(search_key)
    #  actions.send_keys(Keys.ENTER)
    #  actions.perform()
    prev_search_key = search_key
    time.sleep(4)
    time.sleep(random.random()*15)

print("Done")
driver.quit()

# TODO: 1 Click the search resust to make it more human

# driver.find_element_by_id("token-animation").click()
# print(driver.find_element_by_xpath("//button[@type='submit']"))
# driver.find_element_by_xpath("//input[@type='submit']").click();
# print(input("Enter your Username and Password Menually then enter 1: "))

# driver.execute_script("window.open('https://engine.presearch.org');")
# driver.close()
# driver.get("https://presearch.org")
# driver.find_element_by_id("search").send_keys("username")
# driver.find_element_by_id("search").send_keys(Keys.ENTER)

time.sleep(5)

# driver.quit()
#  driver.close()
