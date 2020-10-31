#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import numpy as np
import time
import random

turn = 0b10
winner = False
draw_counter = 0

class colors:
	"""
	ANSI Color Globals
	Should probably do this with a Python library that is more universal as ANSI doesn't work the same on all terminals.
	"""
	RESET = "\033[0m"
	RED = "\033[1;31;40m"
	YELLOW = "\033[1;33;40m"

#def generate_board(HEIGHT, WIDTH):
#	label = []
#	board = []
#	for i in range(8):
#		if i < HEIGHT:
#			board.append(["_"] * WIDTH)
#		elif i < WIDTH:
#			board.append(["^"] * WIDTH)
#		else:
#			for j in range(WIDTH):
#				label.append(str(j+1))
#			board.append(label)
#	return board

def generate_board()
	"""
	Creation of the game board as a 2D NumPy array
	0 = empty square
	1 = player 1
	2 = player 2
	3 = square that is not a legal move square but exists for computational reason
	4 = current legal move
	"""
	ROWS = 12
	COLUMNS = 13
	board = np.zeros((ROWS, COLUMNS), dtype=int)
	for j in range(COLUMNS):	
		for i in range(ROWS):
			if i < 3 or i > 8:
				board[i, j] = 3
			elif j < 3 or j > 9:
				board[i, j] = 3
	return board

# if you do the conversion here you won't need plain_board and board
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

def mark_board(board, plain_board, column):
	row = None
	for i in range(5, -1, -1):
		if board[i][column] == "_":
			row = i
			break
		if i == 0:
			if turn == 0b01: 
				print("That column is full!")
			play(board, plain_board)
			return
	
	if turn == 0b01:
		board[row][column] = colors.RED + "1" + colors.RESET
		plain_board[row][column] = "1"
	else:
		board[row][column] = colors.YELLOW + "2" + colors.RESET
		plain_board[row][column] = "2"
	print_board(board)

def play(board, plain_board):
	if turn == 0b01:
		column = int(input("Pick a column (1-7): ")) - 1
		if column >= 0 and column <= WIDTH:
			mark_board(board, plain_board, column)
		else:
			print("You picked a column outside the board!")
			play(board, plain_board)
	else:
		column = random.randint(0,6)
		mark_board(board, plain_board, column)

def check_winner(board, player):
	#check horizontal spaces
	for y in range(HEIGHT):
		for x in range(WIDTH - 3):
			if board[y][x] == player and board[y][x+1] == player and board[y][x+2] == player and board[y][x+3] == player:
				return True

	#check vertical spaces
	for x in range(WIDTH):
		for y in range(HEIGHT - 3):
			if board[y][x] == player and board[y+1][x] == player and board[y+2][x] == player and board[y+3][x] == player:
				return True

	#check / diagonal spaces
	for x in range(WIDTH - 3):
		for y in range(3, HEIGHT):
			if board[y][x] == player and board[y-1][x+1] == player and board[y-2][x+2] == player and board[y-3][x+3] == player:
				return True

	#check \ diagonal spaces
	for x in range(WIDTH - 3):
		for y in range(HEIGHT - 3):
			if board[y][x] == player and board[y+1][x+1] == player and board[y+2][x+2] == player and board[y+3][x+3] == player:
				return True

	return False
	
start()
board = generate_board(HEIGHT, WIDTH)
plain_board = generate_board(HEIGHT, WIDTH)
print_board(board)

while winner == False and draw_counter != 42:
	turn = toggle(turn)
	play(board, plain_board)
	draw_counter += 1
	winner = check_winner(plain_board, str(turn))

if winner == True:
	print("Player " + str(turn) + " wins!")

else:
	print("The game is a draw")






