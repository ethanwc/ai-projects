# TCSS 435 PA #2 - Ethan Cheatham
import random
import copy
import numpy as np


class Board:
    def __init__(self, grids, width):
        self.grids = grids
        self.width = width
        self.size = width * width
        self.turn = random.choice(['W', 'B'])

    # Generate all possible rotations the player can pick
    # Should just be 1-4 l or r. Rules might complicate things for initial rounds TODO: hi
    # Takes in all possible moves for next state, returns all rotations for each move
    def getrotations(self, moves):
        rotations = []

        for move in moves:
            # Various rotations for each grid
            for g in range(0, len(self.grids)):
                rotations.append(copy.deepcopy(move).grids[g].rotatecw())
                rotations.append(copy.deepcopy(move).grids[g].rotateccw())

        print(len(rotations))

    # Generate all possible spots where the given player can go
    def getspots(self):
        moves = []

        for g in range(1, len(self.grids) + 1):
            for d in range(1, len(self.grids[g - 1].data) + 1):
                if self.grids[g - 1].data[d - 1] == '.':
                    clone = copy.deepcopy(self)
                    clone.set(self.turn, g, d)
                    moves.append(clone)
                    # clone.print()

        return moves


    def handlewin(self):
        exit(0)

    # Check both players for a win
    def checkwins(self):
        if self.checkwin('W') or self.checkwin('B'):
            self.handlewin()

    # Stitch together grids to check the board for a win for one person
    def checkwin(self, check):
        board = []

        for y in range(3):
            for g in range(2):
                for x in range(3):
                    board.append(self.grids[g].data[x + 3 * y])
        for y in range(3):
            for g in range(2, 4):
                for x in range(3):
                    board.append(self.grids[g].data[x + 3 * y])
        board2 = np.array(board).reshape(6,6)
        print(board2)
        l = board2.tolist()

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

        if l[0][0] == check or l[5][5] == check:
            if l[1][1] == check and l[2][2] == check and l[3][3] == check and l[4][4] == check:
                return True

        if l[0][5] == check or l[5][0] == check:
            if l[1][4] == check and l[2][3] == check and l[3][2] == check and l[4][1] == check:
                return True

        return

    # check if a move can be made...no marble in spot
    def isavail(self, grid, spot):
        return self.grids[grid - 1].data[spot - 1] == '.'

    # input which grid 1-4, and tile 1-9
    def set(self, player, grid, spot):
            self.grids[grid - 1].data[spot - 1] = player

    def print(self):
        print("+------------+------------+")
        for y in range(3):
            for g in range(2):
                for x in range(3):
                    if x == 0:
                        print('|', end='')
                    print(' ', self.grids[g].data[x + 3 * y], end=' ')
            print('|')
        print("+------------+------------+")
        for y in range(3):
            for g in range(2, 4):
                for x in range(3):
                    if x == 0:
                        print('|', end='')
                    print(' ', self.grids[g].data[x + 3 * y], end=' ')
            print('|')
        print("+------------+------------+")


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

board.getrotations(board.getspots())
