# -*- coding: utf-8 -*-

"""
Created: 2024-02-03 15:57:31
Last Modified: 2024-02-03 15:59:04
"""

from django.db import models


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    alias = models.CharField(max_length=255, null=True, blank=True)
    uk = models.BigIntegerField()
    serverFileName = models.CharField(max_length=255)
    type = models.IntegerField()
    path = models.CharField(max_length=255)
    fsId = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.serverFileName
