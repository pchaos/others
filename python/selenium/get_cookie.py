"""
1.学习目标:
    掌握selenium对cookie操作
2.语法
    2.1获取所有cookie
        driver.get.cookies（）
        返同列表格式字典类型 [{},{},{}]
    2.2添加cookie
        driver.add_cookie（参数）
        参数：字典格式{"name":"name值","value":"value值"}
3.需求
    实现selenium对cookie操作
"""
# 1.导入selenium
from selenium import webdriver
from time import sleep

# 2.打开浏览器
driver = webdriver.Chrome()

# 3.打开注册A页面
# 不打开一个页面，cookie为[]。
url = "http://www.baidu.com/"
driver.get(url)

# 4.操作cookie
# 4.1 获取cookie
cookies = driver.get_cookies()
for cookie in cookies:
    # 值打印cookie中的name和value
    print("%s -> %s" % (cookie["name"], cookie["value"]))

print("=======================")
# 4.2 获取一个cookie的指定属性值
# 参数是一个cookie中name的属性值
# 没有找到返回None
print(driver.get_cookie("BAIDUID"))

print("=======================")
# 4.3 添加cookie
cookie = {"name": "key-aaaaaaa", "value": "value-aaaaaaa"}
driver.add_cookie(cookie)

# 添加后再次获取
cookies = driver.get_cookies()
for cookie in cookies:
    print("%s -> %s" % (cookie["name"], cookie["value"]))

print("=======================")
# 4.4 删除指定cookie
# 根据name删除
driver.delete_cookie("key-aaaaaaa")
# 删除后再次获取
cookies = driver.get_cookies()
for cookie in cookies:
    print("%s -> %s" % (cookie["name"], cookie["value"]))

print("=======================")
# 4.5 删除全部cookie
driver.delete_all_cookies()
print(driver.get_cookies())

# 5.关闭浏览器
sleep(2)
driver.quit()
