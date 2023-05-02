import random

class Game_logic:
    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.moved = False

    def show(self):
        return str('\n'.join('\t'.join(map(str, ans)) for ans in self.grid))
    
    def check_game_over(self, grid):
        for i in range(4):
            for j in range(4):
                if grid[i][j]==0:
                    return False
                for r, c in [(i+1, j), (i, j+1)]:
                    if 0<=r<4 and 0<=c<4 and grid[r][c]==grid[i][j]:
                        return False
        return True
    
    def new_number(self, k=1):
        empty_tiles = []
        # get free positions in the grid
        for i in range(4):
            for j in range(4):
                if self.grid[i][j]==0:
                    empty_tiles.append((i, j))

        # print 2 or 4 in two positions on the empty tiles
        while k:
            random.shuffle(empty_tiles)
            x, y = empty_tiles.pop()
            if random.random()<0.1:
                self.grid[x][y] = 4
            else:
                self.grid[x][y] = 2
            k -= 1

    def make_move(self, move):
        merged = [[False for _ in range(4)] for _ in range(4)]
        self.grid = self.grid.copy()

        if move in {'l', 'r'}:
            if move=='r':
                self.grid = [row[::-1] for row in self.grid]
            for i in range(4):
                for j in range(4):
                    if j>0 and self.grid[i][j]:
                        shift = 0
                        for q in range(j):
                            if self.grid[i][q]==0:
                                shift += 1
                        if shift>0:
                            self.grid[i][j-shift] = self.grid[i][j]
                            self.grid[i][j] = 0
                            self.moved = True
                        if j-shift-1>=0 and self.grid[i][j-shift]==self.grid[i][j-shift-1] and not merged[i][j-shift-1]:
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
                        for q in range(i):
                            if self.grid[q][j]==0:
                                shift += 1
                        if shift>0:
                            self.grid[i-shift][j] = self.grid[i][j]
                            self.grid[i][j] = 0
                            self.moved = True
                        if i-shift-1>=0 and self.grid[i-shift-1][j]==self.grid[i-shift][j] and not merged[i-shift-1][j]:
                            self.grid[i-shift-1][j] *= 2
                            self.grid[i-shift][j] = 0
                            merged[i-shift-1][j] = True
                            self.moved = True
            if move=='d':
                self.grid = self.grid[::-1]

    def play(self):
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
    game = Game_logic()
    game.play()