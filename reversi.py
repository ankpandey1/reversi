import random, sys, pygame, time, copy
from pygame.locals import *
import json

WHITE_TILE = 'W'
BLACK_TILE = 'B'
EMPTY_SPACE = 0
FPS = 10

# width of the program's window, in pixels
WINDOWWIDTH = 800
# height in pixels
WINDOWHEIGHT = 700
# width & height of each space on the board, in pixels
SPACESIZE = 50
# columns on the game board
BOARDWIDTH = 8
# rows on the game board
BOARDHEIGHT = 8
ANIMATIONSPEED = 25
SAVED_GAME = False
PLAYER_1 = None
PLAYER_2 = None


# space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE

def init_pygame():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Reversi')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Set up the background image.
    boardImage = pygame.image.load('reversiboard.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('reversibackground.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)



def getNewBoard():
    # Creates a an empty board.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board


def init_board(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    global SAVED_GAME
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE

    # Add starting pieces to the center
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[4][4] = WHITE_TILE
    SAVED_GAME = False

def save_game(board, turn):
    global SAVED_GAME
    data = {}
    data['game'] = []
    data['game'].append({
        'board': board,
        'turn': turn,
        'player1': PLAYER_1,
        'player2': PLAYER_2
    })
    SAVED_GAME = True

    with open('reversi.txt', 'w') as out:
        json.dump(data, out)

def load_game():
    global PLAYER_1, PLAYER_2
    with open('reversi.txt') as json_file:
        data = json.load(json_file)
    PLAYER_1, PLAYER_2 = data['game'][0]['player1'], data['game'][0]['player2']
    return data['game'][0]['board'], data['game'][0]['turn']

def drawBoard(board):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT + 1):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    # Draw the black & white tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                else:
                    tileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)

def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)

