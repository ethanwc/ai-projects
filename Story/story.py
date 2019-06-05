from collections import defaultdict
import random
files = ['alice-27.txt', 'doyle-27.txt', 'doyle-case-27.txt', 'london-call-27.txt', 'melville-billy-27.txt', 'twain-adventures-27.txt']
# files = ['trump.txt']
words = []
story = ""

for file in files:
    with open(file) as f:
        [words.append(word.lower()) for line in f for word in line.split()]

mg = defaultdict(lambda: 0)
bg = defaultdict(lambda: defaultdict(lambda: 0))
tg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))


for i in range(len(words) - 2):
    mg[words[i]] += 1
    bg[words[i]][words[i+1]] += 1
    tg[words[i]][words[i+1]][words[i+2]] += 1

w1 = random.choices([x for x in mg.keys()], mg.values())[0]
w2 = random.choices([x for x in bg[w1].keys()], bg[w1].values())[0]

for x in range(1000):
    w3 = random.choices([x for x in tg[w1][w2].keys()], [y/bg[w1][w2] for y in tg[w1][w2].values()])[0]
    w1 = w2
    w2 = w3
    story += ' ' + w3

print(story)
