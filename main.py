from Chesspieces import ChessPieces, isCheck, Valid_Moves
from AI import minimax
import pygame, sys
from pygame.locals import QUIT
import logging
logging.basicConfig(level = 'DEBUG')
import time
import random
import copy

pygame.init()
pygame.mouse.set_cursor(*pygame.cursors.arrow)
screen = pygame.display.set_mode((1080, 900))
screen.fill((255,0,0))



# setting up graphics
board_graphics = pygame.image.load('Board.png')
board_graphics = pygame.transform.scale(board_graphics, (600,600))
BlackBishop = pygame.image.load('black bishop.png')
BlackBishop = pygame.transform.scale(BlackBishop, (60,60))
WhiteBishop = pygame.image.load('white bishop.png')
WhiteBishop = pygame.transform.scale(WhiteBishop, (60,60))
BlackPawn = pygame.image.load('black pawn.png')
BlackPawn = pygame.transform.scale(BlackPawn, (60,60))
WhitePawn = pygame.image.load('white pawn.png')
WhitePawn = pygame.transform.scale(WhitePawn, (60,60))
WhiteKnight = pygame.image.load('white knight.png')
WhiteKnight = pygame.transform.scale(WhiteKnight, (60,60))
BlackKnight = pygame.image.load('black knight.png')
BlackKnight = pygame.transform.scale(BlackKnight, (60,60))
WhiteQueen = pygame.image.load('white queen.png')
WhiteQueen = pygame.transform.scale(WhiteQueen, (60,60))
BlackQueen = pygame.image.load('black queen.png')
BlackQueen = pygame.transform.scale(BlackQueen, (60,60))
WhiteKing = pygame.image.load('white king.png')
WhiteKing = pygame.transform.scale(WhiteKing, (60,60))
BlackKing = pygame.image.load('black king.png')
BlackKing = pygame.transform.scale(BlackKing, (60,60))
BlackRook = pygame.image.load('black rook.png')
BlackRook = pygame.transform.scale(BlackRook, (60,60))
WhiteRook = pygame.image.load('white rook.png')
WhiteRook = pygame.transform.scale(WhiteRook, (60,60))
Menu_Graphics = pygame.image.load('Menu.png')
Menu_Graphics = pygame.transform.scale(Menu_Graphics, (600,600))



#0 empty 1 white pawn 2 white knight 3 white bishop 4 white queen 5 white king 6 white rook -num for black pieces
def Generate_Board():
    board = [[0 for i in range(8)] for j in range(8)]
    board[0] = [-6,-2,-3,-4,-5,-3,-2,-6]
    board[1] = [-1, -1, -1, -1, -1, -1, -1, -1]
    board[7] = [6,2,3,4,5,3,2,6]
    board[6] = [1, 1, 1, 1, 1, 1, 1, 1]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                board[i][j] = ChessPieces(board[i][j],j,i)

    return board

board = Generate_Board()
#logging.debug(board)

font = pygame.font.Font('freesansbold.ttf', 22)
Overfont = pygame.font.Font('freesansbold.ttf', 60)
blackplayer = font.render('black',True , (0,0,0))
whiteplayer = font.render('white',True , (0,0,0))
whitewin = Overfont.render('White wins', True, (0,0,0))
blackwin = Overfont.render('Black wins', True, (0,0,0))
draw = Overfont.render('draw', True, (0,0,0))
def blitboard():
    screen.blit(blackplayer, (240,125))
    screen.blit(whiteplayer,(240,750))
    screen.blit(board_graphics, (240,150))
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                pass
            elif board[i][j].type == 1:
                screen.blit(WhitePawn, (240+75*j,150+75*i))
            elif board[i][j].type == 2:
                screen.blit(WhiteKnight, (240+75*j,150+75*i))
            elif board[i][j].type == 3:
                screen.blit(WhiteBishop, (240+75*j,150+75*i))
            elif board[i][j].type == 4:
                screen.blit(WhiteQueen, (240+75*j,150+75*i))
            elif board[i][j].type == 5:
                screen.blit(WhiteKing, (240+75*j,150+75*i))
            elif board[i][j].type == 6:
                screen.blit(WhiteRook, (240+75*j,150+75*i))
            elif board[i][j].type == -1:
                screen.blit(BlackPawn, (240+75*j,150+75*i))
            elif board[i][j].type == -2:
                screen.blit(BlackKnight, (240+75*j,150+75*i))
            elif board[i][j].type == -3:
                screen.blit(BlackBishop, (240+75*j,150+75*i))
            elif board[i][j].type == -4:
                screen.blit(BlackQueen, (240+75*j,150+75*i))
            elif board[i][j].type == -5:
                screen.blit(BlackKing, (240+75*j,150+75*i))
            elif board[i][j].type == -6:
                screen.blit(BlackRook, (240+75*j,150+75*i))




