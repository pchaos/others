# -*- coding=utf-8 -*-

"""获取dns地址，并验证
这个文件是一个Python测试脚本，主要用于获取DNS地址并进行验证。以下是文件的主要内容概括：


2. 导入了必要的模块：logging, re, sys, 和 seleniumbase 中的 BaseCase。

3. 配置了日志系统，设置了日志级别和格式。

4. 定义了一个名为 DnsTestClass 的测试类，继承自 BaseCase：
   - setUp 方法：初始化测试环境，设置为无头模式运行。
   - iterate_pages 方法：这是一个生成器函数，用于遍历网页的不同页面。
     * 打开基础URL并找到首页和末页链接
     * 解析页面编号和步进大小
     * 生成每个页面的URL和页码

5. 这个类似乎是为了抓取多个页面的DNS相关信息而设计的，但具体的DNS测试逻辑尚未实现。

6. 文件使用了 seleniumbase 库，这表明它可能会进行一些web自动化测试。

总的来说，这个文件为DNS地址的获取和验证搭建了一个基础框架，但核心的测试逻辑还需要进一步实现。
"""
import logging
import re
import sys

from seleniumbase import BaseCase
from  dns_check import check_dns_availability

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DnsTestClass(BaseCase):
    def setUp(self):
        super().setUp()
        # Set window size to 90% of screen size and center it
        screen_width = self.driver.execute_script("return window.screen.width;")
        screen_height = self.driver.execute_script("return window.screen.height;")
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.driver.set_window_size(window_width, window_height)
        self.driver.set_window_position(x_position, y_position)

    def iterate_pages(self, base_url):
        """
        遍历网页的不同页面，生成每个页面的URL和页码。

        此函数执行以下操作：
        1. 打开基础URL并找到首页和末页链接。
        2. 解析页面编号和步进大小。
        3. 生成每个页面的URL和页码。

        参数:
        base_url (str): 要遍历的网页的基础URL。

        返回:
        generator: 生成器，每次迭代返回一个元组 (url, current_page)。
        """
        # Get the first page number
        if self.get_current_url() != base_url:
            self.open(base_url)
        first_page_link = self.find_element('a:contains("首页")')
        logger.info(f"First page link: {first_page_link} {first_page_link.get_attribute('href')}")
        first_page = 1
        if first_page_link:
            href = first_page_link.get_attribute('href')
            match = re.search(r'page=(\d+)', href)
            if match:
                first_page = int(match.group(1))

            # Get the last page number
            last_page_link = self.find_element('a:contains("末页")')
            last_page = int(re.search(r'page=(\d+)', last_page_link.get_attribute('href')).group(1)) if last_page_link else 1

            # Get the step size
            next_page_link = self.find_element('a:contains("下一页")')
            next_page_url = next_page_link.get_attribute('href')
            next_page_number = int(re.search(r'page=(\d+)', next_page_url).group(1))
            step_size = next_page_number - first_page
               
        current_page = first_page
        while last_page is None or current_page <= last_page:
            if current_page == 1:
                url = base_url
            else:
                url = f"{base_url}&page={current_page}"
            yield url, current_page
            current_page += step_size

    def test_singapore_dns(self):
        """
        测试新加坡DNS服务器的可用性。

        此方法执行以下操作：
        1. 遍历指定网页的所有页面，提取DNS IP地址。
        2. 收集所有唯一的DNS IP地址。
        3. 检查这些DNS服务器的可用性。
        4. 记录结果。

        步骤详解：
        - 使用基础URL开始遍历页面。
        - 对每个页面，提取HTML内容并解析DNS IP地址。
        - 收集所有页面的DNS IP地址，去重。
        - 使用check_dns_availability函数检查DNS服务器的可用性。
        - 记录各个步骤的结果，包括每页的DNS IP地址、总的唯一DNS IP地址和可用的DNS IP地址。
        """
        base_url = "https://dns.supfree.net/mabi.asp?id=SG"
        dns_servers = []
        for url, page in self.iterate_pages(base_url):
            html_content = self.get_html_content(url)
            self.sleep(0.5)  # 等待页面加载
            if self.headless:
                self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                self.scroll_to_bottom()

            self.sleep(0.5)  # 再次等待页面加载完成

            logger.debug(f"HTML Content: {html_content}")
            tbody_content = extract_tbody(html_content)
            page_dns_servers = extract_dns_ips(tbody_content)
            dns_servers.extend(page_dns_servers)
            logger.info("当前页面的DNS IP地址:")
            for ip in page_dns_servers:
                logger.info(ip)
            logger.info(f"当前页面的DNS IP地址总数: {len(page_dns_servers)}")

        # 遍历结束后的处理
        unique_dns_servers = list(dict.fromkeys(dns_servers))
        logger.info(f"所有页面的唯一DNS IP地址总数: {len(unique_dns_servers)}")
        logger.info("所有唯一的DNS IP地址:")
        for ip in unique_dns_servers:
            logger.info(ip)
        if unique_dns_servers:
            available_dns = check_dns_availability(unique_dns_servers)
            logger.info(f"可用的DNS IP地址: {available_dns}")
    def get_html_content(self, url):
        self.open(url)
        self.wait_for_element_present("body")
        return self.get_page_source()


def extract_dns_ips(html_content):
    """
    从HTML内容中提取唯一的DNS IP地址。

    此函数执行以下操作：
    1. 使用正则表达式匹配HTML中的IP地址。
    2. 从匹配的结果中提取所有IP地址。
    3. 去除重复的IP地址，保留唯一值。
    4. 返回唯一的DNS IP地址列表。

    参数:
    html_content (str): 包含DNS IP地址的HTML内容。

    返回:
    list: 唯一的DNS IP地址列表。
    """
    ip_pattern = r'<td>(\b(?:\d{1,3}\.){3}\d{1,3}\b)</td>'
    dns_ips = re.findall(ip_pattern, html_content)
    unique_dns_ips = list(dict.fromkeys(dns_ips))
    return unique_dns_ips


def extract_tbody(html_content):
    """
    从HTML内容中提取tbody标签的内容。

    此函数执行以下操作：
    1. 使用正则表达式匹配HTML中的tbody标签。
    2. 提取并返回tbody标签的内容。

    参数:
    html_content (str): 包含HTML内容的字符串。

    返回:
    str: tbody标签的内容。
    """
    tbody_pattern = r'<tbody.*?>(.*?)</tbody>'
    match = re.search(tbody_pattern, html_content, re.DOTALL)
    return match.group(1) if match else ''


if __name__ == "__main__":
    sys.argv = [__file__, "--browser=chrome", "--headed"]
    BaseCase.main(__name__, __file__)
