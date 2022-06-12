import pandas as pd
import jieba


def drop_stopwords(content_res, stopwords):
    contents_clean = []
    all_words = []
    for line in content_res:
        # 用于存储清洗后的词
        line_clean = []
        for word in line:
            # 如果这个词出现在停用词里，过滤掉
            if word in stopwords:
                continue
            # 存储过滤后的词
            line_clean.append(word)

            all_words.append(str(word))
        # 把已经清洗的列表存储起来
        contents_clean.append(line_clean)
    return contents_clean, all_words  # contents_clean为清理完的数据，为二维列表


# 读取语料数据
df_news = pd.read_table("val.txt", names=['category', 'theme', 'url', 'content'], encoding='utf-8')
df_news = df_news.dropna()
# 将数据转为二维列表:list of list
content = df_news.content.values.tolist()  # 将每个content列转为列表，结果为二维列表

# 读取停用词表
df_stop = pd.read_csv("/ie/data/stop_words.txt", encoding="utf-8", sep="\n", names=['stopword'])
# 将数据转为二维列表:list of list
stopwords = df_stop.stopword.values.tolist()

# 分词，数据格式：list of list
content_res = []
for line in content:
    current_segment = jieba.lcut(line)
    if len(current_segment) > 1 and current_segment != '\r\n':
        content_res.append(current_segment)

# 清停用词，数据格式：list of list
contents_clean, all_words = drop_stopwords(content_res, stopwords)

# 查看清洗后的数据
# df_content =pd.DataFrame({'content_res':contents_clean})
# print(df_content.head())

# 词频统计
# df_all_words = pd.DataFrame({'all_words':all_words})
# words_count = df_all_words.groupby(by=['all_words'])['all_words'].agg({"count":np.size})
# words_count =words_count.reset_index().sort_values(by=['count'],ascending=False)
# print(words_count.head())
