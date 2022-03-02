"""
使用度中心性算法计算节点排序
分多种情况排序：
无向图：
①不排除重复边，即两点之间允许存在多条边；
②将两点之间的重复边排除，大概能降重一万多条关系；
有向图：
①仅计算出度排序
②仅计算入度排序

度中心性算法：最简单的节点重要性度量算法

DC(i) = ki/(n-1)

其中ki = 累加i aij
aij即网络邻接矩阵 A 中第 i 行第 j 列元素, n 为网络的节点数目, 分母 n-1 为节点可能的最大度值

需要的参数（需要去除自指向边）：
n：节点总数
numInputList：每个节点入度和
numOutputList：每个节点出度和
avgInputList：入度平均
avgOutPutList：出度平均
"""
import json
import csv
import re

import networkx as nx
import numpy as np
from tools.pageRank2 import pageRank2
from tools.pageRankTool import pageRank
from tools.leaderRank import leaderrank
from tools.requestKGWork import getPreConcept
from tools.wordnetTest import getPreAndNextWord

# 读取边数据
from waterDict.extractRelation import getAllRel


def readRelation(inputPath,relationForArr,relationBackArr,exclusiveIdStart):
    """
    由路径，要排除的一级目录名称读出关系
    """
    with open(inputPath, 'r', newline='', encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
        for row in file_reader:
            start = row[0]
            end = row[1]
            # 去自指向
            if start == end or start in exclusiveIdStart or end in exclusiveIdStart:
                continue
            # 出度
            if start not in relationForArr:
                relationForArr[start] = []
            # 降重
            if end not in relationForArr[start]:
                relationForArr[start].append(end)
            # 入度
            if end not in relationBackArr:
                relationBackArr[end] = []
            # 降重
            if start not in relationBackArr[end]:
                relationBackArr[end].append(start)

def getSubConcepts(inputPath,nameId):
    """
    根据一级目录名字，找出其直接对应的所有子类
    @param inputPath: 输入路径
    @param nameId: 名字id
    """
    result = []
    with open(inputPath, 'r', newline='', encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
        for row in file_reader:
            start = row[0]
            end = row[1]
            if start == nameId:
                result.append(end)
    return result

def saveSortResult(outputPath,result):
    """
    保存排序结果
    @param outputPath: 保存路径
    @param result: id列表
    """
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for res in result:
            f.write(id2name[res[0]] + '\n')

def saveRelationship(outputPath,relationForArr):
    """
    保存关系字典
    @param outputPath:路径
    @param relationForArr: 关系字典
    """
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for rel in relationForArr:
            for val in relationForArr[rel]:
                f.write(str(rel) + ',' + str(val) + '\n')

def saveNodes(outputPath,nodes):
    """
    保存节点list
    @param outputPath: 输出路径
    @param nodes: 节点列表
    @return: 保存
    """
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for node in nodes:
            f.write(str(node) + '\n')

def saveRelationshipAsId(outputPath,relationships):
    """
    保存关系 由name转id
    @param outputPath: 输出路径
    @param relationships: 关系列表
    """
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for rel in relationships:
            for val in relationships[rel]:
                f.write(name2id[rel] + ',' + name2id[val] + '\n')

def getExclusiveIds(levelRelUrl, exclusiveIdStart):
    """
    根据词条小标题排除所有以其为起点的节点
    @param levelRelUrl: 水利词典原本存在的上下位关系
    @param exclusiveIdStart: 起始节点列表
    @return: 要排除的所有节点名字
    """
    exclusives = []
    with open(levelRelUrl, 'r', newline='', encoding='utf8') as file_read:
        file_reader = csv.reader(file_read)
        for row in file_reader:
            start = row[0]
            end = row[1]
            if start in exclusiveIdStart:
                exclusives.append(end)
    return exclusives

def getMatrix(relationForArr,relationBackArr,keys):
    """
    根据关系字典获得矩阵
    测试版本，失败，不再考虑
    """
    n = len(keys)
    G1 = [[0]*n for i in range(n)]
    id2index = {}
    index2id = {}
    index = 0
    for key in keys:
        id2index[key] = index
        index2id[index] = key
        index += 1
    for index in range(0,n):
        key = index2id[index]
        if key in relationForArr:
            listFor = relationForArr[key]
            for lf in listFor:
                G1[id2index[key]][id2index[lf]] = 1
        # if key in relationBackArr:
        #     listBack = relationBackArr[key]
        #     for lb in listBack:
        #         G1[id2index[lb]][id2index[key]] = 1
    return np.array(G1),n

def getKeys(relationForArr,relationBackArr):
    """
    根据关系字典获得所有节点名称
    @param relationForArr:正向字典
    @param relationBackArr: 逆向字典
    @return: 字典中存在的所有节点
    """
    keys = []  # 过滤后剩余的词条key
    for rr in relationForArr:
        keys.append(rr)
    for rb in relationBackArr:
        if rb not in keys:
            keys.append(rb)
    return keys

def useDegreeCentrality(relationForArr,relationBackArr):
    """
    使用度中心性算法计算节点重要程度
    @param relationForArr: 正向关系字典
    @param relationBackArr: 逆向关系字典
    @return: 排序结果
    """
    numInputList = {}  # 入度计算
    numOutputList = {}  # 出度计算
    avgInputList = {}
    avgOutputList = {}
    allAvg = {}
    # 计算
    keys = getKeys(relationForArr, relationBackArr)
    n = len(keys)
    for start in relationForArr:
        numOutputList[start] = len(relationForArr[start])
        avgOutputList[start] = numOutputList[start] / (n - 1)
    for end in relationBackArr:
        numInputList[end] = len(relationBackArr[end])
        avgInputList[end] = numInputList[end] / (n - 1)
    for name in namesLexicon:
        ids = int(name2id[name])
        if ids in avgOutputList and ids in avgInputList:
            allAvg[ids] = avgInputList[ids] + avgOutputList[ids]
        elif ids in avgOutputList:
            allAvg[ids] = avgOutputList[ids]
        elif ids in avgInputList:
            allAvg[ids] = avgInputList[ids]

    # 排序
    outDegree = sorted(avgOutputList.items(), key=lambda x: x[1], reverse=True)
    inDegree = sorted(avgInputList.items(), key=lambda x: x[1], reverse=True)
    allDegree = sorted(allAvg.items(), key=lambda x: x[1], reverse=True)
    # 输出
    outputPath = '../output/'
    # saveRes(outputPath+'出度排序2.csv',outDegree)
    # saveRes(outputPath+'入度排序2.csv',inDegree)
    # saveRes(outputPath+'综合排序2.csv',allDegree)
    return allDegree

def usePageRank1(relationForArr,relationBackArr):
    """
    使用V1的pageRank算法
    @param relationForArr:正向关系
    @param relationBackArr: 逆向关系
    @return: 排序结果，此版本不成立
    """
    keys = getKeys(relationForArr, relationBackArr)
    # 启用pagerank
    G, n = getMatrix(relationForArr, relationBackArr, keys)
    # 存在不收敛甚至一直变大的问题
    print(pageRank(G,s=0.85))

def usePageRank2(relationForArr):
    """
    使用V2的pageRank算法
    @param relationForArr:关系列表
    @return: 排序结果，包含两列，id和分数
    """
    # 写出relationForArr
    outPathArr = '../output/relationships.txt'
    saveRelationship(outPathArr, relationForArr)
    # 调用pageRank
    result = pageRank2(outPathArr)
    return result

def removeNotIn(hySets,namesLexicon):
    """
    移除上下位结果里所有需要排除的词条
    @param hySets: 上下位单词集合
    @param namesLexicon: 单词列表
    @return: 排除不在nameLexicon内的单词
    """
    delList = []
    for hy in hySets:
        hyList = hySets[hy]
        for item in hyList[:]:
            if item not in namesLexicon:
                # print(item)
                hyList.remove(item)
            # else:
            #     print(item)
        hySets[hy] = hyList
        if len(hyList) == 0:
            delList.append(hy)
        else:
            hySets[hy] = hyList
    for d in delList:
        hySets.pop(d)
    return hySets

def generateG(relationForArr):
    """
    生成调用leaderrank算法所用图节点
    @param relationForArr:
    @return:
    """
    edges = []
    for start in relationForArr:
        for end in relationForArr[start]:
            edge = (start,end)
            edges.append(edge)
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    return graph

def getPreAndNextWords(limit=500):
    # print(resultName)
    # 获取前k个词条对应的概念集
    hypernymSets = {}  # 上位词集合
    hyponymsSets = {}  # 下位词集合
    sameSets = {}  # 同义词集合
    sameMeansDict = {}  # 同义词典
    if isLimit:
        limit = 500
    else:
        limit = len(result)
    terms = []
    attachWords = {}
    sameDict = {}
    sortNamesLimit = [id2name[res[0]] for res in result[:limit]]

    for ald in result[:limit]:
        name = id2name[ald[0]]
        preSyn, nextSyn, sameSyn, sameDictItems = getPreAndNextWord(name, sortNamesLimit)
        for sd in sameDictItems:
            if sd not in sameDict:
                sameDict[sd] = sameDictItems[sd]
            else:
                sameDict[sd].union(sameDictItems[sd])
        if len(preSyn) > 0:
            hypernymSets[name] = preSyn
        if len(nextSyn) > 0:
            hyponymsSets[name] = nextSyn
        if len(sameSyn) > 0:
            sameSets[name] = sameSyn

        # 数据处理
        for p in preSyn:
            if p not in attachWords:
                attachWords[p] = 1
            else:
                attachWords[p] += 1

        if isRequestConcepts:
            print(name)
            concepts = getPreConcept(name)
            if concepts == False:
                print('请求失败，当前请求到:' + name)
                isRequestConcepts = False
            elif '词语' in concepts:
                terms.append(name2id[name])

    print(hypernymSets)

url = '../data/process/水利大辞典-定义-整理数据.json'
dictRelUrl = '../data/output/水利大辞典-关系-词条2定义.csv'
levelRelUrl = '../data/output/水利大辞典-关系-下位.csv'
jsonData = json.load(open(url,encoding='utf-8'))
isRequestConcepts = False
isExclusive = True
isUsePageRank = True
# 0:degreeCentrality 1:pageRank 2:leaderRank
useAlgorithms = 0
isSave = True
isLimit = True
isSaveSomeWords = False

# 初始化参数
name2id = {}
id2name = {}
name2Definition = {}
namesLexicon = []

for data in jsonData:
    namesLexicon.append(data['name'])
    name2id[data['name']] = str(data['id'])
    id2name[str(data['id'])] = data['name']
    name2Definition[data['name']] = data['context']

if __name__ == '__main__':
    # 定义
    relationForArr = {}  # 出度节点字典
    relationBackArr = {}  # 入度节点字典
    exclusives = []
    if isExclusive:
        # 排除一些概念
        exclusiveNameStart = ['地质', '工程力学', '水力学', '河流动力学', '土力学', '岩石力学', '给水排水工程', '海洋水文学与海岸动力学', '港口', '航道', '河口', '海岸',
                              '生态水利', '水利管理', '水利科技','水利经济']
        exclusiveIdStart = [name2id[name] for name in exclusiveNameStart]
        # 所有需要排除的节点
        exclusives = getExclusiveIds(levelRelUrl, exclusiveIdStart)+exclusiveIdStart
        exclusives = [id2name[exId] for exId in exclusives]

    # 读入边数据
    # readRelation(dictRelUrl, relationForArr, relationBackArr, exclusives)
    # readRelation(levelRelUrl, relationForArr, relationBackArr, exclusives)
    getAllRel(relationForArr, relationBackArr, exclusives)
    if useAlgorithms == 0:
        # 调用度中心性算法
        result = useDegreeCentrality(relationForArr, relationBackArr)
    elif useAlgorithms == 1:
        # 调用pageRank
        # result = usePageRank2(relationForArr)
        result = usePageRank2(relationBackArr)
    else:
        # 调用leaderRank
        # G = generateG(relationForArr)
        G = generateG(relationBackArr)
        result = leaderrank(G)
    resultName = [id2name[str(index[0])] for index in result]
    # getPreAndNextWords(500)
    """
    sortNamesLimit：节点重要性排序
    hypernymSets：上位词map
    hyponymsSets：下位词map
    sameDict：同义词map
    attachWords：上位词中出现，而词典中未出现的词map，统计每个词出现次数
    找传递关系：
    原词条--->上位词--->另一原词条
    """
    # 找传递关系---不存在传递关系
    # for pre in hypernymSets:
    #     for pname in hypernymSets[pre]:
    #         if pname in sameDict:
    #             for hypernymName in sameDict[pname]:
    #                 preSynTemp,_,_,_ = getPreAndNextWord(hypernymName,resultName)
    #                 print("-------------------------")
    #                 print(preSynTemp)
    #                 print("-------------------------")
    #                 for pst in preSynTemp:
    #                     if pst in sortNamesLimit:
    #                         print("-----------111--------------")

    # 可添加的词
    # realAttachWords = []
    # for asw in attachWords:
    #     if attachWords[asw] > 1:
    #         realAttachWords.append(asw)
    # print(realAttachWords)
    # # 同义词整理
    # for snl in sameSets:
    #     someSameMeanWords = sameSets[snl]
    #     for ssmw in someSameMeanWords:
    #         if ssmw in sortNamesLimit:
    #             # print(str(snl)+'的同义词是：'+str(ssmw))
    #             if ssmw not in sameMeansDict:
    #                 sameMeansDict[snl] = [ssmw]
    # print(sameMeansDict)
    if isSave:
        # 导出路径
        outputSortWordPath = '../output/java/sortWord1.csv'
        outputSortWordLimitPath = '../output/java/排序词条1.csv'
        outputEntytiesPath = '../output/java/entyties'
        outputHypernymPath = '../output/java/hypernym.csv'
        outputHyponymsPath = '../output/java/hyponyms.csv'
        outputDictHyponymsPath = '../output/java/dictHyponyms.csv'
        outputTermsPath = '../output/java/terms.csv'
        outputSameMeansPath = '../output/java/sameMeans.csv'
        # 保存时也要按照id来，这样才好保持唯一性，因此还要额外保存一个对应的词典，或者直接让java去读json文件
        # 1.排序词条
        sortWord = [res[0] for res in result]
        saveNodes(outputSortWordPath, sortWord)
        saveNodes(outputSortWordLimitPath, resultName)
        # 2.上下位关系
        # saveRelationshipAsId(outputHypernymPath, hypernymSets)
        # saveRelationshipAsId(outputHyponymsPath, hyponymsSets)
        # 3.词典中的下位关系
        # saveRelationship(outputDictHyponymsPath, relationForArr)
        # 4.将所有标为词语的词都单独保存
        # saveNodes(outputTermsPath, terms)

    if isSaveSomeWords:
        # 5.将实体类都分别保存
        entytiesName = ['水利史', '水利科技']
        baseOutputPath = '../output/java/'
        for name in entytiesName:
            result = getSubConcepts(levelRelUrl, name2id[name])
            saveNodes(baseOutputPath + name + ".csv", result)

