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
import csv
import json
import os
import re
from ltp import LTP

url = '../data/process/水利大辞典-定义-整理数据.json'
output = '../output/水利大辞典-关系-词条2定义.csv'
outputMerge = '../output/水利大辞典-关系-一对多关系.csv'
outputAllRel = '../output/relationships/allRelationships.csv'

personSciUrl = '../output/java/水利科技-人名.csv'
personHisUrl = '../output/java/水利史-人名.csv'
orgUrl = '../output/java/水利科技-组织机构.csv'
rivUrl = '../output/java/河流沟渠.csv'

outputSameMeanPath = '../output/relationships/sameMeanRel.csv'
outputWordInOthPath = '../output/relationships/wordInOtherWords.csv'
outputTripletPath = '../output/relationships/tripletPath.csv'
outputSegWordsPath = '../output/relationships/segWords.csv'
outputNoFindPath = '../output/relationships/noFindWords.csv'

jsonData = json.load(open(url, encoding='utf-8'))

# 读取数据阶段
name2id = {}
name2Definition = {}
namesLexicon = []

ltp = LTP()

for data in jsonData:
    namesLexicon.append(data['name'])
    name2id[data['name']] = data['id']
    name2Definition[data['name']] = data['context']
# 数据处理阶段 添加词典
ltp.add_words(words=namesLexicon)

num = 0
relArr = []
relMerge = []
wordNumDict = {}


def getIndividuals():
    individuals = []
    individuals += getIndividualData(personHisUrl)
    individuals += getIndividualData(personSciUrl)
    individuals += getIndividualData(orgUrl)
    individuals += getIndividualData(rivUrl)
    return individuals


