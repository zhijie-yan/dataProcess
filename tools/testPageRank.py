import numpy as np
from tools.pageRankTool import pageRank

def getMatrix(relationForArr,relationBackArr,keys):
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

relationForArr = {'0':['3'],'1':['0','2'],'2':['0','1']}  # 出度节点字典
relationBackArr = {'0':['1','2'],'1':['2'],'2':['1'],'3':['0']}   #入度节点字典

keys = [] #过滤后剩余的词条key
for rr in relationForArr:
    keys.append(rr)
for rb in relationBackArr:
    if rb not in keys:
        keys.append(rb)
# 启用pagerank
n = len(keys)
G , n = getMatrix(relationForArr,relationBackArr,keys)
print(pageRank(G,s=0.85))