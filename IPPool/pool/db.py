#-*- conding:utf-8 -*-

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

import re
import redis
from .error import PoolEmptyError
from .setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from .setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice

class RedisClient(object):
	def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
		self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

	def add(self, proxy, score=INITIAL_SCORE):
		if not self.db.zscore(REDIS_KEY, proxy):
			return self.db.zadd(REDIS_KEY, score, proxy)

	def random(self):
		result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
		if len(result):
			return choice(result)
		else:
			result = self.db.zrevrange(REDIS_KEY, 0, 100)
			if len(result):
				return choice(result)
			else:
				raise PoolEmptyError

	def decrease(self, proxy):
		score = self.db.zscore(REDIS_KEY, proxy)
		if score and score > MIN_SCORE:
			print('代理', proxy, '当前分数', score, '减 1')
			return self.db.zincrby(REDIS_KEY, proxy, -1)
		else:
			print('代理', proxy, '当前分数', score, '移除')
			return self.db.zrem(REDIS_KEY, proxy)

	def exists(self, proxy):
		return not self.db.zscore(REDIS_KEY, proxy) == None

	def max(self, proxy):
		print('代理', proxy, '可用，设置为', MAX_SCORE)
		return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

	def count(self):
		return self.db.zcard(REDIS_KEY)

	def all(self):
		return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

	def batch(self, start, stop):
		return self.db.zrevrange(REDIS_KEY, start, stop-1)

if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)