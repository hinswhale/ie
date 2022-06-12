import re
from ie.utils.tools import CN_NUMBER_PATTERN, num_str, cn_num_digit, NUMBER_PATTERN, num_digit
from ie.utils.tools import repalce_tag
from ie.units.worktype import worktype_tag
import cn2an
from itertools import groupby

# ---薪酬根据数据内容获取，含多种薪资单位的，获取优先级日薪>月薪>时薪，获取不到则为面议，日薪区间50-1999；月薪区间2000-29999；时薪区间1-100，区间外为面议；
time_map = ['小时', '月', '天', '日', 'H', '时']
time_unit = '(小?时|天|个?月|H|日)'
num_danwei = '十百千万亿kw仟'
p = f'{num_str}\d+(.\d+)?'
zhongwen = r'[\u4e00-\u9fa5]+'
digit_float = r'\d+(.\d+)?'
p = f'{num_str}\d+(.\d+)?kw'
_ganraoci = '班|位|人|点|号|个|名|\(周?岁\)|\(岁\)|单元|平方|千米|台'
gaoraoci = [
    f'\d+点-\d+点',
    f'[每|\d+]月\d+日',
    f'[123456789][:.、]{zhongwen}',
    '\d{2}(-\d{2})?周?岁',
    '\d+[点:：]\d+',
    '休\d+天\d+',
    f'\d+([-一]\d+)?({_ganraoci})',
    '吃?补\d+(元|\/天)?',
    '\d+(元|\/天)餐补',
    f'[{p}半](天|个?月)[{p}](算|一?结)',
    f'[{cn_num_digit}][月|天][{cn_num_digit}]',
    '每天\d+小时',
    f'\d、'
]


def _cmp(x):
    if x == '元/天':
        x = -3
    elif x == '元/月':
        x = -2
    elif x == '元/时':
        x = -1
    else:
        x = 0
    return x


def compare(data):
    if not data:
        return data

    data.sort(key=lambda x: _cmp(x[u'unit']))
    # 按时间分组，并且取首日体温最大值
    for k, g in groupby(data, key=lambda x: x[u'unit']):
        g = list(g)
        res = max(g, key=lambda x: x['salary'])
        return res
    return data


def normalize_unit(data):
    d = []
    for i in data:
        salary = i[0]['salary'].split('-')[-1] if i[0]['salary'] else ''
        unit = i[0].get('unit')

        try:
            salary = salary.strip('+').strip('.')
            salary = salary.split('/')[-1]
            salary = salary.replace('k', '千').replace('w', '万') \
                .replace('w', '万').replace('元', '').replace('块', '')
            if '+' in salary:
                try:
                    salary = eval(salary)
                except:
                    salary = salary.strip('+')
            salary = int(cn2an.cn2an(salary, 'smart'))
            unit, salary = _normalize_unit(salary, unit)
            d.append({'salary': salary, 'unit': unit, 'i': i[0]})
        except Exception as e:
            print(i[0])
            continue
    return compare(d) or {}


def _normalize_unit(salary, unit):
    """
    根据数据内容获取，含多种薪资单位的，获取优先级日薪>月薪>时薪，获取不到则为面议，
    日薪区间100-1999；
    月薪区间2000-29999；
    时薪区间1-100，区间外为面议；
    :return:
    """
    if unit == '日薪':
        unit = '元/天'
        return unit

    salary = int(salary)
    unit = ''
    if unit:
        unit = unit.replace('一', '1').replace('每', '1') \
            .replace('二', '2') \
            .replace('两', '2') \
            .replace('三', '3') \
            .replace('四', '4') \
            .replace('五', '5') \
            .replace('六', '6') \
            .replace('七', '7') \
            .replace('八', '8') \
            .replace('九', '9') \
            .replace('十', '10') \
            .replace('H', '时').strip('/')
        g = re.search(f'(?P<num>[{p}])个?小?(?P<unit>{time_unit})', unit)
        if g:
            m = g.groupdict()
            unit = m.get('unit')
            num = m.get('num')
            if num and int(num) > 1 and unit in ['小时', '时']:
                unit = '元/天'
            else:
                for i in ['时', '天', '月']:
                    if i in unit:
                        unit = f'元/{i}'
        else:
            unit = f'元/{unit}'

    if 1 < salary < 100:
        unit = '元/时'
    elif 100 <= salary < 1999:
        unit = '元/天'
    elif 1999 <= salary < 29999:
        unit = '元/月'
    else:
        unit = ''
    if unit == '元/天' and salary > 1999:
        salary = ''
    if unit in ['元/天', '元/月'] and salary < 100:
        salary = ''
    return unit, salary


