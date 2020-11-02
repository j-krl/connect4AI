# So far this only works if you do an even numbered depth in the game tree!

#import numpy as np

ROWS = 12
COLS = 13
LEGAL_ROWS = [8, 7, 6, 5, 4, 3] # Bottom to top
LEGAL_COLS = [3, 4, 5, 6, 7, 8, 9] # Left to right

def is_even(num):
	num += 2
	if num % 2 == 0:
		return True
	else:
		return False

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
			if board[j, i] == 0:
				open_cols.append(j)
	return open_cols

def open_square(board, column):
	# Returns coordinates of open square if a single column can accept more pieces, False if it can't
	for i in LEGAL_ROWS:
		if board[i, column] == 0:
			return [i, column]
	return False

def mark_board(board, player, column):
	if not open_square(board, column):
		raise IOError("AI attempting to mark a column that is already full")

	for i in LEGAL_ROWS:
		if board[i, column] == 0:
			board[i, column] = player

	return board

def check_adjacent(board, square, player):
	# Check the AI score for a single square.
	ROW = square[0]
	COL = square[1]
	opp_player = opp_player(player)
	count = 0 # Temporary count of connected piece on a single pass of the inner "j" loop
	total = 0 # Cumulative score of position
	piece = 0 # Piece on currently selected square

	for n in range(4):
		for	i in range(4):
			for j in range(4):

				if n == 0: piece = board[ROW, COL - i + j] # Horizontal
				elif n == 1: piece = board[ROW - i + j, COL] # Vertical
				elif n == 2: piece = board[ROW + i - j, COL - i + j] # Diagonal /
				elif n == 3: piece = board[ROW - i + j, COL - i + j] # Diagonal \

				if piece in [opp_player, 3]:
					count = 0
					break
				if piece == player:
					count += 1
				if j == 3:
					if count == 2:
						total += 2 # 2 points for 2 in a row
					elif count == 3:
						total += 5 # 5 points for 3 in a row
					elif count == 4:
						total += 1000 # 1000 points (always select) for 4 in a row
					count = 0
	
	if COL == 6:
		total += 4 # 4 points for center column moves

	return total

def play_node(board, player):
	# Play all moves on a single board and return arrays of moves, new boards, and scores for each move
	# Polarity is for returning either positive (True) or negative (False) scores
	open_cols = open_check(board)
	scores = []
	boards = []

	for i in open_cols:
		square = open_square(board, i)
		scores.append(check_adjacent(board, square, player))
		boards.append(mark_board(board, player, i))
		
	return [open_cols, boards, scores]

def plant_tree(passes, board, player):
	# Derive game tree through specified number of recursive passes
	# Final tree structure will be of the form [node, [level]] with level being a list of all the same shaped nodes below it.
	opp_player = opp_player(player)
	level = []
	node = play_node(board, player)

	for i in node[0]:
		if passes:
			level.append(play_tree(passes - 1, node[1][i], opp_player if is_even(passes) else player))
	
	return [node, level]

def score_tree(passes, tree):
	"""
	tree is the return value of plant_tree
	The first element of return_branch is the cumulative score of the branch to the specificied number of passes.
	The second element is a list of move that the computer predicts as best, the last element in the list being the move to make now.
	"""
	return_branch = [0,[]]
	element = []
	
	return_branch[0] = max(tree[0][2])
	return_branch[1].append(tree[0][2].index(return_branch[0]))

	for i in passes:
		prev_node = score_tree(passes - 1, tree[1])

		if is_even(passes):
			return_branch[0] -= prev_node[0]
		if not is_even(passes):
			return_branch[0] += prev_node[0]

		for j in prev_node[1]:
			return_branch[1].append(prev_node[1][j])
		
	return return_branch

def ai_move(passes, board, player):
	# The final AI method that returns the move the AI makes!
	tree = plant_tree(passes, board, player)
	branch = score_tree(passes, tree)

	return branch[1][-1]

