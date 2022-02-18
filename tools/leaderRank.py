# import get_graph
import networkx as nx

def leaderrank(graph):
    """
    节点排序
    :param graph:复杂网络图Graph
    :return: 返回节点排序值
    """
    # 节点个数
    num_nodes = graph.number_of_nodes()
    # 节点
    nodes = graph.nodes()
    # 在网络中增加节点g并且与所有节点进行连接
    graph.add_node('-1')
    for node in nodes:
        graph.add_edge('-1', node)
        graph.add_edge(node, '-1')
    # LR值初始化
    LR = dict.fromkeys(nodes, 1.0)
    LR['-1'] = 0.0
    k = 0
    # 迭代从而满足停止条件
    while True:
        tempLR = {}
        for node1 in graph.nodes():
            s = 0.0
            # for node2 in graph.nodes():
            #     if node2 in graph.neighbors(node1):
            #         s += 1.0 / graph.degree([node2])[node2] * LR[node2]
            for node2 in graph.nodes():
                if node1 in graph.neighbors(node2):
                    s += (1.0 / graph.out_degree()[node2]) * LR[node2]
            tempLR[node1] = s
        print('当前是第%s轮迭代'%k)
        # print(tempLR)
        # 终止条件:LR值不在变化
        error = 0.0
        for n in tempLR.keys():
            error += abs(tempLR[n] - LR[n])
        if error <= 0.000000001:
            break
        print('当前轮error为：%s'%error)
        LR = tempLR
        k += 1
    # 节点g的LR值平均分给其它的N个节点并且删除节点
    avg = LR['-1'] / num_nodes
    LR.pop('-1')
    for k in LR.keys():
        LR[k] += avg
    # print(LR)
    # return LR
    return sorted(LR.items(), key=lambda x: x[1], reverse=True)


# if __name__ == "__main__":
#     path = "/home/dreamhome/network-datasets/karate/karate.paj"
#     graph = get_graph.read_graph_from_file(path)
#     print(sorted(leaderrank(graph).items(), key=lambda item: item[1]))

