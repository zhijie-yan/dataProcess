"""
用来评估不同算法跑出来的结果
"""
import csv
import json

jsonUrl = '../data/process/水利大辞典-定义-整理数据.json'
levelRelUrl = 'data/output/水利大辞典-关系-下位.csv'
baseUrl = 'output/'
noExclusiveUrl = '不排除已加入关系/'
exclusiveUrl = '排除已加入关系/'
simpleUrl = '最简单提取方案/'
conceptUrl = 'data/concepts.csv'

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

nameFather = {}
# 规范中的词
concepts = []
# 限制比较词语数
# limit = 30

scoreArr = {}

def setScore():
    scoreArr['水利'] = 8
    scoreArr['水利史'] = 3
    scoreArr['水文学'] = 9
    scoreArr['水资源'] = 8
    scoreArr['防洪抗旱'] = 10
    scoreArr['农业水利'] = 7
    scoreArr['城市水利'] = 7
    scoreArr['给水排水工程'] = 6
    scoreArr['水力发电'] = 10
    scoreArr['环境水利'] = 7
    scoreArr['生态水利'] = 7
    scoreArr['水利经济'] = 5
    scoreArr['水利管理'] = 5
    scoreArr['水利科技'] = 5

def readNodes(url):
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

def evaluate(path):
    fileNames = '排序词条'
    # for i in range(4):
    i = 3
    print('--------------------------------------------------')
    for limit in range(31):

        newSortNames = readNodes(path+fileNames+str(i)+'.csv')
        newNames = newSortNames[:limit]
        inWord = 0
        for name in newNames:
            # if name in concepts:
            inWord += scoreArr[nameFather[name]]
            # print(nameFather[name])
        # print(path+fileNames+str(i)+'总分数为：')
        # print((inWord+0.00)/limit)
        print(inWord)


def readRel(path):
    result = {}
    with open(path, 'r', newline='', encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
        for row in file_reader:
            start = id2name[row[0]]
            end = id2name[row[1]]
            result[end] = start
    return result

if __name__ == '__main__':
    pass
    # setScore()
    # nameFather = readRel(levelRelUrl)
    # concepts = readNodes(conceptUrl)
    # evaluate(baseUrl+noExclusiveUrl)
    # evaluate(baseUrl+exclusiveUrl)
    # evaluate(baseUrl+simpleUrl)
