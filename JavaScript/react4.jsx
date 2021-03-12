import React, { useState, useEffect, useRef } from "react"
import ReactDOM from "react-dom"
import PropTypes from "prop-types"
import { Spring } from "react-spring/renderprops"

import {
    generateBoard,
    toggleTurn,
    legalRowCheck,
    getColumn,
    markBoard,
    checkGameOverState,
} from "./connect4"
import aiMove from "./conn4ai"

import "./react4.css"

//------------------------------------------------------------------------------
// Board GUI
//------------------------------------------------------------------------------

function AnimateChecker(yPos, colour) {
    return (
        <Spring from={{ number: 0 }} to={{ number: 50 + 100 * yPos }}>
            {(props) => (
                <circle cx="50" cy={props.number} r="40" fill={colour} />
            )}
        </Spring>
    )
}
AnimateChecker.propTypes = {
    number: PropTypes.number.isRequired,
}

function Checker(props) {
    return props.colour ? AnimateChecker(props.row, props.colour) : null
}

function CheckerColumn(props) {
    const colour = ["red", "yellow"]
    // column elements that are 0 will not map to an element from 'colour' and so // will return null in the Checker function
    const gameCol = props.gameCol
    return gameCol.map((element, index) => {
        return <Checker key={index} colour={colour[element - 1]} row={index} />
    })
}

function Defs() {
    return (
        <defs>
            <pattern
                id="cell-pattern"
                patternUnits="userSpaceOnUse"
                width="100"
                height="100"
            >
                <circle cx="50" cy="50" r="40" fill="black" />
            </pattern>
            <mask id="cell-mask">
                <rect width="100" height="600" fill="white"></rect>
                <rect width="100" height="600" fill="url(#cell-pattern)"></rect>
            </mask>
        </defs>
    )
}

function Rectangle() {
    return (
        <rect
            width="100"
            height="600"
            fill={"#1887ff"}
            mask="url(#cell-mask)"
        ></rect>
    )
}

function FinalColumn(props) {
    return (
        <svg x={props.num * 100} y="0" onClick={props.colUpdate}>
            <CheckerColumn gameCol={props.gameCol} />
            <Rectangle />
        </svg>
    )
}
FinalColumn.propTypes = {
    colUpdate: PropTypes.func.isRequired,
    gameCol: PropTypes.array.isRequired,
    num: PropTypes.number.isRequired,
}

//------------------------------------------------------------------------------
// Final App
//------------------------------------------------------------------------------

function Conn4GUI() {
    const [boardState, setBoardState] = useState(generateBoard())
    const [turnState, setTurnState] = useState(2)
    const [lastMove, setLastMove] = useState([null, null])
    const [gameOverState, setGameOverState] = useState(0)
    const [gameOverMessage, setGameOverMessage] = useState("")
    const [turnCounter, setTurnCounter] = useState(0)
    const [gameMode, setGameMode] = useState(1) // 0 = PvP, 1 = PvAI
    const [aiPlies, setAIPlies] = useState(3) // Layers used for AI computation. Right now 3 seems to be hard and 2 seems to be easy. 1 is harder than 2???

    const effectCounter = useRef(0) // hacky workaround to avoid useEffect trigger on initial render

    useEffect(() => {
        if (effectCounter.current > 1) {
            const boardCopy = JSON.parse(JSON.stringify(boardState))
            setBoardState(markBoard(boardCopy, lastMove[1], turnState))
        } else effectCounter.current++
    }, [lastMove])

    useEffect(() => {
        if (effectCounter.current > 1) {
            const gameOver = checkGameOverState(
                boardState,
                lastMove,
                turnCounter
            )
            if (gameOver) {
                setGameOverState(gameOver)
                displayMessage(gameOver)
            }
            setTurnCounter(turnCounter + 1)
            setTurnState(toggleTurn(turnState))
        } else effectCounter.current++
    }, [boardState])

    useEffect(() => {
        if (gameMode && turnState == 1 && effectCounter.current > 1) {
            // AI moves if gameMode is PvAI
            setTimeout(() => {
                const aiCol = aiMove(aiPlies, boardState, turnState)
                colClick(aiCol, true)
            }, 500)
        } else effectCounter.current++
    }, [turnState])

    function colClick(colNum, aiClick) {
        if (gameMode && !aiClick && turnState == 1) return // disallows clicking on AI's turn
        if (gameOverState) return // disallows clicking if game is over

        const row = legalRowCheck(boardState, colNum)
        if (!row) return

        setLastMove([row, colNum])
    }

    function displayMessage(gameOverState) {
        if (gameOverState == 1) setGameOverMessage("Red wins!")
        if (gameOverState == 2) setGameOverMessage("Yellow wins!")
        if (gameOverState == 3) setGameOverMessage("The Game is a draw.")
    }

    function resetGame(gameType, plies) {
        effectCounter.current = 1
        setAIPlies(plies)
        setGameOverState(0)
        setTurnCounter(0)
        setGameMode(gameType) // 0 for human, 1 for AI
        setGameOverMessage("")
        setBoardState(generateBoard())
        setTurnState(2)
    }

    const columnsArray = new Array(7).fill(null).map((e, index) => {
        return (
            <FinalColumn
                key={index}
                num={index}
                gameCol={getColumn(boardState, index + 3)}
                colUpdate={() => colClick(index + 3, false)}
            />
        )
    })

    return (
        <div className="container">
            <h1>Connect Four</h1>
            <strong className="grid-inline grid-center">
                {gameOverMessage}
            </strong>
            <div className="gameBox">
                <svg className="rounded" viewBox="0 0 700 600">
                    <Defs />
                    {columnsArray}
                </svg>
            </div>
            <div className="grid-inline grid-center">
                <button
                    className="btn btn-default"
                    onClick={() => resetGame(1, 2)}
                >
                    Play vs Easy AI
                </button>
                <button
                    className="btn btn-default"
                    onClick={() => resetGame(1, 3)}
                >
                    Play vs Hard AI
                </button>

                <button
                    className="btn btn-default"
                    onClick={() => resetGame(0, null)}
                >
                    Play vs Human
                </button>
            </div>
        </div>
    )
}

ReactDOM.render(<Conn4GUI />, document.getElementById("root"))
