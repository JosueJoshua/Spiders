#-*- conding:utf-8 -*-
import requests
import json
import os
import time
from hashlib import md5

headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
	              " (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",
	"referer": "https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D"
}
def get_page(offset):
	base_url = 'https://www.toutiao.com/search_content/?offset={0}&format=json&' \
	           'keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab'.format(offset)
	response = requests.get(base_url, headers=headers).content.decode('utf-8')
	res = json.loads(response)
	return res

def get_images(data_json):
	data = data_json['data']
	for one in data:
		content = {}
		if ('image_list' in one.keys()):
			images = one['image_list']
			title = one['title']
			content['title'] = title
			content['img'] = images
			yield content

def save_image(images):
	title = images['title']
	path = '{0}/{1}'.format('data', title.replace('?', '？'))
	if not os.path.exists(path):
		os.mkdir(path)
	for item in images['img']:
		try:
			response = requests.get('http:' + item['url'])
			file_path = '{0}/{1}.{2}'.format(path, md5(response.content).hexdigest(), 'jpg')
			if not os.path.exists(file_path):
				if response.status_code == 200:
					with open(file_path, 'wb') as f:
						f.write(response.content)
			else:
				print('Already Downloaded', file_path)
		except requests.ConnectionError:
			print('Failed to Save Image')


offset = 0
if __name__ == '__main__':
	while True:
		if not os.path.exists('data'):
			os.mkdir('data')
		print(offset)
		data_json = get_page(offset)
		if data_json['data'] == []:
			break
		for image in get_images(data_json):
			print('-------------------------------')
			save_image(image)
		offset += 20

