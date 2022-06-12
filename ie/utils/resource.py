from ie.utils.tools import strQ2B
import logging
from ie.settings import proj_relpath


class ResourceStore(object):
    u"""资源存储器

    让不同的存储工具提供相同的对外接口 供存储资源内容
    """

    def save(self, id, name, content):
        # type: (str, str, str) -> None
        raise NotImplementedError()

    def load(self, id, name):
        # type: (str, str) -> str
        raise NotImplementedError()


class CodeStore(ResourceStore):
    u"""CodeStore 会把资源当作代码保存在代码仓库中"""

    def save(self, id, name, content):
        with open(self._file_path(name), 'w') as f:
            f.write(content)

    def load(self, id, name):
        u"""获取此资源的内容"""
        return self._load_file(self._file_path(name))

    def _file_path(self, name):
        if isinstance(name, str):
            fn = name
        else:
            raise TypeError('invalid dict name')
        fn += '.dict.txt'
        fn0 = proj_relpath('data', fn)
        return fn0

    @staticmethod
    def _load_file(full_file_name):
        with open(full_file_name) as f:
            return f.read()

    def __str__(self):
        return '<code-store>'


code_store = CodeStore()


class Resource(object):
    def __init__(self, id, name, parser_func):
        self.id = id
        self.name = name
        self.skip_immutable = False
        self.parser_func = parser_func
        self._lazy_obj = self.get_parsed_obj()

        # 废弃属性
        self.description = u''
        self.created_at = None
        self.updated_at = None

    def _select_store(self):
        return code_store

    # TODO: 支持二进制 content

    def set_content(self, content):
        self._select_store().save(self.id, self.name, content)

    def get_content(self):
        u"""获取此资源的内容"""
        store = self._select_store()
        c = store.load(self.id, self.name)
        return c

    @property
    def words(self):
        u"""为了向后兼容 也可以通过 res.words 这种方式获取内容 等同于 res.get_content()"""
        return self.get_content()

    @property
    def data(self):
        return self._lazy_obj

    def get_parsed_obj(self):
        res = self.parser_func(self)
        return res

    def reload(self):
        self.data.__reset__()

    def set_skip_immutable(self):
        self.skip_immutable = True


class ResourceNotFound(Exception):
    pass


class DictManager(object):
    def __init__(self):
        self.log = logging.getLogger('engine')
        self._res = {}  # {<res-key> : <resource-obj>}

    def register(self, key, dict_name, parser_func):
        u"""
        :param key:  资源唯一标示 不能重复
        :param dict_name:   资源文件的文件名，不带后缀
        :param parser_func:
        :return:
        """
        self._res[key] = Resource(key, dict_name, parser_func)
        return self._res[key].data

    def resource(self, id):
        u"""获取已注册的 resource 对象"""
        try:
            return self._res[id]
        except KeyError:
            raise ResourceNotFound(id)

    def get_parsed_obj_by_key(self, key):
        return self._res[key].data

    # 几个向上兼容的方法
    def load_all(self):
        pass

    def load_dict(self, dict_name):
        pass

    def update(self):
        pass


# 全局唯一的 DictManager 实例
dict_manager = DictManager()


def naive_regionalism_code(dictionary):
    data = {}
    lines = dictionary.words.splitlines()
    for line in lines:
        line = strQ2B(line)
        lines = line.split('\t')
        if not lines:
            continue
        level = len(lines)
        if lines[-1]:
            code, name = lines[-1].split(u'|')
            if level == 1:
                province = name
                data[province] = {'code': code, 'data': {}}
            elif level == 2:
                city = name
                data[province]['data'][city] = {'code': code, 'data': {}}
            elif level == 3:
                area = name
                data[province]['data'][city]['data'][area] = {'code': code, 'data': {}}
    return data


xingzhenquhuadaima = dict_manager.register('address', u'area', naive_regionalism_code)
