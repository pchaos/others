# -*- coding: utf-8 -*-

"""
Created: 2024-02-03 15:57:31
Last Modified: 2024-02-06 23:35:00
"""

from django.db import models


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255, null=False)
    alias = models.CharField(max_length=255, null=True, blank=True)
    uk = models.BigIntegerField()  # "unit of kilobyte"??
    fileName = models.CharField(max_length=255)
    type = models.IntegerField()
    path = models.CharField(max_length=255)
    fsId = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.fileName

    @classmethod
    def path_json2model(cls, json_data):
        # json_data是解码得到的Python对象
        result = -1
        try:
            if json_data["errorCode"] == 0:
                for item in json_data["result"]:
                    resource = Resource(
                        url='your_url_here',  # 请替换为实际的url值
                        alias=item['alias'],
                        fileName=item['serverFileName'],
                        uk=item['uk'],
                        type=item['type'],
                        path=item['path'],
                        fsId=item['fsId'],
                    )
                    result = resource.save()
        except Exception as e:
            print(f"raise {e}")
            result = -2
        finally:
            return result
