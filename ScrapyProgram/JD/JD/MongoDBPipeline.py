# -*-coding:utf-8-*-
from pymongo import MongoClient
from scrapy import Item

class MongoDBPipeline:
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'scrapy_default')

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

        self.db.books.insert_one(item)