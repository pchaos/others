# -*- coding: utf-8 -*-
"""
# Run tests using: python manage.py test your_app_name.tests
python manage.py test sudayun.tests.models.test_resource -v 2

Last Modified: 2024-02-16 18:26:06
"""


from django.test import TestCase
from sudayun.models import Resource


class ResourceModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print("test:\npython manage.py test tests.sudayun.models.test_resource -v 2")

    def setUp(self):
        # Create a sample Resource instance for testing
        self.resource = Resource.objects.create(
            url="https://www.test.com",
            alias="Sample Alias",
            uk=123456789,
            fileName="sample_file.txt",
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
        self.assertEqual(self.resource.fileName, "sample_file.txt")
        self.assertEqual(self.resource.type, 1)
        self.assertEqual(self.resource.path, "/sample/path/")
        self.assertEqual(self.resource.fsId, 987654321)
        self.assertEqual(self.resource.remark, "Sample Remark")

    def test_resource_defaults(self):
        # Test default values for optional fields
        resource_with_defaults = Resource.objects.create(
            url="https://www.test.com", fileName="default_file.txt", type=2, path="/default/path/", uk=12345678909
        )
        self.assertIsNone(resource_with_defaults.alias)
        self.assertIsNone(resource_with_defaults.fsId)
        self.assertIsNone(resource_with_defaults.remark)

    def test_path_json2model(self):
        import json

        data = b'{"msg":"ok","errorCode":0,"result":[{"id":3632,"alias":null,"uk":1102622597917,"serverFileName":"\xe6\x95\x99\xe8\x82\xb2\xe4\xb8\x80\xe5\x8c\xba","type":1,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe6\x95\x99\xe8\x82\xb2\xe4\xb8\x80\xe5\x8c\xba","fsId":null},{"id":3633,"alias":null,"uk":1102622597917,"serverFileName":"\xe6\x95\x99\xe8\x82\xb2\xe4\xba\x8c\xe5\x8c\xba","type":1,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe6\x95\x99\xe8\x82\xb2\xe4\xba\x8c\xe5\x8c\xba","fsId":null},{"id":3634,"alias":null,"uk":1102622597917,"serverFileName":"\xe6\x95\x99\xe8\x82\xb2\xe4\xb8\x89\xe5\x8c\xba","type":1,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe6\x95\x99\xe8\x82\xb2\xe4\xb8\x89\xe5\x8c\xba","fsId":null},{"id":3635,"alias":null,"uk":1102622597917,"serverFileName":"\xe6\x95\x99\xe8\x82\xb2\xe8\xb5\x84\xe6\x96\x99\xe4\xb8\x80","type":1,"path":"/\xe6\x95\x99\xe8\x82\xb2\xe8\xb5\x84\xe6\x96\x99\xe4\xb8\x80","fsId":null},{"id":3636,"alias":null,"uk":1102622597917,"serverFileName":"\xe8\x8b\xb1\xe8\xaf\xad\xe4\xb8\x93\xe5\x8c\xba","type":1,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe8\x8b\xb1\xe8\xaf\xad\xe4\xb8\x93\xe5\x8c\xba","fsId":null},{"id":6305,"alias":null,"uk":1102622597917,"serverFileName":"\xe5\xa5\xbd\xe8\xaf\xbe\xe6\x94\xb6\xe9\x9b\x86","type":1,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe5\xa5\xbd\xe8\xaf\xbe\xe6\x94\xb6\xe9\x9b\x86","fsId":null}]}'
        decoded_data = data.decode('utf-8')  # 将字节字符串解码为普通字符串
        json_data = json.loads(decoded_data)  # 解码JSON字符串为Python对象
        print(json_data)
        result = Resource.path_json2model(json_data)
        self.assertIsNone(result, f"Resource save error {result}")

    # Clean up after each test
    def tearDown(self):
        self.resource.delete()

    @classmethod
    def tearDownClass(cls):
        print("test done!!!")
