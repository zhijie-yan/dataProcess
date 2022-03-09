def saveNodes(outputPath,nodes):
    """
    保存节点list
    @param outputPath: 输出路径
    @param nodes: 节点列表
    @return: 保存
    """
    with open(outputPath, 'w', encoding='utf-8', newline='') as f:
        for node in nodes:
            f.write(str(node) + '\n')