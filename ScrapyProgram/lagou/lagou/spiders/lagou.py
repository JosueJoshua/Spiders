# -*- coding: utf-8 -*-
import scrapy
import json
import re
import itertools
from urllib.parse import quote
from bs4 import BeautifulSoup
from scrapy import Request, Spider, FormRequest
from lagou.items import LagouItem
from urllib.parse import quote


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/66.0.3359.170 Safari/537.36',
        'Origin': 'https://www.lagou.com',
        'Host': 'www.lagou.com',
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/66.0.3359.170 Safari/537.36',
        'Host': 'www.lagou.com',
    }
    cookies = {
        'Cookie': "_ga=GA1.2.219114762.1528442194; user_trace_token=20180608151633-df96bf55-6aeb-11e8-942d-5254005c3644; LGUID=20180608151633-df96c42d-6aeb-11e8-942d-5254005c3644; _gid=GA1.2.192310382.1528823118; JSESSIONID=ABAAABAAAGFABEF5699DDF6AFA59C96FF737F9A754A436F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528587010,1528592628,1528823119,1528858548; X_HTTP_TOKEN=9654cb850e1225cb8df8c60bc48c16c0; TG-TRACK-CODE=search_code; SEARCH_ID=147b832e619443e6bd5b028814e75fbd; LGSID=20180613181028-ff5f5180-6ef1-11e8-9f23-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E7%2588%25AC%25E8%2599%25AB%3Fpx%3Ddefault%26city%3D%25E5%2585%25A8%25E5%259B%25BD; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fts%3D1528884628078%26serviceId%3Dlagou%26service%3Dhttps%25253A%25252F%25252Fwww.lagou.com%25252F%26action%3Dlogin%26signature%3D49D504E49295B8642970521345A22F6B; LG_LOGIN_USER_ID=27400ec6ace34a779ab29d4f3c8befecba45ad6c3c666165; _putrc=0CD321B4047EC50A; _gat=1; login=true; unick=%E5%88%98%E6%94%BF; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=26; gate_login_token=50b4356c6ac77ad00a42eacf306019a03b1193367169663c; index_location_city=%E6%B7%B1%E5%9C%B3; LGRID=20180613181223-442901de-6ef2-11e8-9573-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528884745",
    }
    start_urls = ['https://www.lagou.com/jobs/list_{keyword}?city={city}&cl=false&fromSearch=true&labelWords=&suginput=']
    referer_url = 'https://www.lagou.com/jobs/list_{keyword}?city={city}&cl=false&fromSearch=true&labelWords=&suginput='
    url_job = 'https://www.lagou.com/jobs/{id}.html'

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for city in self.settings.get('CITYS'):
                self.settings.get('DATA')['kd'] = keyword
                url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&city={city}'.\
                    format(city=quote(city))
                self.headers['referer'] = self.referer_url.format(keyword=quote(keyword), city=quote(city))
                print(self.settings.get('DATA'))
                print(self.headers)
                print(url)
                yield FormRequest(url, headers=self.headers, callback=self.parse_json, dont_filter=True,
                                  formdata=self.settings.get('DATA'), meta={'keyword': keyword, 'city': city})


    def parse_json(self, response):
        print('-----------------')
        # print(response.text)
        print(type(response.text))
        print(response.url)
        print('-----------------')
        data = json.loads(response.text)
        keyword = response.meta.get('keyword')
        city = response.meta.get('city')
        # if self.headers['Origin']:
            # del self.headers['Origin']
        if data['success']:
            for result in data['content']['positionResult']['result']:
                id = result['positionId']
                print(id)
                print(self.headers)
                self.headers['referer'] = 'https://www.lagou.com/jobs/list_{keyword}?px=default&city={city}'.\
                    format(keyword=quote(keyword), city=quote(city))
                print(self.url_job.format(id=id), self.headers)
                yield Request(self.url_job.format(id=id), callback=self.parse, headers=self.headers, cookies=self.cookies)


    def parse(self, response):
        print('-----------------------')
        print('=======================')
        print(response.status)
        print(response.url)
        print('=======================')
        print('=======================')
        if response.status == 302:
            yield Request(self.url_job.format(id=id), callback=self.parse, headers=self.header, cookies=self.cookies)
        elif response.status == 200:
            # print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            item = LagouItem()
            item['job_name'] = ''.join(soup.find(class_='job-name').find(class_='name').text)
            item['salary'] = ''.join(soup.find(class_='salary').text)
            item['address'] = ''.join(itertools.chain(*re.findall(u'[\u4e00-\u9fa5]+|[a-zA-Z]+', soup.find(class_='work_addr').text)[:-1]))
            item['description'] = ''.join(soup.find(class_='job_bt').text)
            print(item)
