"""
测试ltp api
"""
from ltp import LTP

ltp = LTP()

str = "兼顾兴利除害、满足不同部门用水需求和水生态环境保护目标而对河流水资源所进行的多目标开发利用。在规划时，按水资源可持续利用与统筹兼顾、适当安排的方针，同时考虑当前和长远，尽可能满足防洪、除涝、供水、灌溉、治碱、水力发电、航运、漂木、水产养殖、水生态环境保护等不同要求。"

segment1, hidden1 = ltp.seg([str])
pos1 = ltp.pos(hidden1)
# 自定义分词
# user_dict.txt 是词典文件， max_window是最大前向分词窗口
ltp.init_dict(path="../data/process/词条.txt")
# 也可以在代码中添加自定义的词语
# ltp.add_words(words=["负重前行", "长江大桥"], max_window=4)


segment, hidden = ltp.seg([str])
print(segment)
# 对于已经分词的数据
# segment, hidden = ltp.seg(["他/叫/汤姆/去/拿/外衣/。".split('/')], is_preseged=True)
# print(segment)

pos = ltp.pos(hidden)
print(pos)

ner = ltp.ner(hidden)
tag, start, end = ner[0][0]
print(tag,":", "".join(segment[0][start:end + 1]))

