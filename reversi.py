def init_board():
    board = []
    for i in range(64):
        if i == 27 or i == 36:
            board.append("W")
        elif i == 28 or i == 35:
            board.append("B")
        else:
            board.append(0)
    return board

def string_board(board):
    board_str = ""
    for i in range(64):
        if(i%8 == 0):
            board_str = board_str + "|"

        if(board[i] == 0):
            board_str = board_str + " |"
        elif(board[i] == "B"):
            board_str = board_str + "B|"
        else:
            board_str = board_str + "W|"

        if(i%8 == 7):
            board_str = board_str + "\n"
    return board_str

def getCurrentPlayer(player):
    if(player == "W"):
        return "W"
    else:
        return "B"

def getOpponent(player):
    if(player == "W"):
        return "B"
    else:
        return "W"

def replacePiece(piece, pos, board):
    pass

def updateBoard (board, player, move):
    pass

def getValidMoves (playerPositions, board, player):
    validMoves = []
    leftChecked = False
    leftUpChecked = False
    upChecked = False
    rightUpChecked = False
    rightChecked = False
    rightDownChecked = False
    downChecked = False
    leftDownChecked = False

    for i in playerPositions:
        if validLeftIndex(i, board, player) >= 0 and (not leftChecked):
            validMoves.append(validLeftIndex(i, board, player))
            leftChecked = True
        if validLeftUpIndex(i, board, player) >= 0 and (not leftUpChecked):
            validMoves.append(validLeftUpIndex(i, board, player))
            leftUpChecked = True
        if validUpIndex(i, board, player) >= 0 and (not upChecked):
            validMoves.append(validUpIndex(i, board, player))
            upChecked = True
        if validRightUpIndex(i, board, player) >= 0 and (not rightUpChecked):
            validMoves.append(validRightUpIndex(i, board, player))
            rightUpChecked = True
        if validRightIndex(i, board, player) >= 0 and (not rightChecked):
            validMoves.append(validRightIndex(i, board, player))
            rightChecked = True
        if validRightDownIndex(i, board, player) >= 0 and (not rightDownChecked):
            validMoves.append(validRightDownIndex(i, board, player))
            rightDownChecked = True
        if validDownIndex(i, board, player) >= 0 and (not downChecked):
            validMoves.append(validDownIndex(i, board, player))
            downChecked = True
        if validLeftDownIndex(i, board, player) >= 0 and (not leftDownChecked):
            validMoves.append(validLeftDownIndex(i, board, player))
            leftDownChecked = True

        leftChecked = False
        leftUpChecked = False
        upChecked = False
        rightUpChecked = False
        rightChecked = False
        rightDownChecked = False
        downChecked = False
        leftDownChecked = False
    return validMoves

def getPlayerPositions (board, player):
    return [i for i in range(len(board)) if (board[i] == player)]

def validLeftIndex (pos, board, player):
    isOpponent = False
    isEmpty = False

    while(True):
        if (isOpponent and isEmpty):
            return pos
        elif ((((pos - 1) % 8) == 7) or ((pos - 1) < 0)):
            return -1
        elif ((board[(pos - 1)] == getOpponent(player)) and (not isOpponent)):
            isOpponent = True
            pos = pos - 1
        elif ((board[(pos - 1)] == getOpponent(player)) and isOpponent):
            pos = pos - 1
        elif ((board[(pos - 1)] != getOpponent(player)) and (board[(pos - 1)] != getCurrentPlayer(player)) and isOpponent and (not isEmpty)):
            pos = pos - 1
            isEmpty = True
        else:
            return -1

def validLeftUpIndex (pos, board, player):
    isOpponent = False
    isEmpty = False

    while(True):
        if (isOpponent and isEmpty):
            return pos
        elif ((((pos - 9) % 8) == 7) or ((pos - 9) < 0)):
            return -1
        elif ((board[(pos - 9)] == getOpponent(player)) and (not isOpponent)):
            isOpponent = True
            pos = pos - 9
        elif ((board[(pos - 9)] == getOpponent(player)) and isOpponent):
            pos = pos - 9
        elif ((board[(pos - 9)] != getOpponent(player)) and (board[(pos - 9)] != getCurrentPlayer(player)) and isOpponent and (not isEmpty)):
            pos = pos - 9
            isEmpty = True
        else:
            return -1

