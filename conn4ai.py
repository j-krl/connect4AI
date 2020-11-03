from copy import deepcopy
import pdb

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

def opposing_player(player):
	# Accepts integer player and returns opposing player
	MASK = 0b11
	opp_player = MASK ^ player
	return opp_player

def open_check(board):
	# Returns a list of columns that can legally accept more pieces
	open_cols = []
	for i in LEGAL_COLS:
		for j in LEGAL_ROWS:
			if board[j, i] == 0:
				open_cols.append(i)
				break
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
			break

	return board

def check_adjacent(board, square, player):
	# Check the AI score_node for a single square.
	ROW = square[0]
	COL = square[1]
	opp_player = opposing_player(player)
	count = 0 # Temporary count of connected piece on a single pass of the inner "j" loop
	total = 0 # Cumulative score_node of position
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
					if count == 3:
						total += 5 # 5 points for 3 in a row
					if count == 4:
						total += 1000 # 1000 points (always select) for 4 in a row
					count = 0
	
	if COL == 6:
		total += 4 # 4 points for center column moves

	return total

def play_node(board, player):
	# Play all moves on a single board and return arrays of moves, new boards, and score_nodes for each move
	open_cols = open_check(board)
	score_nodes = []
	boards = []
	
	for i in open_cols:
		square = open_square(board, i)
		score_nodes.append(check_adjacent(board, square, player))
		new_board = deepcopy(board)
		boards.append(mark_board(new_board, player, i))

	return [open_cols, boards, score_nodes]

def plant_tree(passes, board, player):
	# Derive game tree through specified number of recursive passes
	# Final tree structure will be of the form [node, [level]] with level being a list of all the same shaped nodes below it.
	new_player = opposing_player(player)
	branches = []
	node = play_node(board, player)

	if passes:
		for i in range(len(node[0])):
			branches.append(plant_tree(passes - 1, node[1][i], new_player))
	
	return [node, branches]

def score_tree(passes, tree):
	"""
	tree is the return value of plant_tree
	"""
	score_node = [0, 0]
	score_node[0] = max(tree[0][2])

	for i in range(len(tree[1])): 
		prev_score = score_tree(passes - 1, tree[1][i])
		
		if is_even(passes):
			tree[0][2][i] += prev_score[0]
		if not is_even(passes):
			tree[0][2][i] -= prev_score[0]
	
	print(tree[0][2])
	score_node[1] = tree[0][0][tree[0][2].index(max(tree[0][2]))]

	return score_node

def ai_move(passes, board, player):
	# The final AI method that returns the move the AI makes!
	tree = deepcopy(plant_tree(passes, board, player))
	branch = score_tree(passes, tree)
	
	return branch[1]

