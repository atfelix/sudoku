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
        self.start()

        self.entries = []
        for i in range(9):
            self.entries.append([])
            for j in range(9):
                self.entries[-1].append([-1] * 9)

        self.__find_permissible_entries()
        for x in self.entries:
            print(x)


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



class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board
    and accepting user input.
    """

    def __init__(self, parent, game):

        self.game = game
        self.parent = parent

        Frame.__init__(self, parent)

        self.__initUI()


    def __initUI(self):

        self.parent.title('Shadow Sudoku')

        self.grid()

        # The sudoku grid

        self.canvas = Canvas(self,
                             width=SUDOKU_WIDTH,
                             height=SUDOKU_HEIGHT,
                             highlightthickness=0)

        self.canvas.grid(column=0, row=1, columnspan=15, rowspan=15)
        self.canvas.row, self.canvas.col = -1, -1

        # The shadow sudoku grid

        self.shadow = Canvas(self,
                             width=SUDOKU_WIDTH,
                             height=SUDOKU_HEIGHT,
                             highlightthickness=0)

        self.shadow.grid(column=25, row=1, columnspan=15, rowspan=15)
        self.shadow.row, self.shadow.col = -1, -1
        self.shadow.subrow, self.shadow.subcol = -1, -1

        self.__make_buttons()
        self.__draw_activity_log_title()
        self.__draw_canvas_title()
        self.__draw_shadow_title()

        self.__make_log()
        self.__draw_activity_log()

        self.__set_cursor()
        self.__set_shadow_cursor()
        self.__set_drawing_puzzle_rectangles()
        self.__set_drawing_shadow_puzzle_rectangles()

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
        clear_puzzle_button.grid(column=0, row=30)

        clear_row_button = Button(self,
                                  text='Clear Row',
                                  command=self.__clear_row,
                                  width=BUTTON_WIDTH)
        clear_row_button.grid(column=2, row=30)

        clear_column_button = Button(self,
                                     text='Clear Column',
                                     command=self.__clear_column,
                                     width=BUTTON_WIDTH)
        clear_column_button.grid(column=4, row=30)

        clear_box_button = Button(self,
                                  text='Clear Box',
                                  command=self.__clear_box,
                                  width=BUTTON_WIDTH)
        clear_box_button.grid(column=6, row=30)

        clear_cell_button = Button(self,
                                   text='Clear Cell',
                                   command=self.__clear_cell,
                                   width=BUTTON_WIDTH)
        clear_cell_button.grid(column=8, row=30)


    def __make_solve_buttons(self):

        solve_puzzle_button = Button(self,
                                     text='Solve Puzzle',
                                     command=self.__solve_puzzle,
                                     width=BUTTON_WIDTH)
        solve_puzzle_button.grid(column=0, row=25)

        solve_row_button = Button(self,
                                  text='Solve Row',
                                  command=self.__solve_row,
                                  width=BUTTON_WIDTH)
        solve_row_button.grid(column=2, row=25)

        solve_column_button = Button(self,
                                     text='Solve Column',
                                     command=self.__solve_column,
                                     width=BUTTON_WIDTH)
        solve_column_button.grid(column=4, row=25)

        solve_box_button = Button(self,
                                     text='Solve Box',
                                     command=self.__solve_box,
                                     width=BUTTON_WIDTH)
        solve_box_button.grid(column=6, row=25)

        solve_cell_button = Button(self,
                                     text='Solve Cell',
                                     command=self.__solve_cell,
                                     width=BUTTON_WIDTH)
        solve_cell_button.grid(column=8, row=25)


    def __draw_activity_log_title(self):

        log_title = Label(self,
                          text='Activity Log',
                          font=('Palatino', 20),
                          justify=LEFT)
        log_title.grid(column=SUDOKU_WIDTH // SIDE + 11, row=0)

    def __draw_canvas_title(self):

        canvas_title = Label(self,
                             text='Sudoku Puzzle',
                             font=('Palatino', 20),
                             justify=LEFT)
        canvas_title.grid(column=SUDOKU_WIDTH // SIDE // 2, row=0)


    def __draw_shadow_title(self):

        shadow_title = Label(self,
                             text='Shadow Puzzle',
                             font=('Palatino', 20),
                             justify=LEFT)
        shadow_title.grid(column=SUDOKU_WIDTH // SIDE * 2 + 14, row=0)


    def __make_log(self):
        self.log = []


    # Helper function for __initUI

    def __draw_grid(self, grid):
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
            grid.create_line(x0, y0, x1, y1, fill=color, width=width)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = SUDOKU_WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            grid.create_line(x0, y0, x1, y1, fill=color, width=width)


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

        self.listbox.grid(column=20, row=1)
        self.scrollbar.grid(column=21, row=1, sticky=N+S)
        self.scrollbar['command'] = self.listbox.yview


    def __draw_puzzle(self):

        for i in range(9):
            for j in range(9):

                answer = self.game.puzzle[i][j]
                original = self.game.start_puzzle[i][j]

                if answer == original != 0:
                    bgcolor, color = 'black', 'white'

                elif self.canvas.row == i or self.canvas.col == j:
                    bgcolor, color = 'light cyan', 'black'

                elif self.canvas.row // 3 == i // 3 and self.canvas.col // 3 == j // 3:
                    bgcolor, color = 'light cyan', 'black'

                else:
                    bgcolor, color = 'white', 'black'

                self.canvas.itemconfig(self.canvas.rectangles[i][j],
                                       fill=bgcolor,
                                       outline=bgcolor,
                                       width=1)

                self.canvas.itemconfig(self.canvas.text[i][j],
                                       text=answer if answer != 0 else '',
                                       fill=color)

        self.__draw_cursor(self.canvas)
        self.__draw_grid(self.canvas)

        self.canvas.lift('numbers')


    def __draw_shadow_puzzle(self):

        for i in range(9):
            for j in range(9):

                answer = self.game.puzzle[i][j]
                original = self.game.start_puzzle[i][j]

                for ii in range(3):
                    for jj in range(3):

                        number = ii * 3 + jj + 1
                        font = ('', 12)


                        if original == 0:
                            if self.shadow.row == i or self.shadow.col == j:
                                bgcolor = 'light cyan'

                            elif self.shadow.row // 3 == i // 3 and self.shadow.col // 3 == j // 3:
                                bgcolor = 'light cyan'

                            else:
                                bgcolor = 'white'

                            color = 'black' if self.game.entries[i][j][number - 1] else bgcolor

                            if self.game.entries[i][j][number - 1] == 2:
                                number = 'X'

                        elif answer == original:
                            bgcolor, number = 'black', answer
                            color = 'white' if ii == jj == 1 else 'black'
                            font = ('', 25) if ii == jj == 1 else font

                        self.shadow.itemconfig(self.shadow.rectangles[i][j][ii][jj],
                                               fill=bgcolor,
                                               outline=bgcolor)

                        self.shadow.itemconfig(self.shadow.text[i][j][ii][jj],
                                               text=number,
                                               tags='numbers',
                                               fill=color,
                                               font=font)

        self.__draw_cursor(self.shadow)
        self.__draw_shadow_cursor()
        self.__draw_grid(self.shadow)

        self.shadow.lift('numbers')


    def __set_cursor(self):
        if (self.canvas.row, self.canvas.col) == (-1, -1):
            for i in range(9):
                for j in range(9):
                    if self.game.start_puzzle[i][j] == 0:
                        self.canvas.row, self.canvas.col = i, j
                        self.shadow.row, self.shadow.col = i, j
                        return

    def __set_shadow_cursor(self, row=-1, col=-1):
        for i in range(3):
            for j in range(3):
                number = i * 3 + j + 1
                if self.game.entries[self.shadow.row][self.shadow.col][number - 1]:
                    self.shadow.subrow, self.shadow.subcol = i, j
                    if (row == -1 and col == -1) or (row == i and col == j):
                        return


    def __set_rows_and_cols(self, row, col):
        self.canvas.row = (self.canvas.row + row) % 9
        self.canvas.col= (self.canvas.col + col) % 9
        self.__set_shadow_rows_and_cols(row, col)


    def __set_shadow_rows_and_cols(self, row, col):
        self.shadow.row = (self.shadow.row + row) % 9
        self.shadow.col= (self.shadow.col + col) % 9
        self.__set_shadow_cursor()


    def __set_drawings(self):
        self.__set_drawing_puzzle_rectangles()
        self.__set_drawing_shadow_puzzle_rectangles()


    def __set_drawing_puzzle_rectangles(self):

        self.canvas.rectangles = []
        self.canvas.text = []

        for i in range(9):
            self.canvas.rectangles.append([])
            self.canvas.text.append([])
            for j in range(9):

                x = MARGIN + j * SIDE + SIDE / 2
                y = MARGIN + i * SIDE + SIDE / 2
                x0 = MARGIN + j * SIDE + 1
                y0 = MARGIN + i * SIDE + 1
                x1 = MARGIN + (j + 1) * SIDE - 1
                y1 = MARGIN + (i + 1) * SIDE - 1

                rect = self.canvas.create_rectangle(x0, y0, x1, y1)
                self.canvas.rectangles[-1].append(rect)

                text = self.canvas.create_text(x, y, tags='numbers', font=('', 25))
                self.canvas.text[-1].append(text)


    def __set_drawing_shadow_puzzle_rectangles(self):

        self.shadow.rectangles = []
        self.shadow.text = []

        for i in range(9):
            self.shadow.rectangles.append([])
            self.shadow.text.append([])
            for j in range(9):
                self.shadow.rectangles[-1].append([])
                self.shadow.text[-1].append([])
                for ii in range(3):
                    self.shadow.rectangles[-1][-1].append([])
                    self.shadow.text[-1][-1].append([])
                    for jj in range(3):

                        x = MARGIN + j * SIDE + jj * SIDE / 3 + SIDE / 6
                        y = MARGIN + i * SIDE + ii * SIDE / 3 + SIDE / 6
                        x0 = MARGIN + j * SIDE + jj * (SIDE - 1) / 3
                        y0 = MARGIN + i * SIDE + ii * (SIDE - 1) / 3
                        x1 = MARGIN + j * SIDE + (jj + 1) * (SIDE - 1) / 3
                        y1 = MARGIN + i * SIDE + (ii + 1) * (SIDE - 1) / 3

                        rect = self.shadow.create_rectangle(x0, y0, x1, y1)
                        self.shadow.rectangles[-1][-1][-1].append(rect)

                        text = self.shadow.create_text(x, y, tags='numbers', font=('', 12))
                        self.shadow.text[-1][-1][-1].append(text)


    def __draw_cursor(self, grid):

        """
        Highlight the particular cell that the user has clicked on.
        """

        grid.delete('cursor')

        if grid.row >= 0 and grid.col >=0:
            x0 = MARGIN + grid.col * SIDE + 1
            y0 = MARGIN + grid.row * SIDE + 1
            x1 = MARGIN + (grid.col + 1) * SIDE - 1
            y1 = MARGIN + (grid.row + 1) * SIDE - 1

            grid.create_rectangle(x0,
                                  y0,
                                  x1,
                                  y1,
                                  outline='dark cyan',
                                  tags='cursor',
                                  width=3)

    def __draw_shadow_cursor(self):
        """
        Highlight the particular subcell that the user has clicked on
        in the shadow grid.
        """

        self.shadow.delete('shadow cursor')

        if self.shadow.row >= 0 and self.shadow.col >= 0:
            if self.shadow.subrow >= 0 and self.shadow.subcol >= 0:
                x0 = MARGIN + self.shadow.col * SIDE + self.shadow.subcol * SIDE / 3 + 1
                y0 = MARGIN + self.shadow.row * SIDE + self.shadow.subrow * SIDE / 3 + 1
                x1 = MARGIN + self.shadow.col * SIDE + (self.shadow.subcol + 1) * SIDE / 3 - 1
                y1 = MARGIN + self.shadow.row * SIDE + (self.shadow.subrow + 1) * SIDE / 3 - 1

                self.shadow.create_rectangle(x0,
                                             y0,
                                             x1,
                                             y1,
                                             fill='light yellow',
                                             outline='dark green',
                                             width=3,
                                             tags='shadow cursor')

                self.shadow.lift('shadow cursor')


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

        x = y = MARGIN + 4 * SIDE + SIDE / 2

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

            if self.game.start_puzzle[row][col] == 0:
                self.__set_rows_and_cols(row - self.canvas.row,
                                         col - self.canvas.col)

        self.__draw_puzzle()
        self.__draw_shadow_puzzle()


    def __key_pressed(self, event):
        if self.game.game_over:
            return

        if self.canvas.row >= 0 and self.canvas.col >= 0:

            if event.keysym in '123456789':
                self.game.puzzle[self.canvas.row][self.canvas.col] = int(event.keysym)

                string = 'Entered %c in row %d column %d' % (event.keysym,
                                                             self.canvas.row + 1,
                                                             self.canvas.col + 1)

                if not self.log or string != self.log[-1]:
                    self.log.append(string)
                    self.listbox.insert(0, string)

            elif event.keysym == 'Left':
                self.__set_rows_and_cols(0, -1)

                while self.game.start_puzzle[self.canvas.row][self.canvas.col] != 0:
                    self.__set_rows_and_cols(0, -1)

            elif event.keysym == 'Right':
                self.__set_rows_and_cols(0, 1)

                while self.game.start_puzzle[self.canvas.row][self.canvas.col] != 0:
                    self.__set_rows_and_cols(0, 1)

            elif event.keysym == 'Up':
                self.__set_rows_and_cols(-1, 0)

                while self.game.start_puzzle[self.canvas.row][self.canvas.col] != 0:
                    self.__set_rows_and_cols(-1, 0)

            elif event.keysym == 'Down':
                self.__set_rows_and_cols(1, 0)

                while self.game.start_puzzle[self.canvas.row][self.canvas.col] != 0:
                    self.__set_rows_and_cols(1, 0)

            self.__draw_puzzle()
            self.__draw_shadow_puzzle()

            if self.game.check_win():
                self.__draw_victory()

    def __shadow_cell_clicked(self, event):

        if self.game.game_over:
            return

        x, y = event.x, event.y

        if (MARGIN < x < SUDOKU_WIDTH - MARGIN and MARGIN < y < SUDOKU_HEIGHT - MARGIN):
            self.shadow.focus_set()

            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            if self.game.start_puzzle[row][col] == 0:
                self.__set_shadow_rows_and_cols(row - self.shadow.row,
                                                col - self.shadow.col)
                self.__set_shadow_cursor()

        self.__draw_shadow_puzzle()


    def __shadow_key_pressed(self, event):
        if self.game.game_over:
            return

        row, col = self.shadow.row, self.shadow.col

        if row >= 0 and col >= 0 and event.keysym in '123456789':
            number = int(event.keysym)
            if self.game.entries[row][col][number - 1] and 1 <= number <= 9:
                number = int(event.keysym)
                subrow, subcol = (number - 1) // 3, (number - 1) % 3

                self.__set_shadow_cursor(row=subrow, col=subcol)

                if self.game.entries[row][col][number - 1] == 1:
                    self.game.entries[row][col][number - 1] = 2

                elif self.game.entries[row][col][number - 1] == 2:
                    self.game.entries[row][col][number - 1] = 1

            self.__draw_shadow_puzzle()


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
        root.geometry('%dx%d' % (WIDTH, HEIGHT))
        root.mainloop()

if __name__ == '__main__':
    main()
