# TCSS 435 PA #2 - Ethan Cheatham
import random
import copy
import heapq
import numpy as np


class Statevalue:
    def __init__(self, state, value):
        self.state = state
        self.value = value

    # Min that looks at an object's value to keep state
    def min(self, other):
        if self.value < other.value:
            return self
        return other

    # Max that looks at an object's value to keep state
    def max(self, other):
        if self.value > other.value:
            return self
        return other


class Minmax:
    def __init__(self, root):
        self.root = root

    def utility(self, node):
        return node.data.heuristic()

    def MinMax(self):
        return self.Max(self.root)

    def Max(self, state):
        if state.terminal():
            return Statevalue(state, self.utility(state))
        v = Statevalue(None, float("-inf"))
        for c in state.children:
            v = v.max(self.Min(c))
        return v

    def Min(self, state):
        if state.terminal():
            return Statevalue(state, self.utility(state))
        v = Statevalue(None, float("inf"))
        for c in state.children:
            v = v.min(self.Max(c))
        return v


class Alphabeta:
    def __init__(self, root):
        self.root = root

    def utility(self, node):
        return node.data.heuristic()

    def AlphaBeta(self):
        return self.Min(self.root, float("-inf"), float("inf"))

    def Max(self, state, a, b):
        if state.terminal():
            return self.utility(state)
        v = float("-inf")
        for c in state.children:
            v = max(v, self.Min(c, a, b))
            if v >= b:
                return b
            a = max(a, v)
        return v

    def Min(self, state, a, b):
        if state.terminal():
            return self.utility(state)
        v = float("inf")
        for c in state.children:
            v = min(v, self.Max(c, a, b))
            if v <= a:
                return v
            b = min(b, v)
        return v


class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def terminal(self):
        return len(self.children) == 0


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
        self._size = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
        self._size += 1

    def pop(self):
        self._size -= 1
        return heapq.heappop(self._queue)[-1]

    def size(self):
        return self._size


class Board:
    def __init__(self, grids, width):
        self.grids = grids
        self.width = width
        self.size = width * width
        self.turn = random.choice(['W', 'B'])
        self.move = None
        self.rotation = None

    def swapturn(self):
        self.turn = 'W' if self.turn == 'B' else 'B'

    # Gi
    # ven a line, evaluate it's sub-heuristic value, increases exponentially for streaks
    def evalline(self, line):
        count, streak = 0, 0
        for s in line:
            if s != self.turn:
                streak = 0
            else:
                streak += 1
                count += 1 if count == 0 else count * streak

        return count

    # Generates every sequence horizontally, vertically, diagonally forward and backwards.
    def gensequences(self):
        state = self.getboard()
        sequences = []
        sequence = ""
        # Rotate board after first loop
        for loop in range(2):
            for x in range(6):
                for y in range(6):
                    sequence += state[x][y]
                sequences.append(sequence)
                sequence = ""

            for k in range(12):
                for j in range(0, k + 1):
                    i = k - j
                    if i < 6 and j < 6:
                        sequence += state[i][j]
                sequences.append(sequence)
                sequence = ""

            state = np.rot90(state)

        return sequences

    # Evaluate the board with exponential increase for streaks.
    def heuristic(self):
        total = 0
        for r in self.gensequences():
            current = self.evalline(r)
            total += current
        return total

    # Generate all possible rotations the player can pick
    # Should just be 1-4 l or r. Rules might complicate things for initial rounds TODO: hi
    # TODO: can't twist the grid that you just placed a marble on
    # TODO: check that board is full with no winners

    # Takes in all possible moves for next state, returns all rotations for each move
    def getrotations(self, moves):
        rotations = []

        for move in moves:
            # Various rotations for each grid
            for g in range(0, len(self.grids)):
                for r in range(2):
                    clone = copy.deepcopy(move)
                    if r == 1:
                        clone.grids[g].rotatecw()
                        clone.rotation = [g, 'R']
                    else:
                        clone.grids[g].rotateccw()
                        clone.rotation = [g, 'L']
                    rotations.append(clone)

        return rotations

    # Get the board as a single 2d array
    def getboard(self):
        board = []

        for y in range(3):
            for g in range(2):
                for x in range(3):
                    board.append(self.grids[g].data[x + 3 * y])
        for y in range(3):
            for g in range(2, 4):
                for x in range(3):
                    board.append(self.grids[g].data[x + 3 * y])
        board2 = np.array(board).reshape(6, 6)
        # print(board2)
        return board2

    # Generate all possible spots where the given player can go
    def getspots(self):
        moves = []

        for g in range(1, len(self.grids) + 1):
            for d in range(1, len(self.grids[g - 1].data) + 1):
                if self.grids[g - 1].data[d - 1] == '.':
                    clone = copy.deepcopy(self)
                    clone.set(self.turn, g, d)
                    moves.append(clone)

        return moves

    def handlewin(self):
        self.print()
        print("Somebody won I guess...")
        exit(0)

    # Check both players for a win
    def checkwins(self):
        if self.checkwin():
            self.handlewin()

    # check the board for a win for one person
    def checkwin(self):
        for sequence in self.gensequences():
            if len(sequence) >= 5:
                count = 0
                for c in range(len(sequence)):
                    count += 1 if sequence[c] == self.turn else 0
                    if count == 5:
                        return True
        return False

    # check if a move can be made...no marble in spot
    def isavail(self, grid, spot):
        return self.grids[grid - 1].data[spot - 1] == '.'

    # input which grid 1-4, and tile 1-9
    def set(self, player, grid, spot):
            self.grids[grid - 1].data[spot - 1] = player
            self.move = [grid, spot]

    def print(self):
        divider = "+------------+------------+"
        print(divider)
        for y in range(3):
            for g in range(2):
                for x in range(3):
                    if x == 0:
                        print('|', end='')
                    print(' ', self.grids[g].data[x + 3 * y], end=' ')
            print('|')
        print(divider)
        for y in range(3):
            for g in range(2, 4):
                for x in range(3):
                    if x == 0:
                        print('|', end='')
                    print(' ', self.grids[g].data[x + 3 * y], end=' ')
            print('|')
        print(divider)


