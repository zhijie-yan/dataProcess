import csv
import json
import re

from ltp import LTP

from waterDict.extractRelation import readRelCsv, saveRel

jsonUrl = '../data/process/水利大辞典-定义-整理数据.json'
termUrl = '../output/java/terms.csv'
hisUrl = '../output/java/水利史.csv'
sciUrl = '../output/java/水利科技.csv'
sortUrl = '../output/java/sortWord.csv'
relUrl = '../output/水利大辞典-关系-词条2定义.csv'
allRelUrl = '../output/relationships/allRelationships.csv'
conceptsUrl = '../data/concepts.csv'

outputHisName = '../output/java/水利史-人名.csv'
outputSciStartName = '../output/java/水利科技-组织机构.csv'
outputSciEndName = '../output/java/水利科技-人名.csv'
outputTerms = '../output/java/termIds.csv'
outputSortWords = '../output/java/排序词条0.csv'
outputRiver = '../output/java/河流沟渠.csv'
outputAllRel = '../output/relationships/allRelationshipsIds.csv'

jsonData = json.load(open(jsonUrl,encoding='utf-8'))

ltp = LTP()




def getCsvData(url):
    """
    根据url读取csv数据,只拿第一列数据
    @param url:
    @return:
    """
    dataList = []
    with open(url, 'r', newline='', encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
        for row in file_reader:
            dataList.append(row[0])
    return dataList

# 保存节点list
def saveNodes(outputPath,nodes):
    """
    保存list数据，最基础的保存
    @param outputPath:路径
    @param nodes: 数据
    """
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for node in nodes:
            f.write(node + '\n')
    f.close()
# 保存某节点前所有list
def saveStartNodes(outputPath,nodes,nodeName):
    """
    保存保存某节点前所有list
    @param outputPath: 路径
    @param nodes: 节点list
    @param nodeName: 节点名称
    """
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for node in nodes:
            # f.write(name2id[node] + '\n')
            f.write(node + '\n')
            if node == nodeName:
                f.close()
                return
# 保存某节点和其后所有节点
def saveEndNodes(outputPath,nodes,nodeName):
    """
    保存某节点和其后所有节点
    @param outputPath: 路径
    @param nodes: 节点list
    @param nodeName: 名称
    """
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
    """
    name列表全转换成id保存
    """
    termsName = getCsvData(termUrl)
    print(termsName)
    termsIds = [name2id[name] for name in termsName]
    print(termsIds)
    saveNodes(outputTerms, termsIds)

def getNameFromHistory():
    """
    将保存的水利史id数据，全部转换成name
    """
    historyIds = getCsvData(hisUrl)
    historyNames = [id2name[id] for id in historyIds]
    print(historyNames)
    # saveStartNodes(outputHisName,historyNames,'管子')
    saveEndNodes(outputRiver,historyNames,'京杭运河')

def getNameFromSci():
    """
    保存组织机构
    """
    sciIds = getCsvData(sciUrl)
    sciNames = [id2name[id] for id in sciIds]
    print(sciNames)
    saveStartNodes(outputSciStartName, sciNames, '意大利结构模型研究所')
    saveEndNodes(outputSciEndName,sciNames,'李仪祉')

def transSortNames():
    """
    读取先前保存的按照节点重要性保存的节点list，将其从id保存转换成name保存
    @return: 保存新的排序节点
    """
    sortIds = getCsvData(sortUrl)
    sortNames = [id2name[id] for id in sortIds]
    print(sortNames)
    print(len(sortNames))
    saveNodes(outputSortWords,sortNames)

def transRelNameToIds(inputUrl,outPutUrl):
    inputNames = readRelCsv(inputUrl)
    outPutIds = [[name2id[input[0]],name2id[input[1]]] for input in inputNames]
    saveRel(outPutUrl,outPutIds)


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

    test = {}
    itra = 0
    for name in namesLexicon:
        print(itra)
        itra += 1
        seg, _ = ltp.seg([name2Definition[name]])
        test[name],_ = ltp.seg([name2Definition[name]])
    # 添加自定义字典
    ltp.add_words(words=namesLexicon)
    itra = 0
    for name in namesLexicon:
        print(itra)
        itra += 1
        seg,_ = ltp.seg([name2Definition[name]])
        if len(test[name]) != len(seg):
            print(name)
            print(seg)
    # transRelNameToIds(allRelUrl,outputAllRel)
    # transferTerms()
    # getNameFromHistory()
    # getNameFromSci()
    # getSortNames()
    # 判断水利大辞典中，水利规范的词占多少
    conceptDatas = getCsvData(conceptsUrl)
    conceptLen = len(conceptDatas)
    conceptNotInArr = []
    nameConcept = []
    for cdata in conceptDatas:
        if cdata not in namesLexicon:
            conceptNotInArr.append(cdata)
            for name in namesLexicon:
                if cdata in name:
                    nameConcept.append([cdata,name])
                    conceptNotInArr.remove(cdata)
                    break
    print('出现比例为:%s'%(len(conceptNotInArr)/conceptLen))
    print('未出现词汇为：')
    print(conceptNotInArr)
    print(nameConcept)


