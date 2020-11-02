#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import numpy as np
import time
import random
import conn4ai

ROWS = 12
COLS = 13
VISIBLE_ROWS = 6
VISIBLE_COLS = 7
LEGAL_ROWS = [3, 4, 5, 6, 7, 8]
LEGAL_COLS = [3, 4, 5, 6, 7, 8, 9]

turn = 0b10
winner = False
draw_counter = 0

class colors:
	"""
	ANSI Color Globals
	TODO: do this with ai Python library that is more universal than ANSI.
	"""
	RESET = "\033[0m"
	RED = "\033[1;31;40m"
	YELLOW = "\033[1;33;40m"

def generate_board():
	"""
	Creation of the game board as a 2D NumPy array
	0 = empty square
	1 = player 1
	2 = player 2
	3 = square that is not a legal move square but exists for computational reason
	"""
	board = np.zeros((ROWS, COLS), dtype=int)
	for j in range(COLS):	
		for i in range(ROWS):
			if i < 3 or i > 8:
				board[i, j] = 3
			elif j < 3 or j > 9:
				board[i, j] = 3
	return board

def make_printable_board(board):
	printable_board = []

	for i in range(8):
		printable_board.append([])

	for i in LEGAL_ROWS:
		for j in LEGAL_COLS:
			element = None

			if board[i][j] == 0:
				element = "_"
			elif board[i][j] == 1:
				element = colors.RED + "1" + colors.RESET
			elif board[i][j] == 2:
				element = colors.YELLOW + "2" + colors.RESET

			printable_board[i - 3].append(element)
	
	for i in LEGAL_COLS:
		printable_board[6].append("^")
		printable_board[7].append(str(i - 2))
	
	return printable_board

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

def mark_board(board, column):
	row = None
	for i in reversed(LEGAL_ROWS):
		if board[i][column] == 0:
			row = i
			break
		if i == 3:
			if turn == 0b01: 
				print("That column is full!")
			play(board)
			return
	
	if turn == 0b01:
		board[row][column] = 1
	else:
		board[row][column] = 2
	
	print_board(make_printable_board(board))

def play(board):
	if turn == 0b01:
		column = int(input("Pick a column (1-7): ")) + 3
		if column in LEGAL_COLS:
			mark_board(board, column)
		else:
			print("You picked a column outside the board!")
			play(board)
	else:
		ai_move(2, board, turn)	
		mark_board(board, column)

def check_winner(board, player):
	#check horizontal spaces
	for y in range(LEGAL_ROWS):
		for x in range(LEGAL_COLS - 3):
			if board[y][x] == player and board[y][x+1] == player and board[y][x+2] == player and board[y][x+3] == player:
				return True

	#check vertical spaces
	for x in range(LEGAL_COLS):
		for y in range(LEGAL_ROWS - 3):
			if board[y][x] == player and board[y+1][x] == player and board[y+2][x] == player and board[y+3][x] == player:
				return True

	#check / diagonal spaces
	for x in range(LEGAL_COLS - 3):
		for y in range(3, LEGAL_ROWS):
			if board[y][x] == player and board[y-1][x+1] == player and board[y-2][x+2] == player and board[y-3][x+3] == player:
				return True

	#check \ diagonal spaces
	for x in range(LEGAL_COLS - 3):
		for y in range(LEGAL_ROWS - 3):
			if board[y][x] == player and board[y+1][x+1] == player and board[y+2][x+2] == player and board[y+3][x+3] == player:
				return True

	return False
	
board = generate_board()
print_board(make_printable_board(board))

while winner == False and draw_counter != 42:
	turn = toggle(turn)
	play(board)
	draw_counter += 1
	winner = check_winner(board, str(turn))

if winner == True:
	print("Player " + str(turn) + " wins!")

else:
	print("The game is a draw")






