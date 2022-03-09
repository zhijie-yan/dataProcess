import numpy as np, pandas as pd
from nltk import edit_distance

def edit_distance3(w1, w2):
    l1, l2 = len(w1) + 1, len(w2) + 1
    matrix = np.zeros(shape=(l1, l2), dtype=np.int8)

    for i in range(l1):
        matrix[i][0] = i
    for j in range(l2):
        matrix[0][j] = j

    for i in range(1, l1):
        for j in range(1, l2):
            delta = 0 if w1[i - 1] == w2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j - 1] + delta,
                               matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1)

    # print(pd.DataFrame(
    #     matrix, index=[''] + list(w1), columns=[''] + list(w2)))

    return matrix[-1][-1]

def edit_distance2(w1, w2):
    l1, l2 = len(w1) + 1, len(w2) + 1
    matrix = [[0 for j in range(l2)] for i in range(l1)]
    for i in range(l1):
        matrix[i][0] = i
    for j in range(l2):
        matrix[0][j] = j
    for i in range(1, l1):
        for j in range(1, l2):
            delta = 0 if w1[i - 1] == w2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j - 1] + delta,
                               matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1)
    return matrix[-1][-1] / (l1 / 2 + l2 / 2 - 1)

# ed = edit_distance3('通航建筑物', '通船建筑物')
# print('edit_distance:', ed)
#
#
# a, b = '通航建筑物', '通船建筑物'
# print(edit_distance(a, b), edit_distance(a, b, transpositions=True))