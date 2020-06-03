#coding=utf-8

from reversi import *

def main():
#    FONT = pygame.font.Font('freesansbold.ttf', 16)
#    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
    init_pygame()
    board = getNewBoard()

    init_board(board)
    #print(board)


    # Draw the starting board and ask the player what color they want.
    drawBoard(board)

    playerTile, opponentTile = enterPlayerTile()
    print(playerTile)
    turn = playerTile


    while (len(getValidMoves(board, turn)) != 0) or (len(getValidMoves(board, getOpponent(turn))) != 0):
        turn = makeMoveUsingMouse(board, turn)
#        move = makeMove(board, turn, x, y, True)

 #       if move in getValidMoves(board, turn):
  #          playMove(move, board, turn)
  #          if len(getValidMoves(board, getOpponent(turn))) != 0:
  #              turn = getOpponent(turn)
  #      else:
  #          print("Invalid move... try again!")

if __name__ == "__main__":
    main()