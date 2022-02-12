"""
使用知识工厂的api进行请求
"""
import requests

# 使用复旦大学知识工厂获取实体列表和上下位词
def request_data(url):
    req = requests.get(url, timeout=30)  # 请求连接
    req_jason = req.json()  # 获取数据
    return req_jason
# 获取同义词集
def getEntities(q):
    url = 'http://shuyantech.com/api/cnprobase/ment2ent?q='
    return request_data(url+q)

def getConcept(q):
    url = 'http://shuyantech.com/api/cnprobase/concept?q='
    return request_data(url+q)

def getPreConcept(q):
    getNames = getEntities(q)
    if getNames['status'] != 'ok':
        return False
    names = getNames['ret']
    concepts = {}
    for name in names:
        getConcepts = getConcept(name)
        if getConcepts['status'] != 'ok':
            return False
        concept = getConcepts['ret']
        if len(concept) != 0:
            for c in concept:
                if c[0] not in concepts:
                    concepts[c[0]] = 1
                else:
                    concepts[c[0]] += 1
    # return sorted(concepts.items(), key=lambda x: x[1], reverse=True)
    return concepts


# q = '水力发电'
#
# print(getEntities(q))
# print(getConcept(q))
# print(getPreConcept(q))