import pandas as pd
from sklearn.utils import shuffle

from ie.settings import data_root


def deal_excel(path, label, columns={'Unnamed: 0': 'content'}):
    df = pd.read_excel(path)
    df.dropna()
    print(df.columns)
    df.rename(columns=columns, inplace=True)
    df['label'] = label
    print(df.shape[0])
    return df


def deal_data():
    """
    聚合采集数据
    :return:
    """
    path = data_root + '自动摘录样本&相关词表/【样本】-工人-人工采集(不含字段抽取).xlsx'
    label = 1
    df1 = deal_excel(path, label)
    print(df1)

    path = data_root + '自动摘录样本&相关词表/【样本】-招工-平台抓取.xlsx'
    label = 0
    df2 = deal_excel(path, label, columns={'招工详情': 'content'})
    print(df2)
    df = pd.concat([df1, df2])
    df.reset_index(drop=True, inplace=True)
    df.to_csv(data_root + '/data.csv', index=False)


def load_data(path, num=800):
    def sample_(df, num):
        df = shuffle(df[df['label'] == 0])
        return df.iloc[:num, :]

    print(path)
    df = pd.read_csv(path)
    print(df.loc[:, 'label'].value_counts())
    group = df.groupby('label')
    res = []
    for key, df0 in group:
        if key == 0:  # 样本不均衡，需g采样
            df0 = sample_(df0, num)
        res.extend(df0.to_dict('records'))
    return res


def preprocess_worktype():
    file = data_root + '/自动摘录样本&相关词表/工种列表和工种关键词.csv'
    df = pd.read_csv(file)
    records = df.to_dict('records')
    cols = [i for i in df.columns if i not in ['名称', '代码', '上级代码']]
    df['工种类型'] = df[cols].apply(
        lambda x: ','.join(x.dropna().astype(str)),
        axis=1
    )
    df.drop(df.columns.difference(['名称', '代码', '上级代码', '工种类型']), 1, inplace=True)
    df.to_csv(data_root + '/工种列表和工种关键词.csv', index=False)

preprocess_worktype()
#
# # import pandas as pd
# # from imblearn.over_sampling import SMOTE  # 过度抽样处理库SMOTE
# #
# # df = pd.read_table('data2.txt', sep=' ', names=['col1', 'col2', 'col3', 'col4', 'col5', 'label'])
# # x = df.iloc[:, :-1]
# # y = df.iloc[:, -1]
# # groupby_data_orginal = df.groupby('label').count()
# # model_smote=SMOTE()    #建立smote模型对象
# # x_smote_resampled,y_smote_resampled=model_smote.fit_sample(x,y)
# # x_smote_resampled=pd.DataFrame(x_smote_resampled,columns=['col1','col2','col3','col4','col5'])
# # y_smote_resampled=pd.DataFrame(y_smote_resampled,columns=['label'])
# # smote_resampled=pd.concat([x_smote_resampled,y_smote_resampled],axis=1)
# # groupby_data_smote=smote_resampled.groupby('label').count()
#
#
# path = data_root + 'data.csv'
# data = load_data(path, num=880)
# filepath = data_root + 'data.json'
# print(filepath)
# # 打乱数据顺序
#
# index = [i for i in range(len(data))]
# random.shuffle(index)
# sents = [data[i] for i in index]
# write_json_file(sents, filepath)
