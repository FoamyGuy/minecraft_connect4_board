import random
import numpy as np
import mcpi.minecraft as minecraft
import mcpi.vec3 as vec3
import mcpi.block as Block
import mcpi_writing as mcw

# Where we will pu
winner_output_pos = vec3.Vec3(-91, 1, 265)

# bottom left corner of board.
board_pos = vec3.Vec3(-94, 0, 266)

# char representations of board pieces
pieces = ['X', 'O']

mc = minecraft.Minecraft.create()


def read_mc_board():
    board = [[' ' for x in range(7)] for x in range(6)]
    for y in range(6):
        for x in range(7):
            #print(y)
            block = mc.getBlock(board_pos.x - x, board_pos.y + y, board_pos.z)
            #print ("(%s,%s,%s) = %s" % (board_pos.x - x, board_pos.y + y, board_pos.z, block))
            if block == Block.SAND.id:
                board[5-y][x] = 'X'
            elif block == Block.GRAVEL.id:
                board[5-y][x] = 'O'
            elif block == Block.AIR.id:
                board[5-y][x] = ' '
    return board

def clear_mc_board():
    for y in range(6):
        for x in range(7):
            mc.setBlock(board_pos.x - x, board_pos.y + y, board_pos.z, 0)


def draw_mc_board(board):
    for row in board:
        for col in row:
            if board[col][row] == 'X':
                mc.setBlock(board_pos.x+col, board_pos.y + row)


def check_win(board):
    win_check = build_win_check_array(board)
    x_wins = 0
    o_wins = 0
    for row in win_check:
        if 'XXXX' in row:
            x_wins += 1
        if 'OOOO' in row:
            o_wins += 1
    print ("x wins: %s" % (x_wins))
    print ("o wins: %s" % (o_wins))
    if x_wins > 0 and x_wins > o_wins:
        return 'X'
    if o_wins > 0 and o_wins > x_wins:
        return 'O'
    return ''

def build_win_check_array(board):
    win_check_array = []
    # Horizontals
    for row in board:
        win_check_array.append(''.join(row))

    # Verticals
    for row in rotate_board(board):
        win_check_array.append(''.join(row))

    # Diagonals
    x,y = 6,7
    a = np.array(board)
    print(a)

    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
    diag_list = [n.tolist() for n in diags]

    for row in diag_list:
        if len(row) >= 4:
            win_check_array.append(''.join(row))

    return win_check_array


def rotate_board(original):
    rotated = zip(*original[::-1])
    return rotated


def random_board():
    board = [[' ' for x in range(7)] for x in range(6)]
    for y in range(6):
        for x in range(7):
            board[y][x] = random.choice(pieces)
    return board


if __name__ == "__main__":
    clear_mc_board()
    mc.setBlock(winner_output_pos, 0)
    try:
        while True:
            board = read_mc_board()
            result = check_win(board)
            if result == 'X':
                mc.setBlock(winner_output_pos, Block.SAND)
                break
            elif result == 'O':
                mc.setBlock(winner_output_pos, Block.GRAVEL)
                break
    except KeyboardInterrupt:
        print("stopping")
    print("game over")
    """
    board = read_mc_board()
    for row in board:
        print row
    check_win(board)
    """



