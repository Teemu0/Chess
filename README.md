# Chess

## Description

A chess program where you can play against bots, or control both white and black pieces and play against a friend or yourself.

Currently the program has 2 bots to play against. One of them uses approximately 5 seconds per move, and the other one uses 20 seconds. My long term goal is to make this bot better at chess than I am, while keeping it fast enough (one move should not take more than 30 seconds).

## Requirements

- python
- pygame

## How to use

- To start the program, run the chess.py file in the folder stage5.
- Use mouse click to select a game mode.
- To make a move, first click on the piece that you want to move. After the piece is highlighted in yellow, click on a square where you would like to move the piece. If you want to change the highlighted piece, click on the piece again, or on any square where the highlighted piece cannot move.
- To castle, first click on your king to highlight it, and then click two squares to either side of the king.
- When promoting a pawn, the program will ask for keyboard input for what piece do you want to promote to. Click on terminal and then press the preferred key (Q, R, B, K) and press Enter.
- The game ends when there is a checkmate or a stalemate on the board.
- You can always quit the program by clicking the X on the top right of the window.

## Folders

### stage5
Current state of the program. 3 game modes with functioning main menu and end menu.

### old back ups
Previous iterations of the program.

- stage1: working practice board
- stage2: playable but bad chessAI. white player vs black AI
- stage3: improvements to chessAI

## Progression

First step was to make a functioning chess board. I used pygame to draw the game window. After that I added logic which ensures that every move follows the rules of chess. This includes special rules such as castling, promoting a pawn, and en passant. After that I added an evaluation function and a recursive minimax algorithm which searches for best moves. When first testing the bot, one main concern was time usage. If the bot's depth was set too high, it would take hours to search for a best move. To combat this, I will implement useful evaluation methods in order to cut down on the amount of computation needed.
