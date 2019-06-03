# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyperclip


# for _ in range(10):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(0.5)


def scrollToEnd(brower):
    # from selenium.webdriver.common.keys import Keys
    # html = browser.find_element_by_tag_name('html')
    # html.send_keys(Keys.END)
    SCROLL_PAUSE_TIME = 0.6
    time.sleep(SCROLL_PAUSE_TIME)
    while True:
        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling
        last_height = brower.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        brower.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = brower.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            # try again (can be removed)
            brower.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = brower.execute_script(
                "return document.body.scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue


def contentExtract(pageNum):
    pageInput.clear()
    pageInput.send_keys(str(pageNum))
    pageInput.send_keys(u'\ue007')
    pageElemId = "pageNo-" + str(pageNum)
    print(pageElemId)
    time.sleep(1)
    elem = browser.find_element_by_id(pageElemId)
    subelems = elem.find_elements_by_class_name("reader-word-layer")

    def getYpos(e):
        """获取一个字符block的style里面的top属性，相关的regex在函数外面已经compile完成"""
        mo = reTopVal.search(e.get_attribute('style'))
        return mo.group(1)

    def lineMerging(elems):
        """根据位置top信息判断是否属于一行，如果是新的一行加上换行符以后再连接文字"""
        topTemp = ""
        rstString = ""
        for e in elems:
            if topTemp == getYpos(e):
                rstString += e.text
            else:
                topTemp = getYpos(e)
                rstString += '\r\n' + e.text
        return rstString

    return lineMerging(subelems)


# 文库地址
# url='https://wenku.baidu.com/view/6b5d50c608a1284ac850438e.html'  # 分页大于50页
url = 'https://wenku.baidu.com/view/c5c9b8f0d4bbfd0a79563c1ec5da50e2524dd113.html'
url = 'https://wenku.baidu.com/view/d8f922f4eefdc8d377ee3298.html?sxts=1559283875938'
browser = webdriver.Firefox()
browser.get(url=url)
# first finishe fire up the driver and load the page
browser.fullscreen_window()

scrollToEnd(browser)
# 不延时会找不到moreBth
waitBtn = True
while waitBtn:
    time.sleep(1)
    try:
        moreBtn = browser.find_element_by_class_name('moreBtn')
        moreBtn.click()
        waitBtn = False
    except Exception as e:
        print('错误！增加延时等待时间')
pageInput = browser.find_element_by_class_name('page-input')
datalist = []
reTopVal = re.compile(r'top: (\d+)px')

pageTtl = int(browser.find_element_by_class_name('page-count').text[1:])
# 这里根据最大页码手动填写一下范围。如果最大页码在50页以内就可以直接用pageTtl，但是如果超过了50页，这里要分两块才行
for i in range(pageTtl):
    print(i + 1)
    datalist.append(contentExtract(i + 1))
pyperclip.copy('\r\n'.join(datalist))

browser.close()
