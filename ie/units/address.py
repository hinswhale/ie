import logging

from cocoNLP.extractor import extractor

from ie.utils.resource import xingzhenquhuadaima as regionalism_code
from ie.core.common import ganraoci

logger = logging.getLogger('engine')
zhixiashi = {
    u'北京': u'北京市',
    u'天津': u'天津市',
    u'上海': u'上海市',
    u'重庆': u'重庆市',
}
SUFFIXES = u'省市县区'

special_words = ['村']
ex = extractor()

ganraoci = ['长白班', '长期合作']


def short_name(name):
    short_name = name
    if len(short_name) > 2 and short_name[-1] in SUFFIXES and short_name[-3:-1] != u'自治':
        short_name = short_name[:-1]
    return short_name


class NaiveRegion(object):
    u"""行政区"""

    SUFFIXES = u'省市县区'
    # 一些旧称，注意不要和其他重复
    ts = {
        'province': 'city',
        'city': 'county',
    }

    def __init__(self):
        self._names = {}

    @property
    def names(self):
        if not self._names:
            for k, v in regionalism_code.items():
                self._names.setdefault(k, set())
                for kk, vv in v['data'].items():
                    self._names.setdefault(kk, set()).add(k)
                    for kkk, vvv in vv['data'].items():
                        self._names.setdefault(kkk, set()).update([k, kk])
        return self._names

    def best_split(self, names, name):
        # 最长拆分策略
        tmp = {u'len': 0, u'names': []}
        for i in names:
            if i not in name:
                continue

            new_name = name[name.index(i) + len(i):]
            child = self.best_split(names, new_name)
            l = len(i) + child[u'len']
            if l > tmp[u'len']:
                tmp[u'len'] = l
                tmp[u'names'] = [i] + child[u'names']
        return tmp

    def short_name(self, name):
        short_name = name
        if len(short_name) > 2 and short_name[-1] in self.SUFFIXES:
            short_name = short_name[:-1]
        return short_name


    def look_up_name(self, names, tree, level='province'):
        data = {
            level: '',
            level + '_code': '',
        }
        for name in names:
            for k, v in tree.items():
                if name in k:
                    data[level] = k
                    data[level + '_code'] = v['code']

                    if level in self.ts:
                        data.update(self.look_up_name(names, v['data'], self.ts[level]))

                    break
            else:
                continue
            break
        return data

    def _adress_detail(self, txt):
        locations = ex.extract_locations(txt)
        location = ''
        for location in locations:
            if location in ganraoci:
                location = ''
            else:
                break
        return location

    def search(self, txt):
        tmp_names = {}
        for name, v in self.names.items():
            short_name = self.short_name(name)
            # 多个省说明有重名情况
            if short_name in txt and len([i for i in v if i.endswith(u'省')]) <= 1:
                tmp_names.setdefault(short_name, set()).update(v)

        # 干扰词 勘误
        # 工农村 工农被识别成黑龙江鹤岗
        for i in tmp_names.copy():
            for g in special_words:
                if i + g in txt:
                    tmp_names.pop(i)
        for k, v in tmp_names.items():
            if k.strip('市') in zhixiashi:
                tmp_names[k] = {'市辖区', f'{k}市'}

        tmp = self.best_split(sorted([i for i in tmp_names], key=lambda x: txt.index(x)), txt)

        # 顺序不能乱，在前面的说明级别高
        names = []
        new_txt = txt
        for name in tmp[u'names']:
            names.append(name)
            names.extend(tmp_names[name])
            new_txt = new_txt.replace(name, '_' * len(name))

        names = list(set(names))
        from collections import defaultdict
        d = [{} for _ in range(len(names))]
        data = naive_region.look_up_name(names, regionalism_code)

        # address_lst = []
        # for i, v in data.items():
        #     d = {}
        #     d[v1]
        if data.get('city') == u'市辖区':
            data['city'] = data.get('province') or u''
        if data.get('city') == u'省直辖县级行政区划':
            data['city'] = data.get('county') or u''
        address = self._adress_detail(txt)
        if address in ''.join(names):
            address = ''
        data['address'] = address
        return data


naive_region = NaiveRegion()


def search(s):
    for i in ganraoci:
        s = s.replace(i, '')
    data1 = naive_region.search(s)
    print(data1)
    return data1
