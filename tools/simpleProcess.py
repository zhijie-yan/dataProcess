import csv
import json

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

    # transferTerms()
    getNameFromHistory()
    # getNameFromSci()
    # getSortNames()