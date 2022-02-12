"""
将爬取来的词典整理成json格式保存
"""
import csv
import json

def readCsv(inputPath,outputArr,allNames,id):
    with open(inputPath, 'r', newline='',encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
            file_reader = csv.reader(file_read)  # 通过csv的reader()方法读取文件
            header = next(file_reader)  # 取出文件的第一行，也就是表头
            for row in file_reader:
                jsonData = {}
                names = row[0].split(' ',1)
                name = names[0]
                aliasName = []
                if len(names) > 1:
                    aliasName = names[1].split(';')
                context = row[1]
                if name not in allNames:
                    jsonData['id'] = id
                    id += 1
                    jsonData['name'] = name
                    allNames.append(name)
                    jsonData['alias'] = aliasName
                    jsonData['context'] = context
                    outputArr.append(jsonData)
    return id

def writeJson(outputPath,output_file):
    with open(outputPath, "w",encoding='utf-8') as write_f:
        json.dump(output_file, write_f, indent=4, ensure_ascii=False)
        # write_f.write(json.dumps(output_file, indent=4, ensure_ascii=False))
    print("写入文件完成...")


input_file = '../data/base/水利大辞典'
allNames = []
outputArr = []
outputPath = '../output/水利大辞典-定义-整理数据2.json'
id = 0

for i in range(1,10):
    inputPath = input_file+str(i)+'.csv'
    id = readCsv(inputPath,outputArr,allNames,id)
jsonData = json.dumps(outputArr, ensure_ascii = False)
writeJson(outputPath,outputArr)
with open('../output/目录.csv', 'w', encoding='utf-8', newline='') as f:
    for name in allNames:
        # print(name)
        f.write(name+'\n')
    print(len(allNames))
    f.close()