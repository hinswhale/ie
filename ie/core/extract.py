"""
1. 获取数据
2. 找出找工作&找工人数据
3。重复数据验重
4。屏蔽词过滤
5。获取关键字段
6。录入系统
"""
import re
import datetime
import traceback

from ie.utils.similar import sim
from ie.core.config import threshold
from ie.utils.tools import clean_text, strQ2B
from ie.core.common import sensitive_trie
from ie.core import search_job, search_worker
from ie.utils.db import my_conn, redis_conn

redis_key = 'data_from_wechat_3'


def _query_data(table, fields):
    if not fields:
        fieldstr = '*'
    else:
        fieldstr = ','.join(fields)

    sql = f'select {fieldstr} from {table}'
    print(sql)
    data = my_conn.query(sql)
    return data


def query_jobdata():
    data = _query_data('hpwk_jobdata_from_wechat', ['data_info'])
    return data


def query_userdata():
    data = _query_data('hpwk_userdata_from_wechat', ['data_info'])
    return data


def query_():
    data = []
    if not redis_conn.smembers(redis_key):
        d1 = query_jobdata()
        d2 = query_userdata()
        data.extend(d1)
        data.extend(d2)
        data = [i['data_info'] for i in data]
        redis_conn.sadd(redis_key, *set(data))
    else:
        print('------')
        data = redis_conn.smembers(redis_key)
    return data


def propress_text(content):
    content = strQ2B(content)
    content = content.replace('o', '0') \
        .replace('O', '0')
    content = clean_text(content)
    content = content.lower()
    content = re.sub(r'(\d+)一(\d+)', '\g<1>-\g<2>', content)
    return content


def has_sensitive_word(content):
    status = 0
    result = sensitive_trie.search(content)
    if result:
        status = -1
    return status


def get_data():
    url = ''
    data = {}
    return data


def classify_type(content):
    # 找出找工作&找工人数据
    jobs = []
    workers = []
    return jobs, workers


def load_data_from_sql():
    r = []
    r.append(query_jobdata())
    r.append(query_userdata())


def check_similarity(text):
    query_data = query_()
    for i in query_data:
        text11, text22, vec1, vec2 = sim.transform(i, text)
        res = sim.cosine_similarity(vec1, vec2)
        if res > threshold:
            return True
    return False


def run(content):
    # 找出找工作&找工人数据

    # 1. 获取数据
    # 屏蔽词过滤
    status = has_sensitive_word(content)
    if status == -1:
        print('有敏感词')
        return 1, '有敏感词'

    # 数据验重
    s = check_similarity(content)
    if s:
        print('数据重复')
        return 1, '数据重复'

    # 找出找工作&找工人数据
    data_type = classify_type(content)
    data_type = 2
    content = propress_text(content)

    # 抽取
    try:
        if data_type == 1:
            # 招工数据表
            data = search_worker.extract(content)
            sql_table = 'hpwk_jobdata_from_wechat'
        elif data_type == 2:
            # 找工作
            data = search_job.extract(content)
            sql_table = 'hpwk_userdata_from_wechat'
    except Exception as e:
        print(traceback.format_exc())
        return -1, '抽取失败'

    create_time = datetime.datetime.now()
    data['create_time'] = create_time
    last_id = my_conn.table_insert(sql_table, data)
    if last_id:
        redis_conn.sadd(redis_key, content)
        return 1, 'sucess'
    else:
        return 1, '插入失败'

    # 5。获取关键字段
    # 6。录入系统


if __name__ == "__main__":
    content = """水电工2人，有证，找活，工具齐全，，工装，可包，点工，都行，人在北京大兴黄村，需要用人，加微信或者，联系电话"""
    print(run(content))
# 电工一人到多人找活，安装穿线配管都可以，工装家装都行 