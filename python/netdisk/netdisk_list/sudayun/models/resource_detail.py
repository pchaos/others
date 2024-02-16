# -*- coding: utf-8 -*-
"""
Created: 2024-02-03 16:04:30
Last Modified: 2024-02-11 20:21:54

"""
import datetime

from django.db import models
# from django.db.models import Case, When
from pytz import timezone


class Resource_detail(models.Model):
    id = models.AutoField(primary_key=True)
    fileName = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    fsId = models.BigIntegerField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    category = models.IntegerField()
    size = models.BigIntegerField(null=True, blank=True)
    fileTime = models.DateTimeField(verbose_name="文件时间", null=True, blank=True)
    isDir = models.BooleanField(verbose_name="是否目录", default=False)
    remark = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.fileName + ' (' + str(self.category) + ')'

    def fullpath(self):
        if self.parentId:
            return self.parentId.fullpath() + '/' + self.fileName
        else:
            return self.fileName

    def categoryName(self):
        if self.category == 6:
            return '目录'
        elif self.category == 2:
            return '说明文件'
        elif self.category == 4:
            return '文件'
        else:
            return '未知分类'

    # def categoryName(self):
    #     # python >= 3.10
    #     return Case(
    #         When(category=6, then='目录'), When(category=2, then='说明文件'), When(category=4, then='文件'), default='未知分类'
    #     )

    @classmethod
    def list_json2model(cls, json_data, parentId):
        def timestamp2timezone(timestamp):
            # datetime.datetime.utcfromtimestamp
            utc_dt = datetime.datetime.utcfromtimestamp(timestamp)

            # 将 UTC 时间转换为带时区的 datetime 对象
            aware_utc_dt = timezone('UTC').localize(utc_dt)
            return aware_utc_dt

        # json_data是解码得到的Python对象
        result = -1
        try:
            if json_data["errorCode"] == 0:
                for item in json_data["result"]:
                    resource = Resource_detail(
                        fileName=item['serverFileName'],
                        path=item['path'],
                        fsId=item['fsId'],
                        category=item['category'],
                        size=item["size"],
                        # fileTime=datetime.datetime.utcfromtimestamp(int(item['fileTime'])),
                        fileTime=timestamp2timezone(int(item['fileTime'])),
                        isDir=item['isDir'],
                        parentId=parentId,
                    )
                    result = resource.save()
        except Exception as e:
            print(f"raise {e}")
            result = -2
        finally:
            return result