# Board is composed of four grids to represent game state.
class Grid:
    def __init__(self, width):
        self.width = width
        self.size = width * width
        self.data = []

        for i in range(self.size):
            self.data.append('.')

    # Set a specific spot to a move from either player, should probably use the board set method.
    def set(self, x, y, val):
        self.data[(x - 1) + (y - 1) * self.width] = val

    def print(self):
        for i in range(1, self.size + 1):
            print(self.data[i-1], end=' ')
            if i % self.width == 0:
                print("\n")

    def rotate(self, direction):
        if direction == 'L':
            self.rotateccw()
        else:
            self.rotatecw()

    def rotatecw(self):
        self.data = np.rot90(np.array(self.data).reshape(self.width, self.width), 3).flatten().tolist()

    def rotateccw(self):
        self.data = np.rot90(np.array(self.data).reshape(self.width, self.width)).flatten().tolist()


def readinput():
    userinput = input('Enter move\n')
    gridmove = userinput[0]
    spot = userinput[2]
    gridrotate = userinput[4]
    direction = userinput[5]
    return gridmove, spot, gridrotate, direction


# used to generate a tree two levels deep to determine a move
def tempgentree(state):
    tree = Node(state)

    for r in board.getrotations(board.getspots()):
        val = Node(r)
        tree.add_child(val)

    return tree


board = Board([Grid(3), Grid(3), Grid(3), Grid(3)], 2)

while 1:
    # B for bot aka AI
    if board.turn == 'B':
        possibilities = tempgentree(board)
        minmax = Minmax(possibilities)
        val = minmax.MinMax().state.data
        board.set(board.turn, val.move[0], val.move[1])
        board.checkwins()
        board.grids[val.rotation[0]].rotate(val.rotation[1])
        board.rotation = [val.rotation[0], val.rotation[1]]
        board.checkwins()
        board.print()
        print(board.move, board.rotation)
        board.turn = 'W'

    # Human Turn
    elif board.turn == 'W':
        res = readinput()
        if board.isavail(int(res[0]), int(res[1])):
            board.set(board.turn, int(res[0]), int(res[1]))
            board.checkwins()
            board.grids[int(res[2]) - 1].rotate(res[3])
            board.rotation = [int(res[2]), res[3]]
            board.checkwins()
            board.print()
            print(board.move, board.rotation)
            board.turn = 'B'
        else:
            print("Spot taken.")
