#coding=utf-8

import random, sys, pygame, time, copy
from pygame.locals import *
import json
import GameSettings
import os
from pygame import mixer
#import MainMenu

WHITE_TILE = 'W'
BLACK_TILE = 'B'
EMPTY_SPACE = 0
FPS = 10
HINT_TILE = 'HINT_TILE'

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

languages = ["English", "Svenska"]
GameSettings.readDataFromJSON()
#languageIndex = GameSettings.returnLanguageIndex()

soundInfo = GameSettings.volume_numbers
languageIndex = GameSettings.returnLanguageIndex()
print(languageIndex)
hud_names = GameSettings.returnMainMenuTextList(languageIndex)
options = GameSettings.returnOptionsTextList(languageIndex)

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
DARKGRAY   =  (169, 169,169)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BRIGHTBLUE


boardText = None

# Set up the background image.
#boardImage = pygame.image.load('reversiboard.png')
# Use smoothscale() to stretch the board image to fit the entire board:
#boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
#boardImageRect = boardImage.get_rect()
#boardImageRect.topleft = (XMARGIN, YMARGIN)
BGIMAGE = pygame.image.load('reversibackground.png')
# Use smoothscale() to stretch the background image to fit the entire window:
BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
BGIMAGE.blit(pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT)), (0, 0))
#BGIMAGE.blit(boardImage, boardImageRect)

def changeLanguage():
    GameSettings.readDataFromJSON()
    # languageIndex = GameSettings.returnLanguageIndex()
    global soundInfo
    global languageIndex
    soundInfo = GameSettings.volume_numbers
    languageIndex = GameSettings.returnLanguageIndex()
    print(languageIndex)
    global hud_names
    hud_names = GameSettings.returnMainMenuTextList(languageIndex)
    global options
    options = GameSettings.returnOptionsTextList(languageIndex)


def changeScreenSize(event):
    DISPLAYSURF = pygame.display.set_mode((event.w, event.h),
                                          pygame.RESIZABLE)
    global WINDOWWIDTH
    widthDifference = abs(event.w - WINDOWWIDTH)
    #global SPACESIZE
    #if(event.w > WINDOWWIDTH):
        #print('*****************')
        #SPACESIZE = SPACESIZE + widthDifference/16
    #if event.w < WINDOWWIDTH:
        #print('^^^^^^^^^^^^^^^^^')
        #SPACESIZE = SPACESIZE - widthDifference/16

    WINDOWWIDTH = event.w
    print("*****************", event.w)
  #  print("*****************",widthDifference)
    global WINDOWHEIGHT
    heightDifference = abs(event.h - WINDOWHEIGHT)
    WINDOWHEIGHT = event.h
   # print("^^^^^^^^^^^^^^^^^^^^6",heightDifference)
    print("^^^^^^^^^^^^^^^^^^^^6", event.h)

#    global SPACESIZE
#    SPACESIZE = SPACESIZE + widthDifference

    global XMARGIN
    XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
    global YMARGIN
    YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

    #BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))

    #WINDOWHEIGHT = height
    #WINDOWWIDTH = width
#    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
#    BGIMAGE.blit(boardImage, boardImageRect)



def init_pygame():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE, boardText

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
    #DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Reversi')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # print(GameSettings.volume_numbers)
    GameSettings.readDataFromJSON()
    languageIndex = GameSettings.returnLanguageIndex()
    boardText = GameSettings.returnBoardTextList(languageIndex)


    # Set up the background image.
    #boardImage = pygame.image.load('reversiboard.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    #boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    #boardImageRect = boardImage.get_rect()
    #boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('reversibackground.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT)), (0, 0))
    #BGIMAGE.blit(boardImage, boardImageRect)



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
    global BGIMAGE
    #global boardImage, boardImageRect
    #boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    #boardImageRect = boardImage.get_rect()
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    #DISPLAYSURF.blit(BGIMAGE, boardImageRect)
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())
    print(XMARGIN)
    print(YMARGIN)
    # Draw grid lines of the board.
    for x in range(BOARDWIDTH):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        #drawing green rectangle on every tile
        boardRect = pygame.Rect(startx, starty, 50, 50)
        pygame.draw.rect(DISPLAYSURF, GREEN, boardRect)
        cellRect = starty
        for i in range(7):
            cellRect += 50
            rect = pygame.Rect(startx, cellRect, 50, 50)
            pygame.draw.rect(DISPLAYSURF, GREEN, rect)
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx+50, starty), (endx+50, endy))

        #print("StartX",startx,"StartY",starty,)
        #print("EndX",endx,"EndY",endy)

    for y in range(BOARDHEIGHT):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty+50), (endx, endy+50))

    # Draw the black & white tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            textSurf1 = FONT.render((chr(97+y)+str(x)), True, DARKGRAY , TEXTBGCOLOR2)


            DISPLAYSURF.blit(textSurf1,(centerx + 6, centery + 1))
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                else:
                    tileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
            if board[x][y] == HINT_TILE:
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx, centery, int(SPACESIZE / 2),int(SPACESIZE / 2)))


