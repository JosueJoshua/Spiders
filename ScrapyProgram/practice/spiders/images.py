# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from urllib.parse import urlencode
import json

from practice.items import PracticeItem

class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {
            'ch': 'photography',
            'listtype': 'new',
        }
        base_url = 'https://image.so.com/zj?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            print(data)
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = PracticeItem()
            item['id'] = image.get('imageid')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
            print(item)
            yield item