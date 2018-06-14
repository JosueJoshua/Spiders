#-*- conding:utf-8 -*-
import requests
import json
import re
import pymysql
import itertools
from pyquery import PyQuery as pq
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
	              ' Chrome/66.0.3359.170 Safari/537.36',
    'Origin': 'https://www.lagou.com'
}

referer_url = 'https://www.lagou.com/jobs/list_{keyword}?city={city}&cl=false&fromSearch=true&labelWords=&suginput='
data = {
    'first': 'true',
    'pn': 1,
    'kd': '爬虫'
}
db = pymysql.connect(host='localhost', user='root', password='mysqldb', port=3306, db='lagou')
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
version = cursor.fetchone()
print(version)
db.close()
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&city={city}'.format(city=quote('北京'))
print(url)
headers['referer'] = referer_url.format(keyword=quote('爬虫'), city=quote('北京'))
response = requests.post(url, headers=headers, data=data)
print(response.status_code)
print(response.text)
json = json.loads(response.text)
if response.status_code == 200 and json['success']:
    print(json['success'])
    id = json['content']['positionResult']['result'][0]['positionId']
    print(id)
    url_job = 'https://www.lagou.com/jobs/{id}.html'.format(id=id)
    headers['referer'] = 'https://www.lagou.com/jobs/list_{keyword}?px=default&city={city}'.format(
        keyword=quote('爬虫'), city=quote('北京'))
    del headers['Origin']
    print(url_job)
    response = requests.get(url_job, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_name = soup.find(class_='job-name').find(class_='name').text
        salary = soup.find(class_='salary').text
        address = soup.find(class_='job_request').select('span')[1].text.strip('/')
        job_add = "".join(itertools.chain(
            *re.findall(u'[\u4e00-\u9fa5]+|[a-zA-Z]+', soup.find(class_='work_addr').text)[:-1]))
        print(soup.find(class_='description'))
        t = soup.find(class_='description')
        description = soup.find(class_='job_bt').text
        print(job_name, salary, address, job_add)
        print(description)

