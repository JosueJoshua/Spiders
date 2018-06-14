# -*- coding: utf-8 -*-
import scrapy
from scrapy import spider, Request
from urllib.parse import quote
from seleniumtaobao.items import SeleniumtaobaoItem

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['https://s.taobao.com/search?q=']

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE')+1):
                url = self.start_urls[0] + quote(keyword)  # 对字符串进行编码
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)
    
    def parse(self, response):
        products = response.xpath(
            '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class, "item")]')
        for product in products:
            item = SeleniumtaobaoItem()
            item['price'] = ''.join(
                product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
            item['title'] = ''.join(
                product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop'] = ''.join(
                product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
            item['image'] = ''.join(product.xpath(
                './/div[@class, "pic")]//img[contains(@class, "img")]/@data-src()').extract()).strip()
            item['deal'] = product.xpath(
                './/div[contains(@class, "deal-cnt")]//text()').extract_first().strip()
            item['location'] = product.xpath(
                './/div[contains(@class, "location")]//text()').extract_first().strip()
            yield item