# 联系人有姓名则匹配姓名，没有匹配如下关键词：X工，X师傅，X经理，X总，X老板，X先生，X女士，X小姐，X为姓，匹配不到任何信息默认为先生；
from ie.utils.tools import retry


def hanlp_username(sentences: str) -> list:
    from pyhanlp import HanLP
    segment = HanLP.newSegment().enableNameRecognize(True)
    seg_words = segment.seg(sentences)
    user_list = []
    for value in seg_words:
        split_words = str(value).split('/')  # check //m
        word, tag = split_words[0], split_words[-1]
        if tag == 'nr':
            user_list.append(word)
    return user_list


def ltp_username(sentences: str) -> list:
    from ltp import LTP

    ltp = LTP()  # 默认加载 Small 模型，下载的路径是：~/.cache/torch/ltp
    seg, hidden = ltp.seg([sentences])  # 分词
    nh_user_list = []
    pos_index_values = ltp.pos(hidden)
    # seg 是 list to list 的格式
    for index, seg_i in enumerate(seg):
        pos_values = pos_index_values[index]
        for _index, _pos in enumerate(pos_values):
            if _pos == "nh":
                nh_user_list.append(seg_i[_index])
    return nh_user_list


def lac_username(sentences: str) -> list:
    # 装载LAC模型
    from LAC import LAC

    user_name_list = []
    lac = LAC(mode="lac")
    lac_result = lac.run(sentences)
    for index, lac_label in enumerate(lac_result[1]):
        if lac_label == "PER":
            user_name_list.append(lac_result[0][index])
    return user_name_list


@retry(max_retry=5)
def search(text):
    v = '先生'
    user_name_list = ltp_username(text)
    if not user_name_list:
        return v

    if len(user_name_list[0]) == 1:
        return user_name_list[0] + v
    return user_name_list[0]
