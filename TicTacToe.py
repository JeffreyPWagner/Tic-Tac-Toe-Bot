from random import randint

board = [0] * 9
player1 = 1
player2 = 2
p1Wins = 0
p2Wins = 0
draws = 0
numGames = 10000


def reset_board():
    global board
    board = [0] * 9


def print_board():
    global board
    print(board[0:3])
    print(board[3:6])
    print(board[6:])


def random_move(player):
    global board
    while True:
        move = randint(0, 8)
        if board[move] == 0:
            board[move] = player
            break


def game_won(player):
    global board
    if ((board[0] == player and board[1] == player and board[2] == player) or
        (board[3] == player and board[4] == player and board[5] == player) or
        (board[6] == player and board[7] == player and board[8] == player) or
        (board[0] == player and board[3] == player and board[6] == player) or
        (board[1] == player and board[4] == player and board[7] == player) or
        (board[2] == player and board[5] == player and board[8] == player) or
        (board[0] == player and board[4] == player and board[8] == player) or
        (board[2] == player and board[4] == player and board[6] == player)):
            return True


def play_games():
    global board
    global player1
    global player2
    global p1Wins
    global p2Wins
    global draws
    global numGames

    for i in range(numGames):
        numMoves = 0
        currentPlayer = 1
        while True:
            random_move(currentPlayer)
            if game_won(currentPlayer):
                if currentPlayer == player1:
                    p1Wins = p1Wins + 1
                else:
                    p2Wins = p2Wins + 1
                break
            if numMoves == 8:
                draws = draws + 1
                break
            if currentPlayer == 1:
                currentPlayer = 2
            else:
                currentPlayer = 1
            numMoves = numMoves + 1
        print_board()
        print(p1Wins)
        print(p2Wins)
        print(draws)
        reset_board()


play_games()

