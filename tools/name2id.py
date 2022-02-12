"""
将文字转成json对应的id映射
"""
import json
import csv
url = '../data/process/水利大辞典-定义-整理数据.json'
inputUrl = '../data/process/目录.csv'
outputRelUrl = '../output/水利大辞典-关系-下位.csv'
outputEntityUrl = '../output/水利大辞典-可视化-节点.csv'
jsonData = json.load(open(url,encoding='utf-8'))

# 读取数据阶段
name2id = {}
name2Definition = {}
namesLexicon = []
nameAttach = []
relArr = []

for data in jsonData:
    namesLexicon.append(data['name'])
    name2id[data['name']] = data['id']
    name2Definition[data['name']] = data['context']

with open(inputUrl, 'r', newline='',encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
        # header = next(file_reader)  # 取出文件的第一行，也就是表头
        for row in file_reader:
            if row[0] in namesLexicon:
                relArr.append([name2id[row[0]],name2id[row[1]]])

with open(outputRelUrl, 'w', encoding='utf-8', newline='') as f:
    for rel in relArr:
        f.write(str(rel[0]) + ','+str(rel[1]) + '\n')

with open(outputEntityUrl, 'w', encoding='utf-8', newline='') as f:
    for name in name2id:
        f.write(str(name2id[name]) + ','+name + '\n')