def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)

def enterPlayerTile():
    global PLAYER_1, PLAYER_2
    # Draws the text and handles the mouse click events for letting
    # player1 choose which color they want to be.

    # Create the text.
    textSurf = FONT.render(boardText[0] + ": " + boardText[1], True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    #White Tile Button
    xSurf = BIGFONT.render(boardText[2], True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    #Black Tile Button
    oSurf = BIGFONT.render(boardText[3], True, TEXTCOLOR, TEXTBGCOLOR1)
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

def save_game_dialog(board, turn):
    textSurf = FONT.render(boardText[4], True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    yesSurf = BIGFONT.render(boardText[5], True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    noSurf = BIGFONT.render(boardText[6], True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    save_game(board, turn)
                    return [WHITE_TILE, BLACK_TILE]
                elif noRect.collidepoint( (mousex, mousey) ):
                    PLAYER1 = BLACK_TILE #stating that Player 1 is BLACK
                    PLAYER2 = WHITE_TILE #stating that Player 2 is WHITE
                    return [BLACK_TILE, WHITE_TILE]

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
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
    print(validMoves)
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
    if tile == PLAYER_1:
        playerNumber = 1
    elif tile == PLAYER_2:
        playerNumber = 2
    else:
        print("Invalid User")
    playVoiceSound(chr(97+ystart), str(xstart), playerNumber)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def newGame():
    newGameSurf = FONT.render("Do you want to start a new game", True, TEXTCOLOR, TEXTBGCOLOR1)
    newGameRect = newGameSurf.get_rect()
    newGameRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    #YES Button
    yesSurf = BIGFONT.render("YES", True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    #NO Button
    noSurf = BIGFONT.render("NO", True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint((mousex, mousey)):
                    return True
                elif noRect.collidepoint((mousex, mousey)):
                    return False
        DISPLAYSURF.blit(newGameSurf, newGameRect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()


def makeMoveUsingMouse(board, turn):
    global SAVED_GAME, DISPLAYSURF
#    if getValidMoves(board, turn) == []:
        # If it's the player's turn but they
        # can't move, then end the game.
 #       break

   # make the Surface and Rect objects for the "New Game"
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)

# make the Surface and Rect objects for the "Save Game"
    saveGameSurf = FONT.render(boardText[7], True, TEXTCOLOR, TEXTBGCOLOR2)
    saveGameRect = saveGameSurf.get_rect()
    saveGameRect.topright = (WINDOWWIDTH - 138, 10)

    hintSurf = FONT.render('Hint', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintRect = hintSurf.get_rect()
    hintRect.topright = (WINDOWWIDTH - 250, 10)

    showHints = False
    movexy = None
    while movexy == None and not SAVED_GAME:
        boardToDraw = board

        if showHints:
            boardToDraw = markValidMoves(board, turn)
        else:
            boardToDraw = board

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONDOWN:
                # Handle mouse click events
                mousex, mousey = event.pos
                if newGameRect.collidepoint((mousex, mousey)):
                    # Start a new game
                    option = newGame()
                    if option == True:
                        return("new game")
                if saveGameRect.collidepoint((mousex, mousey)):
                    # Save the game
                    save_game_dialog(board, turn)
                    return turn
                if hintRect.collidepoint((mousex, mousey)):
                    # Mark Hints
                    showHints = True
                movexy = getSpaceClicked(mousex, mousey)
                if movexy != None and not isValidMove(board, turn, movexy[0], movexy[1]):
                    movexy = None
                    sound_folder_path = os.path.dirname((os.path.realpath(__file__))) + "\Voice\\" + languages[
                        languageIndex]
                    soundFile = sound_folder_path + "\\" + "invalidmove.wav"
                    mixer.music.load(soundFile)
                    mixer.music.set_volume(soundInfo[1])
                    mixer.music.play(0)
                    while pygame.mixer.music.get_busy():
                        pass
            if event.type == pygame.VIDEORESIZE:
                if(event.w > 300 and event.h > 300):
                    changeScreenSize(event)
                else:
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


        # Draw the game board.
        drawBoard(boardToDraw)
        drawInfo(boardToDraw, turn, getOpponent(turn), turn)

        # Draw the "New Game" and "Save Game" buttons.
        DISPLAYSURF.blit(newGameSurf, newGameRect)
        DISPLAYSURF.blit(saveGameSurf, saveGameRect)
        DISPLAYSURF.blit(hintSurf, hintRect)

        MAINCLOCK.tick(FPS)
        pygame.display.update()

    # Make the move and end the turn.
    if not SAVED_GAME:
        finalx, finaly = undo_redo_done_move(turn, (movexy[0], movexy[1]), board)
        makeMove(board, turn, finalx, finaly, True)
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
    scoreSurf = FONT.render("%s %s: %s    %s %s: %s    %s's %s" % (boardText[0], boardText[8], str(scores[PLAYER_1]),
                                                                     boardText[9], boardText[8], str(scores[PLAYER_2]),
                                                                     turn.title(), boardText[10]), True, TEXTCOLOR)
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



def undo_redo_done_move(tileColor, pixel_coord, board):
    undoStack = []
    redoStack = []
    action = ()
    played = True

    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardToPixelCoord(pixel_coord[0], pixel_coord[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    undoStack.append((additionalTileColor, (additionalTileX, additionalTileY)))

    textSurf = FONT.render(boardText[11], True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), 40)

    undoSurf = FONT.render('UNDO', True, TEXTCOLOR, TEXTBGCOLOR1)
    undoRect = undoSurf.get_rect()
    undoRect.center = (int(WINDOWWIDTH / 2) - 60, 80)

    redoSurf = FONT.render('REDO', True, TEXTCOLOR, TEXTBGCOLOR1)
    redoRect = redoSurf.get_rect()
    redoRect.center = (int(WINDOWWIDTH / 2), 80)

    doneSurf = FONT.render(boardText[12], True, TEXTCOLOR, TEXTBGCOLOR1)
    doneRect = doneSurf.get_rect()
    doneRect.center = (int(WINDOWWIDTH / 2) + 60, 80)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if undoRect.collidepoint((mousex, mousey)): #When UNDO is clicked
                    if undoStack != []:
                        action = undoStack.pop()
                        pygame.draw.circle(DISPLAYSURF, GREEN, (action[1][0], action[1][1]),
                                           int(SPACESIZE / 2) - 4)
                        pygame.display.update()
                        redoStack.append(action)
                        played = False
                elif redoRect.collidepoint((mousex, mousey)) and redoStack != []: #When REDO is clicked
                    action = redoStack.pop()
                    pygame.draw.circle(DISPLAYSURF, action[0], (action[1][0], action[1][1]),
                                       int(SPACESIZE / 2) - 4)
                    pygame.display.update()
                    undoStack.append(action)
                    played = True
                elif doneRect.collidepoint((mousex, mousey)): #When DONE is clicked
                    if played:
                        return pixel_coord[0], pixel_coord[1]
                elif undoStack == []:
                    #for event in pygame.event.get():  # event handling loop
                        #if event.type == MOUSEBUTTONDOWN:
                            # Handle mouse click events
                    mousex, mousey = event.pos
                    pixel_coord = getSpaceClicked(mousex, mousey)
                    if pixel_coord != None and not isValidMove(board, tileColor, pixel_coord[0], pixel_coord[1]):
                        pixel_coord = None
                    additionalTileX, additionalTileY = translateBoardToPixelCoord(pixel_coord[0], pixel_coord[1])
                    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY),
                                       int(SPACESIZE / 2) - 4)
                    pygame.display.update()
                    redoStack.pop()
                    undoStack.append((additionalTileColor, (additionalTileX, additionalTileY)))
                    played = True

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(undoSurf, undoRect)
        DISPLAYSURF.blit(redoSurf, redoRect)
        DISPLAYSURF.blit(doneSurf, doneRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

def playVoiceSound(alpha, numeric, playerNumber):
    #self.textContainer.lower()
    sound_folder_path = os.path.dirname((os.path.realpath(__file__))) + "\Voice\\" + languages[languageIndex]

    soundFiles = []
    file_extension = ".wav"
    if playerNumber == 1:
        soundFiles.append(sound_folder_path + "\\" + "player_1" + file_extension)
    else:
        soundFiles.append(sound_folder_path + "\\" + "player_2" + file_extension)

    soundFiles.append(sound_folder_path + "\\" + alpha + file_extension)
    soundFiles.append(sound_folder_path + "\\" + numeric + file_extension)

    for i in range(len(soundFiles)):
        mixer.music.load(soundFiles[i])
        mixer.music.set_volume(soundInfo[1])
        mixer.music.play(0)
        while pygame.mixer.music.get_busy():
            pass

def markValidMoves(board, tile):
    duplicateBoard = copy.deepcopy(board)

    #Mark valid moves as hint tiles
    for x, y in getValidMoves(duplicateBoard, tile):
        duplicateBoard[x][y] = HINT_TILE
    return duplicateBoard
