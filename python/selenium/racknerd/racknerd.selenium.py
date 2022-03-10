# -*- coding: utf-8 -*- #
import os
#  import json
import time
#  import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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
    filename = "racknerd"
cookieFileName = f'cookies.{filename}.pkl'
#  PROXY = "127.0.0.1:1080"  #  HOST:PORT
PROXY = "socks5://127.0.0.1:1081"  #  HOST:PORT
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = headless
if isProxy:
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_argument("ignore-certificate-errors")
chrome_options.add_argument("--window-size=1280,1080")
chrome_options.add_argument("--lang=en-us")
chrome_options.add_argument("--incognito")
# 关闭提示条：”Chrome 正受到自动测试软件的控制”
chrome_options.add_argument("--disable-infobars")
# 不加载图片, 提升速度
chrome_options.add_argument('blink-settings=imagesEnabled=false')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.ipchicken.com/")
#  driver.get("https://my.racknerd.com/index.php")
driver.get("https://www.racknerd.com")
if os.path.exists(cookieFileName):
    #  url = 'https://justhost.ru'
    cookies = pickle.load(open(cookieFileName, "rb"))
    for cookie in cookies:
        print(f"loading cookies:{cookie}")
        driver.add_cookie(cookie)
else:
    pass

url = "https://my.racknerd.com/index.php"
driver.get(url)

try:
    driver.find_element_by_name('username').send_keys(
        email)  # enter your email
    driver.find_element_by_name('password').send_keys(
        password)  # enter your password
    #  print(f"passwd:{password}")
    time.sleep(1.5)
    loginbutton = driver.find_element_by_class_name('btn-primary')
    if loginbutton:
        loginbutton.click()
    time.sleep(2)

    if os.path.exists(cookieFileName):
        # 重新登录系统，删除以前的cookie文件
        os.remove(cookieFileName)
        print("loading cookies")
except Exception as e:
    print("using cookies, no need login")
    print(e.args)

url = 'https://my.racknerd.com/clientarea.php'


def checkurl(url):
    counts = 100
    print("waiting ", end='')
    for i in range(counts):
        time.sleep(2)
        #  if driver.current_url != url:
        if url in driver.current_url:
            print(driver.current_url)
            driver.switch_to.default_content()
            break
        print(".", end='', flush=True)


checkurl(url)

if not os.path.exists(cookieFileName):
    # 保存cookies，下次免登录
    pickle.dump(driver.get_cookies(), open(cookieFileName, "wb"))

driver.find_element_by_id(
    "ClientAreaHomePagePanels-Active_Products_Services-0").click()
url = 'https://my.racknerd.com/clientarea.php?action=productdetails'
checkurl(url)
time.sleep(1)
# scroll to end
#  driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
current_y = (driver.execute_script('return window.innerHeight') /
             2) + driver.execute_script('return window.pageYOffset')
scroll_y_by = current_y + 100
driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

#  reboot button
#  driver.find_element_by_class_name("btn-default").click()
#  print(driver.current_url)


def restarting(isRestart):
    if isRestart:
        try:
            html = driver.find_element_by_id('main-body')
            if html:
                html.send_keys(Keys.PAGE_DOWN)
            #  restart =driver.find_elements_by_link_text("Перезагрузите сервер")
            restart = driver.find_elements_by_class_name("btn-default")
        except Exception as e:
            restart = driver.find_elements_by_class_name("btn-default")
        if isinstance(restart, list):
            for i in restart:
                print(f"'{i.text}'")
                if i.text.lower() == 'reboot':
                    print(f"found '{i.text}'")
                    i.click()
                    time.sleep(1)
                    delay = 10
                    try:
                        elem = WebDriverWait(driver, delay).until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, 'modal-dialog')))
                        #  elem=driver.find_elements_by_class_name("modal-dialog")
                        if elem:
                            elems = driver.find_elements_by_class_name(
                                "btn-warning")
                            print(f"reboot type:{type(elems)}")
                            if isinstance(elems, list):
                                for el in elems:
                                    try:
                                        print(f"modal element {el}")
                                        print(f"{el.get_attribute('value')}")
                                        el.send_keys("\n")
                                        time.sleep(5)
                                    except Exception as e:
                                        pass
                            else:
                                #  elems.send_keys(Keys.ENTER)
                                #  print(f"reboot type:{type(elems)}")
                                elems = driver.find_elements_by_xpath(
                                    '//*[@id="confirm-reboot"]/div/div/div[3]/input'
                                )
                                if elems:
                                    elems.click()

                    except TimeoutException:
                        print("Loading took too much time!")
                        print("not found modal-dialog")

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
