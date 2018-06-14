# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'job'
    job_name = Field()
    salary = Field()
    description = Field()
    address = Field()