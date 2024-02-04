# -*- coding: utf-8 -*-
"""
Created: 2024-02-03 16:04:30
Last Modified: 2024-02-03 16:39:03

"""
from django.db import models
from django.db.models import Case, When


class Resource_detail(models.Model):
    id = models.AutoField(primary_key=True)
    serverFileName = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    fsId = models.BigIntegerField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    category = models.IntegerField()
    size = models.BigIntegerField(null=True, blank=True)
    serverTime = models.DateTimeField(null=True, blank=True)
    isDir = models.BooleanField(default=False)
    remark = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.serverFileName + ' (' + str(self.category) + ')'

    def fullpath(self):
        if self.parentId:
            return self.parentId.fullpath() + '/' + self.serverFileName
        else:
            return self.serverFileName

    def categoryName(self):
        return Case(
            When(category=6, then='目录'), When(category=2, then='说明'), When(category=4, then='文件'), default='未知分类'
        )
