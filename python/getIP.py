import time
from selenium import webdriver
from selenium.webdriver.common.proxy import *

myProxy = "socks5://127.0.0.1:1080"

def my_proxy(PROXY_HOST,PROXY_PORT):
        fp = webdriver.FirefoxProfile()
        # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
        print(PROXY_PORT)
        print(PROXY_HOST)
        fp.set_preference("network.proxy.type", 1)
        # fp.set_preference("network.proxy.http",PROXY_HOST)
        # fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
        # fp.set_preference("network.proxy.https",PROXY_HOST)
        # fp.set_preference("network.proxy.https_port",int(PROXY_PORT))
        # fp.set_preference("network.proxy.ssl",PROXY_HOST)
        # fp.set_preference("network.proxy.ssl_port",int(PROXY_PORT))
        # fp.set_preference("network.proxy.ftp",PROXY_HOST)
        # fp.set_preference("network.proxy.ftp_port",int(PROXY_PORT))
        fp.set_preference("network.proxy.socks",PROXY_HOST)
        fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))
        fp.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A")
        fp.update_preferences()
        return webdriver.Firefox(firefox_profile=fp)

# browser = webdriver.Firefox(proxy=proxy)
# 代理端口
browser = my_proxy("127.0.0.1", "1080")
browser.maximize_window()
browser.implicitly_wait(15)

browser.get("http://ifconfig.me/ip")
time.sleep(1)
try:
	# el = browser.find_element_by_xpath('/html/body/pre')
	el = browser.find_element_by_css_selector('body > pre:nth-child(1)')
	if el:
		print(el)
except Exception as e:
	pass
time.sleep(1)
print(browser.current_url)  # current_url 方法可以得到当前页面的URL
browser.quit()
