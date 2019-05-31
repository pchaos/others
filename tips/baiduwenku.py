# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyperclip
browser = webdriver.Firefox()
browser.get('https://wenku.baidu.com/view/6b5d50c608a1284ac850438e.html')
# first finishe fire up the driver and load the page

moreBtn = browser.find_element_by_class_name('moreBtn')
moreBtn.click()
pageInput = browser.find_element_by_class_name('page-input')
datalist = []
reTopVal = re.compile(r'top: (\d+)px')
def contentExtract(pageNum):
    pageInput.clear()
    pageInput.send_keys(str(pageNum))
    pageInput.send_keys(u'\ue007')
    pageElemId = "pageNo-"+str(pageNum)
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
pageTtl = int(browser.find_element_by_class_name('page-count').text[1:])
# 这里根据最大页码手动填写一下范围。如果最大页码在50页以内就可以直接用pageTtl，但是如果超过了50页，这里要分两块才行
for i in range(pageTtl):
    print(i+1)
    datalist.append(contentExtract(i+1))
pyperclip.copy('\r\n'.join(datalist))

browser.close()
