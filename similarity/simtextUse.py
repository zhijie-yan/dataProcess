# simtext相似度：
# simtext可以计算两文档间四大文本相似性指标，分别为：
#     Sim_Cosine cosine相似性
#     Sim_Jaccard Jaccard相似性
#     Sim_MinEdit 最小编辑距离
#     Sim_Simple 微软Word中的track changes
from simtext import similarity

data4_message = ['河流','通航建筑物']
data4_answer = ['河流','通船建筑物']
for i in range(len(data4_message)):
    text1 = data4_message[i]
    text2 = data4_answer[i]
    sim = similarity()
    res = sim.compute(text1, text2)
    print('第'+str(i)+'条')
    print(res)
