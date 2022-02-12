"""
读取json文件内容,返回字典格式
"""
import json

txts = []
with open('../data/base/bmes_test.json', 'r', encoding='utf8')as fp:
    json_data = json.load(fp)
    for item in json_data:
        # print(item['id'])
        # print(item['text'])
        txts.append(item['text'])

with open('../output/bmes_test.txt', 'w', encoding='utf8')as fw:
    for txt in txts:
        fw.write(txt+'\n')