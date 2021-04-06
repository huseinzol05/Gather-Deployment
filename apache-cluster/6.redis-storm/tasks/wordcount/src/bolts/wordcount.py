import os
from redis import StrictRedis
from streamparse import Bolt


class RedisWordCountBolt(Bolt):
    outputs = ['word', 'count']

    def initialize(self, conf, ctx):
        self.redis = StrictRedis(host = 'redis')
        self.total = 0

    def _increment(self, word, inc_by):
        self.total += inc_by
        return self.redis.zincrby('words', word, inc_by)

    def process(self, tup):
        word = tup.values[0]
        count = self._increment(word, 10 if word == 'dog' else 1)
        if self.total % 1000 == 0:
            self.logger.info('counted %i words', self.total)
        self.emit([word, count])
