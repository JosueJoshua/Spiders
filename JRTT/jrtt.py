#-*- conding:utf-8 -*-
import requests
import os
import shutil
from hashlib import md5
from urllib.parse import urlencode
from multiprocessing.pool import Pool
headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
	              " (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",
	"referer": "https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D"
}

def get_page(offset):
	params = {
		'offset': offset,
		'format': 'json',
		'keyword': '街拍',
		'autoload': 'true',
		'count': '20',
		'cur_tab': '1',
		'from': 'search_tab'
	}
	url = 'https://www.toutiao.com/search_content/?'+urlencode(params)
	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.json()
	except requests.ConnectionError:
		return None

def get_images(json):
	if json.get('data'):
		for item in json.get('data'):
			title = item.get('title')
			images = item.get('image_list')
			for image in images:
				yield {
					'image': image.get('url'),
					'title': title,
				}

def save_image(item):
	if os.path.exists(item.get('title')):
		shutil.rmtree(item.get('title'))
	os.mkdir(item.get('title'))

	try:
		response = requests.get('http:'+item.get('image'))
		if response.status_code == 200:
			print(response.content)
			file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
			if not os.path.exists(file_path):
				with open(file_path, 'wb') as f:
					f.write(response.content)
			else:
				print('Already Downloaded', file_path)
	except requests.ConnectionError:
		print('Failed to Save Image')

def main(offset):
	json = get_page(offset)
	for item in get_images(json):
		print(item)
		save_image(item)

GROUP_START = 0
GROUP_END = 20

if __name__=='__main__':
	pool = Pool()
	groups = ([x * 20 for x in range(GROUP_START, GROUP_END)])
	print(groups)
	pool.map(main, groups)
	pool.close()
	pool.join()