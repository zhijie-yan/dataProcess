import numpy as np
from scipy.sparse import csc_matrix
import matplotlib.pyplot as plt

def pageRank(G, s=.85, maxerr=0.001,maxRound=1000):
    """
      Computes the pagerank for each of the n states
      Parameters
      ----------
      G: matrix representing state transitions
      Gij is a binary value representing a transition from state i to j.
      s: probability of following a transition. 1-s probability of teleporting
      to another state.
      maxerr: if the sum of pageranks between iterations is bellow this we will
         have converged.
    """
    n = G.shape[0]
    # 将 G into 马尔科夫 A
    A = csc_matrix(G, dtype=float)
    rsums = np.array(A.sum(1))[:, 0]
    ri, ci = A.nonzero()
    A.data /= rsums[ri]
    sink = rsums == 0
    # 计算PR值，直到满足收敛条件
    ro, r = np.zeros(n), np.ones(n)
    roundNum = 0
    pltArr = []
    while np.sum(np.abs(r - ro)) > maxerr:
        print(roundNum)
        if roundNum >= maxRound:
            break
        else:
            roundNum += 1
        pltArr.append(np.sum(np.abs(r - ro)))
        ro = r.copy()
        for i in range(0, n):
            Ai = np.array(A[:, i].todense())[:, 0]
            Di = sink / float(n)
            Ei = np.ones(n) / float(n)
            r[i] = ro.dot(Ai * s + Di * s + Ei * (1 - s))
    # 绘图
    y = pltArr
    x = range(len(y))
    plt.xlabel("epoch")
    plt.ylabel("err")
    # my_x_ticks = np.arange(len(y))  # 横坐标设置0,1,...,len(acc)-1,间隔为1
    # my_x_ticks = np.arange(0,len(acc),2) # 横坐标设置0,2,...,len(acc)-1，间隔为2
    # plt.xticks(my_x_ticks)
    # plt.xticks(range(0, len(y), 50), rotation=45)
    plt.plot(y)
    # plt.axis('tight')  # 坐标轴适应数据量 axis 设置坐标轴
    plt.show()
    # 归一化
    return r / float(sum(r))

# if __name__ == '__main__':
#   # 上面的例子
#   G = np.array([[0, 0, 1],
#           [1, 0, 0],
#           [1, 1, 0]])
  # print(pageRank(G, s=0.85))
# 结果：
# 41  [0.51203622 0.19313191 0.29483187]