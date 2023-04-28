import pygame
import random

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60

# 2048 game color library
colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light text': (249, 246, 242),
    'dark text': (119, 110, 101),
    'other': (0, 0, 0),
    'bg': (187, 173, 160)
}

# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
font = pygame.font.Font('freesansbold.ttf', 24)
game_over = False
spawn_new = True
direction = ''
score = 0
file_high_score = open('high_score.txt', 'r')
init_high = int(file_high_score.readline())
file_high_score.close()
high_score = init_high

# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('GAME OVER !', True, 'white')
    game_over_text2 = font.render('Press ENTER to restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

# Take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc=='UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i>0:
                    for q in range(i):
                        if board[q][j]==0:
                            shift += 1
                    if shift>0:
                        board[i-shift][j] = board[i][j]
                        board[i][j] = 0
                    if i-shift-1>=0 and board[i-shift-1][j]==board[i-shift][j] and not merged[i-shift-1][j]:
                        board[i-shift-1][j] *= 2
                        score += board[i-shift-1][j]
                        board[i-shift][j] = 0
                        merged[i-shift-1][j] = True
    elif direc=='DOWN':
        for i in reversed(range(4)):
            for j in range(4):
                shift = 0
                if i<3:
                    for q in range(i+1, 4):
                        if board[q][j]==0:
                            shift += 1
                    if shift>0:
                        board[i+shift][j] = board[i][j]
                        board[i][j] = 0
                    if i+shift+1<=3 and board[i+shift+1][j]==board[i+shift][j] and not merged[i+shift+1][j]:
                        board[i+shift+1][j] *= 2
                        score += board[i+shift+1][j]
                        board[i+shift][j] = 0
                        merged[i+shift+1][j] = True
    elif direc=='LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                if j>0:
                    for q in range(j):
                        if board[i][q]==0:
                            shift += 1
                    if shift>0:
                        board[i][j-shift] = board[i][j]
                        board[i][j] = 0
                    if j-shift-1>=0 and board[i][j-shift-1]==board[i][j-shift] and not merged[i][j-shift-1]:
                        board[i][j-shift-1] *= 2
                        score += board[i][j-shift-1]
                        board[i][j-shift] = 0
                        merged[i][j-shift-1] = True
    elif direc=='RIGHT':
        for i in range(4):
            for j in reversed(range(4)):
                shift = 0
                if j<3:
                    for q in range(j+1, 4):
                        if board[i][q]==0:
                            shift += 1
                    if shift>0:
                        board[i][j+shift] = board[i][j]
                        board[i][j] = 0
                    if j+shift+1<=3 and board[i][j+shift+1]==board[i][j+shift] and not merged[i][j+shift+1]:
                        board[i][j+shift+1] *= 2
                        score += board[i][j+shift+1]
                        board[i][j+shift] = 0
                        merged[i][j+shift+1] = True
    
    return board

# detect if no move available => game over
def is_game_over(board):
    for i in range(4):
        for j in range(4):
            for r, c in [(i+1, j), (i, j+1)]:
                if 0<=r<4 and 0<=c<4:
                    if board[i][j]==board[r][c] or board[r][c]==0 or board[i][j]==0:
                        return False
    return True

# spawn in new pieces randomly when turns start
def new_pieces(board):
    cnt_new_tiles = 0

    while any(0 in row for row in board) and cnt_new_tiles<2:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col]==0:
            cnt_new_tiles += 1
            if random.randint(1, 10)==10:
                board[row][col] = 4
            else:
                board[row][col] = 2

    return board, is_game_over(board)

# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value>8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value<=2048:
                color_tile = colors[value]
            else:
                color_tile = colors['other']
            pygame.draw.rect(screen, color_tile, [j*95 + 20, i*95 + 20, 75, 75], 0, 5)
            if value>0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5*value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j*95 + 57, i*95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j*95 + 20, i*95 + 20, 75, 75], 2, 5)

# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')

    draw_board()
    draw_pieces(board_values)
    
    if spawn_new:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
    
    if direction!='':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    
    if game_over:
        draw_over()
        if high_score>init_high:
            file_high_score = open('high_score.txt', 'w')
            file_high_score.write(f'{high_score}')
            file_high_score.close()
            init_high = high_score
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False    

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_UP:
                direction = 'UP'
            elif event.key==pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key==pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key==pygame.K_RIGHT:
                direction = 'RIGHT'
            
            if game_over:
                if event.key==pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    score = 0
                    direction = ''
                    game_over = True

    if score>high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()