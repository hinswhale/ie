from os import environ as e
import redis

test_size = 0.2
threshold = 0.9


def load_int(name, default):
    try:
        return int(e.get(name, default))
    except (ValueError, TypeError):
        return default


MYSQL_HOST = e.get('MYSQL_HOST', 'localhost')
MYSQL_PORT = load_int('MYSQL_PORT', 3306)
MYSQL_USER = e.get('MYSQL_USER', 'root')
MYSQL_DB_NAME = e.get('MYSQL_DB_NAME', 'wx')
MYSQL_PWD = e.get('MYSQL_PWD', 'root123')

#依赖的redis
REDIS_HOST = e.get('REDIS_HOST', 'localhost')
REDIS_PORT = load_int('REDIS_PORT', 6379)
REDIS_DB = int(e.get('CIE_REDIS_DB', '0'))

REDIS_URL = e.get('TIDE_REDIS', 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB))
