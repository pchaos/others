import logging
import re
import sys

from seleniumbase import BaseCase

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DnsTestClass(BaseCase):
    def setUp(self):
        super().setUp()
        self.headed = False  # Disable headed mode to run in headless mode

    def iterate_pages(self, base_url):
        # Get the first page number
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
        last_page = int(re.search(r'page=(\d+)', last_page_link.get_attribute('href')).group(1)) if last_page_link else None

        # Get the step size
        next_page_link = self.find_element('a:contains("下一页")')
        next_page_url = next_page_link.get_attribute('href')
        next_page_number = int(re.search(r'page=(\d+)', next_page_url).group(1))
        step_size = next_page_number - first_page
               
        current_page = first_page
        while last_page is None or current_page <= last_page:
            url = f"{base_url}&page={current_page}"
            yield url, current_page
            current_page += step_size
    def test_singapore_dns(self):
        base_url = "https://dns.supfree.net/mabi.asp?id=SG"
        page = 1
        last_page_number = None
        for url, page in self.iterate_pages(base_url):
            html_content = self.get_html_content(url)
            if self.headless:
                self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                self.scroll_to_bottom()

            self.sleep(1)  # Wait for the page to load

            logger.debug(f"HTML Content: {html_content}")
            page_dns_servers = extract_dns_ips(html_content)
            if 'dns_servers' not in locals():
                dns_servers = []
            dns_servers.extend(page_dns_servers)
            logger.info("DNS IP Addresses for this page:")
            for ip in page_dns_servers:
                logger.info(ip)
            logger.info(f"Total DNS IP Addresses on this page: {len(page_dns_servers)}")

        # After the loop ends
        unique_dns_servers = list(dict.fromkeys(dns_servers))
        logger.info(f"Total unique DNS IP Addresses across all pages: {len(unique_dns_servers)}")
        logger.info("All unique DNS IP Addresses:")
        for ip in unique_dns_servers:
            logger.info(ip)

    def get_html_content(self, url):
        self.open(url)
        self.wait_for_element_present("body")
        return self.get_page_source()


def extract_dns_ips(html_content):
    ip_pattern = r'<td>(\b(?:\d{1,3}\.){3}\d{1,3}\b)'
    dns_ips = re.findall(ip_pattern, html_content)
    unique_dns_ips = list(dict.fromkeys(dns_ips))
    return unique_dns_ips


if __name__ == "__main__":
    sys.argv = [__file__, "--browser=chrome", "--headed"]
    BaseCase.main(__name__, __file__)
