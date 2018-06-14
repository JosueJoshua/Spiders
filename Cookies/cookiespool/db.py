# -*- coding=utf-8 -*-
import random
import redis
from cookiespool.config import *


class RedisClient(object):
    # 初始化Redis连接
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website
    # 获取hash名称
    def name(self):
        return "{type}:{website}".format(type=self.type, website=self.website)
    # 设置键值对，用户名：密码/Cookies
    def set(self, username, value):
        return self.db.hset(self.name(), username, value)
    # 根据键名获取键值
    def get(self, username):
        return self.db.hget(self.name(), username)
    # 根据键名删除键值对
    def delete(self, username):
        return self.db.hdel(self.name(), username)
    # 获取数目
    def count(self):
        return self.db.hlen(self.name())
    # 随机得到键值，用于Cookies获取
    def random(self):
        return random.choice(self.db.hvals(self.name()))
    # 获取所有账户信息
    def usernames(self):
        return self.db.hkeys(self.name())
    # 获取所有键值对
    def all(self):
        return self.db.hgetall(self.name())

if __name__ == '__main__':
    conn = RedisClient('accounts', 'weibo')
    result = conn.set('hell2o', 'sss3s')
    print(result)