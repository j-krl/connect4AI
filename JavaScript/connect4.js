const ROWS = 12
const COLS = 13
// const VISIBLE_ROWS = 6
// const VISIBLE_COLS = 7
// const LEGAL_ROWS = [3, 4, 5, 6, 7, 8]
// const LEGAL_COLS = [3, 4, 5, 6, 7, 8, 9]

export function generateBoard() {  
    /*
     * Creation of the game board as a 2D js array
     * 0 = empty square
     * 1 = player 1
     * 2 = player 2
     * 3 = square that is not a legal move square but exists for computational reason
     */

    let board = new Array(ROWS).fill(0).map(() => new Array(COLS).fill(0)) // Initialize board of 0s
    
    for (let j = 0; j < COLS; j++) {  	
        for (let i = 0; i < ROWS; i++) {  
            if (i < 3 || i > 8) {  
                board[i][j] = 3
            }
            else if (j < 3 || j > 9) {  
                board[i][j] = 3
            }
        }
    }
    return board
}


export function toggleTurn(old_turn) {  
    const mask = 0b11
    const new_turn = (old_turn ^ mask)
    return new_turn
}

export function legalRowCheck(board, column) {
    // returns row piece will fall in that column, false if the move is illegal
    for (let i = 8; i > 2; i--) {  
        if (!board[i][column]) {  
            return i
        }
    }
    return false
}

export function getColumn(board, colNum) {
    const colArray = new Array(6).fill(null).map((e, index) => board[index + 3][colNum])
    return colArray
}

export function markBoard(board, column, turn) {  
    // only run after legalMoveCheck
    // returns new board state
    let row = null
    
    for (let i = 8; i > 2; i--) {  
        if (!board[i][column]) {  
            row = i
            break
        }
    }

    if (turn == 0b01) {  
        board[row][column] = 1
    } 
    else {  
        board[row][column] = 2
    }

    return board
}

export function checkGameOverState(board, square, turnCounter) {  
    // Returns player number if they won on the last move. Otherwise returns 0.
    const ROW = square[0]
    const COL = square[1]
    const player = board[ROW][COL]
    let piece = 0 // Currently selected piece
    
    if (turnCounter == 42) return 3

    for (let n = 0; n < 4; n++) {  
        for (let i = 0; i < 4; i++) {  
            for (let j = 0; j < 4; j++) {  
                
                if (n == 0) piece = board[ROW][COL - i + j] // Horizontal
                else if (n == 1) piece = board[ROW - i + j][COL] // Vertical
                else if (n == 2) piece = board[ROW + i - j][COL - i + j] // Diagonal /
                else if (n == 3) piece = board[ROW - i + j][COL - i + j] // Diagonal \
                if (piece != player) {  
                    break
                }
                if (j == 3) {  
                    return player
                }
            }
        }
    }
    return 0
}