def validUpIndex (pos, board, player):
    isOpponent = False
    isEmpty = False

    while(True):
        if (isOpponent and isEmpty):
            return pos
        elif ((pos - 8) < 0):
            return -1
        elif ((board[(pos - 8)] == getOpponent(player)) and (not isOpponent)):
            isOpponent = True
            pos = pos - 8
        elif ((board[(pos - 8)] == getOpponent(player)) and isOpponent):
            pos = pos - 8
        elif ((board[(pos - 8)] != getOpponent(player)) and (board[(pos - 8)] != getCurrentPlayer(player)) and isOpponent and (not isEmpty)):
            pos = pos - 8
            isEmpty = True
        else:
            return -1

def validRightUpIndex (pos, board, player):
    isOpponent = False
    isEmpty = False

    while(True):
        if (isOpponent and isEmpty):
            return pos
        elif ((((pos - 7) % 8) == 0) or ((pos - 7) < 0)):
            return -1
        elif ((board[(pos - 7)] == getOpponent(player)) and (not isOpponent)):
            isOpponent = True
            pos = pos - 7
        elif ((board[(pos - 7)] == getOpponent(player)) and isOpponent):
            pos = pos - 7
        elif ((board[(pos - 7)] != getOpponent(player)) and (board[(pos - 7)] != getCurrentPlayer(player)) and isOpponent and (not isEmpty)):
            pos = pos - 7
            isEmpty = True
        else:
            return -1

def validRightIndex (pos, board, player):
    isOpponent = False
    isEmpty = False

    while(True):
        if (isOpponent and isEmpty):
            return pos
        elif ((((pos + 1) % 8) == 0) or ((pos + 1) > 63)):
            return -1
        elif ((board[(pos + 1)] == getOpponent(player)) and (not isOpponent)):
            isOpponent = True
            pos = pos + 1
        elif ((board[(pos + 1)] == getOpponent(player)) and isOpponent):
            pos = pos + 1
        elif ((board[(pos + 1)] != getOpponent(player)) and (board[(pos + 1)] != getCurrentPlayer(player)) and isOpponent and (not isEmpty)):
            pos = pos + 1
            isEmpty = True
        else:
            return -1

def validRightDownIndex (pos, board, player):
    isOpponent = False
    isEmpty = False

    while(True):
        if (isOpponent and isEmpty):
            return pos
        elif ((((pos + 9) % 8) == 0) or ((pos + 9) > 63)):
            return -1
        elif ((board[(pos + 9)] == getOpponent(player)) and (not isOpponent)):
            isOpponent = True
            pos = pos + 9
        elif ((board[(pos + 9)] == getOpponent(player)) and isOpponent):
            pos = pos + 9
        elif ((board[(pos + 9)] != getOpponent(player)) and (board[(pos + 9)] != getCurrentPlayer(player)) and isOpponent and (not isEmpty)):
            pos = pos + 9
            isEmpty = True
        else:
            return -1

def validDownIndex (pos, board, player):
    isOpponent = False
    isEmpty = False

    while(True):
        if (isOpponent and isEmpty):
            return pos
        elif ((pos + 8) > 63):
            return -1
        elif ((board[(pos + 8)] == getOpponent(player)) and (not isOpponent)):
            isOpponent = True
            pos = pos + 8
        elif ((board[(pos + 8)] == getOpponent(player)) and isOpponent):
            pos = pos + 8
        elif ((board[(pos + 8)] != getOpponent(player)) and (board[(pos + 8)] != getCurrentPlayer(player)) and isOpponent and (not isEmpty)):
            pos = pos + 8
            isEmpty = True
        else:
            return -1

def validLeftDownIndex (pos, board, player):
    isOpponent = False
    isEmpty = False

    while(True):
        if (isOpponent and isEmpty):
            return pos
        elif ((((pos + 7) % 8) == 7) or ((pos + 7) > 63)):
            return -1
        elif ((board[(pos + 7)] == getOpponent(player)) and (not isOpponent)):
            isOpponent = True
            pos = pos + 7
        elif ((board[(pos + 7)] == getOpponent(player)) and isOpponent):
            pos = pos + 7
        elif ((board[(pos + 7)] != getOpponent(player)) and (board[(pos + 7)] != getCurrentPlayer(player)) and isOpponent and (not isEmpty)):
            pos = pos + 7
            isEmpty = True
        else:
            return -1

