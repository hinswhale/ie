import re
import cn2an
import time
import functools
CN_NUM = {
    '零': 0,
    '〇': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
    '两': 2,
}

CN_UNIT = [
    (u'兆', 1000000000000),
    (u'亿', 100000000),
    (u'億', 100000000),
    (u'万', 10000),
    (u'萬', 10000),
    (u'千', 1000),
    (u'仟', 1000),
    (u'百', 100),
    (u'佰', 100),
    (u'十', 10),
    (u'拾', 10),
    (u'〇', 0),
    (u'零', 0),
]

num_str = '零〇一二三四五六七八九十百千万亿仟'
unit_str = '十百千万亿仟'
cn_num_digit = '一二三四五六七八九十'
num_digit = '1234567890'
CN_NUMBER_PATTERN = f'[{num_str}]+'
NUMBER_PATTERN = f'[{num_str}{num_digit}]+'
TIME_UNIT = '月天时'


def strQ2B(ustring):
    """把字符串全角转半角"""
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


def strB2Q(ustring):
    """把字符串全角转半角"""
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 32:  # 全角空格直接转换
                inside_code = 12288
            elif (inside_code >= 33 and inside_code <= 126):  # 全角字符（除空格）根据关系转化
                inside_code += 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


def clean_text(text):
    if not text:
        return text
    text = text.replace('o', '0')
    text = re.sub('\s+', u' ', text)
    text = re.sub('-{2,}', u'-', text)
    text = strQ2B(text)
    text = text.replace(u'﹙', u'(').replace(u'﹚', u')')
    text = text.replace(u'\r\n', u'\n')
    text = text.strip()

    return text


def cn_to_num(s):
    for c, n in CN_UNIT:
        if s == c:
            return n
        l = s.split(c)
        if len(l) == 2:
            l[0] = l[0] if l[0] else '一'
            l[1] = l[1] if l[1] else '〇'
            try:
                t = cn_to_num(l[0]) * n + cn_to_num(l[1])
            except:
                t = ''
            return t
    if s not in CN_NUM:
        t = ''
        for i in s:
            t += CN_NUM.get(i, '')
        return t
    return CN_NUM[s]


def repalce_tag(preys, content):
    preys = sorted(preys, key=lambda x: (x[1], x[2]))
    start = 0
    text = ''
    for prey in preys:
        text += content[start: prey[1]]
        text += '_' * (prey[2] - prey[1])
        start = prey[2]
    text += content[start:len(content)]
    return text


def pattern_lst(pattern, content):
    l = []
    for m in re.finditer(pattern, content):
        if m.groupdict():
            n = m.groupdict()
            if 'num1' in n and n['num1']:
                v = n['num1']
                start = m.regs[1][0]
                end = m.regs[-1][1]
            else:
                v = n['num']
                start = m.regs[1][0]
                end = m.regs[1][1]
            l.append([v, start, end, content[start:end]])
    return l


def catch_chinese_digit(aim):
    # 中文转数字
    """
        '山东威海在在招一个管工九小时四百五,工期一年,__九小时230,工资押一付一,钱准,电话微信同步'
    =>
         山东威海在在招1个管工9小时450,工期1年,__9小时230,工资押1付1,钱准,电话微信同步
    :param aim:
    :return:
    """
    cn_number_dict = {}
    matches = re.finditer(CN_NUMBER_PATTERN, aim)
    for match in matches:
        mat = match.group(0)
        if mat in unit_str:
            continue
        digit = cn2an.cn2an(mat, 'normal')
        cn_number_dict[match.group(0)] = digit
    for k, v in cn_number_dict.items():
        aim = aim.replace(k, str(v))
    return aim


def merge_se(self, all_data):
    # 当前遇到交叉项时，简单取第一项
    all_data.sort(key=lambda x: (x[0], x[1]))
    res = []
    last_e = 0
    for data in all_data:
        s = data[0]
        e = data[1]
        if s < last_e:
            # 交叉
            continue
        res.append(data)
        last_e = e
    return res


def gen_replaced_txt(se_list, astr):
    """根据开始和结束idx的列表生成替换文本"""
    to_replace_text = []
    last_e = 0
    for (s, e) in se_list:
        # s < last_e TODO logger
        if s > last_e:
            to_replace_text.append(astr[last_e:s])
        replace = u'→' * (e - s)
        to_replace_text.append(replace)
        last_e = e
    if last_e < len(astr):
        to_replace_text.append(astr[last_e:])
    return u"".join(to_replace_text)


# 最大重试次数/重试间隔(单位秒）
def retry(max_retry=3, wait_fixed=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            retry_num = 0
            while retry_num < max_retry:
                rs = None
                try:
                    rs = func(*args, **kw)
                    break
                except Exception as e:
                    retry_num += 1
                    time.sleep(wait_fixed)
                    if retry_num == max_retry:
                        raise Exception(e)
                finally:
                    if rs:
                        return rs

        return wrapper

    return decorator