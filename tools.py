import jieba
from typing import Tuple
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from ie.utils import read_json_file
from ie.settings import data_root

def load_dataset(sample: bool or int = False) -> Tuple:
    train_path = data_root + 'data.json'
    data = read_json_file(train_path)
    texts, labels = [], []
    for i, line in enumerate(data):
        if sample and i == sample:
            break
        text = ' '.join(jieba.cut(line['content']))
        texts.append(text)
        labels.append(line['label'])
    return texts, labels


def apply(instance, train, test):
    """ 对train和test分别处理"""
    train = instance.fit_transform(train)
    test = instance.transform(test)
    return train, test


class ModelTest:
    def __init__(self, X_train, y_train, X_test, y_test):
        self.X_train, self.y_train, self.X_test, self.y_test = X_train, y_train, X_test, y_test

    def eval(self, classifier):
        """测试模型"""
        classifier.fit(self.X_train, self.y_train)
        predictions = classifier.predict(self.X_test)

        score = metrics.f1_score(predictions, self.y_test, average='weighted')
        print(classification_report(self.y_test, predictions))
        print(confusion_matrix(self.y_test, predictions))
        print('weighted f1-score : %.03f' % score)

    def apply(self, instance):
        """ 对train和test分别处理"""
        self.X_train = instance.fit_transform(self.X_train)
        self.X_test = instance.transform(self.X_test)
