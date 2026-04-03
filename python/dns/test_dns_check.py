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

from dns_check import (
    check_dns_availability,
    check_dns_availability_query,
    check_dns_availability_with_country,
    get_country_from_ip,
)


class TestDNSCheck(unittest.TestCase):
    @patch("dns.resolver.Resolver")
    def test_check_dns_availability(self, mock_resolver):
        # Mock the resolver and its methods
        mock_resolver_instance = MagicMock()
        mock_resolver.return_value = mock_resolver_instance
        mock_resolver_instance.resolve.return_value = [MagicMock(address="1.2.3.4")]

        dns_list = ["8.8.8.8", "1.1.1.1"]
        result = check_dns_availability(dns_list)

        self.assertEqual(result, dns_list)

    @patch("dns.resolver.Resolver")
    def test_check_dns_availability_query(self, mock_resolver):
        # Mock the resolver and its methods
        mock_resolver_instance = MagicMock()
        mock_resolver.return_value = mock_resolver_instance
        mock_resolver_instance.query.return_value = [MagicMock(address="1.2.3.4")]

        dns_list = ["8.8.8.8", "114.114.1.1"]
        result = check_dns_availability_query(dns_list)

        self.assertEqual(result, dns_list, f"Expected {dns_list}, but got {result}")

    @patch("dns_check.geoip2.database.Reader")
    @patch("dns_check.requests.get")
    # 这两行代码使用了Python的unittest.mock模块中的patch装饰器。
    # @patch('dns_check.geoip2.database.Reader') 模拟了geoip2.database.Reader类，用于测试时替换真实的GeoIP数据库读取操作。
    # @patch('dns_check.requests.get') 模拟了requests.get函数，用于测试时替换真实的HTTP请求操作。
    # 这些模拟（mock）允许我们在不实际访问外部资源（如GeoIP数据库或进行HTTP请求）的情况下进行单元测试。
    def test_get_country_from_ip_mock(self, mock_get, mock_reader):
        country_map = {
            "1.1.1.1": "United States",
            "101.167.180.1": "Singapore",
            "p19992003.duckdns.org": "China",
            "45.202.243.213": "China",
        }

        def country_side_effect(*args, **kwargs):
            ip = kwargs.get("ip_address", args[0] if args else None)
            mock_response = MagicMock()
            mock_response.country.name = country_map.get(ip, "Unknown")
            return mock_response

        mock_reader_instance = MagicMock()
        mock_reader.return_value.__enter__.return_value = mock_reader_instance
        mock_reader_instance.country.side_effect = country_side_effect

        def mock_get_side_effect(*args, **kwargs):
            url = args[0] if args else kwargs.get("url", "")
            mock_resp = MagicMock()
            if "ip-api.com" in url:
                ip = url.split("/")[-1]
                mock_resp.json.return_value = {
                    "country": country_map.get(ip, "Unknown")
                }
            else:
                mock_resp.status_code = 200
            return mock_resp

        mock_get.side_effect = mock_get_side_effect

        ip_address = "1.1.1.1"
        result = get_country_from_ip(ip_address)
        self.assertEqual(
            result,
            "United States",
            f"{ip_address} Expected 'United States', but got {result}",
        )

        ip_address = "101.167.180.1"
        result = get_country_from_ip(ip_address)
        self.assertEqual(
            result, "Singapore", f"{ip_address} Expected 'Singapore', but got {result}"
        )

        ip_address = "p19992003.duckdns.org"
        result = get_country_from_ip(ip_address)
        self.assertIn(
            result,
            ["China", "United States"],
            f"{ip_address} Expected 'China' or 'United States', but got {result}",
        )

        ip_address = "101.167.180.1"
        result = get_country_from_ip(ip_address)
        self.assertEqual(
            result, "Singapore", f"{ip_address} Expected 'Singapore', but got {result}"
        )

        ip_address = "p19992003.duckdns.org"
        result = get_country_from_ip(ip_address)
        self.assertIn(
            result,
            ["China", "United States"],
            f"{ip_address} Expected 'China' or 'United States', but got {result}",
        )

    def test_get_country_from_ip(self):
        ip_address = "1.0.0.1"
        result = get_country_from_ip(ip_address)
        self.assertEqual(
            result, "Australia", f"{ip_address} Expected 'Australia', but got {result}"
        )

        ip_address = "www.mfa.gov.sg"
        result = get_country_from_ip(ip_address)
        self.assertEqual(
            result,
            "United States",
            f"{ip_address} Expected 'United States', but got {result}",
        )

        ip_address = "p19992003.duckdns.org"
        result = get_country_from_ip(ip_address)
        self.assertIn(
            result,
            ["China", "United States"],
            f"{ip_address} Expected 'China' or 'United States', but got {result}",
        )

    @patch("dns_check.get_country_from_ip")
    @patch("dns.resolver.query")
    def test_check_dns_availability_with_country(self, mock_query, mock_get_country):
        # Mock dns.resolver.query (module-level function used in check_dns_availability_with_country)
        mock_query.return_value = [MagicMock(address="1.2.3.4")]

        # Mock the get_country_from_ip function
        mock_get_country.return_value = "United States"

        dns_list = ["8.8.8.8", "1.1.1.1"]
        result = check_dns_availability_with_country(dns_list)

        expected_result = [
            {"ip": "8.8.8.8", "country": "United States"},
            {"ip": "1.1.1.1", "country": "United States"},
        ]
        self.assertEqual(
            result, expected_result, f"Expected {expected_result}, but got {result}"
        )


if __name__ == "__main__":
    unittest.main()
