import re

REPLACE = [
    re.compile('\d+'),
]


def preprocess(txt, ex=None):
    ex = ex if ex else []
    for s, e in ex:
        txt = txt[:s] + u'_' * (e - s) + txt[e:]
    for r in REPLACE:
        ms = r.finditer(txt)
        se = [(m.start(), m.end()) for m in ms]
        txt = gen_replaced_txt(se, txt)
    return txt


def gen_replaced_txt(se_list, astr):
    """根据开始和结束idx的列表生成替换文本"""
    to_replace_text = []
    last_e = 0
    for (s, e) in se_list:
        if s > last_e:
            to_replace_text.append(astr[last_e:s])
        replace = u'→' * (e - s)
        to_replace_text.append(replace)
        last_e = e
    if last_e < len(astr):
        to_replace_text.append(astr[last_e:])
    return u"".join(to_replace_text)


res = preprocess('价格20-30')
print(res)
