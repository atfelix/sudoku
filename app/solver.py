# file:     solver.py
# author:   Adam Felix
# help:     Sudoku Solving with C (Giuluo Zambon)
#           and
#           Programming Sudoku (Wei-Meng Lee)


from sudokugame import SudokuError, SudokuGame



class SudokuSolver(object):

    def __init__(self, boardfile):
        self.game = SudokuGame(boardfile)
        self.__strategies = [[], [], [], []]
        self.__strats_used = []
        self.solve()


    def __str__(self):
        ans = ''
        for i in range(9):
            for j in range(9):
                ans += str(self.game.puzzle[i][j])
            ans += '\n'

        return ans


    def __count_solved(self):
        count = 0

        for i in range(9):
            for j in range(9):
                if self.game.puzzle[i][j] != 0:
                    count += 1

        return count


    def cleanup(self):
        self.__cleanup()


    def __cleanup(self):
        for i in range(9):
            for j in range(9):

                if sum(self.game.entries[i][j]) == 1:

                    for k in range(9):

                        if self.game.entries[i][j][k] == 1:
                            self.game.puzzle[i][j] = k + 1

                    problem = self.__cleanup_at(i, j)

                    if problem:
                        self.__reset_value_at(i, j)


    def __cleanup_at(self, row, col):
        value = self.game.puzzle[row][col]

        for _row in range(9):
            if _row != row:
                self.game.entries[_row][col][value - 1] = 0

        for _col in range(9):
            if _col != col:
                self.game.entries[row][_col][value - 1] = 0

        _row_, _col_ = row // 3, col // 3

        for i in range(3):
            for j in range(3):
                if 3 * _row_ + i != row and 3 * _col_ + j != col:
                    self.game.entries[3 * _row_ + i][3 * _col_ + j][value - 1] = 0

        return not self.__is_valid()


    def __is_valid(self, char=-1, row=-1, col=-1):

        if char == row == col == -1:

            for i in range(9):
                for j in range(9):
                    if sum(self.game.entries[i][j]) == 0:
                        return False

            return True

        else:
            if self.__is_valid_row(char=char, row=row):
                if self.__is_valid_col(char=char, col=col):
                    if self.__is_valid_box(char=char, row=row, col=col):
                        return True

            return False


    def __is_valid_row(self, char, row):
        return all(self.game.puzzle[row][i] != char for i in range(9))


    def __is_valid_col(self, char, col):
        return all(self.game.puzzle[i][col] != char for i in range(9))


    def __is_valid_box(self, char, row, col):
        x, y = row // 3 * 3, col // 3 * 3

        for i in range(3):
            for j in range(3):
                if self.game.puzzle[x + i][y + j] == char:
                    return False

        return True


    def __reset_value_at(self, i, j):
        self.game.puzzle[i][j] = 0
        self.game.find_permissible_entries(start_puzzle=False)


    def __keep_going(self):
        return self.__count_solved() < 81 and self.__is_valid()


    def __count_candidates(self):
        count = 0

        for i in range(9):
            for j in range(9):
                count += sum(self.game.entries[i][j])

        return count


    def solve(self):
        n_candidates = self.__count_candidates()
        n_old_candidates = n_candidates + 1

        while self.__keep_going() and n_candidates < n_old_candidates:
            n_old_candidates = n_candidates

            if self.__keep_going() and not self.__execute_strategies(0):
                if self.__keep_going() and not self.__execute_strategies(1):
                    if self.__keep_going() and not self.__execute_strategies(2):
                        self.__execute_strategies(3)

            n_candidates = self.__count_candidates()

        if self.__keep_going():
            self.__backtrack()


    def __execute_strategies(self, level):
        if level > 3:
            raise SudokuError

        n_initial_candidates = self.__count_candidates()

        i = 0

        while i < len(self.__strategies[level]) and self.__keep_going():
            self.__strategies[level][i](self.game.entries)

            if self.__count_candidates() < n_initial_candidates:
                self.__strats_used.append(10 * level + k)
                return True

        return False


    def __backtrack(self):
        _unassigned, row, col = self.__unassigned()

        if not _unassigned:
            return True

        for x in range(9):

            if self.__is_valid(char=x+1, row=row, col=col):
                self.game.puzzle[row][col] = x + 1

                if self.__backtrack():
                    return True

                self.game.puzzle[row][col] = 0

        return False


    def backtrack(self):
        self.__backtrack()


    def __unassigned(self):
        for i in range(9):
            for j in range(9):
                if self.game.puzzle[i][j] == 0:
                    return True, i, j

        return False, -1, -1



def main():
    solver = SudokuSolver(open('n00b.sudoku', 'r'))
    print(solver)
    solver = SudokuSolver(open('l33t.sudoku', 'r'))
    print(solver)


if __name__ == '__main__':
    main()
