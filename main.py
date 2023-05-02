import pygame
import random
from game_constants import COLORS

# size of the grid
N = 4

class Game_2048:
    def __init__(self):
        # Initialization
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('2048')

        # Variables
        self.grid = [[0 for _ in range(N)] for _ in range(N)]
        self.is_over = False
        self.moved = False
        self.initial_high_score = 0
        self.score = 0
        self.high_score = self.find_high_score()
        self.width = 400
        self.height = 500
        self.spacecing = 10
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.screen.fill(pygame.Color('gray'))

        # time
        self.time = pygame.time.Clock()

    def find_high_score(self):
        file_high_score = open('high_score.txt', 'r')
        self.initial_high_score = int(file_high_score.readline())
        file_high_score.close()
        return self.initial_high_score
    
    def draw_score(self):
        """Draw the score on the screen"""

        # Clear the area where scores are displayed
        score_rect = pygame.Rect(10, 410, self.width, 40)
        high_score_rect = pygame.Rect(10, 450, self.width, 40)
        pygame.draw.rect(self.screen, pygame.Color('gray'), score_rect)
        pygame.draw.rect(self.screen, pygame.Color('gray'), high_score_rect)

        font = pygame.font.Font('freesansbold.ttf', 24)
        score_text = font.render(f'Score: {self.score}', True, 'black')
        high_score_text = font.render(f'High Score: {self.high_score}', True, 'black')
        self.screen.blit(score_text, (10, 410))
        self.screen.blit(high_score_text, (10, 450))
        pygame.display.flip()
        
    def is_game_over(self):
        """Chech if the player lose. He can't move any of 4 directions"""

        for i in range(N):
            for j in range(N):
                for r, c in [(i+1, j), (i, j+1)]:
                    if 0<=r<N and 0<=c<N:
                        if self.grid[r][c]==self.grid[i][j] or self.grid[i][j]==0 or self.grid[r][c]==0:
                            self.is_over = False
                            return False

        self.is_over = True
        return True
    
    def draw_game_over(self):
        """Print Game over on the screen if the user lose"""

        # font
        font = pygame.font.Font('freesansbold.ttf', 24)

        # rectangle
        pygame.draw.rect(self.screen, 'black', [50, 50, 300, 100], 0, 10)

        game_over_text1 = font.render('GAME OVER !', True, 'white')
        game_over_text2 = font.render('Press ENTER to restart', True, 'white')

        self.screen.blit(game_over_text1, (130, 65))
        self.screen.blit(game_over_text2, (70, 105))

        pygame.display.flip()

    def new_number(self, k=1):
        """Add number after each user move"""

        empty_tiles = []
        # get free positions in the grid
        for i in range(N):
            for j in range(N):
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
        """Actualise the grid after user move"""

        merged = [[False for _ in range(N)] for _ in range(N)]
        self.grid = self.grid.copy()

        if move in {'l', 'r'}:
            if move=='r':
                self.grid = [row[::-1] for row in self.grid]
            for i in range(N):
                for j in range(N):
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
                            self.score += self.grid[i][j-shift-1]
                            self.grid[i][j-shift] = 0
                            merged[i][j-shift-1] = True
                            self.moved = True
            if move=='r':
                self.grid = [row[::-1] for row in self.grid]
        
        elif move in {'u', 'd'}:
            if move=='d':
                self.grid = self.grid[::-1]
            for i in range(N):
                for j in range(N):
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
                            self.score += self.grid[i-shift-1][j]
                            self.grid[i-shift][j] = 0
                            merged[i-shift-1][j] = True
                            self.moved = True
            if move=='d':
                self.grid = self.grid[::-1]

    def draw_game(self):
        """Draw the board with tile and number"""

        # background color
        background_rect = pygame.Rect(0, 0, self.width, self.width)
        pygame.draw.rect(self.screen, COLORS['bg'], background_rect, border_bottom_left_radius=8, border_bottom_right_radius=8)

        # print each cell
        for i in range(N):
            for j in range(N):
                val = self.grid[i][j]
                # 1. Create rectangle
                pos_x = j*self.width // N + self.spacecing
                pos_y = i*self.width // N + self.spacecing
                w_rect = self.width // N - 2*self.spacecing
                h_rect = self.width // N - 2*self.spacecing
                board_rect = pygame.Rect(pos_x, pos_y, w_rect, h_rect)
                
                # 2. draw rectangle
                if val<=2048:
                    tile_color = COLORS[val]
                else:
                    tile_color = COLORS['highest value']
                pygame.draw.rect(self.screen, tile_color, board_rect, border_radius=5)

                # Print the value on the Tile
                font = pygame.font.Font('freesansbold.ttf', w_rect-12*len(str(val)))
                if val<=8:
                    val_color = COLORS['dark text']
                elif 8<val<=2048:
                    val_color = COLORS['light text']
                else:
                    val_color = COLORS['other']
                if val:
                    text_surface = font.render(str(val), True, val_color)
                    text_rect = text_surface.get_rect(center=(pos_x + w_rect//2, pos_y + h_rect//2))
                    self.screen.blit(text_surface, text_rect)
                    pygame.draw.rect(self.screen, 'black', [pos_x, pos_y, w_rect, h_rect], 1, 5)

    def user_move(self):
        """Wait for user move"""

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return 'q'
                if event.type==pygame.KEYDOWN:
                    if self.is_over:
                        if event.key==pygame.K_RETURN:
                            return 'y'
                        elif event.key==pygame.K_ESCAPE:
                            return 'q'
                        else:
                            continue
                    else:
                        if event.key==pygame.K_UP:
                            return 'u'
                        elif event.key==pygame.K_DOWN:
                            return 'd'
                        elif event.key==pygame.K_LEFT:
                            return 'l'
                        elif event.key==pygame.K_RIGHT:
                            return 'r'
                        elif event.key==pygame.K_ESCAPE:
                            return 'q'
                        else:
                            continue

    def play(self):
        """Play the game 2048 (main)"""

        self.new_number(k=2)

        while True:
            self.draw_score()
            self.draw_game()
            pygame.display.flip()

            key = self.user_move()

            if key == 'q':
                pygame.quit()
                exit()

            self.make_move(key)

            if not self.moved:
                continue

            self.new_number()
            self.moved = False

            if self.is_game_over():
                if self.high_score > self.initial_high_score:
                    file_high_score = open('high_score.txt', 'w')
                    file_high_score.write(f'{self.high_score}')
                    file_high_score.close()

                self.draw_score()
                self.draw_game()
                self.draw_game_over()
                pygame.display.flip()

                key = self.user_move()

                if key == 'y':
                    play_2048 = Game_2048()
                    play_2048.play()
                else:
                    pygame.quit()
                    exit()

            if self.score > self.high_score:
                self.high_score = self.score

            self.time.tick(60)

if __name__=="__main__":
    play_2048 = Game_2048()
    play_2048.play()