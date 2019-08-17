import requests
import pyperclip
import time

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
		img_data = requests.get(image_url).content
		with open(filename, 'wb') as handler:
			handler.write(img_data)
			print('save {}'.format(filename))
	else:
		print('错误的网址： {}'.format(image_url))


if __name__ == '__main__':
	# n秒没有图片url则退出
	n = 100
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