from collections import defaultdict
import random


words = []

with open("alice-27.txt") as f:
    [words.append(word.lower()) for line in f for word in line.split()]

mg = defaultdict(lambda: 0)
bg = defaultdict(lambda: defaultdict(lambda: 0))
tg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
for i in range(len(words) - 2):  # loop to the next-to-last word
    mg[words[i]] += 1
    bg[words[i]][words[i+1]] += 1
    tg[words[i]][words[i+1]][words[i+2]] += 1




# pretty print the defaultdict
# {k: dict(v) for k, v in dict(cfd).items()}



w1 = random.choice(list(mg.keys()))
w2 = random.choice(list(mg.keys()))



# w1 = random.choice(mg)

# print(w1)
# print(tg[w1][w2][w3]/bg[w1][w2])



# print(cfd)

# list = [x for x in cfd.get(cfd.keys())]
#
# data_list = ['A'] + ['B'] + ['C'] * 18
# print(random.choice(data_list))
