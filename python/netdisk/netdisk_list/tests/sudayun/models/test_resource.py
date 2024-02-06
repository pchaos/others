# -*- coding: utf-8 -*-
"""
# Run tests using: python manage.py test your_app_name.tests
python manage.py test tests.sudayun.models.test_resource

Last Modified: 2024-02-06 11:13:13
"""

# import unittest
from django.db import transaction
from django.test import TestCase
from sudayun.models import Resource


class ResourceModelTest(TestCase):
    def setUp(self):
        # Create a sample Resource instance for testing
        self.resource = Resource.objects.create(
            url="https://www.test.com",
            alias="Sample Alias",
            uk=123456789,
            serverFileName="sample_file.txt",
            type=1,
            path="/sample/path/",
            fsId=987654321,
            remark="Sample Remark",
        )

    def test_resource_str_method(self):
        # Test the __str__ method of the Resource model
        self.assertEqual(str(self.resource), "sample_file.txt")

    def test_resource_fields(self):
        # Test individual fields of the Resource model
        self.assertEqual(self.resource.url, "https://www.test.com")
        self.assertEqual(self.resource.alias, "Sample Alias")
        self.assertEqual(self.resource.uk, 123456789)
        self.assertEqual(self.resource.serverFileName, "sample_file.txt")
        self.assertEqual(self.resource.type, 1)
        self.assertEqual(self.resource.path, "/sample/path/")
        self.assertEqual(self.resource.fsId, 987654321)
        self.assertEqual(self.resource.remark, "Sample Remark")

    @transaction.atomic
    def test_resource_defaults(self):
        # Test default values for optional fields
        resource_with_defaults = Resource.objects.create(
            url="https://www.test.com", serverFileName="default_file.txt", type=2, path="/default/path/", uk=12345678909
        )
        self.assertIsNone(resource_with_defaults.alias)
        self.assertIsNone(resource_with_defaults.fsId)
        self.assertIsNone(resource_with_defaults.remark)

    # Clean up after each test
    def tearDown(self):
        self.resource.delete()
