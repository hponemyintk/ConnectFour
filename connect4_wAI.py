import numpy as np
import random
import pygame
import pygame.gfxdraw
import sys
import math

Row_ct = 6          # capitalize as global/static variable
Col_ct = 7

PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY_PIECE = 0

WINDOW_LENGTH = 4

# Colors
BLACK = (255,255,255)       # white
BLUE = (121,121,121)        # STEEL
RED = (234,52,51)           # RED
YELLOW = (65,30,255)        # BLue
PURE_BLACK = (0,0,0)        # black

def make_board():
    board = np.zeros((Row_ct,Col_ct))
    return board


def check_tile_status(board, col):
    return board[5][col] ==0


def get_free_row(board,col):
    for r in range(Row_ct):
        if board[r][col] == 0:
            return r

def fill_tile(board, row, col, piece):
    board[row][col] = piece



def end_cases(board,piece):
    # check horizontal locations for win
    for cc in range(Col_ct-3):
        for rr in range(Row_ct):
            if board[rr][cc] == piece and board[rr][cc+1] == piece and board[rr][cc+2] == piece and board[rr][cc+3] == piece:
                return True

    # check vertical locations for win
    for cc in range(Col_ct):
        for rr in range(Row_ct-3):
            if board[rr][cc] == piece and board[rr+1][cc] == piece and board[rr+2][cc] == piece and board[rr+3][cc] == piece:
                return True

    # check positive slope locations for win
    for cc in range(Col_ct-3):
        for rr in range(Row_ct-3):
            if board[rr][cc] == piece and board[rr+1][cc+1] == piece and board[rr+2][cc+2] == piece and board[rr+3][cc+3] == piece:
                return True

    # check negative slope locations for win
    for cc in range(Col_ct-3):
        for rr in range(3,Row_ct):
            if board[rr][cc] == piece and board[rr-1][cc+1] == piece and board[rr-2][cc+2] == piece and board[rr-3][cc+3] == piece:
                return True

def print_game_state(board):
    print(np.flip(board,axis=0))


def draw_cur_state(board):
    # draw rectangles and empty circles
    for cc in range(Col_ct):
        for rr in range(Row_ct):
            pygame.draw.rect(screen, BLUE, (cc*Square_len, rr*Square_len+Square_len, Square_len, Square_len))          # exclude the topmost row in the gird
            pygame.gfxdraw.aacircle(screen, int(cc*Square_len+Square_len/2), int(rr*Square_len+Square_len+Square_len/2), radius, BLACK) 
            pygame.gfxdraw.filled_circle(screen, int(cc*Square_len+Square_len/2), int(rr*Square_len+Square_len+Square_len/2), radius, BLACK) 

    # draw player 1 & 2's pieces
    for cc in range(Col_ct):
        for rr in range(Row_ct):
            if board[rr][cc] ==PLAYER_PIECE:
                pygame.gfxdraw.aacircle(screen, int(cc*Square_len+Square_len/2), height-int(rr*Square_len+Square_len/2), radius, RED)
                pygame.gfxdraw.filled_circle(screen, int(cc*Square_len+Square_len/2), height-int(rr*Square_len+Square_len/2), radius, RED)
            elif board[rr][cc] == AI_PIECE:
                pygame.gfxdraw.aacircle(screen, int(cc*Square_len+Square_len/2), height-int(rr*Square_len+Square_len/2), radius, YELLOW)
                pygame.gfxdraw.filled_circle(screen, int(cc*Square_len+Square_len/2), height-int(rr*Square_len+Square_len/2), radius, YELLOW)

    pygame.display.update()


def evaluate_window(window, piece):
    # for minimax 
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY_PIECE) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score -=4
    return score


def score_position(board, piece):
    score= 0

    # Score center column
    center_array = [int(i) for i in list(board[:, Col_ct//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # score horizontal
    for rr in range(Row_ct):
        row_array = [int(i) for i in list(board[rr,:])]
        for cc in range(Col_ct-3):
            window = row_array[cc:cc+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # score vertical
    for cc in range(Col_ct):
        col_array = [int(i) for i in list(board[:,cc])]
        for rr in range(Row_ct-3):
            window = col_array[rr:rr+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # positive slope
    for rr in range(Row_ct-3):
        for cc in range(Col_ct-3):
            window = [int(board[rr+i,cc+i]) for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # negative slope
    for rr in range(3, Row_ct):
        for cc in range(Col_ct-3):
            window = [int(board[rr-i,cc+i]) for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score


def is_terminal_node(board):
    return end_cases(board, PLAYER_PIECE) or end_cases(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if end_cases(board, AI_PIECE):
                return (None, 1e9)
            elif end_cases(board, PLAYER_PIECE):
                return (None, -1e9)
            else:           # No more valid moves
                return (None, 0)
        else: # when depth is zero
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -np.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_free_row(board, col)
            b_copy = board.copy()
            fill_tile(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = np.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_free_row(board, col)
            b_copy = board.copy()
            fill_tile(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(Col_ct):
        if check_tile_status(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_free_row(board, col)
        temp_board = board.copy()
        fill_tile(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


board = make_board()
print(board)
game_over = False
turn = random.randint(PLAYER,AI)

#############################
### set up pygame for gui ###
#############################
pygame.init()

Square_len = 100
width = Col_ct * Square_len
height = (Row_ct+1) * Square_len
radius = int(Square_len/2-4)
size = (width,height)
screen = pygame.display.set_mode(size)
draw_cur_state(board)
gfont = pygame.font.SysFont("Helvatica",60)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0,width, Square_len))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.gfxdraw.aacircle(screen,posx, int(Square_len/2), radius, RED)
                pygame.gfxdraw.filled_circle(screen,posx, int(Square_len/2), radius, RED)
            pygame.display.update()

        # Ask for player input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn ==0:
                posx = event.pos[0]
                pygame.event.set_blocked(None)
                col =  int(math.floor(posx/Square_len))

                if check_tile_status(board,col):
                    row = get_free_row(board,col)
                    fill_tile(board,row,col,PLAYER_PIECE)
                    if end_cases(board, PLAYER_PIECE):
                        label = gfont.render("Red Wins! Drum Roll Please!!!", PLAYER_PIECE, PURE_BLACK)
                        screen.blit(label,(48,30))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print_game_state(board)
                    draw_cur_state(board)
                pygame.event.set_allowed(None)


    # Ask for player 2 input
    if turn == AI and not game_over:
        # col = random.randint(0,Col_ct-1)
        # col = pick_best_move(board,AI_PIECE)
        pygame.event.set_blocked(None)
        col, minimax_score = minimax(board, 5, -np.inf, np.inf, True)
        if check_tile_status(board,col):
            row = get_free_row(board,col)
            fill_tile(board,row,col,AI_PIECE)
            if end_cases(board, AI_PIECE):
                label = gfont.render("Blue Wins! Drum Roll Please!!!", AI_PIECE, PURE_BLACK)
                screen.blit(label,(43,30))
                game_over = True

            turn += 1
            turn = turn % 2
            # pygame.time.wait(300)
            pygame.event.set_allowed(None)
            print_game_state(board)
            draw_cur_state(board)

pygame.display.update()
# pygame.event.pump()         # to allow os to still interact with pygame
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
