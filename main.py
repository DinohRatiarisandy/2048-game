"""
    This module is the main implementation
    of the 2048 game, including the game logic
    with a graphical interface built with Pygame.
"""

import random
import sys
import pygame
from game_constants import COLORS

# Initialization
pygame.init()
pygame.font.init()
pygame.display.set_caption('2048')

# logo
ICON_PATH = "assets\\2048.png"
icon_surface = pygame.image.load(ICON_PATH)
pygame.display.set_icon(icon_surface)

# time
time = pygame.time.Clock()

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
SPACE_BETWEEN_TILES = 10
SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
SCREEN.fill(pygame.Color('gray'))
GRID_SIZE = 4

class Game2048:
    """Play the game with all fonctionalities"""
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.is_over = False
        self.moved = False
        self.initial_high_score = 0
        self.score = 0
        self.high_score = self.find_high_score()

    def find_high_score(self):
        """Find the past high score in high_score.txt"""      
        with open('high_score.txt', 'r', encoding='utf-8') as file:
            self.initial_high_score = int(file.read())
        return self.initial_high_score

    def draw_score(self):
        """Draw the score on the screen"""
        # Clear the area where scores are displayed
        score_rect = pygame.Rect(10, 410, WINDOW_WIDTH, 40)
        high_score_rect = pygame.Rect(10, 450, WINDOW_WIDTH, 40)
        pygame.draw.rect(SCREEN, pygame.Color('gray'), score_rect)
        pygame.draw.rect(SCREEN, pygame.Color('gray'), high_score_rect)

        font = pygame.font.Font('freesansbold.ttf', 24)
        score_text = font.render(f'Score: {self.score}', True, 'black')
        high_score_text = font.render(f'High Score: {self.high_score}', True, 'black')
        SCREEN.blit(score_text, (10, 410))
        SCREEN.blit(high_score_text, (10, 450))
        pygame.display.flip()
        
    def is_game_over(self):
        """Chech if the player lose. He can't move any of 4 directions"""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                for row, col in [(i+1, j), (i, j+1)]:
                    if 0<=row<GRID_SIZE and 0<=col<GRID_SIZE:
                        if self.grid[row][col]==self.grid[i][j] \
                            or self.grid[i][j]==0 or self.grid[row][col]==0:
                            self.is_over = False
                            return False

        self.is_over = True
        return True
    
    def draw_game_over(self):
        """Print Game over on the screen if the user lose"""
        # font
        font = pygame.font.Font('freesansbold.ttf', 24)

        # rectangle
        pygame.draw.rect(SCREEN, 'black', [50, 50, 300, 100], 0, 10)

        game_over_text1 = font.render('GAME OVER !', True, 'white')
        game_over_text2 = font.render('Press ENTER to restart', True, 'white')

        SCREEN.blit(game_over_text1, (130, 65))
        SCREEN.blit(game_over_text2, (70, 105))

        pygame.display.flip()

    def new_number(self, k=1):
        """Add number after each user move"""
        empty_tiles = []
        # get free positions in the grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
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
        """Actualise the grid after user move"""
        merged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        if move in {'l', 'r'}:
            if move=='r':
                self.grid = [row[::-1] for row in self.grid]
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
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
                            self.score += self.grid[i][j-shift-1]
                            self.grid[i][j-shift] = 0
                            merged[i][j-shift-1] = True
                            self.moved = True
            if move=='r':
                self.grid = [row[::-1] for row in self.grid]
        
        elif move in {'u', 'd'}:
            if move=='d':
                self.grid = self.grid[::-1]
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
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
                            self.score += self.grid[i-shift-1][j]
                            self.grid[i-shift][j] = 0
                            merged[i-shift-1][j] = True
                            self.moved = True
            if move=='d':
                self.grid = self.grid[::-1]

    def draw_game(self):
        """Draw the board with tile and number"""
        # background color
        background_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_WIDTH)
        pygame.draw.rect(
            SCREEN,
            COLORS['bg'],
            background_rect,
            border_bottom_left_radius=8,
            border_bottom_right_radius=8
        )

        # print each cell
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                val = self.grid[i][j]
                # 1. Create rectangle
                pos_x = j*WINDOW_WIDTH // GRID_SIZE + SPACE_BETWEEN_TILES
                pos_y = i*WINDOW_WIDTH // GRID_SIZE + SPACE_BETWEEN_TILES
                w_rect = WINDOW_WIDTH // GRID_SIZE - 2*SPACE_BETWEEN_TILES
                h_rect = WINDOW_WIDTH // GRID_SIZE - 2*SPACE_BETWEEN_TILES
                board_rect = pygame.Rect(pos_x, pos_y, w_rect, h_rect)
                
                # 2. draw rectangle
                if val<=2048:
                    tile_color = COLORS[val]
                else:
                    tile_color = COLORS['highest value']
                pygame.draw.rect(SCREEN, tile_color, board_rect, border_radius=5)

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
                    SCREEN.blit(text_surface, text_rect)
                    pygame.draw.rect(SCREEN, 'black', [pos_x, pos_y, w_rect, h_rect], 1, 5)

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
                        if event.key==pygame.K_ESCAPE:
                            return 'q'

                    else:
                        if event.key==pygame.K_UP:
                            return 'u'
                        if event.key==pygame.K_DOWN:
                            return 'd'
                        if event.key==pygame.K_LEFT:
                            return 'l'
                        if event.key==pygame.K_RIGHT:
                            return 'r'
                        if event.key==pygame.K_ESCAPE:
                            return 'q'

    def play(self):
        """Play the game 2048 (main)"""
        self.new_number(k=2)

        while True:
            self.draw_score()
            self.draw_game()
            pygame.display.flip()

            key = self.user_move()

            if key=='q':
                pygame.quit()
                sys.exit()

            self.make_move(key)

            if not self.moved:
                continue

            self.new_number()
            self.moved = False

            if self.is_game_over():
                if self.high_score > self.initial_high_score:
                    with open('high_score.txt', 'w', encoding='utf-8') as file:
                        file.write(f'{self.high_score}')

                self.draw_score()
                self.draw_game()
                self.draw_game_over()
                pygame.display.flip()

                key = self.user_move()

                if key=='y':
                    play_again_2048 = Game2048()
                    play_again_2048.play()
                else:
                    pygame.quit()
                    sys.exit()

            if self.score>self.high_score:
                self.high_score = self.score

            time.tick(60)

if __name__=="__main__":
    play_2048 = Game2048()
    play_2048.play()
