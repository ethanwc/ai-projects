import sys
import numpy as np
import copy
import array as arr
from random import randint


# Based on: http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaQueueinPython.html


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Point:
    def __init__(self, initx, inity):
        self.x = initx
        self.y = inity


searchMethods = {'BFS', 'DFS', 'DLS', 'ID', 'GBFS', 'ASTAR'}
heuristics = {'h1', 'h2'}
solution = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', ' '])
solution2 = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'F', 'E', ' '])

size = 4


# print(solution)


# move the blank space of the board, by swapping its index with another piece
def move(board, move):
    newboard = copy.deepcopy(board)
    for i in range(0, size):
        for j in range(0, size):
            if newboard[i][j] == ' ':
                xoff = yoff = 0
                if move == 'right':
                    xoff = 1
                if move == 'left':
                    xoff = -1
                if move == 'up':
                    yoff = -1
                if move == 'down':
                    yoff = 1

                temp = newboard[i + yoff][j + xoff]
                newboard[i + yoff][j + xoff] = newboard[i][j]
                newboard[i][j] = temp
                return newboard

    return newboard


# get all possible moves that can be made based on a board in a certain state
def getmoves(board):
    for i in range(0, size):
        for j in range(0, size):
            if board[i][j] == ' ':
                moves = []

                # right
                if j < size - 1:
                    moves.append('right')
                # down
                if i < size - 1:
                    moves.append('down')
                # left
                if j > 0:
                    moves.append('left')
                # up
                if i > 0:
                    moves.append('up')
                print(moves)
                return moves

    return 0


def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges


# Breadth first search
def bfs(goal, initial):
    # graph is solution
    # state is current version
    # want graph to equal state, done by the bfs algorithm

    # move: right, down, left, right

    queue = Queue()
    queue.enqueue(initial)

    # explored = np.array([])
    explored = []
    attempts = 1
    maxFringe = 0
    numCreated = 0
    while not queue.isEmpty():
        # print('in queue: ', queue.size())
        # for each node at the curre
        # nt depth level
        if queue.size() > maxFringe:
            maxFringe = queue.size()
        state = queue.dequeue()
        statevalue = ','.join([np.unicode(i) for i in state])

        if np.array_equal(goal, state.flatten()) or np.array_equal(solution2, state.flatten()):
            print('Found the solution in ', attempts, ' attempts')
            print('Num Created:', numCreated)
            print('Max Size:', maxFringe)
            print(state)
            exit()

        explored.append(statevalue)

        # do all the possible moves, right, down, left, right, then check if they equal the goal

        for m in getmoves(state):
            newboard = move(state, m)
            numCreated += 1
            newboardvalue = ','.join([np.unicode(i) for i in newboard])

            if newboardvalue not in explored:
                queue.enqueue(newboard)
                attempts += 1

    return 0


# Depth first search
def dfs(goal, initial, visited=None):
    print(initial)
    # treat list as a stack
    # more recursively, right first

    # def dfs(graph, start, visited=None):
    #     if visited is None:
    #         visited = set()
    #     visited.add(start)
    #     for next in graph[start] - visited:
    #         dfs(graph, next, visited)
    #     return visited
    #
    # dfs(graph, 'C')

    if visited is None:
        visited = []
        visited.append(initial)
        for x in getmoves(initial):
            moved = move(initial, x)

            if x == 'right':
                dfs(goal, moved)
            if x == 'down':
                dfs(goal, moved)
            if x == 'left':
                dfs(goal, moved)
            if x == 'up':
                dfs(goal, moved)
    #
    #
    # stack = []
    # stack.append('test')
    # stack.pop()
    #
    # newboard = move(initial, getmoves(initial)[0])
    #
    # print(newboard)
    #
    # if np.array_equal(goal, newboard.flatten()):
    #     print('Found the solution')
    #     print(newboard)
    #     exit()

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
    global initialstate, searchmethod, argcount, extra, startstate, boardinput
    initialstate = sys.argv[1].replace('\'', '').replace('\"', '').upper()
    initialstate = '123456789AB DEFC'
    print('here', initialstate)
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
    startstate = []
    temp = []
    for c in initialstate:
        temp += c
        i += 1
        if i % 4 == 0 and i > 0:
            startstate += temp
            temp = []

    startstate = np.array(startstate).reshape(4, 4)
    boardinput = startstate
    # print(state)


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
        print('dfs chosen')
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
# def swap(p1, p2):
#     temp = state[p1.x][p1.y]
#     state[p1.x][p1.y] = state[p2.x][p2.y]
#     state[p2.x][p2.y] = temp
#     # print(state)


parseinput()
validateinput()

# print(boardinput)
# moves = getmoves(boardinput)
# print(moves)
# move(boardinput, moves[0])
#
print(solution)
print('input')
print(boardinput)

# print(solution, boardinput.flatten())
bfs(solution, boardinput)
# dfs(solution, boardinput)
