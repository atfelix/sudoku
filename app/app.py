#!/Users/Owner1/anaconda3/bin/python3
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
WIDTH = 3 * SUDOKU_WIDTH
HEIGHT = SUDOKU_HEIGHT + 100
BUTTON_WIDTH=12
NO_SHIFT = 96
SHIFT = 97


class App(object):

    def __init__(self, game):
        self.root = tk.Tk()
        self.root.title('Shadow Sudoku')
        self.ui = SudokuUI(self.root, game)
        self.root.geometry('%dx%d' % (WIDTH, HEIGHT))
        self.__undo_stack = self.ui.log
        self.__redo_stack = []
        self.__update_timer()
        self.__make_menus()
        self.root.bind('<Command-z>', lambda _: self.__undo_move())
        self.root.bind('<Command-Shift-z>', lambda _: self.__redo_move())
        self.ui.listbox.bind('<Double-1>', lambda _: self.__undo_n_moves())
        self.root.focus_set()
        self.root.mainloop()


    def __update_timer(self):
        self.ui.draw_timer()
        self.root.after(1000, self.__update_timer)


    def __make_file_item(self, menu, label, state, command, accelerator):

        menu.add_command(label=label,
                         state=state,
                         command=command,
                         accelerator=accelerator)


    def __make_menus(self):
        self.menubar = tk.Menu(self.root)

        menu = tk.Menu(self.menubar, tearoff=0)

        labels = ['New', 'Open', 'Save Game', 'Save Game As']
        states = [tk.NORMAL] * 4
        commands = [self.__new_game, self.__open_game,
                   self.__save_game, self.__save_game_as]
        accelerators = ['Command+' + s for s in ['N', 'O', 'S', 'Shift+S']]

        self.menubar.add_cascade(label='File', menu=menu)


        for _ in zip(labels, states, commands, accelerators):
            self.__make_file_item(menu, *_)

        menu.add_separator()
        self.__make_file_item(menu, 'Exit', tk.NORMAL, self.root.quit, 'Command+Q')


        menu = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label='Edit', menu=menu)

        self.__make_file_item(menu,
                              'Undo',
                              tk.NORMAL,
                              self.__undo_move(),
                              'Command+Z')
        self.__make_file_item(menu,
                              'Redo',
                              tk.NORMAL,
                              self.__redo_move(),
                              'Command+Shift+Z')

        menu.add_separator()

        labels = ['Clear Puzzle', 'Clear Row', 'Clear Column',
                  'Clear Box', 'Clear Cell']
        states = [tk.NORMAL] * 5
        commands = [self.__clear_puzzle, self.__clear_row,
                    self.__clear_column, self.__clear_box,
                    self.__clear_box]
        accelerators = [''] * 5

        for _ in zip(labels, states, commands, accelerators):
            self.__make_file_item(menu, *_)

        menu.add_separator()

        labels = ['Solve Puzzle', 'Solve Row', 'Solve Column',
                'Solve Box', 'Solve Cell']
        commands = [self.__clear_puzzle, self.__clear_row,
                    self.__clear_column, self.__clear_box,
                    self.__clear_box]

        for _ in zip(labels, states, commands, accelerators):
            self.__make_file_item(menu, *_)

        menu.add_separator()

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help')

        self.__make_file_item(menu,
                              label='Tutorials',
                              state=tk.NORMAL,
                              command=self.__generate_tutorials,
                              accelerator='')


    def __new_game(self):
        pass


    def __open_game(self):
        pass


    def __save_game(self):
        pass


    def __save_game_as(self):
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
