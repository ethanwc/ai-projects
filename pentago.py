import numpy as np


class Board:
    def __init__(self, grids, width):
        self.grids = grids
        self.width = width
        self.size = width * width

    def checkwin(self, check):
        # cases to check: horizontal left, horizontal right, vertical bottom, vertical top, \, \ - 1, /, \ - 1

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
                    else:
                        print(x + 1, y + 1)

                if win:
                    # print(x, y)
                    # print(check, l[x][y])
                    return True

        if l[0][0] == check or l[5][5] == check:
            if l[1][1] == check and l[2][2] == check and l[3][3] == check and l[4][4] == check:
                return True

        if l[0][5] == check or l[5][0] == check:
            if l[1][4] == check and l[2][3] == check and l[3][2] == check and l[4][1] == check:
                return True

        return False

    def print(self):
        print("-----------------------------------------")
        for y in range(3):
            for g in range(2):
                for x in range(3):
                    print(self.grids[g].data[x + 3 * y], end='\t')
            print("\n\n")
        print("-----------------------------------------")
        for y in range(3):
            for g in range(2, 4):
                for x in range(3):
                    print(self.grids[g].data[x + 3 * y], end='\t')
            print("\n\n")


# Board is composed of four grids to represent game state.
class Grid:
    def __init__(self, width):
        self.width = width
        self.size = width * width
        self.data = []

        for i in range(self.size):
            self.data.append('.')

    # Set a specific spot to a move from either player
    def set(self, x, y, val):
        self.data[(x - 1) + (y - 1) * self.width] = val

    def print(self):
        for i in range(1, self.size + 1):
            print(self.data[i-1], end=' ')
            if i % self.width == 0:
                print("\n")

    def rotatecw(self):
        self.data = np.rot90(np.array(self.data).reshape(self.width, self.width), 3).flatten().tolist()

    def rotateccw(self):
        self.data = np.rot90(np.array(self.data).reshape(self.width, self.width)).flatten().tolist()


test = Grid(3)
# test.print()
test.set(1, 1, 11)
test.set(1, 3, 1)
test.set(3, 1, 2)
# test.print()

# test.rotatecw()


# test.print()
r = Grid(3)
v = Grid(3)

r.set(1,1,'g')
r.set(1,2,'g')
r.set(1,3,'g')
r.set(2,1,'g')
r.set(3,1,'g')
f = Grid(3)

f.set(1,1,'g')
f.set(1,2,'g')
f.set(2,1,'g')


v.set(1,1,'g')
v.set(1,2,'g')
f.set(2,2, 5)
# r.print()

test2 = [r, f, v, r]
board = Board(test2, 2)
# board.print()

print(board.checkwin('g'))