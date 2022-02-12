"""
目的：根据词条的定义，为词条间创建关系，另存导出关系文件
读取数据阶段：
1.创建词条词典，词条name和id一一对应
2.创建补充词典，用于存储添加不存在的词条
3.创建定义词典，能根据词条name找到其对应定义
处理：
1.遍历每个词和其对应的定义，使用分词工具（如LTP）对定义进行处理，找出其中所有的n
2.遍历名词，看是否有对应的词条存在，有就添加一条id关系，存到关系list中
补充：2阶段可以对名词调用wordnet的同义词典，然后如果同义词有出现在词条集合中，也可以添加关系
3.使用pagerank算法，找出重要的概念作为本体概念
"""
import json
from ltp import LTP

def get_index(lst=None, item=''):
    return [index for (index,value) in enumerate(lst) if value == item]


ltp = LTP()

url = '../data/process/水利大辞典-定义-整理数据.json'
output = '../output/水利大辞典-关系-词条2定义.csv'
jsonData = json.load(open(url,encoding='utf-8'))

# 读取数据阶段
name2id = {}
name2Definition = {}
namesLexicon = []

for data in jsonData:
    namesLexicon.append(data['name'])
    name2id[data['name']] = data['id']
    name2Definition[data['name']] = data['context']
# 数据处理阶段
ltp.add_words(words=namesLexicon)
num = 0
relArr = []
for d in name2Definition:
    # print(d,name2Definition[d])
    string = name2Definition[d]
    # 分词
    segment, hidden = ltp.seg([string])
    # 词性标注
    pos = ltp.pos(hidden)
    indexs = get_index(pos[0],'n')
    for index in indexs:
        if segment[0][index] in namesLexicon:
            num += 1
            # print(segment[0][index])
            rel = [name2id[d],name2id[segment[0][index]]]
            relArr.append(rel)
# 新创建的关系都在relArr当中，需要将其写入文件中
with open(output, 'w', encoding='utf-8', newline='') as f:
    for rel in relArr:
        f.write( str(rel[0]) + ',' + str(rel[1]) + '\n')


