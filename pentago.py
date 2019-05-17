# TCSS 435 PA #2 - Ethan Cheatham
import random
import copy
import heapq
import numpy as np


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
            # if current > 1:
            total += current
            # total += board.evalline(r)
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
                    else:
                        clone.grids[g].rotateccw()
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
        exit(0)

    # Check both players for a win
    def checkwins(self):
        if self.checkwin('W') or self.checkwin('B'):
            self.handlewin()

    # check the board for a win for one person
    def checkwin(self, check):
        l = self.getboard().tolist()

        for offset in range(0, 2):
            # for x in range()
            for x in range(offset, 5 + offset):
                win = True
                for y in range(offset, 5 + offset):
                    if check != l[x][y]:
                        win = False
                if win:
                    return True

            for y in range(offset, 5 + offset):
                win = True
                for x in range(offset, 5 + offset):
                    if check != l[x][y]:
                        win = False

                if win:
                    return True
        # check \
        if l[0][0] == check or l[5][5] == check:
            if l[1][1] == check and l[2][2] == check and l[3][3] == check and l[4][4] == check:
                return True
        # check 5 in a row 1 above, 1 below
        if l[0][1] == check and l[1][2] == check and l[2][3] == check and l[3][4] == check and l[4][5] == check:
            return True
        if l[1][0] == check and l[2][1] == check and l[3][2] == check and l[4][3] == check and l[5][4] == check:
            return True

        # check /
        if l[0][5] == check or l[5][0] == check:
            if l[1][4] == check and l[2][3] == check and l[3][2] == check and l[4][1] == check:
                return True
        # check 5 in a row 1 above, 1 below
        if l[0][4] == check and l[1][3] == check and l[2][2] == check and l[3][1] == check and l[4][0] == check:
            return True
        if l[1][5] == check and l[2][4] == check and l[3][3] == check and l[4][2] == check and l[5][1] == check:
            return True

        return False

    # check if a move can be made...no marble in spot
    def isavail(self, grid, spot):
        return self.grids[grid - 1].data[spot - 1] == '.'

    # input which grid 1-4, and tile 1-9
    def set(self, player, grid, spot):
            self.grids[grid - 1].data[spot - 1] = player

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


board = Board([Grid(3), Grid(3), Grid(3), Grid(3)], 2)

# while(1):
#     res = readinput()
#     # make sure the move is legal before proceeding
#     if board.isavail(int(res[0]), int(res[1])):
#         board.set(board.turn, int(res[0]), int(res[1]))
#         board.checkwins()
#         board.turn = 'B' if board.turn == 'W' else 'W'
#         board.grids[int(res[2]) - 1].rotate(res[3])
#         board.checkwins()
#         board.print()
#     else:
#         print("Spot taken.")
# board.set(board.turn, 1, 2)
# board.set(board.turn, 1, 8)
# board.set(board.turn, 3, 2)
# board.set(board.turn, 3, 5)

# board.set(board.turn, 1, 2)
# board.set(board.turn, 1, 3)
#
# board.set(board.turn, 1, 6)


board.set(board.turn, 1, 5)
# board.set(board.turn, 1, 1)
board.set(board.turn, 1, 9)
board.set(board.turn, 4, 1)
#
#
board.set(board.turn, 3, 7)
# board.set(board.turn, 3, 5)
board.set(board.turn, 3, 3)
board.set(board.turn, 2, 7)
# board.set(board.turn, 2, 5)
board.set(board.turn, 2, 3)

max = PriorityQueue()

board.print()

for r in board.getrotations(board.getspots()):
    q = PriorityQueue()
    for r2 in r.getrotations(r.getspots()):
        q.push(r, r.heuristic())
    val = q.pop()
    max.push(val, val.heuristic())
    print(val.heuristic())
print("total max", max.pop().heuristic())
