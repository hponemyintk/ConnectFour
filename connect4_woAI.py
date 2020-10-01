import numpy as np
import pygame
import pygame.gfxdraw
import sys
import math

Row_ct = 6          # capitalize as global/static variable
Col_ct = 7
BLACK = (255,255,255)       # white
BLUE = (121,121,121)        # STEEL
RED = (234,52,51)           # RED
YELLOW = (65,30,255)             # BLue
PURE_BLACK = (0,0,0)        # black
def make_board():
    board = np.zeros((Row_ct,Col_ct))
    return board


def check_tile_status(board,col):
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
            if board[rr][cc] ==1:
                pygame.gfxdraw.aacircle(screen, int(cc*Square_len+Square_len/2), height-int(rr*Square_len+Square_len/2), radius, RED)
                pygame.gfxdraw.filled_circle(screen, int(cc*Square_len+Square_len/2), height-int(rr*Square_len+Square_len/2), radius, RED)
            elif board[rr][cc] == 2:
                pygame.gfxdraw.aacircle(screen, int(cc*Square_len+Square_len/2), height-int(rr*Square_len+Square_len/2), radius, YELLOW)
                pygame.gfxdraw.filled_circle(screen, int(cc*Square_len+Square_len/2), height-int(rr*Square_len+Square_len/2), radius, YELLOW)

    pygame.display.update()

board = make_board()
print(board)
game_over = False
turn = 0

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
pygame.display.update()
gfont = pygame.font.SysFont("Helvatica",60)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0,width, Square_len))
            posx = event.pos[0]
            if turn == 0:
                pygame.gfxdraw.aacircle(screen,posx, int(Square_len/2), radius, RED)
                pygame.gfxdraw.filled_circle(screen,posx, int(Square_len/2), radius, RED)
            else:
                pygame.gfxdraw.aacircle(screen,posx, int(Square_len/2), radius, YELLOW)
                pygame.gfxdraw.filled_circle(screen,posx, int(Square_len/2), radius, YELLOW)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            # Ask for player 1 input
            if turn ==0:
                posx = event.pos[0]
                col =  int(math.floor(posx/Square_len))

                if check_tile_status(board,col):
                    row = get_free_row(board,col)
                    fill_tile(board,row,col,1)
                    if end_cases(board, 1):
                        label = gfont.render("Red Wins! Drum Roll Please!!!", 1, PURE_BLACK)
                        screen.blit(label,(48,30))
                        game_over = True
                        # break


            # Ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/Square_len))

                if check_tile_status(board,col):
                    row = get_free_row(board,col)
                    fill_tile(board,row,col,2)
                    if end_cases(board, 2):
                        label = gfont.render("Blue Wins! Drum Roll Please!!!", 2, PURE_BLACK)
                        screen.blit(label,(43,30))
                        game_over = True
                        # break

            print_game_state(board)
            draw_cur_state(board)

            turn += 1
            turn = turn % 2

pygame.display.update()
# pygame.event.pump()         # to allow os to still interact with pygame
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
