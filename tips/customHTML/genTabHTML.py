# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     genTabHTML
   Description : css tab styles
   Author :       pchaos
   date：          2019/9/8
-------------------------------------------------
   Change Activity:
                   2019/9/8:
-------------------------------------------------
"""
__author__ = 'pchaos'

from .genHTML import genHTML


class genTABHTML(genHTML):
    @classmethod
    def replaceTxt(cls, txt, src_str, to_replaced_str) -> str:
        return txt.replace(src_str, to_replaced_str)
