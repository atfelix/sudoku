# file:     gui/gui.py
# author:   Adam Felix
# help:     new coder tutorials

import argparse
import time
import tkinter as tk

from sudokugame import SudokuGame

### Constants

BOARDS = ['debug', 'n00b', 'l33t', 'error']
MARGIN = 10
SIDE = 60
SUDOKU_BOX_SIZE = 3
SUDOKU_SIZE = SUDOKU_BOX_SIZE ** 2
SUDOKU_WIDTH = SUDOKU_HEIGHT = MARGIN * 2 + SIDE * SUDOKU_SIZE
WIDTH = 3 * SUDOKU_WIDTH
HEIGHT = SUDOKU_HEIGHT + 100
BUTTON_WIDTH = 10
NO_SHIFT = 96
SHIFT = 97


class SudokuUI(tk.Frame):
    """
    The Tkinter UI, responsible for drawing the board
    and accepting user input.
    """

    def __init__(self, parent, game):

        self.game = game
        self.parent = parent
        self.__start_time = time.time()

        tk.Frame.__init__(self, parent)

        self.__initUI()


    def __initUI(self):

        self.parent.title('Shadow Sudoku')

        self.grid()

        self.canvas = tk.Canvas(self,
                             width=SUDOKU_WIDTH,
                             height=SUDOKU_HEIGHT,
                             highlightthickness=1)

        self.canvas.grid(column=0, row=1, columnspan=15, rowspan=15)
        self.canvas.row, self.canvas.col = -1, -1

        self.shadow = tk.Canvas(self,
                             width=SUDOKU_WIDTH,
                             height=SUDOKU_HEIGHT,
                             highlightthickness=1)

        self.shadow.grid(column=25, row=1, columnspan=15, rowspan=15)
        self.shadow.row, self.shadow.col = -1, -1
        self.shadow.subrow, self.shadow.subcol = -1, -1

        self.__make_buttons()
        self.__draw_activity_log_title()
        self.__draw_canvas_title()
        self.__draw_shadow_title()

        self.__make_log()
        self.__draw_activity_log()

        self.__make_timer()

        self.__set_cursor()
        self.__set_drawing_puzzle_rectangles()
        self.__set_drawing_shadow_puzzle_rectangles()

        self.__draw_puzzle()
        self.__draw_grid(self.canvas)

        self.__draw_shadow_puzzle()
        self.__draw_grid(self.shadow)

        self.canvas.bind('<Button-1>', self.__cell_clicked)
        self.canvas.bind('<Key>', self.__key_pressed)

        self.shadow.bind('<Button-1>', self.__shadow_cell_clicked)
        self.shadow.bind('<Key>', self.__shadow_key_pressed)


    def __make_buttons(self):

        self.__make_clear_buttons()
        self.__make_solve_buttons()


    def __make_clear_buttons(self):

        text = ['Clear Puzzle', 'Clear Row', 'Clear Column',
                'Clear Box', 'Clear Cell']
        commands = [self.__clear_puzzle, self.__clear_row,
                    self.__clear_column, self.__clear_box,
                    self.__clear_box]
        widths = [BUTTON_WIDTH] * 5
        columns = range(0, 10, 2)
        rows = [18] * 5

        for toople in zip(text, commands, widths, columns,rows):
            self.__make_particular_button(*toople)


    def __make_solve_buttons(self):

        text = ['Solve Puzzle', 'Solve Row', 'Solve Column',
                'Solve Box', 'Solve Cell']
        commands = [self.__clear_puzzle, self.__clear_row,
                    self.__clear_column, self.__clear_box,
                    self.__clear_box]
        widths = [BUTTON_WIDTH] * 5
        columns = range(0, 10, 2)
        rows = [20] * 5

        for toople in zip(text, commands, widths, columns, rows):
            self.__make_particular_button(*toople)


    def __make_particular_button(self, text, command, width, column, row):
        button = tk.Button(self, text=text, command=command, width=width)
        button.grid(column=column, row=row)


    def __draw_activity_log_title(self):

        log_title = tk.Label(self,
                          text='Activity Log',
                          font=('Palatino', 20),
                          justify=tk.LEFT)
        log_title.grid(column=SUDOKU_WIDTH // SIDE + 11, row=0)

    def __draw_canvas_title(self):

        canvas_title = tk.Label(self,
                             text='Sudoku Puzzle',
                             font=('Palatino', 20),
                             justify=tk.LEFT)
        canvas_title.grid(column=SUDOKU_WIDTH // SIDE // 2, row=0)


    def __draw_shadow_title(self):

        shadow_title = tk.Label(self,
                             text='Shadow Puzzle',
                             font=('Palatino', 20),
                             justify=tk.LEFT)
        shadow_title.grid(column=SUDOKU_WIDTH // SIDE * 2 + 14, row=0)


    def __make_timer(self):
        self.timer = tk.Label(self,
                           text='%.2d:%.2d:%.2d' % (0, 0, 0),
                           font=('Palatino', 20),
                           justify=tk.RIGHT)
        self.timer.grid(column=20, row=18)


    def draw_timer(self):
        if self.game.game_over:
            return

        total_time = int(time.time() - self.__start_time)
        M, S = divmod(total_time, 60)
        H, M = divmod(M, 60)
        self.timer.configure(text='%.2d:%.2d:%.2d' % (H, M, S))


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

        self.scrollbar = tk.Scrollbar(self,
                                   orient=tk.VERTICAL,
                                   elementborderwidth=2)

        self.listbox = tk.Listbox(self,
                               yscrollcommand=self.scrollbar.set,
                               borderwidth=0,
                               font=('Palatino', 15),
                               width=30,
                               height=29)

        self.listbox.grid(column=20, row=1)
        self.scrollbar.grid(column=21, row=1, sticky=tk.N+tk.S)
        self.scrollbar['command'] = self.listbox.yview


    def __draw_puzzle(self, update=True):

        if update:
            self.game.update_entries()

        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):

                answer = self.game.puzzle[i][j]
                original = self.game.start_puzzle[i][j]

                if 4 in self.game.entries[i][j]:
                    bgcolor, color = 'red', 'black'

                elif answer == original != 0:
                    bgcolor, color = 'black', 'white'

                elif answer != 0:
                    bgcolor, color = 'cyan', 'black'

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


        self.canvas.lift('numbers')


    def __draw_shadow_puzzle(self):

        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):

                answer = self.game.puzzle[i][j]
                original = self.game.start_puzzle[i][j]

                for ii in range(SUDOKU_BOX_SIZE):
                    for jj in range(SUDOKU_BOX_SIZE):

                        number = ii * 3 + jj + 1
                        font = ('', 12)


                        if original == 0:

                            if answer != 0:
                                bgcolor = 'cyan'
                                color = 'black'

                            elif self.shadow.row == i or self.shadow.col == j:
                                bgcolor = 'light cyan'

                            elif self.shadow.row // 3 == i // 3 and self.shadow.col // 3 == j // 3:
                                bgcolor = 'light cyan'

                            else:
                                bgcolor = 'white'

                            color = 'black' if self.game.entries[i][j][number - 1] else bgcolor

                            if self.game.entries[i][j][number - 1] >= 2:

                                if self.game.entries[i][j][number - 1] == 3:
                                    color = 'red'

                                number = '\u2716'
                                font = ('', 15)


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

        self.shadow.lift('numbers')


    def __set_cursor(self):
        if (self.canvas.row, self.canvas.col) == (-1, -1):
            for i in range(SUDOKU_SIZE):
                for j in range(SUDOKU_SIZE):
                    if self.game.start_puzzle[i][j] == 0:
                        self.canvas.row, self.canvas.col = i, j
                        self.shadow.row, self.shadow.col = i, j
                        return

    def __set_shadow_cursor(self, row=-1, col=-1):

        if ((row != -1 or col != -1) and
                self.game.entries[self.shadow.row][self.shadow.col][3 * row + col] == 0):
            row, col = -1, -1

        for i in range(SUDOKU_BOX_SIZE):
            for j in range(SUDOKU_BOX_SIZE):
                number = i * 3 + j + 1
                if self.game.entries[self.shadow.row][self.shadow.col][number - 1]:
                    self.shadow.subrow, self.shadow.subcol = i, j
                    if (row == -1 and col == -1) or (row == i and col == j):
                        return


    def __set_rows_and_cols(self, row, col):
        self.canvas.row = (self.canvas.row + row) % 9
        self.canvas.col= (self.canvas.col + col) % 9
        self.__reset_shadow_rows_and_cols()


    def __set_shadow_rows_and_cols(self, row, col):
        self.shadow.row = (self.shadow.row + row) % 9
        self.shadow.col= (self.shadow.col + col) % 9


    def __reset_shadow_rows_and_cols(self):
        self.shadow.row = self.canvas.row
        self.shadow.col = self.canvas.col


    def __set_drawings(self):
        self.__set_drawing_puzzle_rectangles()
        self.__set_drawing_shadow_puzzle_rectangles()


    def __set_drawing_puzzle_rectangles(self):

        self.canvas.rectangles = []
        self.canvas.text = []

        for i in range(SUDOKU_SIZE):
            self.canvas.rectangles.append([])
            self.canvas.text.append([])
            for j in range(SUDOKU_SIZE):

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

        for i in range(SUDOKU_SIZE):
            self.shadow.rectangles.append([])
            self.shadow.text.append([])
            for j in range(SUDOKU_SIZE):
                self.shadow.rectangles[-1].append([])
                self.shadow.text[-1].append([])
                for ii in range(SUDOKU_BOX_SIZE):
                    self.shadow.rectangles[-1][-1].append([])
                    self.shadow.text[-1][-1].append([])
                    for jj in range(SUDOKU_BOX_SIZE):

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


    def draw_puzzles(self):
        self.__draw_puzzle()
        self.__draw_shadow_puzzle()


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
        self.canvas.delete('winner')
        self.draw_puzzles()


    def __clear_row(self):
        row, col = self.canvas.row, self.canvas.col

        if row >= 0 and col >= 0:
            for i in range(SUDOKU_SIZE):
                if self.game.start_puzzle[row][i] == 0:
                    self.game.puzzle[row][i] = 0

        self.draw_puzzles()


    def __clear_column(self):
        row, col = self.canvas.row, self.canvas.col

        if row >= 0 and col >= 0:
            for i in range(SUDOKU_SIZE):
                if self.game.start_puzzle[i][col] == 0:
                    self.game.puzzle[i][col] = 0

        self.draw_puzzles()


    def __clear_box(self):
        row, col = self.canvas.row // 3, self.canvas.col // 3

        if row >= 0 and col >= 0:
            for i in range(SUDOKU_BOX_SIZE):
                for j in range(SUDOKU_BOX_SIZE):
                    if self.game.start_puzzle[3 * row + i][3 * col + j] == 0:
                        self.game.puzzle[3 * row + i][3 * col + j] = 0

        self.draw_puzzles()


    def __clear_cell(self):
        if self.game.start_puzzle[self.canvas.row][self.canvas.col] == 0:
            self.game.puzzle[self.canvas.row][self.canvas.col] = 0

        self.draw_puzzles()


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
            self.canvas.focus_set()

            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            if self.game.start_puzzle[row][col] == 0:
                self.__set_rows_and_cols(row - self.canvas.row,
                                         col - self.canvas.col)

        self.draw_puzzles()


    def __key_pressed(self, event):
        if self.game.game_over:
            return

        if self.canvas.row >= 0 and self.canvas.col >= 0:

            if event.keysym in '123456789':
                number = int(event.keysym)

                if self.game.entries[self.canvas.row][self.canvas.col][number - 1] == 1:

                    self.game.puzzle[self.canvas.row][self.canvas.col] = number

                    string = 'Entered %c in row %d column %d' % (event.keysym,
                                                                 self.canvas.row + 1,
                                                                 self.canvas.col + 1)

                    if not self.log or string != self.log[-1]:
                        self.log.append(int('%d%d%c' % (self.canvas.row + 1,
                                                        self.canvas.col + 1,
                                                        event.keysym)))
                        self.listbox.insert(0, string)

                elif self.game.entries[self.canvas.row][self.canvas.col][number - 1] in [0, 2]:
                    contradictions = self.__offending_entries(number)

                    if contradictions:
                        for _row, _col in contradictions:
                            self.canvas.itemconfig(self.canvas.rectangles[_row][_col],
                                                   fill='yellow',
                                                   outline='yellow',
                                                   width=1)

                            self.canvas.itemconfig(self.canvas.text[_row][_col],
                                                   fill='red')
                        self.canvas.update()
                        time.sleep(0.2)

                    else:
                        self.game.puzzle[self.canvas.row][self.canvas.col] = number

            elif event.keysym in ['Left', 'Right', 'Up', 'Down']:

                if event.keysym == 'Left':
                    dx, dy = 0, -1

                elif event.keysym == 'Right':
                    dx, dy = 0, 1

                elif event.keysym == 'Up':
                    dx, dy = -1, 0

                elif event.keysym == 'Down':
                    dx, dy = 1, 0

                self.__reset_shadow_rows_and_cols()
                self.__set_rows_and_cols(dx, dy)

                while self.game.start_puzzle[self.canvas.row][self.canvas.col] != 0:
                    self.__set_rows_and_cols(dx, dy)

            elif event.keysym == 'BackSpace':
                char = str(self.game.puzzle[self.canvas.row][self.canvas.col])
                if char != '0':
                    self.game.puzzle[self.canvas.row][self.canvas.col] = 0
                    string = 'Deleted %s from row %d column %d' % (char,
                                                                   self.canvas.row + 1,
                                                                   self.canvas.col + 1)
                    if not self.log or string != self.log[-1]:
                        self.log.append(-int('%d%d%c' % (self.canvas.row + 1,
                                                         self.canvas.col + 1,
                                                         char)))
                        self.listbox.insert(0, string)

            self.draw_puzzles()

            if self.game.check_win():
                self.__draw_victory()


    def __shadow_cell_clicked(self, event):

        if self.game.game_over:
            return

        x, y = event.x, event.y

        if (MARGIN < x < SUDOKU_WIDTH - MARGIN and MARGIN < y < SUDOKU_HEIGHT - MARGIN):
            self.shadow.focus_set()

            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE
            subrow = ((y - MARGIN) - row * SIDE) // (SIDE // 3)
            subcol = ((x - MARGIN) - col * SIDE) // (SIDE // 3)

            if self.game.start_puzzle[row][col] == 0:
                if (self.game.entries[row][col][subrow * 3 + subcol] == 1
                        and self.game.puzzle[row][col] == 0):
                    self.__toggle_subrow_and_subcol(row, col, subrow*3+subcol, value=3)

                elif self.game.entries[row][col][subrow * 3 + subcol] == 3:
                    self.__toggle_subrow_and_subcol(row, col, subrow*3+subcol, value=1)

                self.__set_shadow_rows_and_cols(row - self.shadow.row,
                                                col - self.shadow.col)

        self.__draw_shadow_puzzle()


    def __shadow_key_pressed(self, event):
        if self.game.game_over:
            return

        row, col = self.shadow.row, self.shadow.col

        if row >= 0 and col >= 0:
            if event.keysym in '123456789':

                number = int(event.keysym)

                if self.game.entries[row][col][number - 1] and 1 <= number <= 9:
                    number = int(event.keysym)
                    subrow, subcol = (number - 1) // 3, (number - 1) % 3

                    if self.game.entries[row][col][number - 1] == 1:
                        self.game.entries[row][col][number - 1] = 3

                    elif self.game.entries[row][col][number - 1] == 3:
                        self.game.entries[row][col][number - 1] = 1

            elif event.keysym in ['Left', 'Right', 'Up', 'Down']:

                if event.state == NO_SHIFT:

                    if event.keysym == 'Left':
                        dx, dy = 0, -1

                    elif event.keysym == 'Right':
                        dx, dy = 0, 1

                    elif event.keysym == 'Up':
                        dx, dy = -1, 0

                    elif event.keysym == 'Down':
                        dx, dy = 1, 0

                    self.__set_shadow_rows_and_cols(dx, dy)

                    while self.game.start_puzzle[self.shadow.row][self.shadow.col] != 0:
                        self.__set_shadow_rows_and_cols(dx, dy)

            self.__draw_shadow_puzzle()


    def __toggle_subrow_and_subcol(self, row, col, number, value=-1):

        if value != -1:
            self.game.entries[row][col][number] = value

        elif self.game.entries[row][col][number] == 1:
            self.game.entries[row][col][number] = 2

        elif self.game.entries[row][col][number] == 2:
            self.game.entries[row][col][number] = 1


    def __offending_entries(self, number, row=-1, col=-1):
        if row == -1:
            row = self.canvas.row

        if col == -1:
            col = self.canvas.col

        contradictions = []

        for i in range(SUDOKU_SIZE):
            if i != row and self.game.puzzle[i][col] == number:
                contradictions.append((i, col))

        for j in range(SUDOKU_SIZE):
            if j != col and self.game.puzzle[row][j] == number:
                contradictions.append((row, j))

        _row, _col = row // 3, col // 3

        for ii in range(SUDOKU_BOX_SIZE):
            for jj in range(SUDOKU_BOX_SIZE):
                cell_row, cell_col = _row * 3 + ii, _col * 3 + jj
                if cell_row == row and cell_col == col:
                    continue
                if self.game.puzzle[cell_row][cell_col] == number:
                    contradictions.append((cell_row, cell_col))

        return contradictions
