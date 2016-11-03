# file:     unique.py
# author:   Adam Felix
# help:     Sudoku Programming in C (Giulio Zambon)

# Unique strategy:  If one entry appears only once within a unit
#                   (row, column or box), then that cell must be
#                   that entry.


def __unique_row(sudoku_game, row, char):
    count, _col = 0, -1

    for col in range(9):
        if sudoku_game.game.entries[row][col][char] != 0:
            count += 1
            _col = col

    return (True, row, _col) if count == 1 else (False, -1, -1)



def __unique_col(sudoku_game, col, char):
    count, _row = 0, -1

    for row in range(9):
        if sudoku_game.game.entries[row][col][char] != 0:
            count += 1
            _row = row

    return (True, _row, col) if count == 1 else (False, -1, -1)


def __unique_box(sudoku_game, row, col, char):
    count, row, col = 0, row // 3 * 3, col // 3 * 3
    _row, _col = -1, -1

    for i in range(3):
        for j in range(3):
            if sudoku_game.game.entries[row + i][col + j][char] != 0:
                count += 1
                _row, _col = row + i, col + j

    return (True, _row, _col) if count == 1 else (False, -1, -1)


def __unique_cleanup(sudoku_game, i, j, k):
    sudoku_game.game.puzzle[i][j] = k + 1
    sudoku_game.game.entries[i][j] = [0] * 9
    sudoku_game.game.entries[i][j][k] = 1
    sudoku_game.cleanup_at(i, j)


def unique(sudoku_game):
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if (sudoku_game.game.puzzle[i][j] == 0
                        and sudoku_game.game.entries[i][j][k] != 0):

                    if __unique_row(sudoku_game, i, k)[0]:
                        __unique_cleanup(sudoku_game, i, j, k)
                        return True, 'unique_row', i, j, k

                    if __unique_col(sudoku_game, j, k)[0]:
                        __unique_cleanup(sudoku_game, i, j, k)
                        return True, 'unique_col', i, j, k

                    if __unique_box(sudoku_game, i, j, k)[0]:
                        __unique_cleanup(sudoku_game, i, j, k)
                        return True, 'unique_box', i, j, k

    return False, '', -1, -1, -1
