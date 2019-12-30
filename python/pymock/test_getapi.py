import requests
import unittest
from mock import Mock
from mock import patch
from os import sys, path


def api(url):
    response = requests.get(url)
    return response
 
class TetsApi(unittest.TestCase):

    def setup(self):
        self.url = 'https://www.sohu.com/'
        url = self.url

    def tearDown(self):
        self.url = None

    def test_api_orgin(self):
        url = self.url
        print("url:", url)
        response = api(url)
        print("api response:", response.status_code)
        assert api(url).status_code == 200
        print("api url:", api(url).url)

    def test_api(self):
        # url = 'https://www.sohu.com/'
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            print("api mock response:", api(self.url))
            assert api(self.url).status_code == 200
            print("mock api url:", api(self.url).url)
            assert api(self.url).url == self.url

if __name__ == '__main__' and __package__ is None:
    unittest.main()