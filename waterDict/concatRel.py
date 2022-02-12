import csv

inputUrlDict = '../output/水利大辞典-关系-词条2定义.csv'
inputUrlLevel = '../output/水利大辞典-关系-下位.csv'
outputRel = '../output/水利大辞典-可视化-关系.csv'

relArr = []

def readCsv(inputUrl):
    with open(inputUrl, 'r', newline='', encoding='utf8') as file_read:  # 打开input_file指定的文件进行只读操作
        # file_reader = csv.reader(file_read)
        for row in file_read:
            if row not in relArr:
                relArr.append(row)

def writeCsv(outputUrl):
    with open(outputUrl, 'w', encoding='utf-8', newline='') as f:
        for rel in relArr:
            f.write(rel)

readCsv(inputUrlDict)
readCsv(inputUrlLevel)
writeCsv(outputRel)