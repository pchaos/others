import requests
import pyperclip
import time
import os
from PIL import Image
from io import BytesIO

''' 监控剪贴板粘贴图片url，并保存
如果获取图片出错, 可能需要使用代理
'''


def is_valid_url(url):
	import re
	regex = re.compile(
		r'^https?://'  # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
		r'localhost|'  # localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
		r'(?::\d+)?'  # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	return url is not None and regex.search(url)


def saveUrlToFile(image_url=pyperclip.paste()):
	# image_url = 'https://mk0resourcesinfm536w.kinstacdn.com/wp-content/uploads/2-171-768x176.png'
	if is_valid_url(image_url):
		# 文件名不变
		filename = image_url.split('/')[-1]
		if len(filename) < 5:
			# 不是图片
			print("pass {}".format(filename))
			return False
		else:
			if "=webp" in filename:
				# webp格式
				fn = genFilename(filename=filename)
				response = requests.get(image_url)
				webp2jpg(BytesIO(response.content), fn)
				return
		img_data = requests.get(image_url).content
		with open(filename, 'wb') as handler:
			handler.write(img_data)
			print('save {}'.format(filename))
	else:
		print('错误的网址： {}'.format(image_url))


def genFilename(filename, fileext="jpg", defaultDir='./'):
	#  如果有重复 返回新的文件名
	filename, file_extension = os.path.splitext(filename)
	for a in map(chr, range(97, 123)):
		for b in map(chr, range(65, 91)):  # 增加一层循环 防止文件名冲突
			# or list(map(chr, range(ord('a'), ord('z')+1)))
			if "?" in filename:
				# 截取“？”前面的名称
				fn = filename.split("?")[0]
			fn = os.path.join(defaultDir,
			                  "{}{}.{}".format(fn, "{}{}".format(a, b),
			                                   fileext))
			if not os.path.exists(fn):
				return fn
	return filename


def webp2jpg(webpData, filename):
	try:
		print("webp file")
		im = Image.open(webpData).convert("RGB")
		im.save(filename, "jpeg")
		print('Converting webp to jpeg … {}'.format(filename))
	except Exception as e:
		print(e.args)
		print("错误原因可能是缺少pillow等安装包 ")


if __name__ == '__main__':
	# n秒没有图片url则退出
	n = 90
	lasturl = ""
	sleeping = 0
	while True:
		url = pyperclip.paste()
		if url != lasturl:
			print(url)
			saveUrlToFile(url)
			lasturl = url
			sleeping = 0
		time.sleep(1)
		print('.', end='')
		sleeping += 1
		if sleeping > n:
			break

	print('\nBye!!!')
