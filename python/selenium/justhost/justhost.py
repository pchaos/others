# -*- coding: utf-8 -*- #
import os
#  import json
import time
#  import random
from selenium import webdriver
import pickle
from dotenv import load_dotenv

# explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
searchcounts = int(os.getenv("SEARCHCOUNTS"))  # 查询次数
isProxy = int(os.getenv("PROXY"))  # 是否用proxy
isRestart = int(os.getenv("RESTART"))  # 是否用重启vps
headless = bool(int(os.getenv("HEADLESS")))
if headless:
    print("headless mode")
try:
    filename = os.path.splitext(os.path.basename(__file__))[0]
except Exception as e:
    filename = "justhost"
cookieFileName = f'cookies.{filename}.pkl'
PROXY = "127.0.0.1:1080"  #  HOST:PORT
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = headless
if isProxy:
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_argument("ignore-certificate-errors")
chrome_options.add_argument("--window-size=1280,1080")

driver = webdriver.Chrome(options=chrome_options)
#  driver.get("https://www.ipchicken.com/")
driver.get("https://www.justhost.ru/")
if os.path.exists(cookieFileName):
    #  url = 'https://justhost.ru'
    cookies = pickle.load(open(cookieFileName, "rb"))
    for cookie in cookies:
        print(f"loading cookies:{cookie}")
        driver.add_cookie(cookie)
else:
    pass

url = "https://justhost.ru/billing/active"
driver.get(url)

try:
    driver.find_element_by_name('login').send_keys(email)  # enter your email
    driver.find_element_by_name('password').send_keys(
        password)  # enter your password
    #  print(f"passwd:{password}")
    time.sleep(1.5)
    loginbutton = driver.find_element_by_class_name('nextButton')
    if loginbutton:
        loginbutton.click()
    time.sleep(2)

    if os.path.exists(cookieFileName):
        # 重新登录系统，删除以前的cookie文件
        os.remove(cookieFileName)
        print("loading cookies")
    url = 'https://justhost.ru/auth/login/?returl=/billing/renew'
except Exception as e:
    url = 'https://justhost.ru/auth/login/?returl=/billing/renew'
    print("using cookies, no need login")
    print(e.args)

counts = 100
print("waiting ", end='')
for i in range(counts):
    time.sleep(2)
    if driver.current_url != url:
        print(driver.current_url)
        driver.switch_to.default_content()
        break
    print(".", end='', flush=True)

if not os.path.exists(cookieFileName):
    # 保存cookies，下次免登录
    pickle.dump(driver.get_cookies(), open(cookieFileName, "wb"))

driver.get("https://justhost.ru/billing/active")
time.sleep(1)
#  control button
driver.find_element_by_class_name("a-button").click()
print(driver.current_url)

def restarting(isRestart):
    if isRestart:
        try:
            #  restart =driver.find_elements_by_link_text("Перезагрузите сервер")
            restart=driver.find_elements_by_class_name("ui-corner-all");
        except Exception as e:
            # english version
            restart =driver.find_elements_by_link_text("Restart server")
        if isinstance(restart, list):
            for i in restart:
                print(f"'{i.text}'")
                if i.text == 'Перезапустить сервер':
                    print(f"found '{i.text}' and restart server")
                    i.click()
                    time.sleep(2)
                    break
        print("restarting!!")

def main():
    try:
        restarting(isRestart)
        time.sleep(5)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
