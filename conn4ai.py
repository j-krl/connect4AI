import numpy as np

ROWS = 12
COLS = 13
LEGAL_ROWS = np.array([3, 4, 5, 6, 7, 8])
LEGAL_COLS = np.array([3, 4, 5, 6, 7, 8, 9])

def opp_player(player):
	# Accepts integer player and returns opposing player
	MASK = 0b11
	bin_player = bin(player)
	opp_player = MASK ^ bin_player
	return int(opp_player)

def open_check(board):
	# Returns a list of columns that can legally accept more pieces
	open_cols = []
	for i in LEGAL_COLS:
		for j in LEGAL_ROWS:
			if board[j, i] == 4:
				open_cols.append(j)
	return open_cols

def open_check_single(board, column):
	# Returns boolean for if a single column can accept more pieces
	for i in LEGAL_ROWS:
		if board[i, column] = 4:
			return [i, column]
	return False

def mark_board(board, player, column):
	if not open_check_single(board, column):
		raise IOError("AI attempting to mark a column that is already full")

	for i in LEGAL_ROWS:
		if board[i, column] == 4:
			board[i, column] = player
			if i != 3:
				board[i - 1, column] = 4

	return board

"""
Parameter info for AI functions:

square = a coordinate [ROW, COL] of the current legal move square being tested.
board[square[0], square[1]] will give you the value of that square.
adj_count = number of adjacent pieces being checked for on this particular call.
"""

def check_center(square):
	COL = square[1]
	if COL = 6:
		return 4
	else:
		return 0

def check_adjacent(board, square, player, adj_count):
	ROW = square[0]
	COL = square[1]
	opp_player = opp_player(player)
	count = 0
	zero_count = 0 # Number of legal empty squares encountered during a single pass
	ZERO_MAX = 4 - adj_count # Number of zeros allowed within adj_count parameter
	total = 0 # Cumulative score of position

	# Horizontal
	for	i in range(COL - 3, COL + 1):
		for j in range(4):
			if not board[ROW, i + j]:
				zero_count += 1
				if zero_count > ZERO_MAX
					count = 0
					break
			if board[ROW, i + j] in [opp_player, 3]:
				count = 0
				break
			count += 1
			if count == adj_count:
				if adj_count == 2:
					return 2
				if adj_count == 3:
					return 5
				if adj_count == 4:
					return 1000
	
	# Vertical
	for	i in range(COL - 3, COL + 1):
		for j in range(4):
			if not board[i + j, COL]: 
				zero_count += 1
				if zero_count > ZERO_MAX
					count = 0
					break
			if board[ROW, i + j] in [opp_player, 3]:
				count = 0
				break
			count += 1
			if count == adj_count:
				if adj_count == 2:
					return 2
				if adj_count == 3:
					return 5
				if adj_count == 4:
					return 1000

	# Diagonal /
	for	i in range(COL - 3, COL + 1):
		for j in range(4):
			if not board[ROW + i + j, COL - i + j]: 
				zero_count += 1
				if zero_count > ZERO_MAX
					count = 0
					break
			if board[ROW, i + j] in [opp_player, 3]:
				count = 0
				break
			count += 1
			if count == adj_count:
				if adj_count == 2:
					return 2
				if adj_count == 3:
					return 5
				if adj_count == 4:
					return 1000

	# Diagonal \
	for	i in range(COL - 3, COL + 1):
		for j in range(4):
			if not board[ROW - i + j, COL - i + j]: 
				zero_count += 1
				if zero_count > ZERO_MAX
					count = 0
					break
			if board[ROW, i + j] in [opp_player, 3]:
				count = 0
				break
			count += 1
			if count == adj_count:
				if adj_count == 2:
					return 2
				if adj_count == 3:
					return 5
				if adj_count == 4:
					return 1000

	return 0

