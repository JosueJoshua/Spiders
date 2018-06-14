# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from pymongo import MongoClient
from scrapy import Item

class MongoDBPipeline(object):
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'scrapy_db')

        self.db_client = MongoClient('mongodb://localhost:27017')
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)

        self.db.nv.insert_one(item)

# class JdPipeline(object):
#     #def __init__(self):
#         #self.file = codecs.open("./catalog.json", "wb", encoding="utf-8")
#
#     def process_item(self, item, spider):
#         #print '2'
#         #i = json.dumps(dict(item), ensurt_ascii=False)
#         #print '3'
#         #line = i + '\n'
#         #print line
#         #self.file.write(line)
#         return item
#
#     #def close_spider(self, spider):
#         #self.file.close()