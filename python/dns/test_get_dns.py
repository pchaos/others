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
import time
import unittest

from seleniumbase import BaseCase
from dns_check import check_dns_availability
import dns.resolver as dns_resolver

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
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
        logger.info(
            f"First page link: {first_page_link} {first_page_link.get_attribute('href')}"
        )
        first_page = 1
        if first_page_link:
            href = first_page_link.get_attribute("href")
            match = re.search(r"page=(\d+)", href)
            if match:
                first_page = int(match.group(1))

            # Get the last page number
            last_page_link = self.find_element('a:contains("末页")')
            last_page = (
                int(
                    re.search(
                        r"page=(\d+)", last_page_link.get_attribute("href")
                    ).group(1)
                )
                if last_page_link
                else 1
            )

            # Get the step size
            next_page_link = self.find_element('a:contains("下一页")')
            next_page_url = next_page_link.get_attribute("href")
            next_page_number = int(re.search(r"page=(\d+)", next_page_url).group(1))
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

        优先从 dns.supfree.net 抓取，如遇 500 错误则回退到 ipshu.com。
        """
        base_url = "https://dns.supfree.net/mabi.asp?id=SG"
        fallback_url = "https://zh-hans.ipshu.com/dns-country/SG"
        dns_servers = []

        self.open(base_url)
        self.wait_for_element_present("body")
        page_source = self.get_page_source()

        if "500 - 内部服务器错误" in page_source:
            logger.warning("dns.supfree.net 返回 500，回退到 ipshu.com")
            self.open(fallback_url)
            self.wait_for_element_present("body")
            html_content = self.get_page_source()
            dns_servers = extract_dns_ips_ipshu(html_content)
        else:
            for url, page in self.iterate_pages(base_url):
                html_content = self.get_html_content(url)
                self.sleep(0.5)
                if self.headless:
                    self.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);"
                    )
                else:
                    self.scroll_to_bottom()
                self.sleep(0.5)

                logger.debug(f"HTML Content: {html_content}")
                tbody_content = extract_tbody(html_content)
                page_dns_servers = extract_dns_ips(tbody_content)
                dns_servers.extend(page_dns_servers)
                logger.info("当前页面的DNS IP地址:")
                for ip in page_dns_servers:
                    logger.info(ip)
                logger.info(f"当前页面的DNS IP地址总数: {len(page_dns_servers)}")

        unique_dns_servers = list(dict.fromkeys(dns_servers))
        logger.info(f"所有页面的唯一DNS IP地址总数: {len(unique_dns_servers)}")
        logger.info("所有唯一的DNS IP地址:")
        for ip in unique_dns_servers:
            logger.info(ip)
        if unique_dns_servers:
            test_dns_servers = unique_dns_servers[:5]
            logger.info(f"仅测试前5个DNS服务器（共{len(unique_dns_servers)}个）")
            available_dns = check_dns_availability(test_dns_servers)
            logger.info(f"可用的DNS IP地址: {available_dns}")

    def test_country_dns_speed_sort(self):
        """
        测试指定国家(CN, US, HK, SG, RU)的DNS服务器，并按响应速度排序。

        此测试将：
        1. 从dns.supfree.net抓取每个国家的DNS服务器（如遇500错误回退到ipshu.com）
        2. 测量每个DNS服务器的响应时间（限制前10个以加快测试）
        3. 按响应时间从快到慢排序
        4. 验证前5个最快的DNS服务器的可用性
        """
        target_countries = ["CN", "US", "HK", "SG", "RU"]
        country_dns_data = []  # 存储 (ip, country, response_time) 元组

        for country in target_countries:
            base_url = f"https://dns.supfree.net/mabi.asp?id={country}"
            fallback_url = f"https://zh-hans.ipshu.com/dns-country/{country}"
            dns_servers = []

            logger.info(f"开始处理 {country} 国家的DNS服务器...")

            self.open(base_url)
            self.wait_for_element_present("body")
            page_source = self.get_page_source()

            if "500 - 内部服务器错误" in page_source:
                logger.warning(
                    f"dns.supfree.net 对 {country} 返回 500，回退到 ipshu.com"
                )
                self.open(fallback_url)
                self.wait_for_element_present("body")
                html_content = self.get_page_source()
                dns_servers = extract_dns_ips_ipshu(html_content)
            else:
                for url, page in self.iterate_pages(base_url):
                    html_content = self.get_html_content(url)
                    self.sleep(0.5)
                    if self.headless:
                        self.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);"
                        )
                    else:
                        self.scroll_to_bottom()
                    self.sleep(0.5)

                    logger.debug(f"HTML Content for {country}: {html_content}")
                    tbody_content = extract_tbody(html_content)
                    page_dns_servers = extract_dns_ips(tbody_content)
                    dns_servers.extend(page_dns_servers)
                    logger.info(f"{country} 当前页面的DNS IP地址:")
                    for ip in page_dns_servers:
                        logger.info(ip)
                    logger.info(
                        f"{country} 当前页面的DNS IP地址总数: {len(page_dns_servers)}"
                    )

            unique_dns_servers = list(dict.fromkeys(dns_servers))
            logger.info(
                f"{country} 所有页面的唯一DNS IP地址总数: {len(unique_dns_servers)}"
            )

            # 限制处理的DNS数量以加快测试（取前10个）
            test_dns_servers = unique_dns_servers[:10]
            logger.info(
                f"{country} 将测试前 {len(test_dns_servers)} 个DNS服务器（共{len(unique_dns_servers)}个）"
            )

            # 测量每个DNS服务器的响应时间
            for dns_ip in test_dns_servers:
                response_time = measure_dns_response_time(dns_ip)
                country_dns_data.append((dns_ip, country, response_time))
                logger.info(
                    f"DNS {dns_ip} ({country}) 响应时间: {response_time:.2f} ms"
                )

        # 按响应时间排序（最快的在前）
        country_dns_data.sort(key=lambda x: x[2])

        logger.info("按响应速度排序的DNS服务器列表:")
        for ip, country, response_time in country_dns_data:
            if response_time == float("inf"):
                logger.info(f"{ip} ({country}): 超时或不可达")
            else:
                logger.info(f"{ip} ({country}): {response_time:.2f} ms")

        # 取前5个最快的DNS服务器进行可用性验证
        top_5_dns = [item[0] for item in country_dns_data[:5]]
        logger.info(f"选取前5个最快的DNS服务器进行可用性测试: {top_5_dns}")

        if top_5_dns:
            available_dns = check_dns_availability(top_5_dns)
            logger.info(f"可用的DNS IP地址: {available_dns}")

            # 验证至少有一些DNS是可用的
            self.assertGreater(len(available_dns), 0, "至少应该有一些DNS服务器是可用的")

    def get_html_content(self, url):
        self.open(url)
        self.wait_for_element_present("body")
        return self.get_page_source()


def extract_dns_ips_ipshu(html_content):
    ip_pattern = r'<a href="/dns-ip/[^"]*">(\b(?:\d{1,3}\.){3}\d{1,3}\b)</a>'
    dns_ips = re.findall(ip_pattern, html_content)
    return list(dict.fromkeys(dns_ips))


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
    ip_pattern = r"<td>(\b(?:\d{1,3}\.){3}\d{1,3}\b)</td>"
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
    tbody_pattern = r"<tbody.*?>(.*?)</tbody>"
    match = re.search(tbody_pattern, html_content, re.DOTALL)
    return match.group(1) if match else ""


def measure_dns_response_time(dns_server, qname="www.dnspython.org"):
    """
    测量DNS服务器的响应时间（毫秒）。

    参数:
    dns_server (str): DNS服务器IP地址
    qname (str): 要查询的域名，默认为www.dnspython.org

    返回:
    float: 响应时间（毫秒），如果超时或出错则返回无穷大
    """
    try:
        res = dns_resolver.Resolver(configure=False)
        res.nameservers = [dns_server]
        res.timeout = 5  # 5秒超时
        res.lifetime = 5

        start_time = time.time()
        res.try_ddr()
        answers = res.resolve(qname, "A", tcp=True)
        end_time = time.time()

        if answers:
            response_time = (end_time - start_time) * 1000  # 转换为毫秒
            return response_time
        else:
            return float("inf")
    except Exception:
        return float("inf")  # 返回无穷大表示超时或失败


if __name__ == "__main__":
    sys.argv = [__file__, "--browser=chrome", "--headed"]
    BaseCase.main(__name__, __file__)
