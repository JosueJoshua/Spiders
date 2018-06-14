#-*- conding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os

if os.path.exists('py100.txt'):
	os.remove('py100.txt')
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
}
start_url = 'http://www.runoob.com/python/python-100-examples.html'
response = requests.get(start_url, headers=headers).content.decode('utf-8')
soup = BeautifulSoup(response, 'lxml')

result = soup.find(id='content').find_all('a')
case_url = []
i = 0
for item in result:
	case_url.append(item['href'])
	res = requests.get('http://www.runoob.com'+item['href']).content.decode('utf-8')
	soup = BeautifulSoup(res, 'html.parser')
	content = {}
	target = soup.find(id='content').find_all('p')
	content['header'] = soup.find(id='content').find_all('h1')[0].text
	content['title']  = target[1].text.strip()
	content['analyze'] = target[2].text.strip()
	try:
		content['code'] = soup.find(class_='hl-main').text
	except:
		content['code'] = soup.find('pre').text
	print(content['header']+'爬取成功！')
	with open('py100.txt', 'a+', encoding='utf-8') as file:
		file.write(content['header']+'\n')
		file.write(content['title']+'\n')
		file.write(content['analyze']+'\n')
		file.write(content['code']+'\n')
		file.write('\n'+"="*50+'\n')
