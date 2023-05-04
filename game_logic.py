"""Module for the main logic of 2048 (CONSOLE MODE)"""

import random

class GameLogic:
    """The logic of the game (merge two same numbers, move etc.)"""

    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.moved = False

    def show(self):
        """Print the grid on console"""

        return str('\n'.join('\t'.join(map(str, ans)) for ans in self.grid))

    def check_game_over(self, grid):
        """Check if the game if it's over or not"""

        for i in range(4):
            for j in range(4):
                if grid[i][j]==0:
                    return False
                for row, col in [(i+1, j), (i, j+1)]:
                    if 0<=row<4 and 0<=col<4 and grid[row][col]==grid[i][j]:
                        return False
        return True

    def new_number(self, k=1):
        """Add new numbers on the empty tiles in after user's move"""

        empty_tiles = []

        # get free positions in the grid
        for i in range(4):
            for j in range(4):
                if self.grid[i][j]==0:
                    empty_tiles.append((i, j))

        # print 2 or 4 in two positions on the empty tiles
        while k:
            random.shuffle(empty_tiles)
            row, col = empty_tiles.pop()
            if random.random()<0.1:
                self.grid[row][col] = 4
            else:
                self.grid[row][col] = 2
            k -= 1

    def make_move(self, move):
        """Actualise the grid after user's move"""

        merged = [[False for _ in range(4)] for _ in range(4)]
        self.grid = self.grid.copy()

        if move in {'l', 'r'}:
            if move=='r':
                self.grid = [row[::-1] for row in self.grid]
            for i in range(4):
                for j in range(4):
                    if j>0 and self.grid[i][j]:
                        shift = 0
                        for i_backward in range(j):
                            if self.grid[i][i_backward]==0:
                                shift += 1
                        if shift>0:
                            self.grid[i][j-shift] = self.grid[i][j]
                            self.grid[i][j] = 0
                            self.moved = True
                        if j-shift-1>=0 and self.grid[i][j-shift]==self.grid[i][j-shift-1] \
                            and not merged[i][j-shift-1]:
                            self.grid[i][j-shift-1] *= 2
                            self.grid[i][j-shift] = 0
                            merged[i][j-shift-1] = True
                            self.moved = True
            if move=='r':
                self.grid = [row[::-1] for row in self.grid]

        elif move in {'u', 'd'}:
            if move=='d':
                self.grid = self.grid[::-1]
            for i in range(4):
                for j in range(4):
                    if i>0 and self.grid[i][j]:
                        shift = 0
                        for i_backward in range(i):
                            if self.grid[i_backward][j]==0:
                                shift += 1
                        if shift>0:
                            self.grid[i-shift][j] = self.grid[i][j]
                            self.grid[i][j] = 0
                            self.moved = True
                        if i-shift-1>=0 and self.grid[i-shift-1][j]==self.grid[i-shift][j] \
                            and not merged[i-shift-1][j]:
                            self.grid[i-shift-1][j] *= 2
                            self.grid[i-shift][j] = 0
                            merged[i-shift-1][j] = True
                            self.moved = True
            if move=='d':
                self.grid = self.grid[::-1]

    def play(self):
        """Play the game"""

        self.new_number(k=2)

        while True:
            print("\n Press: u (Up) \t d (Down) \t l (Left) \t r (Right) \t q (Quit) \n")
            print(self.show())
            key = input("\nYour move: ")

            if not key:
                continue
            if key=='q':
                return
            if key in {'u', 'd', 'l', 'r'}:
                self.make_move(key)

                if not self.moved:
                    continue

                self.new_number()
                self.moved = False

                if self.check_game_over(self.grid):
                    print("\n", self.show())
                    print("\nGAME OVER !\n")
                    return

if __name__=='__main__':
    game = GameLogic()
    game.play()