def enterPlayerTile():
    global PLAYER_1, PLAYER_2
    # Draws the text and handles the mouse click events for letting
    # player1 choose which color they want to be.

    # Create the text.
    textSurf = FONT.render('Player 1 : Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    PLAYER_1 = WHITE_TILE #stating that Player 1 is WHITE
                    PLAYER_2 = BLACK_TILE #stating that Player 2 is BLACK
                    return [WHITE_TILE, BLACK_TILE]
                elif oRect.collidepoint( (mousex, mousey) ):
                    PLAYER_1 = BLACK_TILE  # stating that Player 1 is BLACK
                    PLAYER_2 = WHITE_TILE  # stating that Player 2 is WHITE
                    return [BLACK_TILE, WHITE_TILE]

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

#def string_board(board):
#    board_str = ""
#    for i in range(64):
#        if(i%8 == 0):
#            board_str = board_str + "|"

#        if(board[i] == 0):
#            board_str = board_str + " |"
#        elif(board[i] == "B"):
#            board_str = board_str + "B|"
#        else:
#            board_str = board_str + "W|"

#        if(i%8 == 7):
#            board_str = board_str + "\n"
#    return board_str

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


def getValidMoves(board, player):
    # Returns a list of (x,y) tuples of all valid moves.
    validMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if isValidMove(board, player, x, y) != False:
                validMoves.append((x, y))
    return validMoves

def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == WHITE_TILE:
        otherTile = BLACK_TILE
    else:
        otherTile = WHITE_TILE

    tilesToFlip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # The piece belongs to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break # break out of while loop, continue in for loop
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse
                # direction until we reach the original space, noting all
                # the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = EMPTY_SPACE # make space empty
    if len(tilesToFlip) == 0: # If no tiles flipped, this move is invalid
        return False
    return tilesToFlip


#def getValidMoves (playerPositions, board, player):
#    validMoves = []
#    leftChecked = False
#    leftUpChecked = False
#    upChecked = False
#    rightUpChecked = False
#    rightChecked = False
#    rightDownChecked = False
#    downChecked = False
 #   leftDownChecked = False

 #   for i in playerPositions:
 #       if validLeftIndex(i, board, player) >= 0 and (not leftChecked):
#            validMoves.append(validLeftIndex(i, board, player))
#            leftChecked = True
#        if validLeftUpIndex(i, board, player) >= 0 and (not leftUpChecked):
#            validMoves.append(validLeftUpIndex(i, board, player))
#            leftUpChecked = True
#        if validUpIndex(i, board, player) >= 0 and (not upChecked):
 #           validMoves.append(validUpIndex(i, board, player))
#            upChecked = True
#        if validRightUpIndex(i, board, player) >= 0 and (not rightUpChecked):
#            validMoves.append(validRightUpIndex(i, board, player))
#            rightUpChecked = True
#        if validRightIndex(i, board, player) >= 0 and (not rightChecked):
#            validMoves.append(validRightIndex(i, board, player))
#            rightChecked = True
#        if validRightDownIndex(i, board, player) >= 0 and (not rightDownChecked):
#            validMoves.append(validRightDownIndex(i, board, player))
#            rightDownChecked = True
#        if validDownIndex(i, board, player) >= 0 and (not downChecked):
#            validMoves.append(validDownIndex(i, board, player))
#            downChecked = True
#        if validLeftDownIndex(i, board, player) >= 0 and (not leftDownChecked):
#            validMoves.append(validLeftDownIndex(i, board, player))
#            leftDownChecked = True

#        leftChecked = False
#        leftUpChecked = False
#        upChecked = False
#        rightUpChecked = False
#        rightChecked = False
#        rightDownChecked = False
#        downChecked = False
#        leftDownChecked = False
#    return validMoves

def getPlayerPositions (board, player):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if(board[x][y] == player):
                return(x,y)
#    return [i for i in range(len(board)) if (board[i] == player)]

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

def makeMove(board, tile, xstart, ystart, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def makeMoveUsingMouse(board, turn):
    global SAVED_GAME
#    if getValidMoves(board, turn) == []:
        # If it's the player's turn but they
        # can't move, then end the game.
 #       break

   # make the Surface and Rect objects for the "New Game"
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)

# make the Surface and Rect objects for the "Save Game"
    saveGameSurf = FONT.render('Save Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    saveGameRect = saveGameSurf.get_rect()
    saveGameRect.topright = (WINDOWWIDTH - 138, 10)

    movexy = None
    while movexy == None and not SAVED_GAME:
        boardToDraw = board

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                # Handle mouse click events
                mousex, mousey = event.pos
                if newGameRect.collidepoint((mousex, mousey)):
                    # Start a new game
                    return True
                if saveGameRect.collidepoint((mousex, mousey)):
                    # Save the game
                    save_game(board, turn)
                    return turn
                movexy = getSpaceClicked(mousex, mousey)
                if movexy != None and not isValidMove(board, turn, movexy[0], movexy[1]):
                    movexy = None

        # Draw the game board.
        drawBoard(boardToDraw)
        drawInfo(boardToDraw, turn, getOpponent(turn), turn)

        # Draw the "New Game" and "Save Game" buttons.
        DISPLAYSURF.blit(newGameSurf, newGameRect)
        DISPLAYSURF.blit(saveGameSurf, saveGameRect)

        MAINCLOCK.tick(FPS)
        pygame.display.update()

    # Make the move and end the turn.
    if not SAVED_GAME:
        makeMove(board, turn, movexy[0], movexy[1], True)
        if getValidMoves(board, getOpponent(turn)) != []:
            # Only set for the Opponent's turn if it can make a move.
            turn = getOpponent(turn)
        return turn
    else:
        SAVED_GAME = False
        return "save"

def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT

def drawInfo(board, playerTile, opponentTile, turn):
    # Draws scores and whose turn it is at the bottom of the screen.
    scores = getScoreOfBoard(board, playerTile)
    print(scores)
    print(scores[playerTile])
    scoreSurf = FONT.render("Player1 Score: %s    Player2 Score: %s    %s's Turn" % (str(scores[PLAYER_1]), str(scores[PLAYER_2]), turn.title()), True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def getScoreOfBoard(board, playerTile):
    # Determine the score by counting the tiles.
    opponentTile = getOpponent(playerTile)
    xscore = 0
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == WHITE_TILE:
                xscore += 1
            if board[x][y] == BLACK_TILE:
                oscore += 1
    if playerTile == WHITE_TILE:
        return {WHITE_TILE:xscore, BLACK_TILE:oscore}
    else:
        return {BLACK_TILE:oscore, WHITE_TILE:xscore}


def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
               mousex < (x + 1) * SPACESIZE + XMARGIN and \
               mousey > y * SPACESIZE + YMARGIN and \
               mousey < (y + 1) * SPACESIZE + YMARGIN:
                return (x, y)
    return None

def animateTileChange(tilesToFlip, tileColor, additionalTile):
    # Draw the additional tile that was just laid down. (Otherwise we'd
    # have to completely redraw the board & the board info.)
    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if tileColor == WHITE_TILE:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif tileColor == BLACK_TILE:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for x, y in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()



