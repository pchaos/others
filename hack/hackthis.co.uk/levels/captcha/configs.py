# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     configs.py
   Description :
   Author :       pchaos
   date：          18-12-18
-------------------------------------------------
   Change Activity:
                   18-12-18:
-------------------------------------------------
"""
__author__ = 'pchaos'

# from configparser import ConfigParser
import os
from dotenv import load_dotenv

def loadEnv(envFileName="config.env"):
    load_dotenv(envFileName)

# Config = ConfigParser.ConfigParser()
# Config.read("config.env")
#
# def ConfigSectionMap(section):
#     dict1 = {}
#     options = Config.options(section)
#     for option in options:
#         try:
#             dict1[option] = Config.get(section, option)
#             if dict1[option] == -1:
#                 print("skip: %s" % option)
#         except:
#             print("exception on %s!" % option)
#             dict1[option] = None
#     return dict1
#

if __name__ == '__main__':
    configName='config.env'