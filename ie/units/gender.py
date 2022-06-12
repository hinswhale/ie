"""
性别获取不到则默认为男
"""
import re
import os

basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def search(content):
    grc_list = ['女儿墙']
    c = content

    for grc in grc_list:
        c = c.replace(grc, '干扰词')
        # s_list = [(m.start(), m.end(), m.group()) for m in re.finditer(grc, c)]
        # c[]

    value = u'男'
    if re.search(u'[男]', c, re.I):
        value = u'男'
    elif re.search(u'[女]', c, re.I):
        value = u'女'
    return value
