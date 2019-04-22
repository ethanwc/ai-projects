import sys


import numpy as np
import copy
import array as arr
from random import randint


# Based on: http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaQueueinPython.html


# class Queue:
#     def __init__(self):
#         self.items = []
#
#     def isEmpty(self):
#         return self.items == []
#
#     def enqueue(self, item):
#         self.items.insert(0, item)
#
#     def dequeue(self):
#         return self.items.pop()
#
#     def size(self):
#         return len(self.items)


import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
        self._size = 0

    def push(self, item, priority):
        # print('p', priority)
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
        self._size += 1

    def pop(self):
        self._size -= 1
        return heapq.heappop(self._queue)[-1]

    def size(self):
        return self._size

# class PriorityQueue(object):
#     def __init__(self):
#         self.queue = []
#
#     def __str__(self):
#         return ' '.join([str(i) for i in self.queue])
#
#         # for checking if the queue is empty
#
#     def isEmpty(self):
#         return len(self.queue) == []
#
#         # for inserting an element in the queue
#
#     def insert(self, data):
#         self.queue.append(data)
#
#         # for popping an element based on Priority
#
#     def delete(self):
#         try:
#             max = 0
#             for i in range(len(self.queue)):
#                 if self.queue[i] > self.queue[max]:
#                     max = i
#             item = self.queue[max]
#             del self.queue[max]
#             return item
#         except IndexError:
#             print()
#             exit()


class Point:
    def __init__(self, initx, inity):
        self.x = initx
        self.y = inity


searchMethods = {'BFS', 'DFS', 'DLS', 'ID', 'GBFS', 'ASTAR'}
heuristics = {'h1', 'h2'}
solution = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', ' ']).reshape(4, 4)
solution2 = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'F', 'E', ' ']).reshape(4, 4)
heuristic = 'h1'
size = 4


# print(solution)

# dumbe caller
def h(state):
    if heuristic == 'h1':
        return h1(state)
    else:
        return h2(state)


# h1 is the number of misplaced tiles
# goal state is 1:9,abcdef or 1:9,abcdfe
def h1(state):
    n = 0
    sol1 = np.array(solution).flatten()
    sol2 = np.array(solution2).flatten()
    for i in range(0, len(state)):
        if not (state[i] == sol1[i]
                or state[i] == sol2[i]):
            n += 1
    return n


# the sum of the distances of the tiles from their goal positions
# state should be 4x4
def h2(state):
    # print(state)
    # print('--------------')
    distance = 0
    for x in range(0, size):
        for y in range(0, size):
            if state[x][y] == '1':
                distance += abs(x - 0) + abs(y - 0)
                # print(state[x][y],x,y, distance)
            if state[x][y] == '2':
                distance += abs(x - 0) + abs(y - 1)
                # print(state[x][y],x,y,distance)
            if state[x][y] == '3':
                distance += abs(x - 0) + abs(y - 2)
                # print(state[x][y],x,y,distance)
            if state[x][y] == '4':
                distance += abs(x - 0) + abs(y - 3)
                # print(state[x][y],x,y,distance)
            if state[x][y] == '5':
                distance += abs(x - 1) + abs(y - 0)
                # print(state[x][y],x,y,distance)
            if state[x][y] == '6':
                distance += abs(x - 1) + abs(y - 1)
                # print(state[x][y],x,y,distance)
            if state[x][y] == '7':
                distance += abs(x - 1) + abs(y - 2)
                # print(state[x][y],x,y,distance)
            if state[x][y] == '8':
                distance += abs(x - 1) + abs(y - 3)
                # print(state[x][y],x,y,distance)
            if state[x][y] == '9':
                distance += abs(x - 2) + abs(y - 0)
                # print(state[x][y],x,y,distance)
            if state[x][y] == 'A':
                distance += abs(x - 2) + abs(y - 1)
                # print(state[x][y],x,y,distance)
            if state[x][y] == 'B':
                distance += abs(x - 2) + abs(y - 2)
                # print(state[x][y],x,y,distance)
            if state[x][y] == 'C':
                distance += abs(x - 2) + abs(y - 3)
                # print(state[x][y],x,y,distance)
            if state[x][y] == 'D':
                distance += abs(x - 3) + abs(y - 0)
                # print(state[x][y],x,y,distance)
            if state[x][y] == 'E':
                distance += abs(x - 3) + abs(y - 1)
                # print(state[x][y],x,y,distance)
            if state[x][y] == 'F':
                distance += abs(x - 3) + abs(y - 2)
                # print(state[x][y],x,y,distance)
    # print('--------------')
    return distance


# returns the path cost, from the initial state to the current path
# pathcost is just h1 with the initial and current state
def pathcost(initial, current):
    n = 0
    # print(initial, current)
    for i in range(0, len(initial)):
        if not initial[i] == current[i]:
            n += 1
    return n


