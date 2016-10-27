# file:     solver.py
# author:   Adam Felix
# help:     Sudoku Solving with C (Giuluo Zambon)
#           and
#           Programming Sudoku (Wei-Meng Lee)


from sudokugame import SudokuGame



class SudokuSolver(object):

    def __init__(self, boardfile):
        self.game = SudokuGame(boardfile)


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


    def __is_valid(self):
        for i in range(9):
            for j in range(9):
                if sum(self.game.entries[i][j]) == 0:
                    return False

        return True


    def __reset_value_at(self, i, j):
        self.game.puzzle[i][j] = 0
        self.game.find_permissible_entries(start_puzzle=False)


    def __keep_going(self):
        return self.__count_solved() < 81 and self.is_valid()


    def __count_candidates(self):
        count = 0

        for i in range(9):
            for j in range(9):
                count += sum(self.game.entries[i][j])

        return count


    def solve(self):
        pass



def main():
    solver = SudokuSolver(open('n00b.sudoku', 'r'))
    print(solver)
    print('=' * 100)
    solver.cleanup()
    print(solver)


if __name__ == '__main__':
    main()
