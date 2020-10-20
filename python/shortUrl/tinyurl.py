# -*- coding: utf-8 -*-
""" python tinyurl.py https://www.duckduckgo.com
"""
import urllib.request
import sys

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

url = sys.argv[1]
print(url)
print(tiny_url(url))
