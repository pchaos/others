import unittest
from mock import Mock
from mock import patch
import requests

from os import sys, path
# __file__ should be defined in this case
PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
print("上级目录：", PARENT_DIR)
sys.path.append(PARENT_DIR)
from pymock import api
 
 
class TetsApi(unittest.TestCase):
 
    def test_api(self):
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            assert api().status_code == 200
            print("mock api url:", api().url)

if __name__ == '__main__' and __package__ is None:

    # from pymock import *
    unittest.main()