def validPlayLeft(pos, board, player):
    isOpponent = False
    isYours = False

    while True:
        if isOpponent and isYours:
            return True
        elif ((pos - 1) % 8 == 7) or ((pos - 1) < 0):
            return False
        elif (board[(pos - 1)] == getOpponent(player)) and (not isOpponent):
            pos = pos - 1
            isOpponent = True
        elif (board[(pos - 1)] == getOpponent(player)) and isOpponent:
            pos = pos - 1
        elif (board[(pos - 1)] == getCurrentPlayer(player)) and (not isYours) and isOpponent:
            pos = pos - 1
            isYours = True
        else:
            return False


def validPlayLeftUp(pos, board, player):
    isOpponent = False
    isYours = False

    while True:
        if isOpponent and isYours:
            return True
        elif ((pos - 9) % 8 == 7) or ((pos - 9) < 0):
            return False
        elif (board[(pos - 9)] == getOpponent(player)) and (not isOpponent):
            pos = pos - 9
            isOpponent = True
        elif (board[(pos - 9)] == getOpponent(player)) and isOpponent:
            pos = pos - 9
        elif (board[(pos - 9)] == getCurrentPlayer(player)) and (not isYours) and isOpponent:
            pos = pos - 9
            isYours = True
        else:
            return False


def validPlayUp(pos, board, player):
    isOpponent = False
    isYours = False

    while True:
        if isOpponent and isYours:
            return True
        elif (pos - 8) < 0:
            return False
        elif (board[(pos - 8)] == getOpponent(player)) and (not isOpponent):
            pos = pos - 8
            isOpponent = True
        elif (board[(pos - 8)] == getOpponent(player)) and isOpponent:
            pos = pos - 8
        elif (board[(pos - 8)] == getCurrentPlayer(player)) and (not isYours) and isOpponent:
            pos = pos - 8
            isYours = True
        else:
            return False


def validPlayRightUp(pos, board, player):
    isOpponent = False
    isYours = False

    while True:
        if isOpponent and isYours:
            return True
        elif ((pos - 7) % 8 == 0) or ((pos - 7) < 0):
            return False
        elif (board[(pos - 7)] == getOpponent(player)) and (not isOpponent):
            pos = pos - 7
            isOpponent = True
        elif (board[(pos - 7)] == getOpponent(player)) and isOpponent:
            pos = pos - 7
        elif (board[(pos - 7)] == getCurrentPlayer(player)) and (not isYours) and isOpponent:
            pos = pos - 7
            isYours = True
        else:
            return False


def validPlayRight(pos, board, player):
    isOpponent = False
    isYours = False

    while True:
        if isOpponent and isYours:
            return True
        elif ((pos + 1) % 8 == 0) or ((pos + 1) > 63):
            return False
        elif (board[(pos + 1)] == getOpponent(player)) and (not isOpponent):
            pos = pos + 1
            isOpponent = True
        elif (board[(pos + 1)] == getOpponent(player)) and isOpponent:
            pos = pos + 1
        elif (board[(pos + 1)] == getCurrentPlayer(player)) and (not isYours) and isOpponent:
            pos = pos + 1
            isYours = True
        else:
            return False

def validPlayRightDown(pos, board, player):
    isOpponent = False
    isYours = False

    while True:
        if isOpponent and isYours:
            return True
        elif ((pos + 9) % 8 == 0) or ((pos + 9) > 63):
            return False
        elif (board[(pos + 9)] == getOpponent(player)) and (not isOpponent):
            pos = pos + 9
            isOpponent = True
        elif (board[(pos + 9)] == getOpponent(player)) and isOpponent:
            pos = pos + 9
        elif (board[(pos + 9)] == getCurrentPlayer(player)) and (not isYours) and isOpponent:
            pos = pos + 9
            isYours = True
        else:
            return False

def validPlayDown(pos, board, player):
    isOpponent = False
    isYours = False

    while True:
        if isOpponent and isYours:
            return True
        elif (pos + 8) > 63:
            return False
        elif (board[(pos + 8)] == getOpponent(player)) and (not isOpponent):
            pos = pos + 8
            isOpponent = True
        elif (board[(pos + 8)] == getOpponent(player)) and isOpponent:
            pos = pos + 8
        elif (board[(pos + 8)] == getCurrentPlayer(player)) and (not isYours) and isOpponent:
            pos = pos + 8
            isYours = True
        else:
            return False

