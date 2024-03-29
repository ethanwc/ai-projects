# TCSS 435 PA #1 - Ethan Cheatham
# Moving Tile
import hashlib
import sys
import numpy as np
import copy
import heapq


# Represent the state of the board with depth
class State:
    state = []
    depth = None

    def __init__(self, initial):
        self.state = initial
        self.depth = 0


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
        self._size = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
        self._size += 1

    def pop(self):
        self._size -= 1
        return heapq.heappop(self._queue)[-1]

    def size(self):
        return self._size


class Point:
    def __init__(self, initx, inity):
        self.x = initx
        self.y = inity


searchMethods = {'BFS', 'DFS', 'DLS', 'ID', 'GBFS', 'ASTAR', 'FASTBFS'}
heuristics = {'h1', 'h2'}
solution = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', ' ']).reshape(4, 4)
solution2 = np.array(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'F', 'E', ' ']).reshape(4, 4)
size = 4


# dumbe caller
def h(state):
    if extra == 'h1':
        return h1(np.array(state.state).flatten())
    else:
        return h2(np.array(state.state).reshape(4, 4))


# h1 is the number of misplaced tiles
# goal state is 1:9,abcdef or 1:9,abcdfe
def h1(state):
    n = 0
    sol1 = np.array(solution).flatten()
    sol2 = np.array(solution2).flatten()
    for i in range(0, len(state)):
        if not (state[i] == sol1[i]or state[i] == sol2[i]):
            n += 1
    return n


# the sum of the distances of the tiles from their goal positions
# state should be 4x4
def h2(state):
    distance = 0
    for x in range(0, size):
        for y in range(0, size):
            if state[x][y] == '1':
                distance += abs(x - 0) + abs(y - 0)
            if state[x][y] == '2':
                distance += abs(x - 0) + abs(y - 1)
            if state[x][y] == '3':
                distance += abs(x - 0) + abs(y - 2)
            if state[x][y] == '4':
                distance += abs(x - 0) + abs(y - 3)
            if state[x][y] == '5':
                distance += abs(x - 1) + abs(y - 0)
            if state[x][y] == '6':
                distance += abs(x - 1) + abs(y - 1)
            if state[x][y] == '7':
                distance += abs(x - 1) + abs(y - 2)
            if state[x][y] == '8':
                distance += abs(x - 1) + abs(y - 3)
            if state[x][y] == '9':
                distance += abs(x - 2) + abs(y - 0)
            if state[x][y] == 'A':
                distance += abs(x - 2) + abs(y - 1)
            if state[x][y] == 'B':
                distance += abs(x - 2) + abs(y - 2)
            if state[x][y] == 'C':
                distance += abs(x - 2) + abs(y - 3)
            if state[x][y] == 'D':
                distance += abs(x - 3) + abs(y - 0)
            if state[x][y] == 'E':
                distance += abs(x - 3) + abs(y - 1)
            if state[x][y] == 'F':
                distance += abs(x - 3) + abs(y - 2)
    return distance


# pathcost g(n) should be the depth level, the number of moves taken, not the cost between initial and current.
def pathcost(initial, current):
    n = 0
    # print(initial, current)
    for i in range(0, len(initial)):
        if not initial[i] == current[i]:
            n += 1
    return n


# move the blank space of the board, by swapping its index with another piece
def move(state, move):
    newstate = copy.deepcopy(state)
    for i in range(0, size):
        for j in range(0, size):
            if newstate.state[i][j] == ' ':
                xoff = yoff = 0
                if move == 'right':
                    xoff = 1
                if move == 'left':
                    xoff = -1
                if move == 'up':
                    yoff = -1
                if move == 'down':
                    yoff = 1

                temp = newstate.state[i + yoff][j + xoff]
                newstate.state[i + yoff][j + xoff] = newstate.state[i][j]
                newstate.state[i][j] = temp
                newstate.depth += 1
                return newstate
    print('error')
    exit(1)
    return 0


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


def contains(element, list):
    length = len(list)

    for i in range(0, length):
        if np.array_equal(element, list[i]):
            return True
    return False


# hash a string, best way considering space and time
def md5(w):
    return hashlib.md5(w).hexdigest()[:9]


