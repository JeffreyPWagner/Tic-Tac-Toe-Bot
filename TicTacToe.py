from random import randint

# initialize board, players, and win counts
board = [0] * 9
player1 = 1
player2 = 2
p1Wins = 0
p2Wins = 0
draws = 0

# the values associated with every state and move combination a smart player 1 has observed
p1StateValues = dict()

# a stack of states and associated moves that a smart player 1 performed during single game
p1StateMoves = list()

# the values associated with every state and move combination a smart player 2 has observed
p2StateValues = dict()

# a stack of states and associated moves that a smart player 2 performed during single game
p2StateMoves = list()

# set hyperparameters for experiment
numGames = 700000
learningRate = 0.2
discountRate = 0.5

# determine if each player is smart or random
p1Smart = True
p2Smart = False


# reset board to clean slate
def reset_board():
    global board
    board = [0] * 9


# print the current board
def print_board():
    global board
    print(board[0:3])
    print(board[3:6])
    print(board[6:])


# perform a random legal move
def random_move():
    global board
    while True:
        move = randint(0, 8)
        if board[move] == 0:
            return move


# perform a smart move (player 1)
def p1_smart_move():
    global p1StateValues
    global p1StateMoves
    global board
    state = tuple(board)

    # if player has seen this state before, make the most valuable move
    if state in p1StateValues:
        move = p1StateValues[state].index(max(p1StateValues[state]))

        # make a random move if that move is illegal
        if board[move] != 0:
            move = random_move()
        board[move] = player1

        # record the move to learn from later
        p1StateMoves.append([state, move])

    # else make a random move and record it to learn from later
    else:
        move = random_move()
        board[move] = player1
        p1StateMoves.append([state, move])


# backpropogate reward to update state values (player 1)
def p1_learn():
    global p1StateValues
    global p1StateMoves
    global board
    global learningRate
    global discountRate
    finalMove = True

    if game_won(player1):
        reward = 100
    else:
        reward = -100

    # iterate through the stack of state-move pairs from the completed game
    while p1StateMoves:

        # extract the state and move from the stack
        curStateMove = p1StateMoves.pop()
        state = curStateMove[0]
        move = curStateMove[1]

        # if it was the final move of the game, assign it the reward as its value
        if finalMove:
            if state in p1StateValues:
                p1StateValues[state][move] = reward
            else:
                p1StateValues[state] = [0] * 9
                p1StateValues[state][move] = reward
            finalMove = False

            # remember this state so it can be used when assigning the previous state's value
            nextState = state

        # if it was not the final move, assign its value based on Q learning
        else:
            if state in p1StateValues:
                p1StateValues[state][move] = learningRate * (discountRate * max(p1StateValues[nextState]) -
                    p1StateValues[state][move])
            else:
                p1StateValues[state] = [0] * 9
                p1StateValues[state][move] = learningRate * (discountRate * max(p1StateValues[nextState]) -
                    p1StateValues[state][move])

            # remember this state so it can be used when assigning the previous state's value
            nextState = state


# perform a smart move (player 2)
def p2_smart_move():
    global p2StateValues
    global p2StateMoves
    global board
    state = tuple(board)

    # if player has seen this state before, make the most valuable move
    if state in p2StateValues:
        move = p2StateValues[state].index(max(p2StateValues[state]))

        # make a random move if that move is illegal
        if board[move] != 0:
            move = random_move()
        board[move] = player2

        # record the move to learn from later
        p2StateMoves.append([state, move])

    # else make a random move and record it to learn from later
    else:
        move = random_move()
        board[move] = player2
        p2StateMoves.append([state, move])


# backpropogate reward to update state values (player 2)
def p2_learn():
    global p2StateValues
    global p2StateMoves
    global board
    global learningRate
    global discountRate
    finalMove = True

    if game_won(player2):
        reward = 100
    else:
        reward = -100

    # iterate through the stack of state-move pairs from the completed game
    while p2StateMoves:

        # extract the state and move from the stack
        curStateMove = p2StateMoves.pop()
        state = curStateMove[0]
        move = curStateMove[1]

        # if it was the final move of the game, assign it the reward as its value
        if finalMove:
            if state in p2StateValues:
                p2StateValues[state][move] = reward
            else:
                p2StateValues[state] = [0] * 9
                p2StateValues[state][move] = reward
            finalMove = False

            # remember this state so it can be used when assigning the previous state's value
            nextState = state

        # if it was not the final move, assign its value based on Q learning
        else:
            if state in p2StateValues:
                p2StateValues[state][move] = learningRate * (discountRate * max(p2StateValues[nextState]) -
                    p2StateValues[state][move])
            else:
                p2StateValues[state] = [0] * 9
                p2StateValues[state][move] = learningRate * (discountRate * max(p2StateValues[nextState]) -
                    p2StateValues[state][move])

            # remember this state so it can be used when assigning the previous state's value
            nextState = state


# determine if a player has won the game
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

# play games based on provided hyperparameters
def play_games():
    global board
    global player1
    global player2
    global p1Wins
    global p2Wins
    global draws
    global numGames
    global p1StateMoves

    for i in range(numGames + 1):
        numMoves = 0
        currentPlayer = 1

        while True:

            # players move depending on turn and if they are smart
            if currentPlayer == player1:
                if p1Smart:
                    p1_smart_move()
                else:
                    board[random_move()] = player1
            else:
                if p2Smart:
                    p2_smart_move()
                else:
                    board[random_move()] = player2

            # determine if game was won and count win
            if game_won(currentPlayer):
                if currentPlayer == player1:
                    p1Wins = p1Wins + 1
                else:
                    p2Wins = p2Wins + 1
                break

            # determine if game is a draw and count it
            if numMoves == 8:
                draws = draws + 1
                break

            # move on to next player's turn
            if currentPlayer == 1:
                currentPlayer = 2
            else:
                currentPlayer = 1
            numMoves = numMoves + 1

        # players learn after each game if they sre smart
        if p1Smart:
            p1_learn()
        if p2Smart:
            p2_learn()

        # print win rates and board every 100,000 games
        if i % 100000 == 0 and i > 0:
            print("Games: ", i, "\n")
            print("Final board: ")
            print_board()
            print()
            print("Player 1 win rate: ", p1Wins / i)
            print("Player 2 win rate: ", p2Wins / i)
            print("Draw rate: ", draws / i, "\n")

        reset_board()
        p1StateMoves.clear()
        p2StateMoves.clear()


# launch games
play_games()

