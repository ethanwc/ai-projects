import sys

searchMethods = {'BFS', 'DFS', 'DLS', 'ID', 'GBFS', 'AStar'}
heuristics = {'h1', 'h2'}

print "Number of arguments: ", len(sys.argv)

initialstate = sys.argv[1]
searchMethod = sys.argv[2]
print initialstate
print len(initialstate)

if len(initialstate) != 16: print "Invalid Input"

check = True
for c in initialstate:
    if not str.isdigit(c) or (65 <= ord(c) <= 70):
        check = False
        print(check)
        break


def checkSearchMethod():
    return searchMethod in searchMethods


if searchMethod == 'BFS':
elif searchMethod == 'DFS':
elif searchMethod == 'DLS':
print checkSearchMethod()