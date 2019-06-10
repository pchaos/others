# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     run.py
   Description : 下载对应的公告
   Author :       pchaos
   date：          2019/5/28
-------------------------------------------------
   Change Activity:
                   2019/5/28:
-------------------------------------------------
"""


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    # __file__ should be defined in this case
    PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(PARENT_DIR)
    from cninfo import *

    # 更新公告
    save_cninfo()
    download_anance()