def validPlayLeftDown(pos, board, player):
    isOpponent = False
    isYours = False

    while True:
        if isOpponent and isYours:
            return True
        elif ((pos + 7) % 8 == 7) or ((pos + 7) > 63):
            return False
        elif (board[(pos + 7)] == getOpponent(player)) and (not isOpponent):
            pos = pos + 7
            isOpponent = True
        elif (board[(pos + 7)] == getOpponent(player)) and isOpponent:
            pos = pos + 7
        elif (board[(pos + 7)] == getCurrentPlayer(player)) and (not isYours) and isOpponent:
            pos = pos + 7
            isYours = True
        else:
            return False

def playLeft(pos, board, player):
    isYou = False

    while True:
        if isYou:
            return board
        elif board[pos - 1] == getCurrentPlayer(player):
            board[pos] = getCurrentPlayer(player)
            pos = pos - 1
            isYou = True
        else:
            board[pos] = getCurrentPlayer(player)
            pos = pos - 1

def playLeftUp(pos, board, player):
    isYou = False

    while True:
        if isYou:
            return board
        elif board[pos - 9] == getCurrentPlayer(player):
            board[pos] = getCurrentPlayer(player)
            pos = pos - 9
            isYou = True
        else:
            board[pos] = getCurrentPlayer(player)
            pos = pos - 9

def playUp(pos, board, player):
    isYou = False

    while True:
        if isYou:
            return board
        elif board[pos - 8] == getCurrentPlayer(player):
            board[pos] = getCurrentPlayer(player)
            pos = pos - 8
            isYou = True
        else:
            board[pos] = getCurrentPlayer(player)
            pos = pos - 8

def playRightUp(pos, board, player):
    isYou = False

    while True:
        if isYou:
            return board
        elif board[pos - 7] == getCurrentPlayer(player):
            board[pos] = getCurrentPlayer(player)
            pos = pos - 7
            isYou = True
        else:
            board[pos] = getCurrentPlayer(player)
            pos = pos - 7

def playRight(pos, board, player):
    isYou = False

    while True:
        if isYou:
            return board
        elif board[pos + 1] == getCurrentPlayer(player):
            board[pos] = getCurrentPlayer(player)
            pos = pos + 1
            isYou = True
        else:
            board[pos] = getCurrentPlayer(player)
            pos = pos + 1

def playRightDown(pos, board, player):
    isYou = False

    while True:
        if isYou:
            return board
        elif board[pos + 9] == getCurrentPlayer(player):
            board[pos] = getCurrentPlayer(player)
            pos = pos + 9
            isYou = True
        else:
            board[pos] = getCurrentPlayer(player)
            pos = pos + 9

def playDown(pos, board, player):
    isYou = False

    while True:
        if isYou:
            return board
        elif board[pos + 8] == getCurrentPlayer(player):
            board[pos] = getCurrentPlayer(player)
            pos = pos + 8
            isYou = True
        else:
            board[pos] = getCurrentPlayer(player)
            pos = pos + 8

def playLeftDown(pos, board, player):
    isYou = False

    while True:
        if isYou:
            return board
        elif board[pos + 7] == getCurrentPlayer(player):
            board[pos] = getCurrentPlayer(player)
            pos = pos + 7
            isYou = True
        else:
            board[pos] = getCurrentPlayer(player)
            pos = pos + 7

def playMove(move, board, player):
    leftPlayed, leftUpPlayed, upPlayed, rightUpPlayed = False, False, False, False
    rightPlayed, rightDownPlayed, downPlayed, leftDownPlayed = False, False, False, False

    while True:
        if (validPlayLeft(move, board, player)) and (not leftPlayed):
            board = playLeft(move, board, player)
            leftPlayed = True
        elif (validPlayLeftUp(move, board, player)) and (not leftUpPlayed):
            board = playLeftUp(move, board, player)
            leftUpPlayed = True
        elif (validPlayUp(move, board, player)) and (not upPlayed):
            board = playUp(move, board, player)
            upPlayed = True
        elif (validPlayRightUp(move, board, player)) and (not rightUpPlayed):
            board = playRightUp(move, board, player)
            rightUpPlayed = True
        elif (validPlayRight(move, board, player)) and (not rightPlayed):
            board = playRight(move, board, player)
            rightPlayed = True
        elif (validPlayRightDown(move, board, player)) and (not rightDownPlayed):
            board = playRightDown(move, board, player)
            rightUpPlayed = True
        elif (validPlayDown(move, board, player)) and (not downPlayed):
            board = playDown(move, board, player)
            downPlayed = True
        elif (validPlayLeftDown(move, board, player)) and (not leftDownPlayed):
            board = playLeftDown(move, board, player)
            leftDownPlayed = True
        else:
            return board

