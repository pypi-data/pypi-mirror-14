# -*- coding: utf-8 -*-
from memcache import Client as MemcacheClient
import conf
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

MEMCACHE_CLIENT = MemcacheClient(['%s:%s' % (conf.MEMCACHED_IP, conf.MEMCACHED_PORT)])  # 全局 memcached


class Cache(object):
    @staticmethod
    def add(key, value, time=0):
        return MEMCACHE_CLIENT.add("%s_%s" % (conf.PREFFIX, str(key)), value, time=time)

    @staticmethod
    def get(key):
        return MEMCACHE_CLIENT.get("%s_%s" % (conf.PREFFIX, str(key)))

    @staticmethod
    def delete(key, time=0):
        return MEMCACHE_CLIENT.delete("%s_%s" % (conf.PREFFIX, str(key)), time=time)
