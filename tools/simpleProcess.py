import csv
import json
import re

from ltp import LTP

jsonUrl = '../data/process/水利大辞典-定义-整理数据.json'
termUrl = '../output/java/terms.csv'
hisUrl = '../output/java/水利史.csv'
sciUrl = '../output/java/水利科技.csv'
sortUrl = '../output/java/sortWord.csv'
relUrl = '../output/水利大辞典-关系-词条2定义.csv'

outputHisName = '../output/java/水利史-人名.csv'
outputSciStartName = '../output/java/水利科技-组织机构.csv'
outputSciEndName = '../output/java/水利科技-人名.csv'
outputTerms = '../output/java/termIds.csv'
outputSortWords = '../output/java/排序词条.csv'
outputRiver = '../output/java/河流沟渠.csv'

jsonData = json.load(open(jsonUrl,encoding='utf-8'))

ltp = LTP()

def getData(url):
    dataList = []
    with open(url, 'r', newline='', encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
        for row in file_reader:
            dataList.append(row[0])
    return dataList

# 保存节点list
def saveNodes(outputPath,nodes):
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for node in nodes:
            f.write(node + '\n')
    f.close()

# 保存某节点前所有list
def saveStartNodes(outputPath,nodes,nodeName):
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for node in nodes:
            # f.write(name2id[node] + '\n')
            f.write(node + '\n')
            if node == nodeName:
                f.close()
                return

def saveEndNodes(outputPath,nodes,nodeName):
    flag = True
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for node in nodes:
            if node != nodeName and flag:
                continue
            else:
                flag = False
            f.write(node + '\n')
            # f.write(name2id[node] + '\n')

def transferTerms():
    termsName = getData(termUrl)
    print(termsName)
    termsIds = [name2id[name] for name in termsName]
    print(termsIds)
    saveNodes(outputTerms, termsIds)

def getNameFromHistory():
    historyIds = getData(hisUrl)
    historyNames = [id2name[id] for id in historyIds]
    print(historyNames)
    # saveStartNodes(outputHisName,historyNames,'管子')
    saveEndNodes(outputRiver,historyNames,'京杭运河')

def getNameFromSci():
    sciIds = getData(sciUrl)
    sciNames = [id2name[id] for id in sciIds]
    print(sciNames)
    saveStartNodes(outputSciStartName, sciNames, '意大利结构模型研究所')
    saveEndNodes(outputSciEndName,sciNames,'李仪祉')

def getSortNames():
    sortIds = getData(sortUrl)
    sortNames = [id2name[id] for id in sortIds]
    print(sortNames)
    print(len(sortNames))
    saveNodes(outputSortWords,sortNames)

def redp():
    for nameItem in name2Definition:
        context = name2Definition[nameItem]
        print(nameItem+':'+context)
        # 分割句子
        contextList = context.split('。')
        # 去掉“亦称...”和“即...”这些,利用正则
        pattern1 = re.compile(r'^亦称\“.*?\”。')
        pattern2 = re.compile(r'^即\“.*\”')
        for contextItem in contextList:
            flag1 = pattern1.match(contextItem)
            flag2 = pattern2.match(contextItem)
            if flag1 == None and flag2 == None and len(contextItem) > len(nameItem):
                seg, hidden = ltp.seg([contextItem])
                # 统计出现次数
                # numFind = 0
                # realWord = []
                # for wordName in seg[0]:
                #     if wordName in namesLexicon and wordName != nameItem:
                #         realWord.append(wordName)
                #         numFind += 1
                # 语义角色标注
                srl = ltp.srl(hidden)
                # 依存句法分析
                dep = ltp.dep(hidden)
                # 关系表述→状语* 动词 + 补语? 宾语?
                # v1.0 最简单的提取动词和宾语
                subject = []
                object = []
                relations = []
                for d in dep[0]:
                    name = seg[0][d[0]-1]
                    if d[2] == 'SBV' and name in namesLexicon:
                        subject.append(name)
                        # numFind -= 1
                    elif (d[2] == 'VOB' or d[2] == 'POB') and name in namesLexicon:
                        object.append(name)
                        # numFind -= 1
                    elif d[2] == 'HED':
                        relations.append(name)
                # print(relations)
                # print(object)
                print('------------------------------------')
                # print(realWord)
                print(subject + object)
                print(relations)
                # print('实际存在比标出的单词数多了：'+str(numFind))
                print('------------------------------------')
        # break

if __name__ == '__main__':
    # 读取数据阶段
    # 读节点 构造id和name互相映射
    name2id = {}
    id2name = {}
    name2Definition = {}
    namesLexicon = []

    for data in jsonData:
        namesLexicon.append(data['name'])
        name2id[data['name']] = str(data['id'])
        id2name[str(data['id'])] = data['name']
        name2Definition[data['name']] = data['context']
        # 数据处理阶段 添加词典
    # 添加自定义字典
    ltp.add_words(words=namesLexicon)

    # transferTerms()
    # getNameFromHistory()
    # getNameFromSci()
    # getSortNames()
    redp()