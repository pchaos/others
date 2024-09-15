# -*- coding=utf-8 -*-
"""test dns_check.py
pytest test_dns_check.py::TestDNSCheck
pytest test_dns_check.py::TestDNSCheck::test_get_country_from_ip
pytest test_dns_check.py::TestDNSCheck::test_check_dns_availability_with_country
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dns_check import (check_dns_availability, check_dns_availability_query,
                       check_dns_availability_with_country,
                       get_country_from_ip)


class TestDNSCheck(unittest.TestCase):

    @patch('dns.resolver.Resolver')
    def test_check_dns_availability(self, mock_resolver):
        # Mock the resolver and its methods
        mock_resolver_instance = MagicMock()
        mock_resolver.return_value = mock_resolver_instance
        mock_resolver_instance.resolve.return_value = [MagicMock(address='1.2.3.4')]

        dns_list = ['8.8.8.8', '1.1.1.1']
        result = check_dns_availability(dns_list)

        self.assertEqual(result, dns_list)

    @patch('dns.resolver.Resolver')
    def test_check_dns_availability_query(self, mock_resolver):
        # Mock the resolver and its methods
        mock_resolver_instance = MagicMock()
        mock_resolver.return_value = mock_resolver_instance
        mock_resolver_instance.query.return_value = [MagicMock(address='1.2.3.4')]

        dns_list = ['8.8.8.8', '114.114.1.1']
        result = check_dns_availability_query(dns_list)

        self.assertEqual(result, dns_list, f"Expected {dns_list}, but got {result}")

    @patch('geoip2.database.Reader')
    @patch('requests.get')
    # 这两行代码使用了Python的unittest.mock模块中的patch装饰器。
    # @patch('geoip2.database.Reader') 模拟了geoip2.database.Reader类，用于测试时替换真实的GeoIP数据库读取操作。
    # @patch('requests.get') 模拟了requests.get函数，用于测试时替换真实的HTTP请求操作。
    # 这些模拟（mock）操作允许我们在不实际访问外部资源（如GeoIP数据库或进行HTTP请求）的情况下进行单元测试。
    def test_get_country_from_ip_mock(self, mock_get, mock_reader):
        # Mock the GeoIP2 reader
        mock_reader_instance = MagicMock()
        mock_reader.return_value.__enter__.return_value = mock_reader_instance
        mock_reader_instance.country.return_value.country.name = 'United States'

        # Mock the requests.get for database download
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        ip_address = '1.1.1.1'
        # result = get_country_from_ip('8.8.8.8')
        result = get_country_from_ip(ip_address)
        self.assertEqual(result, 'United States', f"{ip_address} Expected 'United States', but got {result}")

        ip_address = '101.167.180.1'
        result = get_country_from_ip(ip_address)
        self.assertEqual(result, 'Singapore', f"{ip_address} Expected 'Singapore', but got {result}")

        ip_address = 'p19992003.duckdns.org'
        result = get_country_from_ip(ip_address)
        self.assertEqual(result, 'China', f"{ip_address} Expected 'China', but got {result}")

    def test_get_country_from_ip(self):
        ip_address = '1.0.0.1'
        result = get_country_from_ip(ip_address)
        # self.assertEqual(result, 'Australia', f"{ip_address} Expected 'Australia', but got {result}")

        ip_address = '101.167.180.1'
        result = get_country_from_ip(ip_address)
        self.assertEqual(result, 'Singapore', f"{ip_address} Expected 'Singapore', but got {result}")

        ip_address = 'p19992003.duckdns.org'
        result = get_country_from_ip(ip_address)
        self.assertEqual(result, 'China', f"{ip_address} Expected 'China', but got {result}")


    @patch('dns.resolver.Resolver')
    @patch('dns_check.get_country_from_ip')
    def test_check_dns_availability_with_country(self, mock_get_country, mock_resolver):
        # Mock the resolver and its methods
        mock_resolver_instance = MagicMock()
        mock_resolver.return_value = mock_resolver_instance
        mock_resolver_instance.query.return_value = [MagicMock(address='1.2.3.4')]

        # Mock the get_country_from_ip function
        mock_get_country.return_value = 'United States'

        dns_list = ['8.8.8.8', '1.1.1.1']
        result = check_dns_availability_with_country(dns_list)

        expected_result = [{'ip': '8.8.8.8', 'country': 'United States'}, {'ip': '1.1.1.1', 'country': 'United States'}]
        self.assertEqual(result, expected_result, f"Expected {expected_result}, but got {result}")


if __name__ == '__main__':
    unittest.main()
