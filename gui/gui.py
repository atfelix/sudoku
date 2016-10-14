# file:     gui/gui.py
# author:   Adam Felix
# help:     new coder tutorials

import argparse

from tkinter import Tk, Canvas, Frame, Label, Listbox, Button, Scrollbar
from tkinter import BOTH, TOP, BOTTOM, LEFT, RIGHT, X, Y, N, E, S, W, VERTICAL

### Constants

BOARDS = ['debug', 'n00b', 'l33t', 'error']
MARGIN = 10
SIDE = 60
SUDOKU_WIDTH = SUDOKU_HEIGHT = MARGIN * 2 + SIDE * 9
WIDTH = 2.5 * SUDOKU_WIDTH
HEIGHT = SUDOKU_HEIGHT + 75
BUTTON_WIDTH=12

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


    def start(self):
        self.game_over = False
        self.puzzle = []

        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])


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


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board
    and accepting user input.
    """

    def __init__(self, parent, game):

        self.game = game
        self.parent = parent

        Frame.__init__(self, parent)

        self.row, self.col = -1, -1

        self.__initUI()


    def __initUI(self):

        self.parent.title('Shadow Sudoku')

        self.grid()

        # The sudoku grid

        self.canvas = Canvas(self,
                             width=SUDOKU_WIDTH,
                             height=SUDOKU_HEIGHT,
                             highlightthickness=0)

        self.canvas.grid(column=0, row=0, columnspan=15, rowspan=15)

        # The shadow sudoku grid

        self.shadow = Canvas(self,
                                  width=SUDOKU_WIDTH,
                                  height=SUDOKU_HEIGHT,
                                  highlightthickness=0)

        self.shadow.grid(column=25, row=0, columnspan=15, rowspan=15)

        self.__make_buttons()
        self.__make_activity_log_title()
        self.__make_log()

        self.__draw_activity_log()

        self.__set_cursor()

        self.__draw_puzzle()

        self.__draw_shadow_puzzle()

        # Bind self.__cell_clicked to a mouse click and
        # self.__key_pressed to a key being pressed

        self.canvas.bind('<Button-1>', self.__cell_clicked)
        self.canvas.bind('<Key>', self.__key_pressed)

        self.shadow.bind('<Button-1>', self.__shadow_cell_clicked)
        self.shadow.bind('<Key>', self.__shadow_key_pressed)


    def __make_buttons(self):

        self.__make_clear_buttons()
        self.__make_solve_buttons()


    def __make_clear_buttons(self):

        clear_puzzle_button = Button(self,
                                     text='Clear Puzzle',
                                     command=self.__clear_puzzle,
                                     width=BUTTON_WIDTH)
        clear_puzzle_button.grid(column=2, row=30)

        clear_row_button = Button(self,
                                  text='Clear Row',
                                  command=self.__clear_row,
                                  width=BUTTON_WIDTH)
        clear_row_button.grid(column=4, row=30)

        clear_column_button = Button(self,
                                     text='Clear Column',
                                     command=self.__clear_column,
                                     width=BUTTON_WIDTH)
        clear_column_button.grid(column=6, row=30)

        clear_box_button = Button(self,
                                  text='Clear Box',
                                  command=self.__clear_box,
                                  width=BUTTON_WIDTH)
        clear_box_button.grid(column=8, row=30)

        clear_cell_button = Button(self,
                                   text='Clear Cell',
                                   command=self.__clear_cell,
                                   width=BUTTON_WIDTH)
        clear_cell_button.grid(column=10, row=30)


    def __make_solve_buttons(self):

        solve_puzzle_button = Button(self,
                                     text='Solve Puzzle',
                                     command=self.__solve_puzzle,
                                     width=BUTTON_WIDTH)
        solve_puzzle_button.grid(column=2, row=25)

        solve_row_button = Button(self,
                                  text='Solve Row',
                                  command=self.__solve_row,
                                  width=BUTTON_WIDTH)
        solve_row_button.grid(column=4, row=25)

        solve_column_button = Button(self,
                                     text='Solve Column',
                                     command=self.__solve_column,
                                     width=BUTTON_WIDTH)
        solve_column_button.grid(column=6, row=25)

        solve_box_button = Button(self,
                                     text='Solve Box',
                                     command=self.__solve_box,
                                     width=BUTTON_WIDTH)
        solve_box_button.grid(column=8, row=25)

        solve_cell_button = Button(self,
                                     text='Solve Cell',
                                     command=self.__solve_cell,
                                     width=BUTTON_WIDTH)
        solve_cell_button.grid(column=10, row=25)


    def __make_activity_log_title(self):

        log_title = Label(self,
                          text='Activity Log',
                          font=('Palatino', 20),
                          justify=LEFT)
        log_title.grid(column=20, row=0)


    def __make_log(self):
        self.log = []


    # Helper function for __initUI

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3 x 3 squares
        """

        for i in range(10):
            color = 'blue' if i % 3 == 0 else 'light gray'
            width = 3 if i % 3 == 0 else 1

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = SUDOKU_HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = SUDOKU_WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=width)


    def __draw_activity_log(self):

        self.scrollbar = Scrollbar(self,
                                   orient=VERTICAL,
                                   elementborderwidth=2)

        self.listbox = Listbox(self,
                               yscrollcommand=self.scrollbar.set,
                               borderwidth=0,
                               font=('Palatino', 15),
                               width=25,
                               height=29)

        for string in self.log:
            self.listbox.insert(0, string)

        self.listbox.grid(column=20, row=1)
        self.scrollbar.grid(column=21, row=1, sticky=N + S)
        self.scrollbar['command'] = self.listbox.yview


    def __draw_puzzle(self):

        #clear the puzzle first

        self.canvas.delete('numbers')

        for i in range(9):
            for j in range(9):
                x = MARGIN + j * SIDE + SIDE // 2
                y = MARGIN + i * SIDE + SIDE // 2
                x0 = MARGIN + j * SIDE + 1
                y0 = MARGIN + i * SIDE + 1
                x1 = MARGIN + (j + 1) * SIDE - 1
                y1 = MARGIN + (i + 1) * SIDE - 1

                answer = self.game.puzzle[i][j]
                original = self.game.start_puzzle[i][j]

                if answer == original != 0:
                    bgcolor, color = 'black', 'white'

                elif self.row == i or self.col == j:
                    bgcolor, color = 'light cyan', 'black'

                elif self.row // 3 == i // 3 and self.col // 3 == j // 3:
                    bgcolor, color = 'light cyan', 'black'

                else:
                    bgcolor, color = 'white', 'black'

                self.canvas.create_rectangle(x0,
                                             y0,
                                             x1,
                                             y1,
                                             fill=bgcolor,
                                             outline=bgcolor)
                self.canvas.create_text(x,
                                        y,
                                        text=answer if answer != 0 else '',
                                        tags='numbers',
                                        fill=color)
        self.__draw_cursor()
        self.__draw_grid()


    def __draw_shadow_puzzle(self):
        pass

    def __set_cursor(self):
        if (self.row, self.col) == (-1, -1):
            for i in range(9):
                for j in range(9):
                    if self.game.start_puzzle[i][j] == 0:
                        self.row, self.col = i, j
                        return

    def __draw_cursor(self):

        """
        Highlight the particular cell that the user has clicked on.
        """

        self.canvas.delete('cursor')

        if self.row >= 0 and self.col >=0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1

            self.canvas.create_rectangle(x0,
                                         y0,
                                         x1,
                                         y1,
                                         outline='dark cyan',
                                         tags='cursor',
                                         width=3)

    def __draw_victory(self):

        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7

        self.canvas.create_oval(x0,
                                y0,
                                x1,
                                y1,
                                tags='victory',
                                fill='dark green',
                                outline='black')

        x = y = MARGIN + 4 * SIDE + SIDE // 2

        self.canvas.create_text(x,
                                y,
                                text='You win!',
                                tags='winner',
                                fill='white',
                                font=('Palatino', 32))


    def __clear_puzzle(self):
        self.game.start()
        self.canvas.delete('victory')
        self.__draw_puzzle()


    def __clear_row(self):
        pass


    def __clear_column(self):
        pass


    def __clear_box(self):
        pass


    def __clear_cell(self):
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

   # Event handlers

    def __cell_clicked(self, event):

        if self.game.game_over:
            return

        x, y = event.x, event.y

        if (MARGIN < x < SUDOKU_WIDTH - MARGIN and MARGIN < y < SUDOKU_HEIGHT - MARGIN):
            self.canvas.focus_set()         # get the focus of the app

            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            #if (row, col) == (self.row, self.col):
            #    self.row, self.col = -1, -1
            if self.game.start_puzzle[row][col] == 0:
                self.row, self.col = row, col

        self.__draw_puzzle()


    def __key_pressed(self, event):
        if self.game.game_over:
            return

        if self.row >= 0 and self.col >= 0:

            if event.keysym in '123456789':
                self.game.puzzle[self.row][self.col] = int(event.keysym)

                string = 'Entered %c in row %d column %d' % (event.keysym,
                                                             self.row + 1,
                                                             self.col + 1)

                if not self.log or string != self.log[-1]:
                    self.log.append(string)
                    self.listbox.insert(0, string)

            elif event.keysym == 'Left':
                self.col = (self.col - 1) % 9

                while self.game.start_puzzle[self.row][self.col] != 0:
                    self.col = (self.col - 1) % 9

            elif event.keysym == 'Right':
                self.col = (self.col + 1) % 9

                while self.game.start_puzzle[self.row][self.col] != 0:
                    self.col = (self.col + 1) % 9

            elif event.keysym == 'Up':
                self.row = (self.row - 1) % 9

                while self.game.start_puzzle[self.row][self.col] != 0:
                    self.row = (self.row - 1) % 9

            elif event.keysym == 'Down':
                self.row = (self.row + 1) % 9

                while self.game.start_puzzle[self.row][self.col] != 0:
                    self.row= (self.row + 1) % 9

            self.__draw_puzzle()

            if self.game.check_win():
                self.__draw_victory()

    def __shadow_cell_clicked(self, event):
        pass


    def __shadow_key_pressed(self, event):
        pass



def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.pu <board name>
    where 'board name' must be in the BOARD list
    """

    arg_parser = argparse.ArgumentParser()
    arg_parser .add_argument('--board',
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

        root = Tk()
        SudokuUI(root, game)
        root.geometry('%dx%d' % (2.5 * WIDTH, HEIGHT))
        root.mainloop()

if __name__ == '__main__':
    main()
