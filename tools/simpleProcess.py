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
# 保存某节点和其后所有节点
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


def depTrans(dep):
    result = {}
    for tuple in dep:
        first = tuple[0]
        second = tuple[1]
        rel = tuple[2]
        if rel not in result:
            result[rel] = [(first,second)]
        else:
            result[rel].append((first,second))
    return result

def extractDataFromStr(contextItem,nameItem):
    """
    提取三种类型的关系，分别是：
    ①能直接提取的主谓宾
    ②不含主语，但是有VOB/IOB指出宾语的
    ③不含主语，未被指出，但是包含在词典中的单词
    @param contextItem: 将要被分析的句子
    @param nameItem: 句子对应的单词
    @return: 上述三种关系
    """
    seg, hidden = ltp.seg([contextItem])
    # 语义角色标注
    # srl = ltp.srl(hidden)
    # 依存句法分析
    dep = ltp.dep(hidden)
    # 声明一些参数
    resultTriplet = [] # 三元组
    noSubRelations = []
    noFindRelations = []
    usedWord = []  #识别出来的单词
    vobWords = []
    iobWords = []
    v_iobWords = []
    subFlag = False
    # v1.1 最简单的提取动词和宾语--->添加CMP类型补语
    newDep = depTrans(dep[0])
    # 该句存在自己的主语
    if 'SBV' in newDep and seg[0][newDep['SBV'][0][0]-1] in namesLexicon:
        subName = seg[0][newDep['SBV'][0][0]-1]
        subFlag = True
        usedWord.append(subName)
    # 提取第①种关系
    # 关系表述→状语* 动词 + 补语? 宾语?
    # 动词中心点
    if 'HED' in newDep:
        hedIndex = newDep['HED'][0][0]
        # ADV 前面是状语 不限个数
        advStr = ''
        if 'ADV' in newDep:
            for adv in newDep['ADV']:
                if adv[1] == hedIndex:
                    advStr += seg[0][adv[0] - 1]
        cmpStr = ''
        # CMP 后面是补语 最多一个
        if 'CMP' in newDep:
            for cmp in newDep['CMP']:
                if cmp[1] == hedIndex:
                    cmpStr += seg[0][cmp[0] - 1]
        rel = advStr + seg[0][hedIndex - 1] + cmpStr

        # VOB/IOB 最多一个
        if 'VOB' in newDep:
            for vob in newDep['VOB']:
                objectVobName = seg[0][vob[0] - 1]
                usedWord.append(objectVobName)
                if vob[1] == hedIndex and objectVobName in namesLexicon:
                    vobWords.append(objectVobName)
                else:
                    v_iobWords.append(objectVobName)

        if 'IOB' in newDep:
            for iob in newDep['IOB']:
                objectIobName = seg[0][iob[0] - 1]
                usedWord.append(objectIobName)
                if iob[1] == hedIndex and objectIobName in namesLexicon:
                    iobWords.append(objectIobName)
                else:
                    v_iobWords.append(objectIobName)
        # 有主语
        if subFlag:
            if len(vobWords) >= 1:
                for vobName in vobWords:
                    resultTriplet.append((subName,vobName,rel))
            if len(iobWords) >= 1:
                for iobName in vobWords:
                    resultTriplet.append((subName,iobName,rel))
        else:
            v_iobWords.append(vobWords)
            v_iobWords.append(iobWords)

    # 提取第②种关系 从v_iobWords中获取
    for ioWord in v_iobWords:
        if len(ioWord) > 0:
            noSubRelations.append((nameItem,ioWord))

    # 提取第三种关系
    for s in seg[0]:
        if s not in usedWord and s in namesLexicon:
            print('未发现的单词:',s)
            noFindRelations.append((nameItem,s))
    return resultTriplet,noSubRelations,noFindRelations

def redp():
    extractTriplet = []
    extractSegObj = []
    extractNoFind = []
    for nameItem in name2Definition:
        print(nameItem)
        if nameItem == '水库特征水位':
            print('')
        context = name2Definition[nameItem]
        context = context.replace('\n','').strip(' ')
        # 分割句子
        contextList = context.split('。')
        # 去掉“亦称...”和“即...”这些,利用正则
        pattern1 = re.compile(r'^亦称\“.*?\”')
        pattern2 = re.compile(r'^即\“.*\”')
        for contextItem in contextList:
            flag1 = pattern1.match(contextItem)
            flag2 = pattern2.match(contextItem)
            if flag1 == None and flag2 == None and len(contextItem) > 0:
                resultTriplet,noSubRelations,noFindRelations = extractDataFromStr(contextItem,nameItem)
                if len(resultTriplet) >= 1:
                    extractTriplet.append(resultTriplet)
                if len(noSubRelations) >= 1:
                    extractSegObj.append(noSubRelations)
                if len(noFindRelations) >= 1:
                    extractNoFind.append(noFindRelations)
    return extractTriplet,extractSegObj,extractNoFind

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
    extractTriplet,extractSegObj,extractNoFind = redp()