# move the blank space of the board, by swapping its index with another piece
def move(board, move):
    newboard = copy.deepcopy(board)
    for i in range(0, size):
        for j in range(0, size):
            # print("board", board)
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
    print('error')
    return newboard


# get all possible moves that can be made based on a board in a certain state
def getmoves(board):
    for i in range(0, size):
        for j in range(0, size):
            # print(board)
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
                # print(moves)
                return moves

    return 0


def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges


def contains(element, list):
    length = len(list)

    for i in range(0, length):
        if np.array_equal(element, list[i]):
            return True
    return False


# Breadth first search
def bfs(initial):
    frontier = [initial]
    explored = []

    if np.array_equal(initial, solution):
        print('Found sol')
    numcreated = 0
    numexpanded = 0
    maxfringe = 0
    depth = 0
    while len(frontier) > 0:
        if len(frontier) > maxfringe:
            maxfringe = len(frontier)
        node = frontier.pop(0)
        numexpanded += 1
        explored.append(node)
        moves = getmoves(node)
        for i in range(0, len(moves)):
            # print(moves[i])
            # if 'right' == moves[i]:
            child = move(node, moves[i])
            numcreated += 1
            if not contains(child, explored):
                # print(child)

                if np.array_equal(child, solution2) or np.array_equal(child, solution):
                    print("Found sol in ", numcreated)
                    print("Maxfringe", maxfringe)
                    print("Numexpanded", numexpanded)
                    print("Depth", depth)
                    # exit()
                    return
                frontier.append(child)
    return 0


# Depth first search
def dfs(initial):
    frontier = [initial]
    explored = []

    if np.array_equal(initial, solution):
        print('Found sol')
    numcreated = 0
    numexpanded = 0
    maxfringe = 0
    depth = 0
    while len(frontier) > 0:
        if len(frontier) > maxfringe:
            maxfringe = len(frontier)
        node = frontier.pop()
        numexpanded += 1
        explored.append(node)
        moves = getmoves(node)
        for i in range(0, len(moves)):
            # print(moves[i])
            # if 'right' == moves[i]:
            child = move(node, moves[i])
            numcreated += 1
            if not contains(child, explored):
                # print(child)

                if np.array_equal(child, solution2) or np.array_equal(child, solution):
                    print("Found sol in ", numcreated)
                    print("Maxfringe", maxfringe)
                    print("Numexpanded", numexpanded)
                    print("Depth", depth)
                    return
                frontier.append(child)
    return 0


# Depth limited search
def dls():
    return 0


# Greedy best-first search, uses the distance function.
def gbfs(initial):
    frontier = PriorityQueue()
    # cost = h2(initial)
    cost = h1(np.array(initial).flatten())
    frontier.push(initial, cost)
    explored = []
    # use a priority queue for frontier instead of a list??
    if np.array_equal(initial, solution):
        print('Found sol')
        return
    while frontier.size() > 0:
        # make sure the highest priority element is popped
        node = frontier.pop()
        explored.append(node)
        moves = getmoves(node)
        for i in range(0, len(moves)):
            child = move(node, moves[i])
            if not contains(child, explored):

                if np.array_equal(child, solution2) or np.array_equal(child, solution):
                    print('Found gbfs solution: ', frontier.size())
                    return
                # append with h1 heuristic
                # cost = h2(child)
                cost = h1(np.array(child).flatten())
                frontier.push(child, cost)
    return 0


# A-Star, uses heuristic and distance
def astar(initial):
    frontier = PriorityQueue()
    # cost = h2(initial)
    cost = h1(np.array(initial).flatten()) + pathcost(np.array(initial).flatten(), np.array(initial).flatten())
    frontier.push(initial, cost)
    explored = []
    # use a priority queue for frontier instead of a list??
    if np.array_equal(initial, solution):
        print('Found sol')
        return
    while frontier.size() > 0:
        # make sure the highest priority element is popped
        node = frontier.pop()
        explored.append(node)
        moves = getmoves(node)
        for i in range(0, len(moves)):
            child = move(node, moves[i])
            if not contains(child, explored):

                if np.array_equal(child, solution2) or np.array_equal(child, solution):
                    print('Found astar solution: ', frontier.size())
                    return
                # append with h1 heuristic
                # cost = h2(child)
                cost = h1(np.array(child).flatten()) + pathcost(np.array(initial).flatten(), np.array(child).flatten())
                frontier.push(child, cost)
    return 0


# Load the cmd arguments into values
def parseinput():
    global initialstate, searchmethod, argcount, extra, startstate, boardinput
    initialstate = sys.argv[1].replace('\'', '').replace('\"', '').upper()
    # initialstate = '123456789ABD EFC'
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
# print(gbfs(boardinput))
# print(astar(boardinput))

astar(boardinput)
