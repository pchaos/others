# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     config.py
   Description :
   Author :       pchaos
   date：          18-12-18
-------------------------------------------------
   Change Activity:
                   18-12-18:
-------------------------------------------------
"""
__author__ = 'pchaos'

from configparser import ConfigParser

Config = ConfigParser.ConfigParser()

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