def _text_match(text, pattern_str, origin):
    dct = []
    for m in re.finditer(pattern_str, text):
        tag_dict = [m.groupdict(), m.start(), m.end(), origin[m.start():m.end()]]
        dct.append(tag_dict)
    return dct


def search(content):
    worktype_preys, content = worktype_tag(content)

    origin = content

    salary_keyword = f'(收入|转正|实习|保底|周结|月入|待遇|女零?工?|男零?工?|一结|薪资|白班?|夜班?|综合薪酬|底薪|月薪|包月|价格|工价|单价|工资|[{time_unit}]结|[{time_unit}]薪|月|[{num_str}]月以?后):?'
    for i, pattern in enumerate(gaoraoci):
        for m in re.finditer(pattern, content):
            content = re.sub(m.group(), '^' * len(m.group()), content)

    # for m in re.finditer(f'[一二三四五六七八九十]({zhongwen})', content):
    #     r = m.group()
    #     flag = True
    #     for i in time_map + ['元'] + num_danwei.split():
    #         if i in r:
    #             flag = False
    #             continue
    #     if flag:
    #         try:
    #             content = re.sub(m.group(), '^' * len(m.group()), content)
    #         except:
    #             pass
    salary_re = f'(?P<salary>{NUMBER_PATTERN}([/-]+{NUMBER_PATTERN})?)\+?元?'
    unit_re = f'[\/一]{time_unit}|/\d+?\/?({time_unit})|(\d+|每|{CN_NUMBER_PATTERN})(小时|天)'
    pattern_lst = [
        f'(?P<salary>\d+)(?P<unit>[{cn_num_digit}]{time_unit})',
        f'{p}天(?P<unit>[{p}](小时|天|个?月))(?P<salary>[{p}]+)(?!小时|(一个)?月)',
        f'(?P<salary>{NUMBER_PATTERN})(?P<unit>/(({cn_num_digit}{num_digit})?(小?时|天|个?月)|[每一二三四五六七八九十](小?时|天|个?月)|日薪))',
        f'(?P<unit>[{p}]{time_unit})(一天)?(?P<salary>{NUMBER_PATTERN})',
        f'({salary_keyword})(?P<salary>[{num_danwei}{digit_float}]+([-|.][{num_danwei}{digit_float}]+))?',
        f'(?P<unit>{unit_re}){salary_re}',
        f'{salary_keyword}{salary_re}',
        f'{salary_re}(元|块)[^餐天](?P<unit>{unit_re})',
        f'(?P<unit>{unit_re}){salary_re}[^餐天]',
        f'(?P<salary>\d+(-\d+)+)元?-(?P<unit>/一天)',
        f'(?P<salary>\d+-\d+-\d+)',
        # f'(?P<salary>\d+)-(?P<unit>\d+{time_unit})',
        f'(?P<salary>{digit_float})[月日]结'
    ]
    salary_lst = []
    for i, pattern in enumerate(pattern_lst):
        for m in re.finditer(pattern, content):
            if not m.groupdict().get('salary'):
                continue
            salary = m.groupdict().get('salary')
            unit = m.groupdict().get('unit')

            if salary in cn_num_digit and len(salary) == 1:
                continue
            if content[m.end():m.end() + 2] in time_map or (unit and '天' in unit and len(salary) == 1):
                continue

            try:
                if re.search(f"{salary}[{'|'.join(time_map)}][^结]", content):
                    continue
            except:
                continue
            tag_dict = [m.groupdict(), m.start(), m.end(), content[m.start():m.end()]]
            salary_lst.append(tag_dict)

        for m in salary_lst:
            content = content.replace(content[m[1]:m[2]], '^' * (m[2] - m[1]))
            content = repalce_tag([m], content)

    if not salary_lst:
        salary_lst = _text_match(content, f'(?P<salary>{digit_float}(-{digit_float})?(元|k|w|块))', origin)

    if not salary_lst:
        pattern_lst = [
            f'_+(?P<salary>\d+(-\d+)?)',
            f'(?<=A-Z)(?P<salary>\d+(-\d+)?)_+',
            f',(?P<salary>\d+(-\d+)?),',
            f'(?P<salary>\d+/月)',
            f'(?P<salary>\d+\d+)(?P<unit>月)',
        ]
        for i, pattern in enumerate(pattern_lst):
            for m in re.finditer(pattern, content):
                flag = True
                tag_dict = [m.groupdict(), m.start(), m.end(), origin[m.start():m.end()]]
                for i in time_map:
                    if tag_dict[-1] + i in content:
                        flag = False
                        continue
                if flag:
                    salary_lst.append(tag_dict)
    salarys = normalize_unit(salary_lst)

    return salarys
