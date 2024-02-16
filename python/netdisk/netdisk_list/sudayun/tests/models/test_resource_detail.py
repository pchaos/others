# -*- coding: utf-8 -*-
"""
Last Modified: 2024-02-07 01:28:21
"""

from datetime import datetime

from django.test import TestCase
from sudayun.models import Resource_detail


class ResourceDetailTestCase(TestCase):
    def test_fullpath(self):
        resource = Resource_detail(
            id=1,
            fileName='file1',
            path='/path/to/file1',
            fsId=12345,
            category=4,
            size=1024,
            fileTime=datetime.now(),
            isDir=False,
            remark='Test file',
        )
        self.assertEqual(resource.fullpath(), 'file1')

    def test_categoryName(self):
        from copy import deepcopy

        resource = Resource_detail(
            id=1,
            fileName='file1',
            path='/path/to/file1',
            fsId=12345,
            category=4,
            size=1024,
            fileTime=datetime.now(),
            isDir=False,
            remark='Test file',
        )

        resource1 = deepcopy(resource)
        resource2 = deepcopy(resource)
        resource3 = deepcopy(resource)
        resource4 = deepcopy(resource)
        resource1.category = 6
        resource2.category = 2
        resource3.category = 4
        resource4.category = 8  # 未知分类

        # print(f"{resource1.categoryName()=}")
        self.assertEqual(resource.categoryName(), '文件')
        self.assertEqual(resource1.categoryName(), "目录", f"目录{resource1.category} {resource1.categoryName()=}")
        self.assertEqual(resource2.categoryName(), '说明文件')
        self.assertEqual(resource3.categoryName(), '文件')
        self.assertEqual(resource4.categoryName(), '未知分类')

    def test_list_json2model(self):
        json_data = {
            "errorCode": 0,
            "result": [
                {
                    "serverFileName": "file1",
                    "path": "/path/to/file1",
                    "fsId": 12345,
                    "category": 4,
                    "size": 1024,
                    "fileTime": 1704116871,
                    "isDir": False,
                }
            ],
        }
        parentId = None  # Replace with actual parent object
        result = Resource_detail.list_json2model(json_data, parentId)
        # self.assertEqual(result, 1)  # Assuming the resource was successfully saved
        # self.assertIsNone(result, f"Resource save error {result}")
        self.assertIsNone(result, f"Resource save error {result}")
