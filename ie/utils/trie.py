class BaseTrie:
    """
        基础检索树类， 如果需要屏蔽大小写等操作，必须在调用检索树和初始化的时候调用strQ2B
        如果需要返回附带信息，则首先检索主key，然后通过主key再去查找附带信息
        检索策略为： 深度优先检索
    """

    def __init__(self, all_words):
        self.root = {}
        if isinstance(all_words, list):
            all_words = list(set(all_words))
        elif isinstance(all_words, dict):
            all_words = all_words.keys()
        self.buildTree(all_words)
        self.max_depth = max([len(w) for w in all_words])

    def buildTree(self, word_list):
        for w in word_list:
            node = self.root
            for c in w:
                if c not in node:
                    node[c] = {}
                node = node[c]
            if node != self.root:
                node['is_word'] = True

    def deep_search(self, corpus, start=0, end=0):
        """
        深度优先检索
        :param corpus:  待检测序列
        :param start:   起始index
        :param end:     终点index
        :return:
        """
        if end <= 0:
            end += len(corpus)
        if end > len(corpus):
            end = len(corpus)

        for s in range(start, end):
            p = self.root
            longest = u''
            e = s
            for i in range(s, s + self.max_depth):
                if i >= end: break
                if corpus[i] in p:
                    p = p[corpus[i]]
                    if 'is_word' in p:
                        longest = corpus[s:i + 1]
                        e = i + 1
                else:
                    break
            if len(longest) != 0:
                return [s, e, longest]
        return []

    def search(self, corpus):
        if corpus is None or len(corpus) == 0:
            return []

        corpus_len = len(corpus)
        s = 0
        match_result = []
        while s < corpus_len:
            res = self.deep_search(corpus, s)
            if len(res) > 0:
                match_result.append(res)
                s = res[1]
            else:
                break
        return match_result
