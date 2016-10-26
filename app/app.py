# file:     app.py
# author:   Adam Felix
# help:     new coder tutorials

import argparse
import time
import tkinter as tk

from gui import SudokuUI
from sudokugame import SudokuGame

### Constants

BOARDS = ['debug', 'n00b', 'l33t', 'error']
MARGIN = 10
SIDE = 60
SUDOKU_WIDTH = SUDOKU_HEIGHT = MARGIN * 2 + SIDE * 9
WIDTH = 2.5 * SUDOKU_WIDTH
HEIGHT = SUDOKU_HEIGHT + 100
BUTTON_WIDTH=12
NO_SHIFT = 96
SHIFT = 97


class App(object):

    def __init__(self, game):
        self.root = tk.Tk()
        self.ui = SudokuUI(self.root, game)
        self.root.geometry('%dx%d' % (WIDTH, HEIGHT))
        self.__undo_stack = self.ui.log
        self.__redo_stack = []
        self.__update_timer()
        self.__make_menus()
        self.root.bind('<Command-z>', lambda _: self.__undo_move())
        self.root.bind('<Command-Shift-z>', lambda _: self.__redo_move())
        self.ui.listbox.bind('<Double-1>', lambda _: self.__undo_n_moves())
        self.root.mainloop()


    def __update_timer(self):
        self.ui.draw_timer()
        self.root.after(1000, self.__update_timer)


    def __make_menus(self):
        self.menubar = tk.Menu(self.root)

        menu = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label='File', menu=menu)
        menu.add_command(label='New',
                         state=tk.NORMAL,
                         command=self.__new_game,
                         accelerator='Command+N')
        menu.add_command(label='Open',
                         state=tk.NORMAL,
                         command=self.__open_game,
                         accelerator='Command+O')
        menu.add_command(label='Save Game',
                         state=tk.NORMAL,
                         command=self.__save_game,
                         accelerator='Command+S')
        menu.add_command(label='Save Game As',
                         state=tk.NORMAL,
                         command=self.__save_as,
                         accelerator='Command+Shift+S')
        menu.add_separator()
        menu.add_command(label='Exit',
                         state=tk.NORMAL,
                         command=self.root.quit,
                         accelerator='Command+Q')

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Edit', menu=menu)
        menu.add_command(label='Undo',
                         state=tk.NORMAL,
                         command=self.__undo_move(),
                         accelerator='Command+Z')
        menu.add_command(label='Redo',
                         state=tk.NORMAL,
                         command=self.__redo_move(),
                         accelerator='Command+Shift+Z')
        self.root.config(menu=self.menubar)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=menu)
        menu.add_command(label='Clear Puzzle',
                         state=tk.NORMAL,
                         command=self.__clear_puzzle)
        menu.add_command(label='Clear Row',
                         state=tk.NORMAL,
                         command=self.__clear_row)
        menu.add_command(label='Clear Column',
                         state=tk.NORMAL,
                         command=self.__clear_column)
        menu.add_command(label='Clear Box',
                         state=tk.NORMAL,
                         command=self.__clear_box)
        menu.add_command(label='Clear Cell',
                         state=tk.NORMAL,
                         command=self.__clear_cell)

        menu.add_separator()

        menu.add_command(label='Solve Puzzle',
                         state=tk.NORMAL,
                         command=self.__solve_puzzle)
        menu.add_command(label='Solve Row',
                         state=tk.NORMAL,
                         command=self.__solve_row)
        menu.add_command(label='Solve Column',
                         state=tk.NORMAL,
                         command=self.__solve_column)
        menu.add_command(label='Solve Box',
                         state=tk.NORMAL,
                         command=self.__solve_box)
        menu.add_command(label='Solve Cell',
                         state=tk.NORMAL,
                         command=self.__solve_cell)

        menu.add_separator()

        menu.add_command(label='Tutorials',
                         state=tk.NORMAL,
                         command=self.__generate_tutorials)




    def __new_game(self):
        pass


    def __open_game(self):
        pass


    def __save_game(self):
        pass


    def __save_as(self):
        pass


    def __generate_tutorials(self):
        pass


    def __solve_puzzle(self):
        pass


    def __solve_row(self):
        pass


    def __solve_column(self):
        pass


    def __solve_box(self):
        pass


    def __solve_cell(self):
        pass


    def __clear_puzzle(self):
        pass


    def __clear_row(self):
        pass


    def __clear_column(self):
        pass


    def __clear_box(self):
        pass


    def __clear_cell(self):
        pass



    def __undo_move(self):
        if self.__undo_stack:
            self.ui.listbox.delete(0)
            number = self.__undo_stack.pop()
            self.__redo_stack.append(number)

            if number > 0:

                row, col = number // 100 - 1, (number % 100) // 10 - 1

                for i in range(len(self.__undo_stack) - 1, -1, -1):
                    x = self.__undo_stack[i]
                    x_row, x_col = x // 100 - 1, (x % 100) // 10 - 1

                    if x_row == row and x_col == col:
                        self.ui.game.puzzle[row][col] = x % 10
                        break

                else:
                    self.ui.game.puzzle[row][col] = 0

            else:
                number *= -1

                row, col, entry = number // 100 - 1, (number % 100) // 10 - 1, number % 10

                self.ui.game.puzzle[row][col] = entry

            self.ui.draw_puzzles()


    def __undo_n_moves(self):
        try:
            index = self.ui.listbox.curselection()[0]
        except IndexError:
            index = -1


        for i in range(index + 1):
            self.__undo_move()


    def __redo_move(self):
        if self.__redo_stack:
            number = self.__redo_stack.pop()
            self.__undo_stack.append(number)

            if number > 0:

                row, col = number // 100 - 1, (number % 100) // 10 - 1
                entry = number % 10

                self.ui.game.puzzle[row][col] = entry

                string = 'Entered %d in row %d column % d' % (entry, row + 1, col + 1)

            else:
                number *= -1
                row, col, entry = number // 100 - 1, (number % 100) // 10 - 1, number % 10

                self.ui.game.puzzle[row][col] = 0

                string = 'Deleted %d in row %d column % d' % (entry, row + 1, col + 1)

            self.ui.listbox.insert(0, string)

            self.ui.draw_puzzles()



def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.py <board name>
    where 'board name' must be in the BOARD list
    """

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--board',
                             help='Desired board name',
                             type=str,
                             choices=BOARDS,
                             required=True)

    args = vars(arg_parser.parse_args())

    return args['board']

def main():
    board_name = parse_arguments()

    with open('%s.sudoku' % board_name, 'r') as boards_file:

        game = SudokuGame(boards_file)
        game.start()

        App(game)

if __name__ == '__main__':
    main()
