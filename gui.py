"""Module for the 2048's GUI (Testing pygame)"""

import random
import sys
import pygame
from game_constants import COLORS, TEST_GRID

# window size
WIDTH = 400
HEIGHT = 500
SPACECING = 10
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.font.init()

def draw_game(grid):
    """Draw the board (tile + color + number"""

    # background color
    background_rect = pygame.Rect(0, 0, WIDTH, WIDTH)
    pygame.draw.rect(
        SCREEN,
        COLORS['bg'],
        background_rect,
        border_bottom_left_radius=8,
        border_bottom_right_radius=8
    )

    # print each cell
    for i in range(4):
        for j in range(4):
            val = grid[i][j]
            # 1. Create rectangle
            pos_x = j*WIDTH // 4 + SPACECING
            pos_y = i*WIDTH // 4 + SPACECING
            w_rect = WIDTH // 4 - 2*SPACECING
            h_rect = WIDTH // 4 - 2*SPACECING
            board_rect = pygame.Rect(pos_x, pos_y, w_rect, h_rect)

            # 2. draw rectangle
            if val<=2048:
                tile_color = COLORS[val]
            else:
                tile_color = COLORS['highest value']
            pygame.draw.rect(SCREEN, tile_color, board_rect, border_radius=5)

            # Print the value on the Tile
            font = pygame.font.Font('freesansbold.ttf', 40-2*len(str(val)))
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
                pygame.draw.rect(SCREEN, 'black', [pos_x, pos_y, 80, 80], 1, 5)

def user_move():
    """Take the user's move"""

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return 'q'
            if event.type==pygame.KEYDOWN:
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

def main():
    """main of the game."""

    # initialization
    pygame.init()
    pygame.display.set_caption('2048')

    while True:
        random.shuffle(TEST_GRID)
        SCREEN.fill(pygame.Color('gray'))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.sys.exit()

        draw_game(TEST_GRID)
        pygame.display.flip()

        # wait the user move
        key = user_move()
        if key=='q':
            pygame.quit()
            sys.exit()

if __name__=="__main__":
    main()
