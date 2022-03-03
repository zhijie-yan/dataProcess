import difflib
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

data4_message = ['河流','通航建筑物']
data4_answer = ['河流','通船建筑物']

for i in range(len(data4_message)):
    s1 = data4_message[i]
    s2 = data4_answer[i]
    print(string_similar(s1, s2))
