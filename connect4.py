#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import time
import random

board = []
plain_board = [] #Same board without piece coloring. Used for win checking.
whos_turn = 0b10
winner = False
draw_counter = 0
column = 0
boardheight = 6
boardwidth = 7

#ANSI Color Globals
#Should probably do this with a Python library that is more universal as ANSI doesn't work the same on all terminals.
class colors:
	RESET = "\033[0m"
	RED = "\033[1;31;40m"
	YELLOW = "\033[1;33;40m"

#generate empty board
def generate_board(board, boardheight, boardwidth):
	label = []
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
	print ("Let's play Connect Four!")

def print_board(board):
	print("\n")
	for row in board:
		print(" ".join(row))
	print("\n")
		
def toggle(old_turn):
	mask = 0b11
	new_turn = old_turn ^ mask
	print("It is player %s's turn." % new_turn)
	return new_turn

def mark_board(column):
	row = None
	for i in range(5, -1, -1):
		if board[i][column] == "_":
			row = i
			break
		if i == 0:
			if whos_turn == 0b01: 
				print("That column is full!")
			play()
			return
	
	if whos_turn == 0b01:
		board[row][column] = colors.RED + "1" + colors.RESET
		plain_board[row][column] = "1"
	else:
		board[row][column] = colors.YELLOW + "2" + colors.RESET
		plain_board[row][column] = "2"
	print_board(board)

def play():
	if whos_turn == 0b01:
		column = int(input("Pick a column (1-7): ")) - 1
		if column >= 0 and column <= boardwidth:
			mark_board(column)
		else:
			print("You picked a column outside the board!")
			play()
	else:
		column = random.randint(0,6)
		mark_board(column)

def ai():
	

def check_winner(board, player):
	#check horizontal spaces
	for y in range(boardheight):
		for x in range(boardwidth - 3):
			if board[y][x] == player and board[y][x+1] == player and board[y][x+2] == player and board[y][x+3] == player:
				return True

	#check vertical spaces
	for x in range(boardwidth):
		for y in range(boardheight - 3):
			if board[y][x] == player and board[y+1][x] == player and board[y+2][x] == player and board[y+3][x] == player:
				return True

	#check / diagonal spaces
	for x in range(boardwidth - 3):
		for y in range(3, boardheight):
			if board[y][x] == player and board[y-1][x+1] == player and board[y-2][x+2] == player and board[y-3][x+3] == player:
				return True

	#check \ diagonal spaces
	for x in range(boardwidth - 3):
		for y in range(boardheight - 3):
			if board[y][x] == player and board[y+1][x+1] == player and board[y+2][x+2] == player and board[y+3][x+3] == player:
				return True

	return False
	
start()
generate_board(board, boardheight, boardwidth)
generate_board(plain_board, boardheight, boardwidth)
print_board(board)

while winner == False and draw_counter != 42:
	whos_turn = toggle(whos_turn)
	play()
	draw_counter += 1
	winner = check_winner(plain_board, str(whos_turn))

if winner == True:
	print("Player " + str(whos_turn) + " wins!")

else:
	print("The game is a draw")






