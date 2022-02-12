"""
测试wordnet
"""
from nltk.corpus import wordnet as wn

# 使用wordnet来求上下位词
# 词必须是result里面出现的key
# word = '水利'
def getPreAndNextWord(word,result):
    preSyn = []
    nextSyn = []
    for synset in wn.synsets(word, lang='cmn'):
        # print(synset.lemmas)
        types_of_n = synset.hyponyms()
        types_of_c = synset.hypernyms()
        pre = sorted([lemma.name() for synset in types_of_c for lemma in synset.lemmas('cmn')])
        next = sorted([lemma.name() for synset in types_of_n for lemma in synset.lemmas('cmn')])
        for p in pre:
            if p in result and word != p:
                preSyn.append(p)
        for n in next:
            if n in result and word != n:
                nextSyn.append(n)
        # if len(pre) != 0:
        #     preSyn += pre
        # if len(next) != 0:
        #     nextSyn += next
    # print(word + "的上位词包含：" + ",".join(preSyn))
    # print(word + "的下位词包含：" + ",".join(nextSyn))
    return preSyn,nextSyn