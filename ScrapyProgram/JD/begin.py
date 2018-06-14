# -*-coding:utf-8-*-
from scrapy import cmdline

cmdline.execute("scrapy crawl nv --nolog".split())
cmdline.execute("mongo scrapy_db".split())
cmdline.execute("scrapy crawl catalog -o catalog.json --nolog".split())