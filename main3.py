# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re
import os
import numpy as np
from argparse import ArgumentParser
import jieba
from sklearn import svm
import pandas as pd
from ie.settings import data_root
import fasttext
from types import MethodType, FunctionType

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression

from ie.utils import write_pkl_file, read_json_file


def get_args():
    parser = ArgumentParser(description='ie')
    parser.add_argument('--input', type=str, default="data")
    parser.add_argument('--file_test', type=str, default='test')
    parser.add_argument('--user_dict', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--char', type=bool, default=False)
    parser.add_argument('--jieba', type=bool, default=True)
    parser.add_argument('--stop', type=bool, default=True)
    args = parser.parse_args()
    return args


def clean_en_text(data):
    return data


def seg(sentence, sw, apply=None):
    if isinstance(apply, FunctionType) or isinstance(apply, MethodType):
        sentence = apply(sentence)
    return ' '.join([i for i in jieba.cut(sentence) if i.strip() and i not in sw])


def stop_words():
    with open(data_root + 'stop_words.txt', 'r', encoding='utf-8') as swf:
        return [line.strip() for line in swf]


def select_features(data_set):
    # dataset = [clean_en_text(data) for data in data_set[0]]
    tf_idf_model = TfidfVectorizer(ngram_range=(1, 1),
                                   binary=True,
                                   sublinear_tf=True)
    tf_vectors = tf_idf_model.fit_transform(data_set)
    vocab = tf_idf_model.vocabulary_

    # # 选出前1/5的词用来做特征
    # k = int(tf_vectors.shape[1] / 6)
    # chi_model = SelectKBest(chi2, k=k)
    # chi_features = chi_model.fit_transform(tf_vectors, data_set[1])
    # print('tf-idf:\t\t' + str(tf_vectors.shape[1]))
    # print('chi:\t\t' + str(chi_features.shape[1]))
    return tf_vectors, vocab, tf_idf_model


def str_q2b(ustring):
    """全角转半角"""
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        # 全角空格直接转换
        if inside_code == 12288:
            inside_code = 32
        # 全角字符（除空格）根据关系转化
        elif 65281 <= inside_code <= 65374:
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def clean_text(text):
    origin_text = text
    if not text:
        return text

    # text = html.unescape(text)
    # text = re.sub(ur'\s+', u' ', text)
    text = '\n'.join(text.split('<br>'))
    text = re.sub(r'<[^>]+>', '', text)

    text = str_q2b(text)
    text = text.replace('﹙', '(').replace('﹚', ')')
    text = text.replace('\r\n', '\n')
    text = text.strip()
    # if origin_text != text:
    #     print(f'origin: {origin_text}\n text :{text} \n\n')
    return text


def load_data(filepath):
    data = read_json_file(filepath)
    sents = [i['content'] for i in data]
    labels = [i['label'] for i in data]
    return sents, labels


def load_data(path):
    """
    其他 33355
    肺癌 2447
    乳腺癌 1830
    """
    dct = Counter()
    labels = []
    contents = []
    cutResult = []
    with open(path, 'r') as f:
        data = json.load(f)
        k = 0
        for i in data:
            text = i["出院诊断"]
            disease_id = get_disease_id(i['疾病大类名称'])
            dct[disease_id] += 1
            text = text.replace('\r\n', '').strip()
            text.replace('<br>', ' ')
            labels.append(disease_id)
            contents.append(text)
            cutResult.append(' '.join(list(jieba.cut(text))))
            k += 1
    return contents, labels, cutResult


def make_word2vec(data, fname):
    EMBEDDING_DIM = 128
    from gensim.models import word2vec
    contents, _, _ = load_data(file_path)
    model = word2vec.Word2Vec(contents, hs=1, min_count=1, window=3, size=EMBEDDING_DIM)
    model.save(fname)


def load_word2vec(word2vec_model_file):
    from gensim.models.keyedvectors import KeyedVectors
    w2v_model = KeyedVectors.load(word2vec_model_file)
    return w2v_model


def svm_train(x_train, y_train):
    svm_model = svm.SVC(kernel='linear', verbose=True)
    svm_model.fit(x_train, y_train)
    return svm_model


def LR_train(x_train, y_train):
    clr = LogisticRegression(penalty='l2', solver='sag', multi_class='multinomial', )
    clr.fit(x_train, y_train)
    return clr


def fasttext_train(x_train, y_train):
    pass


# def save_model(model, model_file):
#     with open(model_file, "wb") as file:
#         pickle.dump(model, file)
#
#
# def load_model(tf_idf_model, svm_model):
#     with open(tf_idf_model, 'rb') as f:
#         tf_idf_model = pickle.load(f)
#
#     with open(svm_model, 'rb') as f:
#         svm_model = pickle.load(f)
#     return tf_idf_model, svm_model


def main():
    test_size = 0.2
    train_path = data_root + 'data.json'
    data_set = load_data(train_path)

    x_train, x_test, y_train, y_test = train_test_split(data_set[0],
                                                        data_set[1],
                                                        test_size=test_size,
                                                        random_state=42)
    X_train, vocab, tf_idf_model = select_features(x_train)
    X_test = tf_idf_model.transform(x_test)
    print('train', X_train.shape, 'test', X_test.shape)
    # 这里采用的是线性分类模型,如果采用rbf径向基模型,速度会非常慢.
    model = svm.SVC(kernel='linear', verbose=True, class_weight='balanced')
    print(model)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print('测试准确率:', score)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    # Create DataFrame
    df = pd.DataFrame({'content': x_test, 'y_pred': y_pred, 'y_true': y_test})
    df.to_csv('../test.csv')
    write_pkl_file(model, '../model.pkl')


def clean_txt(raw):
    fil = re.compile(r"[^0-9a-zA-Z\u4e00-\u9fa5]+")
    return fil.sub(' ', raw)


import fastText.FastText as fasttext


def train_model(ipt=None, opt=None, model='', dim=100, epoch=5, lr=0.1, loss='softmax'):
    np.set_printoptions(suppress=True)
    if os.path.isfile(model):
        classifier = fasttext.load_model(model)
    else:
        classifier = fasttext.train_supervised(ipt, label='__label__', dim=dim, epoch=epoch,
                                               lr=lr, wordNgrams=2, loss=loss)
        classifier.save_model(opt)
    return classifier


if __name__ == '__main__':
    # args = get_args()
    # main()
    # 对某个sentence进行处理：
    content = '上海天然橡胶期价周三再创年内新高，主力合约突破21000元/吨重要关口。'
    res = seg(content.lower().replace('\n', ''), stop_words(), apply=clean_txt)

    print(res)
