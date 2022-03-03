import string
from io import StringIO

from math import log
import numpy as np

KLD = (lambda p, q: sum([_p * log(_p, 2) - _p * log(_q, 2) for (_p, _q) in zip(p, q)]))
"""这个方法是用在文本相似性检测，短句不好使"""

def JSD_core(p, q):
    # p, q = zip(*filter(lambda x,y: x != 0 or y != 0, zip(p, q)))  # 去掉二者都是0的概率值
    n_p = p
    n_q = q
    for p2,q2 in zip(p,q):
        if p2 == 0 or q2 == 0:
            n_p.remove(p2)
            n_q.remove(q2)
    p = n_p
    q = n_q
    M = [0.5 * (_p + _q) for _p, _q in zip(p, q)]
    p = p + np.spacing(1)
    q = q + np.spacing(1)
    M = M + np.spacing(1)
    #     print p,q,M
    return 0.5 * KLD(p, M) + 0.5 * KLD(q, M)


reg = lambda x: [x.count(i) for i in string.ascii_lowercase]  # 频数分布
rate = lambda y: [round(i * 1.0 / sum(reg(y)), 4) for i in reg(y)]  # 概率分布

data4_message = ['河流','通航建筑物']
data4_answer = ['河流','通船建筑物']
s1 = data4_message[1]
s2 = data4_answer[1]
# s1='ahaebssa'
# s2='awohwsess'
print(JSD_core(rate(s1), rate(s2)))