def getIndividualData(url):
    dataList = []
    with open(url, 'r', newline='', encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
        for row in file_reader:
            dataList.append(row[0])
    return dataList


def get_index(lst=None, item=''):
    """
    找出所有item对应坐标
    """
    return [index for (index, value) in enumerate(lst) if value == item]


def computeWordNum():
    """
    统计出现在其他单词中的单词出现频次
    """
    for d in name2Definition:
        for name in namesLexicon:
            if name in d and name != d:
                print(str(name) + '------>' + str(d))
                rel = [name, d]
                relMerge.append(rel)
                if name not in wordNumDict:
                    wordNumDict[name] = 0
                wordNumDict[name] += 1


def extractRelationships():
    """
    根据单词出现的次数来判断方向---无科学依据
    """
    for d in name2Definition:
        # print(d,name2Definition[d])
        string = name2Definition[d]
        # 分词
        segment, hidden = ltp.seg([string])
        # 词性标注
        pos = ltp.pos(hidden)
        indexs = get_index(pos[0], 'n')

        for index in indexs:
            name = segment[0][index]
            if name in namesLexicon:
                if name in wordNumDict and d in wordNumDict:
                    if wordNumDict[name] > wordNumDict[d]:
                        rel = [name2id[name], name2id[d]]
                    else:
                        rel = [name2id[d], name2id[name]]
                elif name in wordNumDict:
                    rel = [name2id[name], name2id[d]]
                else:
                    rel = [name2id[d], name2id[name]]
                relArr.append(rel)
    print(relArr)
    print('----------------------------------------')
    print(relMerge)
    print('----------------------------------------')
    print(wordNumDict)


def getEqualWords():
    """
    获取同义词典
    """
    result = {}
    # 筛选同义词
    for name in name2Definition:
        pattern = re.compile(r'^亦称\“.*?\”。')
        someStrs = pattern.match(name2Definition[name])
        if someStrs != None:
            otherNames = []
            equalWordsArr = re.findall(r'“(.*?)”', someStrs.group(0))
            for equalWord in equalWordsArr:
                # print(str(name)+'亦称：'+equalWord)
                if equalWord in namesLexicon:
                    print(equalWord, name)
                otherNames.append(equalWord)
            result[name] = otherNames
    return result


def getSameMeanWords():
    """
    获取相同概念词典
    """
    sameMeansDict = {}
    for name in namesLexicon:
        # 筛选是否有同义词  即“.*”
        pattern = re.compile(r'即\“.*\”')
        otherNamePattern = pattern.match(name2Definition[name])
        if otherNamePattern != None:
            end = otherNamePattern.end()
            otherName = otherNamePattern.group(0)[2:end - 1]
            if otherName in namesLexicon:
                sameMeansDict[name] = [otherName]
    return sameMeansDict


def depTrans(dep):
    """
    将dep结果转换成字典形式
    @param dep: ltp调用dep后结果
    @return: 返回重新组织的字典结构
    """
    result = {}
    for tuple in dep:
        first = tuple[0]
        second = tuple[1]
        rel = tuple[2]
        if rel not in result:
            result[rel] = [(first, second)]
        else:
            result[rel].append((first, second))
    return result


def extractDataFromStr(contextItem, nameItem):
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
    resultTriplet = []  # 三元组
    noSubRelations = []
    noFindRelations = []
    usedWord = []  # 识别出来的单词
    vobWords = []
    iobWords = []
    v_iobWords = []
    subFlag = False
    # v1.1 最简单的提取动词和宾语--->添加CMP类型补语
    newDep = depTrans(dep[0])
    # 该句存在自己的主语
    if 'SBV' in newDep and seg[0][newDep['SBV'][0][0] - 1] in namesLexicon:
        subName = seg[0][newDep['SBV'][0][0] - 1]
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
                elif objectVobName in namesLexicon:
                    v_iobWords.append(objectVobName)

        if 'IOB' in newDep:
            for iob in newDep['IOB']:
                objectIobName = seg[0][iob[0] - 1]
                usedWord.append(objectIobName)
                if iob[1] == hedIndex and objectIobName in namesLexicon:
                    iobWords.append(objectIobName)
                elif objectIobName in namesLexicon:
                    v_iobWords.append(objectIobName)
        # 有主语
        if subFlag:
            if len(vobWords) >= 1:
                for vobName in vobWords:
                    if vobName != subName:
                        resultTriplet.append((subName, vobName, rel))
            if len(iobWords) >= 1:
                for iobName in vobWords:
                    if subName != iobName:
                        resultTriplet.append((subName, iobName, rel))
        else:
            v_iobWords.append(vobWords)
            v_iobWords.append(iobWords)

    # 提取第②种关系 从v_iobWords中获取
    for ioWord in v_iobWords:
        if len(ioWord) > 0 and nameItem != ioWord and ioWord in namesLexicon:
            noSubRelations.append((nameItem, ioWord))

    # 提取第三种关系
    for s in seg[0]:
        if s not in usedWord and s in namesLexicon and nameItem != s:
            # print('未发现的单词:',s)
            noFindRelations.append((nameItem, s))
    return resultTriplet, noSubRelations, noFindRelations


def redp():
    """
    读取基础数据，抽取三种类型的关系
    @return:
    """
    extractTriplet = []
    extractSegObj = []
    extractNoFind = []
    for nameItem in name2Definition:
        # print(nameItem)
        context = name2Definition[nameItem]
        context = context.replace('\n', '').strip(' ')
        # 分割句子
        contextList = context.split('。')
        # 去掉“亦称...”和“即...”这些,利用正则
        pattern1 = re.compile(r'^亦称\“.*?\”')
        pattern2 = re.compile(r'^即\“.*\”')
        for contextItem in contextList:
            flag1 = pattern1.match(contextItem)
            flag2 = pattern2.match(contextItem)
            if flag1 == None and flag2 == None and len(contextItem) > 0:
                resultTriplet, noSubRelations, noFindRelations = extractDataFromStr(contextItem, nameItem)
                if len(resultTriplet) >= 1:
                    extractTriplet += resultTriplet
                if len(noSubRelations) >= 1:
                    extractSegObj += noSubRelations
                if len(noFindRelations) >= 1:
                    extractNoFind += noFindRelations
    return extractTriplet, extractSegObj, extractNoFind


def getWordInWords():
    """
    获得名字嵌套的单词关系
    @return: 嵌套关系
    """
    nameRel = []
    wordNameNumDict = {}
    for word in namesLexicon:
        for name in namesLexicon:
            if name in word and name != word:
                nameRel.append((name, word))
                if name in wordNameNumDict:
                    wordNameNumDict[name] += 1
                else:
                    wordNameNumDict[name] = 1
    return nameRel, wordNameNumDict


def getNoExclusive(extract, exclusives, individuals=[]):
    """
    排除需要排除的节点数据
    @param extract: 要被提取的关系数据
    @param exclusives: 要被排除的节点list
    @param individuals: 要被排除的实体list
    @return: 排除后的关系
    """
    rel = []
    for exSame in extract:
        start = exSame[0]
        end = exSame[1]
        if start not in individuals and end not in individuals and start not in exclusives and end not in exclusives:
            rel.append((start, end))
    return rel


def getNoDictExclusive(extractSameMeanWords, exclusives, individuals):
    """
    因为存储的名字关系是字典数据，所以要用字典遍历方式进行遍历
    @param extractSameMeanWords: 要提取的关系字典
    @param exclusives: 排除list
    @return: 新的关系
    """
    exSameRel = []
    for exSameWord in extractSameMeanWords:
        for exName in extractSameMeanWords[exSameWord]:
            if exSameWord not in exclusives and exName not in exclusives and exSameWord not in individuals and exName not in individuals:
                exSameRel.append((exSameWord, exName))
    return exSameRel


def readRelCsv(outputAllRel):
    """
    根据url读取csv关系数据
    @param url:
    @return:
    """
    relAll = []
    with open(outputAllRel, 'r', newline='', encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
        for row in file_reader:
            start = row[0]
            end = row[1]
            if start != end:
                relAll.append((start, end))

    return relAll


def addNewRels(relArr, oldRelArr, existsWordRel, wordNameNumDict):
    for oldl, oldr in oldRelArr:
        if oldl + '&' + oldr not in existsWordRel and oldr + '&' + oldl not in existsWordRel:
            existsWordRel.append(oldl + '&' + oldr)
            if (oldr in wordNameNumDict and wordNameNumDict[oldr] > 2) and ((oldl in wordNameNumDict and
                                                                             wordNameNumDict[oldl] < wordNameNumDict[
                                                                                 oldr]) or oldl not in wordNameNumDict):
                relArr.append((oldr, oldl))
            else:
                relArr.append((oldl, oldr))


def getAllRel(relationForArr, relationBackArr, exclusives, individuals=getIndividuals(), relArr=[]):
    """
    获取相等概念，获取同义词，获取名字上的关系，获取提取的三元组，获取提取的宾语角色，获取未标注角色
    关系优先级：同义词（双向）>名字上关系>提取三元组>获取提取的宾语角色关系>未标注角色
    @return: 返回综合关系
    """
    existsWordRel = []
    if not os.path.exists(outputAllRel):
        # 字典
        extractSameMeanWords = getSameMeanWords()
        extractEqualWords = getEqualWords()
        # 关系数组
        extractNameRel, wordNameNumDict = getWordInWords()
        extractTriplet, extractSegObj, extractNoFind = redp()
        # 相等关系词语
        smeRelArr = getNoDictExclusive(extractSameMeanWords, exclusives, individuals)
        saveRel(outputSameMeanPath, smeRelArr)

        reverseRelArr = [[srar, sral] for sral, srar in smeRelArr]
        addNewRels(relArr, smeRelArr, existsWordRel, wordNameNumDict)
        relArr += reverseRelArr
        # 名字关系
        nameRelArr = getNoExclusive(extractNameRel, exclusives, individuals)
        saveRel(outputWordInOthPath, nameRelArr)
        addNewRels(relArr, nameRelArr, existsWordRel, wordNameNumDict)
        # 三元组
        tripletRelArr = getNoExclusive(extractTriplet, exclusives, individuals)
        saveRel(outputTripletPath, tripletRelArr)
        addNewRels(relArr, tripletRelArr, existsWordRel, wordNameNumDict)

        segRelArr = getNoExclusive(extractSegObj, exclusives, individuals)
        saveRel(outputSegWordsPath, segRelArr)
        addNewRels(relArr, segRelArr, existsWordRel, wordNameNumDict)

        noFindRelArr = getNoExclusive(extractNoFind, exclusives, individuals)
        saveRel(outputNoFindPath, noFindRelArr)
        addNewRels(relArr, noFindRelArr, existsWordRel, wordNameNumDict)
        saveRel(outputAllRel, relArr)
    else:
        relArr = readRelCsv(outputAllRel)
    # 转为relationForArr等格式
    for rel in relArr:
        start = name2id[rel[0]]
        end = name2id[rel[1]]
        if start in relationForArr:
            if end not in relationForArr[start]:
                relationForArr[start].append(end)
        else:
            relationForArr[start] = [end]
        if end in relationBackArr:
            if start not in relationBackArr[end]:
                relationBackArr[end].append(start)
        else:
            relationBackArr[end] = [start]
    # print(relationForArr)


def saveRel(outputPath, relArrTemp):
    """
    保存关系
    @param outputPath: 输出路径
    @param relArrTemp: 关系数组
    """
    # 新创建的关系都在relArr当中，需要将其写入文件中
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for rel in relArrTemp:
            f.write(str(rel[0]) + ',' + str(rel[1]) + '\n')
    f.close()


def saveTripletRel(outputPath, relArrTriple):
    """
    保存关系
    @param outputPath: 输出路径
    @param relArrTemp: 关系数组
    """
    # 新创建的关系都在relArr当中，需要将其写入文件中
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for rel in relArrTriple:
            f.write(str(rel[0]) + ',' + str(rel[1]) + str(rel[2]) + '\n')
    f.close()


if __name__ == '__main__':
    pass

    # relationForArr = {}
    # relationBackArr = {}
    # exclusives = []
    # getAllRel(relationForArr, relationBackArr, exclusives)
