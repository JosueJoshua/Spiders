# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from ..items import ClothItem


class CatalogSpider(scrapy.Spider):
    name = "nv"
    allowed_domains = ["coll.jd.com"]
    start_urls = (
        'http://coll.jd.com/list.html?sub=22594',
    )

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }

    # def enter_pages(self, response):
    #     cloth_num = response.xpath('//*[@id="J_topPage"]/span[1]/b/text()').extract_first()
    #     print cloth_num
    #     pages = response.xpath('//*[@id="J_bottomPage"]/span[2]/em[1]/b/text()').extract_first()
    #     print pages
    #     last_num = int(cloth_num) % 60
    #     print last_num
    #     url_pages = []
    #     for i in range(1, int(pages) + 1):
    #         page = i
    #         url_pages.append(self.start_urls[0] + ('&page=%d&JL=6_0_0' % page))
    #     for url_page in url_pages:
    #         print url_page

    def get_price(self, response):
        item1 = response.meta['item']
        data = response.body[8:-4]
        data = json.loads(data)
        item1['price'] = data['p']

    def get_ad(self, response):
        item1 = response.meta['item']
        data = response.body[8:-4]
        data = json.loads(data)
        item1['ad'] = data['ad']

    def get_comment(self, response):
        item1 = response.meta['item']
        data = response.body
        data = json.loads(data)
        print data['CommentsCount'][0]['CommentCountStr']
        item1['comment_Num'] = data['CommentsCount'][0]['CommentCountStr']
        yield item1

    def parse(self, response):
        pages = response.xpath('//*[@id="J_bottomPage"]/span[2]/em[1]/b/text()').extract_first()
        print pages
        goods = response.xpath('//li[@class="gl-item"]')
        print goods
        for good in goods:
            item1 = ClothItem()
            item1['id'] = good.xpath('./div/@data-sku').extract()
            item1['name'] = good.xpath('.//div[@class="p-name"]/a/em/text()').extract()
            item1['img'] = good.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img|.'
                                      '//div[@class="p-img"]/a/img/@src').extract()
            item1['link'] = good.xpath('.//div[@class="p-img"]/a/@href').extract()
            url_price = 'https://p.3.cn/prices/mgets?callback=jQuery&skuIds=J_%s' % item1['id'][0]
            url_ad = 'https://ad.3.cn/ads/mgets?&callback=jQuery&skuids=AD_%s' % item1['id'][0]
            url_comment = 'https://club.jd.com/comment/productCommentSummaries.act' \
                          'ion?my=pinglun&referenceIds=%s' % item1['id'][0]
            item1['link'][0] = 'https:'+item1['link'][0]
            print item1['link']
            #item1['link'] = 'https:'+item1['link']
            yield Request(url_price, meta={'item': item1}, callback=self.get_price, dont_filter=True)
            yield Request(url_ad, meta={'item': item1}, callback=self.get_ad, dont_filter=True)
            yield Request(url_comment, meta={'item': item1}, callback=self.get_comment, dont_filter=True)

            print url_price
        for i in range(2, int(pages) + 1):
            url = self.start_urls[0] + ('&page=%d&JL=6_0_0' % i)
            yield Request(url, callback=self.parse, headers=self.headers)

# def parse(self, response):
    #     cloth_data = ClothItem()
    #     cloth_num = response.xpath('//*[@id="J_topPage"]/span[1]/b/text()').extract_first()
    #     print cloth_num
    #     pages = response.xpath('//*[@id="J_bottomPage"]/span[2]/em[1]/b/text()').extract_first()
    #     print pages
    #     last_num = int(cloth_num) % 60
    #     print last_num
    #     s = response.css('li.gl-item')
    #     print s
    #     for cloth in response.css('li.gl-item'):
    #         #print cloth
    #         img = cloth.xpath('//div[@class="p-img"]//img/@src')
    #         price = cloth.xpath('//div[@class="p-price"]//i')
    #         print price
    #     for i in range(1, int(pages) + 1):
    #         url = self.start_urls[0] + ('&page=%d&JL=6_0_0' % i)
    #         #print url
    #         yield Request(url, self.parse)