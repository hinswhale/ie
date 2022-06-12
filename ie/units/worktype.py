import pandas as pd
from ie.utils.tools import repalce_tag, pattern_lst
from ie.core.common import worktype_trie, worktype_map, worktype_lst
from ie.settings import data_root
from collections import defaultdict
import collections

f = lambda x: x if not pd.isnull(x) else '--'
worktype_keywords = ['木工', '普工', '管工', '中工', '大工', '小工', '切割工', '泥工',
                     '中', '大', '领班', '化工', '男工', '女工']
"""
电力
"""


def search_(content):
    result = worktype_trie.search(content)
    res = []
    for s, e, n in result:
        res.append([n, s, e, content[s:e]])
    return res


def search(content):
    wts = search_(content)
    origin = []
    worktype_lst_ = []
    d = defaultdict(list)
    for wt in wts:
        print(f'wt: {wt}')
        for item in [wt[0], wt[0] + '工']:
            worktypes = worktype_map.get(item)
            origin.append(item)
            # if worktypes:
            #     worktype_lst_.extend(worktypes)
            #     d[wt[0]].extend(worktypes)
            # else:
            #     worktypes = []
            wy = list(worktypes) if worktypes else []
            wy.extend(list(worktype_lst))
            for worktype in wy:
                if item in worktype:
                    worktype_lst_.append(worktype)
                    d[wt[0]].append(worktype)
            if not worktype_lst_:
                worktype_lst_.extend(list(worktypes) if worktypes else [])
    # print(d)
    # print(worktype_lst_)
    # print(collections.Counter(worktype_lst_))
    return ' '.join(list(set(worktype_lst_)))


def worktype_tag(content):
    # 找到工种tag
    preys = search_(content)
    text = repalce_tag(preys, content)

    # 屏蔽词
    # re_pattern = '(?P<num>\d+个[大|小]?班组)'
    # match = pattern_lst(re_pattern, text)
    # content = repalce_tag(match, content)

    preys.extend(pattern_lst(f"(?P<num>{'|'.join(worktype_keywords)})", text))
    text = repalce_tag(preys, content)
    return preys, text


if __name__ == '__main__':
    path = '自动摘录样本&相关词表/【样本】-工人-人工采集(不含字段抽取).xlsx'
    df = pd.read_excel(data_root + path)
    records = df.to_dict('records')
    data = []
    for record in records:
        r = {}
        r['工种_true'] = ' || '.join(map(f, [record['工种'], record['工种.1'], record['工种.2']]))
        r['自我介绍'] = record['自我介绍']
        print(f"自我介绍: {r['自我介绍']}")
        print(f"工种_true: {r['工种_true']}")
        worktype_lst = search(record['自我介绍'])  # 用工需求
        r['工种_pred'] = worktype_lst
        print(f"工种_pred: {r['工种_pred']}")
        data.append(r)
        print('########' * 20)
    df = pd.DataFrame.from_records(data)
    df.to_csv(data_root + '工种_招工.csv')

#自我介绍: 二次结构木工找活，6个人随时可以进场，行程码不带星号。陈师傅。此信息长期有效。请说在建筑用工平台看见的。
# 自我介绍: 专业上材料，ALC格墙板，泡沫砖，地板砖，拉成品砂浆，内外墙，有介绍量大给三仟红包，只做包工，自带工具地方不限要求量大，随时可以进，如有需要的老板联系:杨
#自我介绍: 电工团队找活，强弱电，上下水，焊工，有证，做管，穿线，桥架，线路维修，灯具安装，电箱，配电柜，经验丰富，工作认真，需要人的联系，    北京