import datetime
import pickle
import redis
from config import REDIS


class RedisStore:
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(host=REDIS.host, port=REDIS.port, password=REDIS.password, db=0,
                                               socket_timeout=5, socket_connect_timeout=5)

    def log(self, message):
        print('INFO[{}] <Redis> {}'.format(datetime.datetime.utcnow(), message))

    def get(self, key):
        connection = redis.Redis(connection_pool=self.redis_pool)
        dump = connection.get(key)
        if dump:
            result = pickle.loads(dump)
            return result
        else:
            raise ValueError('No data in redis')

    def set(self, key, data):
        connection = redis.Redis(connection_pool=self.redis_pool)
        dump = pickle.dumps(data)
        connection.set(key, dump)
        self.log('{} saved'.format(key))


if __name__ == '__main__':
    r = RedisStore()
    # q = r.get(TOKEN_TAG)
    # print(q)
    # # q.update({'tokens': {269345635: 1000, 1120248894: 0, 346585363: 1000, 181124055: 0}})
    # # r.set(TOKEN_TAG, q)

    connection = redis.Redis(connection_pool=r.redis_pool)
    k = connection.keys()
    for i in k:
        print(i)


