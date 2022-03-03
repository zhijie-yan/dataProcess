import jieba
from gensimUse import corpora
from gensimUse import models
from gensimUse import similarities
#from corpora.corpus import Corpus
# 1 分词
# 1.1 历史比较文档的分词
all_location_list = []
location_list = []
for doc in location_list:
    doc_list = [word for word in jieba.cut_for_search(doc)]
    # doc_list = [word for word in jieba.cut(doc)]
    all_location_list.append(doc_list)

# 1.2 测试文档的分词

doc_test="A市A市经济学院体育学院"
doc_test_list = [word for word in jieba.cut_for_search(doc_test)]
# doc_test_list = [word for word in jieba.cut(doc_test)]

# 2 制作语料库
# 2.1 获取词袋
dictionary = corpora.Dictionary(all_location_list)

# 2.2 制作语料库
# 历史文档的二元组向量转换
corpus = [dictionary.doc2bow(doc) for doc in all_location_list]
# 测试文档的二元组向量转换
doc_test_vec = dictionary.doc2bow(doc_test_list)

# 3 相似度分析
# 3.1 使用TF-IDF模型对语料库建模
tfidf = models.TfidfModel(corpus)
# 获取测试文档中，每个词的TF-IDF值
tfidf[doc_test_vec]

# 3.2 对每个目标文档，分析测试文档的相似度
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
sim = index[tfidf[doc_test_vec]]

# 根3.3 据相似度排序
sorted(enumerate(sim), key=lambda item: -item[1])
