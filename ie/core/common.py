import pandas as pd
from ie.utils.trie import BaseTrie
from ie.settings import data_root


def load_sensitive_trie():
    df = pd.read_csv(data_root + '/屏蔽词表.csv')
    sensitive_words = df['屏蔽词'].to_list()
    trie = BaseTrie(sensitive_words)
    return trie


def load_worktype_trie():
    worktype_keywords = ['木工',]
    df = pd.read_csv(data_root + '/工种列表和工种关键词.csv')
    records = df.to_dict('records')
    work_lst = set()
    for record in records:
        worktype = record['工种类型']
        name = record['名称']
        if not pd.isna(worktype):
            for i in worktype.split(','):
                work_lst.add(i)
        else:
            for i in name.split('/'):
                work_lst.add(i)

    for i in worktype_keywords:
        work_lst.add(i)
    trie = BaseTrie(work_lst)
    return trie


def load_ganraoci():
    lst = set()
    with open(data_root + '/干扰词.txt', 'r') as f:
        for line in f:
            lst.add(line.strip())
    return list(lst)


def worktype_mapping():
    df = pd.read_csv(data_root + '/工种列表和工种关键词.csv')
    from collections import defaultdict

    mapping = defaultdict(defaultdict)
    dct = {}
    for group in df[df['上级代码'] == 0].to_dict('records'):
        rds = df[df['上级代码'] == group['代码']].to_dict('records')
        for item in rds:
            mapping[group['名称']][item['名称']] = item['工种类型'].split(',') if not pd.isnull(item['工种类型']) else ''
            if item['名称'] == '全部':
                continue
            dct[item['名称']] = item['工种类型'].split(',') if not pd.isnull(item['工种类型']) else []
            if not dct[item['名称']]:
                dct[item['名称']].extend(item['名称'].split('/'))

    worktype_map = defaultdict(set)
    for k, v in dct.items():
        for v1 in v:
            worktype_map[v1].add(k)

        for v1 in k.split('/'):
            worktype_map[v1].add(k)
    return worktype_map, dct.keys()


sensitive_trie = load_sensitive_trie()
worktype_trie = load_worktype_trie()
ganraoci = load_ganraoci()
worktype_map, worktype_lst = worktype_mapping()
