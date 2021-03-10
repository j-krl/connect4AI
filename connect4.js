import ai_move from './conn4ai'

ROWS = 12
COLS = 13
VISIBLE_ROWS = 6
VISIBLE_COLS = 7
LEGAL_ROWS = [3, 4, 5, 6, 7, 8]
LEGAL_COLS = [3, 4, 5, 6, 7, 8, 9]

turn = 0b10
winner = False
draw_counter = 0

passes = 2
if len(sys.argv) > 1:
	passes = int(sys.argv[1])

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
	
	print_board(board)
	return check_winner(board, [row, column], turn)

def play(board):
	if turn == 0b01:
		column = int(input("Pick a column (1-7): ")) + 2
		if column in LEGAL_COLS:
			return mark_board(board, column)
		else:
			print("You picked a column outside the board!")
			play(board)
	else:
		column = int(ai_move(passes, board, turn))
		return mark_board(board, column)

def check_winner(board, square, player):
	# Returns True if a player won the game on the last move
	ROW = square[0]
	COL = square[1]
	piece = 0 # Currently selected piece

	for n in range(4):
		for	i in range(4):
			for j in range(4):

				if n == 0: piece = board[ROW, COL - i + j] # Horizontal
				elif n == 1: piece = board[ROW - i + j, COL] # Vertical
				elif n == 2: piece = board[ROW + i - j, COL - i + j] # Diagonal /
				elif n == 3: piece = board[ROW - i + j, COL - i + j] # Diagonal \

				if piece != player:
					break

				if j == 3:
					return True
	
	return False

while winner == False and draw_counter != 42:
	turn = toggle(turn)
	winner = play(board)
	draw_counter += 1

if winner == True:
	print("Player " + str(turn) + " wins!")

else:
	print("The game is a draw")

