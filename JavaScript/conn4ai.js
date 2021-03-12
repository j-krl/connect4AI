// const ROWS = 12
// const COLS = 13
const LEGAL_ROWS = [8, 7, 6, 5, 4, 3] // Bottom to top
const LEGAL_COLS = [3, 4, 5, 6, 7, 8, 9] // Left to right

function is_even(num) {
    num += 2
    if (!(num % 2)) {
        return true
    }
    return false
}

function opposingPlayer(player) {
    // Accepts integer player and returns opposing player
    const MASK = 0b11
    const opp_player = (MASK ^ player)
    return opp_player
}

function openCheck(board) {  
    // Returns a list of columns that can legally accept more pieces
    const open_cols = []
    for (let i of LEGAL_COLS) {
        for (let j of LEGAL_ROWS) {
            if (!board[j][i]) {
                open_cols.push(i)
                break
            }
        }
    }
    return open_cols
}

function openSquare(board, column) {  
    // Returns coordinates of open square if a single column can accept more pieces, False if it can't
    for (let i of LEGAL_ROWS) {
        if (!board[i][column]) {  
            return [i, column]
        }
    }
    return false    
}

function markBoard(board, player, column) {  
    if (!openSquare(board, column)) {  
        throw "AI attempting to mark a column that is already full"
    }
    for (let i of LEGAL_ROWS) { 
        if (!board[i][column]) {
            board[i][column] = player
            break
        }
    }
    return board
}

function checkAdjacent(board, square, player) {
    // Check the AI score_node for a single square.
    const ROW = square[0]
    const COL = square[1]
    const opp_player = opposingPlayer(player)
    let count = 0 // Temporary count of connected piece on a single pass of the inner "j" loop
    let total = 0 // Cumulative score_node of position
    let piece = 0 // Piece on currently selected square
	
    for (let n = 0; n < 4; n++) {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (n == 0) piece = board[ROW][COL - i + j] // Horizontal
                else if (n == 1) piece = board[ROW - i + j][COL] // Vertical
                else if (n == 2) piece = board[ROW + i - j][COL - i + j] // Diagonal /
                else if (n == 3) piece = board[ROW - i + j][COL - i + j] // Diagonal \

                if (piece == opp_player || piece == 3) {  
                    count = 0
                    break
                }
                if (piece == player) {  
                    count += 1
                }
                if (j == 3) {  
                    if (count == 2) {  
                        total += 2 // 2 points for 2 in a row
                    }
                    if (count == 3) {  
                        total += 5 // 5 points for 3 in a row
                    }
                    if (count == 4) {  
                        total += 1000 // 1000 points (always select) for 4 in a row
                    }                   
                    count = 0
                }           
            }
        }
    }
    if (COL == 6) {   
        total += 4 // 4 points for center column moves
    }
    return total
}

function playNode(board, player) {  
    // Play all moves on a single board and return arrays of moves, new boards, and score_nodes for each move
    const open_cols = openCheck(board)
    const score_nodes = []
    const boards = []

    for (let i of open_cols) {
        const square = openSquare(board, i)
        const new_board = JSON.parse(JSON.stringify(board))
        boards.push(markBoard(new_board, player, i))
        score_nodes.push(checkAdjacent(new_board, square, player))
    }
    return [open_cols, boards, score_nodes]
}

function plantTree(passes, board, opp_player) {
	// Derive game tree through specified number of recursive passes
	// Final tree structure will be of the form [node, [level]] with level being a list of all the same shaped nodes below it.
	// TODO: Fix arguments so that it accepts 'player' rather than 'opp_player'
    const new_player = opposingPlayer(opp_player)
    const branches = []
    const node = playNode(board, opp_player)

    if (passes) {  
        for (let i = 0; i < node[0].length; i++) {  
            branches.push(plantTree(passes - 1, node[1][i], new_player))
        }
    }

    return [node, branches]
}

function scoreTree(passes, tree) {  
    // tree is the return value of plantTree
    
    const score_node = [0, 0]
    
    if (tree[0][2].length) {  
        score_node[0] = Math.max(...tree[0][2])
    }
    else {  
        score_node[0] = 0
    }

    for (let i = 0; i < tree[1].length; i++) {   
        const prev_score = scoreTree(passes - 1, tree[1][i])

        if (is_even(passes)) {  
            tree[0][2][i] += prev_score[0]
        }
        else {  
            tree[0][2][i] -= prev_score[0]
        }
    }

    if (tree[0][2].length) {  
        score_node[1] = tree[0][0][tree[0][2].indexOf(Math.max(...tree[0][2]))]
    }
    else {  
        score_node[1] = tree[0][0][0]
    }

    return score_node
}
    
function aiMove(passes, board, player) {  
    // The final AI method that returns the move the AI makes!
    const tree = JSON.parse(JSON.stringify(plantTree(passes, board, opposingPlayer(player))))
    const branch = scoreTree(passes, tree)
    return branch[1]
}

export default aiMove

