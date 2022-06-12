import os

import thulac
import pandas as pd
import numpy as np

from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from ie.settings import data_root
from ie.utils import read_json_file, write_json_file, write_pkl_file


class Character(object):
    def __init__(self, data_path):
        self.dataset = read_json_file(data_path)

    def batch_segment(self):
        """对json数据集进行分割，返回一个 list"""
        print('start segmenting sentences...')
        return [self.segment(sent) for sent in tqdm(self.dataset)]

    def segment(self, sentence):
        segs = [v for v in sentence]
        # segs = [v for v in segs if not unicode(v).isdigit()]  # 去数字
        # segs = list(filter(lambda x: x.strip(), segs))  # 去左右空格
        # segs = list(filter(lambda x: len(x) > 1, segs))  # 长度为1的字符
        # segs = list(filter(lambda x: x not in stopwords, segs))  # 去掉停用词
        """对一个句子进行分割，返回一个 string"""
        # magic code to solve FUCKING encode issue
        return ' '.join(segs).encode('utf-8')


class Segmenter(object):
    """
    将文本变为分词形式
    """

    def __init__(self, data_path, jieba_=False, user_dict=None, stop=True):
        self.dataset = read_json_file(data_path)
        if jieba_:
            print('using jieba ...')
            self.jieba_ = True
        else:
            print('using thulac ...')
            self.jieba_ = False
            self.segmenter = thulac.thulac(user_dict=user_dict, seg_only=True, filt=True)  # 只进行分词，不进行词性标注
        if stop:
            print('using stop words...')
            stopwords = pd.read_csv('stop_words.txt', index_col=False, quoting=3, sep="\t", names=['stopword'],
                                    encoding='utf-8')
            self.stopwords = stopwords['stopword'].values
            self.stop = True
        else:
            self.stop = False

    def batch_segment(self):
        print('start segmenting sentences...')
        segs = [self.segment(sent) for sent in tqdm(self.dataset)]
        return segs

    def segment(self, sentence):
        """对一个句子进行分割，返回一个 string"""
        # magic code to solve FUCKING encode issue
        if self.jieba_:
            # import pdb; pdb.set_trace()
            segs = jieba.lcut(sentence)
            # pdb.set_trace()
            # segs = [v for v in segs if not v.isdigit()]  # 去数字
            # 加载停用词
            if self.stop:
                segs = [v for v in segs if v not in set(self.stopwords)]
            return ' '.join(segs).encode('utf-8'),

        else:
            return self.segmenter.cut(sentence.encode('utf-8'), text=True)


def load_dataset(data_path, jieba_=False, char=False, stop=True):
    dir = os.path.dirname(data_path)
    print("preprocessing sentences...")
    if char:
        print("char segement")
        segmenter = Character(data_path)
    else:
        print("word segement")
        segmenter = Segmenter(data_path, jieba_, stop=stop)

    dataset = segmenter.batch_segment()
    print("saving sentences...")
    write_json_file(dataset, cache_path)

    return dataset


class FeatureExtracter:
    """
    将分词结果变为向量化矩阵 X
    """

    def __init__(self, batch_seg_sentence, char=False):
        self.dataset = batch_seg_sentence
        if char:
            self.vectorizer = TfidfVectorizer(analyzer='char')
        else:
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 1), max_features=10000)

    def vectorize(self):
        X = self.vectorizer.fit_transform(self.dataset)
        vocab = self.vectorizer.vocabulary_
        return X, vocab, self.vectorizer


class Classifier:
    """
    将 X 分类为 y
    """

    def __init__(self, X, y):
        self.model = svm.LinearSVC()
        self.X = X
        self.y = y

    def train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=2)
        print('train', X_train.shape, 'test', X_test.shape)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))
        write_pkl_file(self.model, '../model.pkl')

    def predict(self, args, X_test, y_test):
        new_data = []
        count = 0
        y_pred = self.model.predict(X_test)
        for input, prediction, label in zip(read_json_file(args.input), y_pred, y_test):
            if prediction != label:
                pass
            else:
                count += 1
                new_data.append(input)
        print('generate new data json', count)
        write_json_file(new_data, 'new_data.json')


# 逻辑回归

# k最近邻算法

# 决策树

# 支持向量机

# 朴素贝叶斯

# # 加载数据
# dataset = load_dataset()
# print('dataset done')
# # 处理特征
# feature_extracter = FeatureExtracter(seg_res)
# X, vocab, vec = feature_extracter.vectorize()
# print(len(vocab))
# print('done tf-idf')
#
# classes, y = preprocess_y(args.input)
# # 模型训练
# classifier = Classifier(X, y)
# print('done init classifier')
# classifier.train()
# classifier.predict(args, X, y)
from collections import defaultdict

filepath = data_root + 'data.json'
data = read_json_file(filepath)
labels = defaultdict(list)
for i in data:
    labels[i['label']].append(i)
np.random.shuffle(labels[0])
labels[0] = np.random.shuffle(labels[0])
res = []
labels_0 = labels[0][:800]
labels_1
data
