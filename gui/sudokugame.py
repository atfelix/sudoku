# file:     gui/sudokugame.py
# author:   Adam Felix
# help:     new coder tutorials


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass


class SudokuBoard(object):
    """
    Sudoku Board representation
    """

    def __init__(self, board_file):
        self.board = self.__create_board(board_file)


    def __create_board(self, board_file):
        board = []

        for line in board_file:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError(
                        'Each line in the sudoku puzzle must be 9 chars long.'
                        )

            board.append([])

            for ch in line:

                if not ch.isdigit():
                    raise SudokuError(
                            'Valid characters for the puzzle must be 0-9.'
                            )

                board[-1].append(int(ch))

        if len(board) != 9:
            raise SudokuError('Each puzzle must be 9 lines long.')

        return board


class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board
    and checking whether the puzzle is completed.
    """

    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board
        self.start()

        self.entries = []
        for i in range(9):
            self.entries.append([])
            for j in range(9):
                self.entries[-1].append([-1] * 9)

        self.__find_permissible_entries()


    def start(self):
        self.game_over = False
        self.puzzle = []
        self.__reset_entries()


    def __reset_entries(self):
        self.entries = []
        for i in range(9):
            self.puzzle.append([])
            self.entries.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])
                self.entries[-1].append([-1] * 9)

        self.__find_permissible_entries()


    def update_entries(self):
        for i in range(9):
            for j in range(9):

                if self.start_puzzle[i][j] != 0:
                    continue

                if self.puzzle[i][j] != 0:
                    for k in range(9):
                        if k + 1 != self.puzzle[i][j] and self.entries[i][j][k] != 0:
                            self.entries[i][j][k] = 2

                    self.entries[i][j][self.puzzle[i][j] - 1] = 1

        for i in range(9):
            for j in range(9):

                if self.start_puzzle[i][j] != 0 or self.puzzle[i][j] != 0:
                    continue

                for value in range(9):
                    if self.entries[i][j][value] in [0, 3]:
                        continue

                    if self.entries[i][j][value] == 1:

                        for row in range(9):
                            if row == i:
                                continue
                            if self.puzzle[row][j] == value + 1:
                                self.entries[i][j][value] = 2

                        for col in range(9):
                            if col == j:
                                continue
                            if self.puzzle[i][col] == value + 1:
                                self.entries[i][j][value] = 2

                        _row, _col = i // 3, j // 3


                        for ii in range(3):
                            new_row = 3 * _row + ii
                            for jj in range(3):
                                new_col = 3 * _col + jj
                                if new_row == i and new_col == j:
                                    continue
                                if self.puzzle[new_row][new_col] == value + 1:
                                    self.entries[i][j][value] = 2

                    if self.entries[i][j][value] == 2:

                        change = True

                        for row in range(9):
                            if row == i:
                                continue
                            if self.puzzle[row][j] == value + 1:
                                change &= False

                        for col in range(9):
                            if col == j:
                                continue
                            if self.puzzle[i][col] == value + 1:
                                change &= False

                        _row, _col = i // 3, j // 3

                        for ii in range(3):
                            new_row = 3 * _row + ii
                            for jj in range(3):
                                new_col = 3 * _col + jj
                                if new_row == i and new_col == j:
                                    continue
                                if self.puzzle[new_row][new_col] == value + 1:
                                    change &= False

                        if change:
                            self.entries[i][j][value] = 1

            if self.puzzle[i][j] == 0:
                continue

            for k in range(9):
                if k != self.puzzle[i][j] - 1:
                    self.entries[i][j][k] = 2


    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False

        for column in range(9):
            if not self.__check_column(column):
                return False

        for row in range(3):
            for column in range(3):
                if not self.__check_box(row, column):
                    return False

        self.game_over = True

        return True


    def __check_block(self, block):
        return set(block) == set(range(1, 10))


    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])


    def __check_column(self, column):
        return self.__check_block([self.puzzle[row][column] for row in range(9)])


    def __check_box(self, row, column):
        box = []
        for r in range(row * 3, (row + 1) * 3):
            for c in range(column * 3, (column + 1) * 3):
                box.append(self.puzzle[r][c])

        return self.__check_block(box)


    def __find_permissible_entries(self):

        for i in range(9):
            for j in range(9):

                value = self.start_puzzle[i][j]

                if value != 0:
                    self.entries[i][j] = [0] * 9
                    self.entries[i][j][value - 1] = 1

                    self.__helper_find(i, j, value)

        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if self.entries[i][j][k] == -1:
                        self.entries[i][j][k] = 1


    def __helper_find(self, row, col, value):
        for x in range(9):
            if x != col:
                self.entries[row][x][value - 1] = 0

            if x != row:
                self.entries[x][col][value - 1] = 0

        i, j = row // 3, col // 3

        for ii in range(3):
            for jj in range(3):
                if 3 * i + ii != row or 3 * j + jj != col:
                    self.entries[3 * i + ii][3 * j + jj][value - 1] = 0
