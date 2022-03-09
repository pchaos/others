# -*- coding: utf-8 -*- #
import os
#  import json
import time
#  import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
#  PROXY = "127.0.0.1:1080"  #  HOST:PORT
PROXY = "socks5://127.0.0.1:1081"  #  HOST:PORT
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = headless
if isProxy:
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_argument("ignore-certificate-errors")
chrome_options.add_argument("--window-size=1360,1080")
chrome_options.add_argument("--lang=en-us")
chrome_options.add_argument("--incognito")
# 关闭提示条：”Chrome 正受到自动测试软件的控制”
chrome_options.add_argument("--disable-infobars")
# 不加载图片, 提升速度
chrome_options.add_argument('blink-settings=imagesEnabled=false')

driver = webdriver.Chrome(options=chrome_options)
#  driver.get("https://www.ipchicken.com/")
try:
    driver.get("https://www.justhost.ru/")
except Exception as e:
    print("url timeout.")
    time.sleep(3)
finally:
    driver.get("https://www.justhost.ru/")

if os.path.exists(cookieFileName):
    #  url = 'https://justhost.ru'
    cookies = pickle.load(open(cookieFileName, "rb"))
    print(f"loading cookies:{cookies}")
    for cookie in cookies:
        #  print(f"loading cookies:{cookie}")
        driver.add_cookie(cookie)

url = "https://justhost.ru/billing/active"
#  url = "https://justhost.ru/auth/login/"
driver.get(url)

try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login")) )
    #  driver.find_element(By.ID,'login').send_keys(email)  # enter your email
    username = driver.find_element(By.ID, 'login')  # enter your email
    print(f"{username=}, {email=}")
    print(f"{dir(username)}")
    if username:
        username.send_keys(email)
    driver.find_element(By.NAME,
                        'password').send_keys(password)  # enter your password
    print(f"passwd:{password}")
    time.sleep(1.5)
    #  loginbutton = driver.find_element_by_class_name('nextButton')
    loginbutton = driver.find_element(By.CLASS_NAME, 'nextButton')
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
#  driver.find_element_by_class_name("a-button").click()
driver.find_element(By.CLASS_NAME, "a-button").click()
print(driver.current_url)


def restarting(isRestart):
    if isRestart:
        try:
            #  restart =driver.find_elements_by_link_text("Перезагрузите сервер")
            #  restart=driver.find_elements_by_class_name("ui-corner-all");
            restart = driver.find_elements(By.CLASS_NAME, "ui-corner-all")
        except Exception as e:
            # english version
            restart = driver.find_elements(By.LINK_TEXT, "Restart server")
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
