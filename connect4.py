#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import time

board = [] 
label = []
whos_turn = 0b10
winner = False
last = 0
column = 0
boardheight = 6
boardwidth = 7

#generate empty board
def generate_board(boardheight, boardwidth):
    for i in range(8):
        if i < boardheight:
            board.append(["_"] * boardwidth)
        elif i < boardwidth:
            board.append(["^"] * boardwidth)
        else:
            for j in range(boardwidth):
                label.append(str(j+1))
            board.append(label)

def start():
    print "Let's play Connect Four!"
    start_seq = ["3",".",".","2",".",".","1",".","."]
    for i in start_seq:
        time.sleep(0.333)
        print i,

def print_board(board):
    print "\n"
    for row in board:
        print " ".join(row)
    print "\n"
        
def toggle(turn):
    mask = 0b11
    turn = turn ^ mask
    print "It is player %s's turn." % turn
    return turn

def mark_board(last, column):
    if whos_turn == 0b01:
        board[last][column] = "1"
    else:
        board[last][column] = "2"
    print_board(board)

def play():
    while True:
        try:
            column = int(input("Pick a column (1-7): ")) - 1
            if column >= 0 and column <= boardwidth:
                for i in range(6):
                    if board[i][column] == "_":
                        last = i
                mark_board(last, column)
            else:
                raise "You picked a column outside the board!"
            break
        except:
            print("Not a valid number! Please try again...")

def check_winner(board, player):
    #check horizontal spaces
    for y in range(boardheight):
        for x in range(boardwidth - 3):
            if board[x][y] == player and board[x+1][y] == player and board[x+2][y] == player and board[x+3][y] == player:
                return True

    #check vertical spaces
    for x in range(boardwidth):
        for y in range(boardheight - 3):
            if board[x][y] == player and board[x][y+1] == player and board[x][y+2] == player and board[x][y+3] == player:
                return True

    #check / diagonal spaces
    for x in range(boardwidth - 3):
        for y in range(3, boardheight):
            if board[x][y] == player and board[x+1][y-1] == player and board[x+2][y-2] == player and board[x+3][y-3] == player:
                return True

    #check \ diagonal spaces
    for x in range(boardwidth - 3):
        for y in range(boardheight - 3):
            if board[x][y] == player and board[x+1][y+1] == player and board[x+2][y+2] == player and board[x+3][y+3] == player:
                return True

    return False
    
start()
generate_board(boardheight, boardwidth)
print_board(board)

while winner == False:
    whos_turn = toggle(whos_turn)
    play()
    winner = check_winner(board, str(whos_turn))
    
if winner == True:
    print "Player " + str(whos_turn) + " wins!"







