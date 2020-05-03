from reversi import *

def main():
    board = init_board()
    turn = "B"

    while (len(getValidMoves(getPlayerPositions(board, turn), board, turn)) != 0) or (len(getValidMoves(getPlayerPositions(board, getOpponent(turn)), board, turn)) != 0):
        print(string_board(board))
        move = input("It's "+turn+" turn. Make a move!: ")
        move = int(move)

        if move in getValidMoves(getPlayerPositions(board, turn), board, turn):
            playMove(move, board, turn)
            if len(getValidMoves(getPlayerPositions(board, getOpponent(turn)), board, getOpponent(turn))) != 0:
                turn = getOpponent(turn)
        else:
            print("Invalid move... try again!")

if __name__ == "__main__":
    main()