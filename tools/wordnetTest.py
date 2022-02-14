"""
测试wordnet
"""
from nltk.corpus import wordnet as wn

"""
使用wordnet来求上下位词
词必须是result里面出现的key
word = '水利'
想要实现的是：
1.找到每个词的上位词，并且确保其同义词都指向同一个上位词
2.将未出现在原词汇集合中的上位词都单独保存起来
3.将2中保存的上位词出现的次数统计下来
4.如果出现过渡上位词，则用特殊方式标记出来
需要做的是：
1.统计每个词和其同义词的上位词，统一成一个上位词，用字典保存下来，多对一结构
2.保存的都是name，不涉及id
3.构造字典，保存每个上位词出现的次数
4.上面构造出了一个关系字典，然后可以通过这个字典遍历，以出现在水利词典中的词汇为起点，找到所有过渡节点
5.将出现次数大于2的上位词保存下来
6.需要一个同义词典，用于后面过滤出过渡节点
7.保存同义词

1.构造一个同义词典
2.构造一个上位词电
3.构造一个下位词典
4.获得同义词典指向上下位词典的关系

"""
def getPreAndNextWord(word,result):
    preSyn = []
    nextSyn = []
    sameSyn = []
    sameDict = {}

    for synset in wn.synsets(word, lang='cmn'):
        # print(synset.lemmas)
        types_of_n = synset.hyponyms()
        types_of_c = synset.hypernyms()
        # 同义词集合
        sameWords = sorted([lemma.name() for lemma in synset.lemmas('cmn')])
        # 上位词集合
        pre = sorted([lemma.name() for syn in types_of_c for lemma in syn.lemmas('cmn')])
        # 下位词集合
        next = sorted([lemma.name() for syn in types_of_n for lemma in syn.lemmas('cmn')])

        sameTemp = [s for s in sameWords if s not in sameSyn]
        preTemp = [p for p in pre if p not in preSyn]
        nextTemp = [n for n in next if n not in nextSyn]

        sameSyn += sameTemp
        preSyn += preTemp
        nextSyn += nextTemp
    # 去除自指向
    if word in preSyn:
        preSyn.remove(word)
    if word in sameSyn:
        sameSyn.remove(word)
    if word in nextSyn:
        nextSyn.remove(word)

    for same in sameSyn:
        setWord = set()
        setWord.add(word)
        sameDict[same] = setWord
    return preSyn,nextSyn,sameSyn,sameDict