import sys
import numpy as np
from random import randint

class Point:
    def __init__(self, initx, inity):
        self.x = initx
        self.y = inity


graph = {'1': ['2', '5'],
         '2': ['1', '3', '6'],
         '3': ['2', '4', '7'],
         '4': ['3', '8'],
         '5': ['1', '6', '9'],
         '6': ['2', '5', '7', 'A'],
         '7': ['3', '6', '8', 'B'],
         '8': ['4', '7', 'C'],
         '9': ['5', 'A', 'D'],
         'A': ['6', '9', 'B', 'E'],
         'B': ['7', 'A', 'C', 'F'],
         'C': ['8', 'B', ' '],
         'D': ['9', 'E'],
         'E': ['A', 'D', 'F'],
         'F': ['B', 'E', ' '],
         ' ': ['C', 'F']
         }

searchMethods = {'BFS', 'DFS', 'DLS', 'ID', 'GBFS', 'ASTAR'}
heuristics = {'h1', 'h2'}
solution = np.array(['A', 'B', 'C', 'D', 'E', 'F', '0', '1', '2', '3', '4', '5', '6', '7', '8', ' '])
size = 4

# print(solution)


def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges


print(generate_edges(graph))


# Random search
def rs():
    x1 = randint(0, size-1)
    y1 = randint(0, size-1)
    x2 = randint(0, size-1)
    y2 = randint(0, size-1)

    p1 = Point(x1, y1)
    p2 = Point(x2, y2)

    swap(p1, p2)


# Breadth first search
def bfs():

    return 0


# Depth first search
def dfs():
    return 0


# Depth limited search
def dls():
    return 0


# Greedy best-first search
def gbfs():
    return 0


# A-Stadwad
def astar():
    return 0


# Load the cmd arguments into values
def parseinput():
    global initialstate, searchmethod, argcount, extra, state
    initialstate = sys.argv[1].replace('\'', '').replace('\"', '').upper()
    searchmethod = sys.argv[2]
    argcount = len(sys.argv) - 1
    input = ''
    extra = ''

    if argcount > 2:
        extra = sys.argv[3]

    for i in sys.argv[1:]:
        input += i + ' '

    print(input)

    # Build the State model
    i = 0
    state = []
    temp = []
    for c in initialstate:
        temp += c
        i += 1
        if (i % 4 == 0 and i > 0):
            state += temp
            temp = []

    state = np.array(state).reshape(4,4)
    print(state)


# Check that the input is valid..
def validateinput():
    valid = True

    if not searchmethod.upper() in searchMethods:
        print('Invalid Search Method')
        valid = False

    if len(initialstate) != 16:
        print("Invalid Initial state length: ", len(initialstate))
        valid = False

    # Check each char is between 0:9 and A:F
    check = True
    for c in initialstate:
        if not (str.isdigit(c) or (65 <= ord(c) <= 70) or ord(c) == 32):
            print('Invalid Initial State Characters')
            print(c, ord(c))
            check = False
            break

    if not check:
        valid = False

    # Special Cases for heuristics
    if searchmethod.lower() == 'gbfs' or searchmethod.lower() == 'astar':
        print('Invalid Input: No heuristic specified')
        if not extra in heuristics:
            valid = False

    # Special Case for depth limited search
    if searchmethod.lower() == 'dfs':
        if extra in heuristics:
            print('Invalid Input: Heuristic specified for depth')
            valid = False
        if argcount < 3:
            print('Invalid Input: Depth length not specified?')
            valid = False

    # Should never be more than 3 input args
    if argcount > 3:
        print('Invalid Input: Too many arguments')
        valid = False

    if valid:
        handleinput()


# Handle input after checking it is okay.
def handleinput():
    if searchmethod.lower() == 'bfs':
        print('bfs chosen')
    elif searchmethod.lower() == 'dfs':
        dfs()
    elif searchmethod.lower() == 'dls':
        print('dls chosen')
    elif searchmethod.lower() == 'id':
        print('id chosen')
    elif searchmethod.lower() == 'gbfs':
        print('gbfs chosen')
    elif searchmethod.lower() == 'astar':
        print('astar chosen')


# Check the bounds to see if the swap values are okay
def checkcoords(p):
    return 0 <= p.x < size and 0 <= p.y < size


# Swap two elements in the array
def swap(p1, p2):
    temp = state[p1.x][p1.y]
    state[p1.x][p1.y] = state[p2.x][p2.y]
    state[p2.x][p2.y] = temp
    # print(state)


parseinput()
validateinput()


# while not np.array_equal(solution, state.flatten()):
#     bfs()
