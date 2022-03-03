import jieba
from gensimUse import corpora, models, similarities

all_location_list = []
location_list = []
for doc in location_list:
    doc_list = [word for word in jieba.cut_for_search(doc)]
    all_location_list.append(doc_list)

# 制作语料库,获取词袋
dictionary = corpora.Dictionary(all_location_list)
corpus = [dictionary.doc2bow(doc) for doc in all_location_list]
# 使用TF-IDF模型对语料库建模
tfidf = models.TfidfModel(corpus)

# 特征数
featureNUM = len(dictionary.token2id.keys())
# 通过TfIdf对整个语料库进行转换并将其编入索引，以准备相似性查询
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featureNUM)
# 稀疏向量.dictionary.doc2bow(doc)是把文档doc变成一个稀疏向量，[(0, 1), (1, 1)]，表明id为0,1的词汇出现了1次，至于其他词汇，没有出现。

doc_test = 'A市A市魅力之城商铺无排烟管道，小区'
doc_test_list = [word for word in jieba.cut_for_search(doc_test)]
# 测试文档的二元组向量转换
new_vec = dictionary.doc2bow(doc_test_list)
# 获取测试文档中，每个词的TF-IDF值
tfidf[new_vec]
# 计算向量相似度
sim = index[tfidf[new_vec]]
print(sim)

for i in range(len(location_list)):
    doc_test = location_list[i]

    #     w_ID = biaoge2_paqu.loc[i,'问题ID']
    w_ID = biaoge2.loc[i, '问题ID']
    if w_ID:
        pass
    else:
        #         p = biaoge2_paqu['问题ID'].max() + 1
        #         biaoge2_paqu.loc[i,'问题ID'] = p
        #     w1_ID = biaoge2_paqu.loc[i,'问题ID']

        p = biaoge2['问题ID'].max() + 1
        biaoge2.loc[i, '问题ID'] = p
    w1_ID = biaoge2.loc[i, '问题ID']

    doc_test_list = [word for word in jieba.cut_for_search(doc_test)]
    # 测试文档的二元组向量转换
    new_vec = dictionary.doc2bow(doc_test_list)
    # 获取测试文档中，每个词的TF-IDF值
    tfidf[new_vec]
    # 计算向量相似度
    sim = index[tfidf[new_vec]]
    for j in range(len(biaoge2)):
        w2_ID = biaoge2.loc[j, '问题ID']
        if w2_ID:
            pass
        elif list(sim)[j]:
            biaoge2.loc[j, '问题ID'] = w1_ID
#     print(sim)
