import re
import gensimUse
import jieba
import numpy as np
from numpy.linalg import norm


def qingli(s):
    #pattern  = r"(https?://|[@#])\S*"
    #a = re.sub(pattern, '', s)
    #string1 = s.apply(lambda x:re.sub('[A-z]','*',str(x)))#去除字母
    string2 = s.apply(lambda x: re.sub('[0-9]', '*',str(x)))#去除数字
    m=re.compile('\s+')#定义空格
    string3 = string2.apply(lambda x: re.sub(m, '*',x))#去除空格
    punctuation = """，！？｡＂#＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""
    re_punctuation = "[{}]+".format(punctuation)#去除标点符号
    string3 = string2.apply(lambda x: re.sub(re_punctuation, '*', x))
    a = string3.apply(lambda x: re.sub('\*','',x))
    return a

data4_all_message = ['河流','通航建筑物']
data4_answer = ['河流','通船建筑物']

data4_message_qingli = qingli(data4_all_message)
data4_answer_qingli = qingli(data4_answer)
data4_all_message_qingli = data4_message_qingli+data4_answer_qingli

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='GB18030').readlines()]
    return stopwords

stopwords = stopwordslist("stopword.txt")

def preprocess_text_unsupervised(content_lines, sentences):
    for line in content_lines:
        try:
            segs = jieba.cut(line)
            segs = filter(lambda x:len(x)>1, segs)
            segs = filter(lambda x:x not in stopwords, segs)
            sentences.append(list(segs))
        except Exception:
            print(line)
            continue
#生成无监督训练数据
sentences = []

preprocess_text_unsupervised(data4_all_message_qingli, sentences)
sentences
model=gensimUse.models.word2vec.Word2Vec(sentences, min_count=1, sg=1, size=100, window=5)
model.most_similar(['管理'])
#需要去除停用词才可达到效果！
def vector_similarity(s1, s2):
    def sentence_vector(s):
        words = jieba.lcut(s)
        #words = jieba.analyse.extract_tags(s,allowPOS=('n','nr','nr1','nr2','nrj','nrf','ns','nsf','nt','nz','nl','ng','nrfg'))
        ba = []
        for i in range(len(words)):
            if len(words[i])<=1:
                ba.append(words[i])
        words=list(set(words)-set(ba))
        words=list(set(words)-set(stopwords))
        v = np.zeros(100)
        for word in words:
                v += model[word]
        v /= len(words)
        return v
    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    return np.dot(v1, v2) / (norm(v1) * norm(v2))

s1 = data4_message_qingli[1]
s2 = data4_answer_qingli[1]
s3 = '您好，由于本人爱人身份证过期，回I6市办了临时身份证，正式身份证要1个月后才能拿到，现在又办不了加急，医院不给办出生证明，必须要正式身份证才给办理，但是小孩刚出生，因黄旦太高住院花了不少钱，急着办落地险，希望能报销一部分，现在医院不给办出生证明无法办理新生儿落地险，等正式身份证拿到，已然过了办理落地险的时间，我很疑惑，临时身份证效力等同正式身份证，信息一样可以手动录入，为什么就是不给办理？'
vector_similarity(s1, s2)
