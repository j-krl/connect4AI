#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import time
import random

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
			print("That column is full!")
			play()
			return
	
	if whos_turn == 0b01:
		board[row][column] = "1"
	else:
		board[row][column] = "2"
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
generate_board(boardheight, boardwidth)
print_board(board)

while winner == False:
	whos_turn = toggle(whos_turn)
	play()
	winner = check_winner(board, str(whos_turn))
	
if winner == True:
	print("Player " + str(whos_turn) + " wins!")







