# coding:utf-8
# @创建者：州的先生
# 博客地址：zmister.com

import os,traceback
from PIL import Image

# 获取文件夹图片
def get_folder(fpath,wm_file,save_path):
    try:
        img_suffix_list = ['png', 'jpg', 'bmp']
        for i in os.listdir(fpath):
            if i.split('.')[-1] in img_suffix_list:
                img_path = fpath + '/' + i
                img_water_mark(img_file=img_path,wm_file=wm_file,save_path=save_path)
    except Exception as e:
        print(traceback.print_exc())

# 图片添加水印
def img_water_mark(img_file, wm_file,save_path):
    try:
        img = Image.open(img_file)  # 打开图片
        watermark = Image.open(wm_file)  # 打开水印
        img_size = img.size
        wm_size = watermark.size
        # 如果图片大小小于水印大小
        if img_size[0] < wm_size[0]:
            watermark.resize(tuple(map(lambda x: int(x * 0.5), watermark.size)))
        print('图片大小：', img_size)
        wm_position = (img_size[0]-wm_size[0],img_size[1]-wm_size[1]) # 默认设定水印位置为右下角
        layer = Image.new('RGBA', img.size)  # 新建一个图层
        layer.paste(watermark, wm_position)  # 将水印图片添加到图层上
        mark_img = Image.composite(layer, img, layer)
        new_file_name = '/new_'+img_file.split('/')[-1]
        mark_img.save(save_path + new_file_name)
    except Exception as e:
        print(traceback.print_exc())
