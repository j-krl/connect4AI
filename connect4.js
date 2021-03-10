import ai_move from './conn4ai'

const ROWS = 12
const COLS = 13
const VISIBLE_ROWS = 6
const VISIBLE_COLS = 7
const LEGAL_ROWS = [3, 4, 5, 6, 7, 8]
const LEGAL_COLS = [3, 4, 5, 6, 7, 8, 9]

let turn = 0b10
let winner = false
let draw_counter = 0

// TODO: Make passes user editable
const passes = 2 // greater number increases AI difficulty

function generate_board() {  
    /*
     * Creation of the game board as a 2D NumPy array
     * 0 = empty square
     * 1 = player 1
     * 2 = player 2
     * 3 = square that is not a legal move square but exists for computational reason
     */

    const board = new Array(6).fill(new Array(7).fill(0)) // Initialize board of 0s
    
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


function toggle(old_turn) {  
    const mask = 0b11
    const new_turn = (old_turn ^ mask)
    console.log(`It is player ${new_turn}'s turn.`)
    return new_turn
}

function mark_board(board, column) {  
    let row = null
    
    for (let i = 8; i > 2; i--) {  
        if !(board[i][column]) {  
            row = i
            break
        }
        if (i == 3) {  
            if (turn == 0b01) {  
                print("That column is full!")
            }
            play(board)
            return
        }

        if (turn == 0b01) {  
            board[row][column] = 1
        } 
        else {  
            board[row][column] = 2
        }

    return check_winner(board, [row, column], turn)
}

function play(board) {
    // TODO: Give an option to toggle between Human v Human and Human v AI
    if (turn == 0b01) {  
        // TODO: function must receive click from front end 
        return mark_board(board, column)
        else {  
            console.log("You picked a column outside the board!")
            play(board)
        }
    }
    else {  
        column = ai_move(passes, board, turn) // TODO: Make sure ai_move is valid for mark_board
        return mark_board(board, column)
    }
}

function check_winner(board, square, player) {  
    // Returns true if a player won the game on the last move
    const ROW = square[0]
    const COL = square[1]
    let piece = 0 // Currently selected piece

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
                    return true
                }
            }
        }
    }
    return false
}

while (!winner && draw_counter != 42) {  
    turn = toggle(turn)
    winner = play(board)
    draw_counter += 1
}

if (winner) {  
    console.log(`Player ${turn} wins!`)
}
else {  
    console.log("The game is a draw")
}

