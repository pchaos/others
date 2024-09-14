# -*- coding=utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dns_check import (
    check_dns_availability,
    check_dns_availability_query,
    get_country_from_ip,
    check_dns_availability_with_country
)

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

        dns_list = ['8.8.8.8', '1.1.1.1']
        result = check_dns_availability_query(dns_list)
        
        self.assertEqual(result, dns_list)

    @patch('geoip2.database.Reader')
    @patch('requests.get')
    def test_get_country_from_ip(self, mock_get, mock_reader):
        # Mock the GeoIP2 reader
        mock_reader_instance = MagicMock()
        mock_reader.return_value.__enter__.return_value = mock_reader_instance
        mock_reader_instance.country.return_value.country.name = 'United States'

        # Mock the requests.get for database download
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = get_country_from_ip('8.8.8.8')
        
        self.assertEqual(result, 'United States')

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
        
        expected_result = [
            {'ip': '8.8.8.8', 'country': 'United States'},
            {'ip': '1.1.1.1', 'country': 'United States'}
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
    