def Game_Selector(pos):
    if pos[0] > 350 and pos[0] < 750:
        if pos[1] > 260 and pos[1] < 360:
            return 2
        elif pos[1] > 380 and pos[1] < 500:
            return 1
        elif pos[1] > 400 and pos[1] < 540:
            return 3
    return 0



Game_State = 0 #game state 0 is menu 1 is 2 player game 2 is one player game 3 is zero player game
Valid_Num = [0,1,2,3,4,5,6,7]
selected = False
curr_colour = 'white'
comp_turn = 'black'

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #get position of click
            pos = pygame.mouse.get_pos()
            #logging.debug(pos)
            if Game_State == 1 or (Game_State == 2 and comp_turn != curr_colour):
                x = (pos[0]-240)//75
                y = (pos[1]-150)//75
                #logging.debug([x,y])
                if selected == False:
                    if x in Valid_Num and y in Valid_Num and board[y][x] != 0:
                        Selected_Piece = board[y][x]
                        selected = True
                        #logging.debug('selected')
                        xprev = x
                        yprev = y
                        time.sleep(0.2)
                elif selected == True:
                    #Add a validity check


                    #logging.debug(isCheck(board,curr_colour))
                    valid = board[yprev][xprev].CheckMove(x, y, curr_colour, board)
                    logging.debug(valid)
                    if valid:
                        backup = board[y][x]
                        board[y][x] = Selected_Piece
                        board[yprev][xprev] = 0
                        Selected_Piece.x = x
                        Selected_Piece.y = y
                        if isCheck(board,curr_colour):
                            board[yprev][xprev] = Selected_Piece
                            board[y][x] = backup
                            Selected_Piece.x = xprev
                            Selected_Piece.y = yprev
                        else:
                            if curr_colour == 'white':
                                curr_colour = 'black'
                            elif curr_colour == 'black':
                                curr_colour = 'white'

                        list_of_moves = Valid_Moves(board,curr_colour)
                        if len(list_of_moves) == 0:
                            if isCheck(board,curr_colour):
                                if curr_colour == 'white':
                                    blitboard()
                                    screen.blit(blackwin, (450,450))
                                    pygame.display.update()
                                    time.sleep(10)
                                    Game_State = 0
                                    screen.fill((255, 0, 0))
                                if curr_colour == 'black':
                                    blitboard()
                                    screen.blit(whitewin, (450, 450))
                                    pygame.display.update()
                                    time.sleep(10)
                                    Game_State = 0
                                    screen.fill((255, 0, 0))

                            else:
                                blitboard()
                                screen.blit(draw, (450, 450))
                                pygame.display.update()
                                time.sleep(10)
                                Game_State = 0
                                screen.fill((255, 0, 0))
                        if Game_State == 2:
                            blitboard()
                            pygame.display.update()

                    selected = False

            if Game_State == 0:
                logging.debug(pos)
                Game_State = Game_Selector(pos)
                if Game_State != 0:
                    screen.fill((255,0,0))
                    selected = False
                    curr_colour = 'white'
                    comp_turn = 'black'
                    board = Generate_Board()




                    #logging.debug('released')
    if Game_State == 3 or (Game_State == 2 and comp_turn == curr_colour):
        list_of_moves = Valid_Moves(board, curr_colour)
        if len(list_of_moves) != 0:
            num = random.randint(0,len(list_of_moves)-1)
            move_selected = list_of_moves[num]
            board[move_selected[1]][move_selected[0]] = board[move_selected[3]][move_selected[2]]
            board[move_selected[3]][move_selected[2]] = 0
            board[move_selected[1]][move_selected[0]].y = move_selected[1]
            board[move_selected[1]][move_selected[0]].x = move_selected[0]
            time.sleep(2)
            if curr_colour == 'white':
                curr_colour = 'black'
            elif curr_colour == 'black':
                curr_colour = 'white'
        elif len(list_of_moves) == 0:
            if isCheck(board, curr_colour):
                if curr_colour == 'white':
                    blitboard()
                    screen.blit(blackwin, (450, 450))
                    pygame.display.update()
                    time.sleep(10)
                    Game_State = 0
                if curr_colour == 'black':
                    blitboard()
                    screen.blit(whitewin, (450, 450))
                    pygame.display.update()
                    time.sleep(10)
                    Game_State = 0


        # b a is final position j i is starting position





    if Game_State == 1 or Game_State == 2 or Game_State == 3:
        blitboard()
    if Game_State == 0:
        screen.blit(Menu_Graphics, (250, 100))
    pygame.display.update()



