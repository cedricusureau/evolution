def print_first_cell_variable(board):
    for i in board.map:
        for j in i:
            print(vars(j))
            break
        break