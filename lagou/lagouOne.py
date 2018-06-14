# -*- coding=utf-8 -*-
import json
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=pac',
}

data = {
    'first': True,
    'pn': 1,
    'kd': '爬虫'
}
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
response = requests.post(url, data=data, headers=headers)
print(response, response.text)