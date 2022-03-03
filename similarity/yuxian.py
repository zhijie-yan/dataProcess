import jieba
import re
import numpy as np
import os
import pandas as pd

# os.chdir(r'C:\Users\Lenovo\Desktop\01040730kg73')
# os.chdir(r'C:\Users\Administrator\Desktop\示例数据')

# data4 = pd.read_excel('4.xlsx')
# data4_message = data4['详情']
# data4_answer = data4['意见']
data4_message = ['河流','通航建筑物']
data4_answer = ['河流','通船建筑物']
message_list = list(data4_message)


# 数据去敏
def qingli(s):
    string1 = s.apply(lambda x: re.sub('[0-9]', '*', str(x)))  # 去除数字
    m = re.compile('\s+')  # 定义空格
    string2 = string1.apply(lambda x: re.sub(m, '*', x))  # 去除空格
    punctuation = """，！？｡＂#＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""
    re_punctuation = "[{}]+".format(punctuation)  # 去除标点符号
    string3 = string2.apply(lambda x: re.sub(re_punctuation, '*', x))
    a = string3.apply(lambda x: re.sub('\*', '', x))
    return a


# 输入一条留言，关键词统计和词频统计，以列表形式返回
def Count(infile):
    t = {}
    f = infile
    count = len(f)

    s = infile
    i = 0
    words = jieba.lcut(infile)
    for word in words:
        if word != "" and t.__contains__(word):
            num = t[word]
            t[word] = num + 1
        elif word != "":
            t[word] = 1
        i = i + 1

    # 字典按键值降序
    dic = sorted(t.items(), key=lambda t: t[1], reverse=True)
    return (dic)


# 合并两篇文档的关键词
def MergeWord(T1, T2):
    MergeWord = []
    duplicateWord = 0
    for ch in range(len(T1)):
        MergeWord.append(T1[ch][0])
    for ch in range(len(T2)):
        if T2[ch][0] in MergeWord:
            duplicateWord = duplicateWord + 1
        else:
            MergeWord.append(T2[ch][0])

    # print('重复次数 = ' + str(duplicateWord))
    # 打印合并关键词
    # print(MergeWord)
    return MergeWord


# 得出文档向量
def CalVector(T1, MergeWord):
    TF1 = [0] * len(MergeWord)
    for ch in range(len(T1)):
        TermFrequence = T1[ch][1]
        word = T1[ch][0]
        i = 0
        while i < len(MergeWord):
            if word == MergeWord[i]:
                TF1[i] = TermFrequence
                break
            else:
                i = i + 1
    return TF1


def CalConDis(v1, v2, lengthVector):
    # 计算出两个向量的乘积
    B = 0
    i = 0
    while i < lengthVector:
        B = v1[i] * v2[i] + B
        i = i + 1

    # 计算两个向量的模的乘积
    A = 0
    A1 = 0
    A2 = 0
    i = 0
    while i < lengthVector:
        A1 = A1 + v1[i] * v1[i]
        i = i + 1
    i = 0
    while i < lengthVector:
        A2 = A2 + v2[i] * v2[i]
        i = i + 1

    A = np.math.sqrt(A1) * np.math.sqrt(A2)
    print('留言和回复的相似度 = ' + format(float(B) / A, ".3f"))


for i in range(len(data4_message)):
    # 数据清洗
    D_message = qingli(data4_message)
    D_answer = qingli(data4_answer)
    # 词频统计
    T_message = Count(D_message[i])
    T_answer = Count(D_answer[i])
    # 相同关键词
    mergeword = MergeWord(T_message, T_answer)
    # 向量化
    V_message = CalVector(T_message, mergeword)
    V_answer = CalVector(T_answer, mergeword)
    # 计算余弦距离
    # cos值越趋向于1，则说明两篇文档越相似，反之越不相似。
    print('第' + str(i) + '条')
    CalConDis(V_message, V_answer, len(V_message))
