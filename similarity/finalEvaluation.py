import difflib
import json
from simtext import similarity


# 本体
from similarity.editDis import edit_distance3
from tools.tools import saveNodes

ontologyNamesUrl = '../data/ontologys.csv'
# 规范
normNamesUrl = '../data/concepts.csv'

jsonUrl = '../data/process/水利大辞典-定义-整理数据.json'
levelRelUrl = '../data/output/水利大辞典-关系-下位.csv'

# 读节点 构造id和name互相映射
name2id = {}
id2name = {}
name2Definition = {}
namesLexicon = []
jsonData = json.load(open(jsonUrl,encoding='utf-8'))

for data in jsonData:
    namesLexicon.append(data['name'])
    name2id[data['name']] = str(data['id'])
    id2name[str(data['id'])] = data['name']
    name2Definition[data['name']] = data['context']

sim = similarity()


# 最基础，自带相似性算法
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def baseSim(normNames,ontoNames):
    bestSimilarity = {}
    scoreSimilarity = {}
    num = 0

    for nName in normNames:
        score = -1
        try:
            for oName in ontoNames:
                temp = string_similar(oName, nName)
                # temp = sim.compute(oName, nName)['Sim_Jaccard']
                if temp > score:
                    score = temp
                    bestSimilarity[nName] = oName
                    scoreSimilarity[nName] = score
        except:
            continue
        # if scoreSimilarity[nName] >= 0.8:
        #     num += 1
    # print(bestSimilarity)
    # print(scoreSimilarity)
    # print(num / len(normNames))
    return bestSimilarity,scoreSimilarity,num

def useEditDis(normNames,ontoNames):
    bestSimilarity = {}
    scoreSimilarity = {}
    num = 0
    for nName in normNames:
        score = 10
        for oName in ontoNames:
            temp = edit_distance3(oName, nName)
            if temp < score:
                score = temp
                bestSimilarity[nName] = oName
                scoreSimilarity[nName] = score
        if scoreSimilarity[nName] <= 1:
            num += 1
    # print(bestSimilarity)
    # print(scoreSimilarity)
    # print(num / len(normNames))
    return bestSimilarity, scoreSimilarity, num

if __name__ == '__main__':
    # 所有本体概念
    # ontoNames = readNodes(ontologyNamesUrl)
    # # 所有规范概念
    # normNames = readNodes(normNamesUrl)
    # # 调用相似性算法
    # bestSimilarity, scoreSimilarity, num = useEditDis(normNames,ontoNames)
    #
    # bestSimilarity2, scoreSimilarity2, num2 = useEditDis(normNames,namesLexicon)
    #
    # nameFather = readRel(levelRelUrl)
    # score1 = 0
    # score2 = 0
    # for bs1,bs2,s1,s2 in zip(bestSimilarity,bestSimilarity2,scoreSimilarity,scoreSimilarity2):
    #     print(bs1,bestSimilarity[bs1],scoreSimilarity[s1],bestSimilarity2[bs2],scoreSimilarity2[s2])
    #     score1 += scoreSimilarity[s1]
    #     score2 += scoreSimilarity2[s2]
    # print(score1,score2)
    # print(num / len(normNames),num2 / len(normNames))
    # useEditDis(normNames,ontoNames)

    centerStr = "水库"
    allNames = {}
    for name in namesLexicon:
        allNames[name] = edit_distance3(centerStr, name)
    result = sorted(allNames.items(), key=lambda x: x[1], reverse=False)
    names = []
    for res in result[:10]:
        names.append(res[0])
    print(names)
    saveNodes("../output/distance/编辑距离.csv",names)