# Input is a state object of state and depth
def bfs(initial):
    frontier = dict()
    explored = dict()
    frontier[md5(np.array(initial.state).tostring())] = initial

    created, expanded, maxfringe = 0, 0, 0

    if np.array_equal(initial.state, solution):
        return 0, 0, 0, 0

    while frontier:
        location = next(iter(frontier))
        node = frontier.pop(location)

        if len(frontier) > maxfringe:
            maxfringe = len(frontier)

        hash = md5(np.array(node.state).tostring())
        explored[hash] = node
        expanded += 1
        movecount = 0
        for path in getmoves(node.state):
            # child should be state object
            child = move(node, path)
            pathhash = md5(np.array(child.state).tostring())
            movecount += 1
            if pathhash not in frontier and pathhash not in explored:
                created += 1

                if np.array_equal(child.state, solution) or np.array_equal(child.state, solution2):
                    return child.depth, created, expanded, maxfringe

                frontier[pathhash] = child

    return -1, 0, 0, 0


# dfs/ dls
def dfs(initial, limit):
    frontier = dict()
    explored = dict()
    frontier[md5(np.array(initial.state).tostring())] = initial
    maxdepth = limit + 1 if limit != 0 else float("inf")
    created, expanded, maxfringe = 0, 0, 0

    while frontier:
        if len(frontier) > maxfringe:
            maxfringe = len(frontier)

        node = frontier.popitem()[1]

        hash = md5(np.array(node.state).tostring())
        explored[hash] = node

        expanded += 1
        movecount = 0
        for path in reversed(getmoves(node.state)):
            child = move(node, path)
            pathhash = md5((np.array(child.state)).tostring())
            movecount += 1
            if pathhash not in frontier and pathhash not in explored:
                created += 1
                if np.array_equal(child.state, solution) or np.array_equal(child.state, solution2):
                    return child.depth, created, expanded, maxfringe
                # only add if depth is less than or equal to max depth
                if child.depth <= maxdepth:
                    frontier[pathhash] = child

    return -1, 0, 0, 0


# A-star(0) and greedy search(1)
def hs(initial, search):
    frontier = PriorityQueue()
    frontier.push(initial, 1)
    explored = []
    if np.array_equal(initial.state, solution) or np.array_equal(initial.state, solution2):
        return 0, 0, 0, 0

    created, expanded, maxfringe = 0, 0, 0

    while frontier.size() > 0:
        node = frontier.pop()
        explored.append(node)
        moves = getmoves(node.state)
        expanded += 1
        if frontier.size() > maxfringe:
            maxfringe = frontier.size()
        for i in range(0, len(moves)):
            child = move(node, moves[i])
            created += 1
            if not contains(child, explored):
                if np.array_equal(child.state, solution2) or np.array_equal(child.state, solution):
                    return child.depth, created, expanded, maxfringe

                # g + h for astar, h for greedy
                # add cost to current path for a-star
                cost = h(child) + child.depth if search else h(child)
                print(child.state, cost)
                frontier.push(child, cost)

    return -1, 0, 0, 0


# Load the cmd arguments into values
def parseinput():
    global extra
    global searchmethod, argcount, extra, startstate
    initialstate = sys.argv[1].replace('\'', '').replace('\"', '').upper()
    searchmethod = sys.argv[2]
    startstate = []
    argcount = len(sys.argv) - 1
    input = ''
    extra = ''

    if argcount > 2:
        extra = sys.argv[3]

    for i in sys.argv[1:]:
        input += i + ' '

    # Build the State model
    i = 0
    temp = []
    for c in initialstate:
        temp += c
        i += 1
        if i % 4 == 0 and i > 0:
            startstate += temp
            temp = []
    boardinput = np.array(startstate).reshape(4, 4)

    validateinput(initialstate, searchmethod, argcount, boardinput)


# Check that the input is valid..
def validateinput(initialstate, searchmethod, argcount, boardinput):
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
        if not extra in heuristics:
            print('Invalid Input: No heuristic specified')
            valid = False

    # Special Case for depth limited search
    if searchmethod.lower() == 'dls':
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

    if valid == 1:
        handleinput(boardinput)


# Handle input after checking it is okay.
def handleinput(boardinput):
    res = 0
    puzzle = State(boardinput)
    if searchmethod.lower() == 'bfs':
        res = bfs(puzzle)
    elif searchmethod.lower() == 'dfs':
        res = dfs(puzzle, 0)
    elif searchmethod.lower() == 'dls':
        res = dfs(puzzle, int(extra))
    elif searchmethod.lower() == 'id':
        print('id chosen, its not implemented though... :)')
    elif searchmethod.lower() == 'gbfs':
        res = hs(puzzle, 1)
    elif searchmethod.lower() == 'astar':
        res = hs(puzzle, 0)
    if res != 0:
        print(*res, sep=", ")


# Start the program
parseinput()
