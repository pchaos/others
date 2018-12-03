from PIL import Image
import requests
import os, errno
import tempfile

'''
使用tesseract循环200次都没有通过验证码识别；改用keras
运行程序前先设置登录用户名、密码
export username=''
export password=''

'''

