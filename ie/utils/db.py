import logging
import traceback
import pymysql
import pymysql.cursors
import time
from ie.core.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB_NAME, REDIS_URL
import redis


class Connection(object):
    """一个封装 MySQL 的类
    """

    def __init__(self, host, database, user=None, password=None,
                 port=0,
                 max_idle_time=7 * 3600, connect_timeout=10,
                 time_zone="+0:00", charset="utf8mb4", sql_mode="TRADITIONAL"):
        '''
        :param host: host
        :param database:指定数据库
        :param user:user
        :param password:password
        :param port:端口
        :param max_idle_time:最大空闲时间，MySQL 默认连接时间为 8 小时，超过机会断开连接，设置比 8 小时小即可，到达设置的时间会重新建立连接
        :param connect_timeout:
        :param time_zone:
        :param charset:编码
        :param sql_mode:
        '''
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)

        # mysql 连接设置
        args = dict(use_unicode=True, charset=charset,
                    database=database,
                    init_command=('SET time_zone = "%s"' % time_zone),
                    cursorclass=pymysql.cursors.DictCursor,
                    connect_timeout=connect_timeout, sql_mode=sql_mode)
        if user is not None:
            args["user"] = user
        if password is not None:
            args["passwd"] = password

        # 接受 MySQL 套接字：ip:port
        if "/" in host:
            args["unix_socket"] = host
        else:
            self.socket = None
            pair = host.split(":")
            if len(pair) == 2:
                args["host"] = pair[0]
                args["port"] = int(pair[1])
            else:
                args["host"] = host
                args["port"] = 3306
        if port:
            args['port'] = port

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self.host,
                          exc_info=True)

    def _ensure_connected(self):
        '''mysql 连接时间
        '''
        if (self._db is None or
                (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        '''获取 SQL 光标
        '''
        self._ensure_connected()
        return self._db.cursor()

    def __del__(self):
        '''手动释放内存
        '''
        self.close()

    def close(self):
        """关闭数据库连接."""
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """关闭数据库再打开."""
        self.close()
        self._db = pymysql.connect(**self._db_args)
        self._db.autocommit(True)

    def query(self, query, *parameters, **kwparameters):
        """返回查询的参数及行号"""
        cursor = self._cursor()
        try:
            cursor.execute(query, kwparameters or parameters)
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()

    def get(self, query, *parameters, **kwparameters):
        """返回查询数据的行.
        """
        cursor = self._cursor()
        try:
            cursor.execute(query, kwparameters or parameters)
            return cursor.fetchone()
        finally:
            cursor.close()

    def execute(self, query, *parameters, **kwparameters):
        """查询语句."""
        cursor = self._cursor()
        try:
            cursor.execute(query, kwparameters or parameters)
            return cursor.lastrowid
        except Exception as e:
            if e.args[0] == 1062:
                pass
            else:
                traceback.print_exc()
                raise e
        finally:
            cursor.close()

    # 别名
    insert = execute

    ## ===============类似 mongo 的用法 ===================

    def table_has(self, table_name, field, value):
        if isinstance(value, str):
            value = value.encode('utf8')
        sql = 'SELECT %s FROM %s WHERE %s="%s"' % (
            field,
            table_name,
            field,
            value)
        d = self.get(sql)
        return d

    def table_insert(self, table_name, item):
        '''以字典的形式插入，键为 mysql 的表字段'''
        fields = list(item.keys())
        values = list(item.values())
        fieldstr = ','.join(fields)
        valstr = ','.join(['%s'] * len(item))
        sql = 'INSERT INTO %s (%s) VALUES(%s)' % (table_name, fieldstr, valstr)
        try:
            last_id = self.execute(sql, *values)
            return last_id
        except Exception as e:
            if e.args[0] == 1062:
                # 如果查询的数据存在于 mysql 中
                pass
            elif e.args[0] == '1364' and e.args[1] == "Field 'id' doesn't have a default value":
                max_id = ' SELECT MAX( id ) FROM employee_designation;'
                item['id'] = max_id
                self.table_insert(table_name, item)
            else:
                traceback.print_exc()
                print('sql:', sql)
                print('item:')
                for i in range(len(fields)):
                    vs = str(values[i])
                    if len(vs) > 300:
                        print(fields[i], ' : ', len(vs), type(values[i]))
                    else:
                        print(fields[i], ' : ', vs, type(values[i]))
                raise e

    def table_update(self, table_name, updates,
                     field_where, value_where):
        '''更新 item'''
        upsets = []
        values = []
        for k, v in updates.items():
            s = '%s=%%s' % k
            upsets.append(s)
            values.append(v)
        upsets = ','.join(upsets)
        sql = 'UPDATE %s SET %s WHERE %s="%s"' % (
            table_name,
            upsets,
            field_where, value_where,
        )
        self.execute(sql, *(values))


class RedisWrapper(object):
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self._redis_conn = None

    @property
    def redis_conn(self):
        if self._redis_conn is None:
            self._redis_conn = redis.Redis.from_url(self.redis_url)
        return self._redis_conn


my_conn = Connection(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PWD,
    database=MYSQL_DB_NAME,
    charset='utf8',
)

redis_conn = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)
# data = {'name': '建筑管理/九大员', 'code': '10', 'parent_code': '0', 'source_num': 3}
# my_conn.table_insert('hpwk_worker_profession_show', data)
