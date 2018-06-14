# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    first_cat = scrapy.Field()  # 一级目录
    second_cat_channel = scrapy.Field()  # 二级通道
    second_cat = scrapy.Field()  # 二级目录
    three_cat = scrapy.Field()  # 三级目录


class ClothItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()  # ID
    link = scrapy.Field()  # 商品链接
    img = scrapy.Field()  # 图片
    price = scrapy.Field()  # 价格
    name = scrapy.Field()  # 名称
    comment_Num = scrapy.Field()  # 评论数
    ad = scrapy.Field()  # 活动

