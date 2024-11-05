import pygame
import logging
import copy

#first find pos of king
#then check if that square is being attacked
#if it is then its check
#if its not then do nothing
#if it is, check if it is checkmate
#done by checking if any of the moves that you make stop the king from being attacked


#functions and their names to remember

#tells us if the user is in check
def isCheck(board, curr_colour):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                pass
            else:
                if abs(board[i][j].type) == 5 and board[i][j].color == curr_colour:
                    x = j
                    y = i
                    #logging.debug([x,y])

    if curr_colour == 'white':
        curr_colour2 = 'black'
    elif curr_colour == 'black':
        curr_colour2 = 'white'

    for a in range(len(board)):
        for b in range(len(board[a])):
            if board[a][b] == 0:
                pass
            else:
                if board[a][b].color != curr_colour:

                    if board[a][b].CheckMove(x,y,curr_colour2,board):
                        #logging.debug('dfgfdgfd')
                        return True

    return False

def Valid_Moves(board, curr_colour):
    board_copy = copy.deepcopy(board)
    list_of_moves = []
    for i in range(len(board_copy)):
        for j in range(len(board_copy[i])):
            if board_copy[i][j] == 0:
                pass
            else:
                if board_copy[i][j].color == curr_colour:
                    for a in range(len(board_copy)):
                        for b in range(len(board_copy[a])):
                            if board_copy[i][j].CheckMove(b,a,curr_colour,board_copy):
                                board_copy[a][b] = board[i][j]
                                board_copy[i][j] = 0


                                if not isCheck(board_copy,curr_colour):
                                #b a is final position j i is starting position
                                    list_of_moves.append([b,a,j,i])
                                board_copy = copy.deepcopy(board)

    logging.debug(list_of_moves)
    return list_of_moves


#0 empty 1 white pawn 2 white knight 3 white bishop 4 white queen 5 white king 6 white rook -num for black pieces
class ChessPieces:
    def __init__(self, piecetype,x,y):#piecetype is the number that corresponds to the piece
        self.x = x
        self.y = y
        if piecetype < 0:
            self.color = 'black'
        else:
            self.color = 'white'
        self.type = piecetype

    def CheckMove(self,x,y,curr_colour,board):
        change_in_x = x-self.x
        change_in_y = y-self.y
        mod_diff = change_in_y*change_in_y + change_in_x*change_in_x
        #logging.debug([self.x,x,self.y,y])
        if change_in_x == 0 and change_in_y == 0:
            return False
        if curr_colour != self.color:
            return False
        #validating white pawn moves
        if self.type == 1:
            if change_in_x == 0 and change_in_y == -1 and board[y][x] == 0: #and change_in_y == -1:
                if y == 0:
                    self.type = 4
                return True
            if self.y == 6 and change_in_x == 0 and change_in_y == -2 and board[y][x] == 0 and board[y+1][x] == 0:
                if y == 0:
                    self.type = 4
                return True
            if abs(change_in_x) == 1 and change_in_y == -1 and board[y][x] != 0: #and change_in_y == -1:
                if self.color != board[y][x].color:#and change_in_y == -1:
                    if y == 0:
                        self.type = 4
                    return True

        #validating black pawn moves
        elif self.type == -1:
            if change_in_x == 0 and change_in_y == 1 and board[y][x] == 0:
                if y == 7:
                    self.type = -4
                return True
            if self.y == 1 and change_in_x == 0 and change_in_y == 2 and board[y][x] == 0 and board[y-1][x] == 0:
                if y == 7:
                    self.type = -4
                return True
            if abs(change_in_x) == 1 and change_in_y == 1 and board[y][x] != 0:
                if self.color != board[y][x].color:#and change_in_y == -1:
                    if y == 7:
                        self.type = -4
                    return True

        type = abs(self.type)
        #validating knights
        if type == 2:
            if mod_diff == 5 and board[y][x] == 0:
                return True
            if mod_diff == 5 and board[y][x].color != self.color:
                return True
        #validating bishop
        if type == 3:
            if abs(change_in_x) == abs(change_in_y):
                stepx = 1
                stepy = 1
                if change_in_x > 0:
                    stepx = -1
                if change_in_y > 0:
                    stepy = -1
                if abs(change_in_x) != 1:
                    loop = abs(change_in_x)
                    #checking every piece between the bishop and the move
                    for a in range(1,loop):
                        if board[y+(a*stepy)][x+(a*stepx)] != 0:
                            return False
                if board[y][x] != 0:
                    if board[y][x].color == self.color:
                        return False
                return True
        #validating queen
        if type == 4:
            if board[y][x] != 0:
                if board[y][x].color == self.color:
                    return False
            if abs(change_in_x) == abs(change_in_y):
                flag = True
                stepx = 1
                stepy = 1
                if change_in_x > 0:
                    stepx = -1
                if change_in_y > 0:
                    stepy = -1
                if abs(change_in_x) != 1:
                    loop = abs(change_in_x)
                    for a in range(1,loop):
                        if board[y+(a*stepy)][x+(a*stepx)] != 0:
                            return False
                return True

            if change_in_x == 0 or change_in_y == 0:
                step = 1
                if change_in_x != 0:
                    if change_in_x > 0:
                        step = -1
                    for a in range(1, abs(change_in_x)):
                        if board[y][x+(a*step)] != 0:
                            return False


                elif change_in_y != 0:
                    if change_in_y > 0:
                        step = -1
                    for a in range(1, abs(change_in_y)):
                        if board[y+(a*step)][x] != 0:
                            return False
                return True



        #validating king
        if type == 5:
            if abs(change_in_x) < 2 and abs(change_in_y) < 2:
                if board[y][x] != 0:
                    if board[y][x].color == self.color:
                        return False
                return True



        #validating rook
        if type == 6:
            if change_in_x == 0 or change_in_y == 0:
                step = 1
                if change_in_x != 0:
                    if change_in_x > 0:
                        step = -1
                    for a in range(1, abs(change_in_x)):
                        if board[y][x+(a*step)] != 0:
                            return False

                elif change_in_y != 0:
                    if change_in_y > 0:
                        step = -1
                    for a in range(1, abs(change_in_y)):
                        if board[y+(a*step)][x] != 0:
                            return False

                if board[y][x] != 0:
                    if board[y][x].color == self.color:
                        return False
                return True
        return False
