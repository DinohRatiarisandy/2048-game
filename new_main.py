import pygame
import random

class Game_logic:
    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        # self.grid[2][2] = 2; self.grid[1][1] = 2; self.grid[3][3] = 2; self.grid[0][0] = 2

    def show(self, grid):
        return str('\n'.join('\t'.join(map(str, ans)) for ans in self.grid))
    
    def new_number(self, k=1):
        empty_tiles = []
        # get free positions in the grid
        for i in range(4):
            for j in range(4):
                if self.grid[i][j]==0:
                    empty_tiles.append((i, j))

        # print 2 or 4 in two positions on the empty tiles
        while k:
            x, y = random.choice(empty_tiles)
            if random.randint(1, 10)==10:
                self.grid[x][y] = 4
            else:
                self.grid[x][y] = 2
            k -= 1

    def make_move(self, move):
        merged = [[False for _ in range(4)] for _ in range(4)]
        grid = self.grid.copy()

        if move in {'l', 'r'}:
            if move=='r':
                grid = [row[::-1] for row in grid]
            for i in range(4):
                for j in range(4):
                    if j>0 and grid[i][j]:
                        shift = 0
                        for q in range(j):
                            if grid[i][q]==0:
                                shift += 1
                        if shift>0:
                            grid[i][j-shift] = grid[i][j]
                            grid[i][j] = 0
                        if j-shift-1>=0 and grid[i][j-shift]==grid[i][j-shift-1] and not merged[i][j-shift-1]:
                            grid[i][j-shift-1] *= 2
                            grid[i][j-shift] = 0
                            merged[i][j-shift-1] = True
            if move=='r':
                grid = [row[::-1] for row in grid]
        
        elif move in {'u', 'd'}:
            if move=='d':
                grid = grid[::-1]
            for i in range(4):
                for j in range(4):
                    if i>0 and grid[i][j]:
                        shift = 0
                        for q in range(i):
                            if grid[q][j]==0:
                                shift += 1
                        if shift>0:
                            grid[i-shift][j] = grid[i][j]
                            grid[i][j] = 0
                        if i-shift-1>=0 and grid[i-shift-1][j]==grid[i-shift][j] and not merged[i-shift-1][j]:
                            grid[i-shift-1][j] *= 2
                            grid[i-shift][j] = 0
                            merged[i-shift-1][j] = True
            if move=='d':
                grid = grid[::-1]

        return grid

    def play(self):
        self.new_number(k=2)

        while True:
            print("\n Press: u (Up) \t d (Down) \t l (Left) \t r (Right) \t q (Quit) \n")
            print(self.show(self.grid))
            key = input()
            if not key:
                continue
            if key=='q':
                return
            if key in {'u', 'd', 'l', 'r'}:
                new_grid = self.make_move(key)
                if new_grid!=self.grid:
                    self.grid = new_grid
                    self.new_number()
    
if __name__=='__main__':
    game = Game_logic()
    game.play()