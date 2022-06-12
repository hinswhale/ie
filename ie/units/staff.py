import copy
import re

from ie.units.worktype import worktype_tag
from ie.utils.tools import cn_to_num, num_str, num_digit, pattern_lst

pa = '十?几多?[个|人]'
pattern = '(?P<num1>\d+几)(-(?P<num1>\d+))?多?[人|个|名]'
team_words = ['队伍', '班组', '施工队', '突击队', '大部队', '团队', '人员', '带干活', '劳务']


def preprocess_cn_num(context):
    data = pattern_lst(f'(?P<num>([{num_str}]))[个?人|个]', context)
    for i in data:
        context = context[:i[1]] + str(cn_to_num(i[0])) + context[i[1] + 1:]
    return context


def preprocess(content):
    # e.g. 七八个
    origin = content
    # 几个=5个 十几个=15个

    for m in re.finditer(f'(?P<num>([{num_str}{num_digit}]+(几|多)?|几|多))(个?人|个)', content):
        digit = m.groupdict()['num']
        if '几' in digit or '多' in digit:
            digit = digit.replace('几', '').replace('多', '')
            digit = cn_to_num(digit) if not digit.isdigit() else digit
            digit = int(digit or 0) + 5
        else:
            digit = digit[-1] if not digit.isdigit() else digit
        content = content[: m.start()] + str(digit) + content[m.end() - 1:]
    return content


def staff_compose(num, origin):
    def __desc(num):
        if v == '班组' and num == 1:
            num = None
        elif v == '个人':
            num = 1
        return num

    v = '个人'
    for word in team_words:
        if word in origin:
            v = '班组'
            num = __desc(num)
            return v, num
    v = '班组' if num and int(num) > 1 else '个人'
    num = __desc(num)
    return v, num


def search(content):
    origin = content
    content = preprocess_cn_num(content)
    content = preprocess(content)

    worktype_preys, text = worktype_tag(content)
    staff_preys = pattern_lst('(?P<num>\d+)几?(个?人|个|名)?_*(-(?P<num1>\d+)(个?人|个|名)?)?(?!级)', text)
    dct = []
    i = 0
    j = 0
    origin_data = copy.copy(staff_preys)

    while i < len(worktype_preys) and j < len(staff_preys):
        dj = staff_preys[j]
        pi = worktype_preys[i]
        if dj[2] + 1 == pi[1] or pi[2] == dj[1]:
            compose, num = staff_compose(dj[0], origin)
            origin_data.remove(dj)
            dct.append({'num': num, 'worktype': pi[0], 'compose': compose})
            i += 1
            j += 1
        elif pi[1] > dj[2]:
            compose, num = staff_compose(dj[0], origin)
            j += 1
            origin_data.pop(i)
            dct.append({'num': num, 'worktype': '', 'compose': compose})
        else:
            print('+++' * 30)
            compose, num = staff_compose(dj[0], origin)
            origin_data.remove(dj)
            dct.append({'num': num, 'worktype': pi[0], 'compose': compose})
            break
    else:
        if not dct:
            for i in origin_data:
                compose, num = staff_compose(i[0], origin)
                dct.append({'num': num, 'worktype': '', 'compose': compose})

    if not dct and not origin_data:
        compose, num = staff_compose(None, origin)
        dct.append({'num': num, 'worktype': '', 'compose': compose})
    return dct
