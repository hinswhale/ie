from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
import jieba
import warnings

warnings.filterwarnings('ignore')


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


class similarity(object):
    def __init__(self):
        pass

    def transform(self, text1, text2):
        """
        把文本text1，text2转化为英文样式的text1，text2和向量vec1，vec2
        :param text1:
        :param text2:
        :return:
        """

        if check_contain_chinese(text1):
            text1 = ' '.join(jieba.lcut(text1))
            text2 = ' '.join(jieba.lcut(text2))
        else:
            pass

        corpus = [text1, text2]
        cv = CountVectorizer(binary=True)
        cv.fit(corpus)
        vec1 = cv.transform([text1]).toarray()
        vec2 = cv.transform([text2]).toarray()
        return text1, text2, vec1, vec2

    def compute(self, text1, text2):
        """
        对输入的text1和text2进行相似性计算，返回相似性信息
        :param text1:  文本字符串
        :param text2: 文本字符串
        :return:  字典， 形如{
                'Sim_Cosine':0.8,
                'Sim_Jaccard': 0.3,
                'Sim_MinEdit': 0.5,
                'Sim_Simple': 0.8
                }
        """
        text11, text22, vec1, vec2 = self.transform(text1, text2)
        data = {
            'Sim_Cosine': self.cosine_similarity(vec1, vec2),
            'Sim_Jaccard': self.jaccard_similarity(vec1, vec2),
            'Sim_MinEdit': self.minedit_similarity(text11, text22),
        }
        return data

    def cosine_similarity(self, vec1, vec2):
        cos_sim = cosine_similarity(vec1, vec2)
        return cos_sim[0][0]

    def jaccard_similarity(self, vec1, vec2):
        """ returns the jaccard similarity between two lists """
        vec1 = set([idx for idx, v in enumerate(vec1[0]) if v > 0])
        vec2 = set([idx for idx, v in enumerate(vec2[0]) if v > 0])
        return len(vec1 & vec2) / len(vec1 | vec2)

    def minedit_similarity(self, text1, text2):
        words1 = jieba.lcut(text1.lower())
        words2 = jieba.lcut(text2.lower())
        leven_cost = 0
        s = SequenceMatcher(None, words1, words2)
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag == 'replace':
                leven_cost += max(i2 - i1, j2 - j1)
            elif tag == 'insert':
                leven_cost += (j2 - j1)
            elif tag == 'delete':
                leven_cost += (i2 - i1)
        return leven_cost

sim = similarity()

if __name__ == '__main__':
    text1 = "悦龙男工，日结，上八下六点半，17一小时，下班结账。装卸打柜。给5元餐补。有去的联系"
    text2 = "悦龙男工，日结，上八下六点半，17一小时，下班结账。装卸打柜。给5元餐补。一共175元。有去的联系"

    sim = similarity()
    res = sim.compute(text1, text2)
    print(res)
