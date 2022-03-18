import copy

from board.cell import Cell


class Board:
    def __init__(self, lines, columns, empty_value=0):
        self.__lines = lines
        self.__columns = columns
        self.__empty_value = empty_value
        self.latest_move = None
        self.verdict = None

        self.__cells = self.__create_board()

    def __create_board(self):
        """
        :return: the board as a two-dimensional array of cells
        """
        return [[Cell(line, column, self.__empty_value) for column in range(self.__columns)]
                for line in range(self.__lines)]

    def set_value(self, line, column, value):
        self.__cells[line][column].value = value

    def get_line_values(self, line):
        """
        :param line: the given line
        :return: the values from the given line as a list
        """
        return [cell.value for cell in self.__cells[line]]

    def get_column_values(self, column):
        """
        :param column: the given column
        :return: the values from the given column as a list
        """
        return [line[column].value for line in self.__cells]

    def get_diagonal_lr(self, row_offset, column_offset):
        """
        :param row_offset: difference between row and column if > 0
        :param column_offset: difference between column and row if > 0
        :return: the values from the diagonal that goes from top left to bottom right and contains the last move
        """
        return [self.__cells[index + row_offset][index + column_offset].value for index in range(6) if
                (index + row_offset) < 6 and (index + column_offset) < 7]

    def get_diagonal_rl(self, row, column):
        """
        :param row: the row coordinate of the last move
        :param column: the column coordinate of the last move
        :return: the values from the diagonal that goes from bottom left to top right and contains the last move
        """
        column = column
        diagonal = []
        while row < 5 and column > 0:
            row += 1
            column -= 1

        while row >= 0 and column <= 6:
            diagonal.append(self.__cells[row][column].value)
            row -= 1
            column += 1

        return diagonal

    def get_diagonal(self, row, column, d):
        """
        :param row: row of the latest move
        :param column: column of the latest move
        :param d: direction 1: top left to bottom right -1: bottom left to top right
        :return: the values from the desired diagonal as a list
        """
        row_offset = row - column
        if row_offset < 0:
            row_offset = 0
        column_offset = column - row
        if column_offset < 0:
            column_offset = 0
        if d == 1:
            return self.get_diagonal_lr(row_offset, column_offset)
        elif d == -1:
            return self.get_diagonal_rl(row, column)

    def get_empty_cells(self):
        """
        :return: list of empty cells
        """
        return [cell for cell in self.__get_all_cells_as_list() if cell.value == self.__empty_value]

    def get_valid_columns(self):
        """
        :return: list of columns that are not full
        """
        return [column for column in range(7) if self.get_bottom_of_column(column) != -1]

    def __get_all_cells_as_list(self):
        """
        :return: the list of all cells
        """
        return [cell for line in self.__cells for cell in line]

    def get_bottom_of_column(self, column):
        """
        :param column: the given column
        :return: the first empty line from a column; -1 if none
        """
        for line in range(len(self.__cells) - 1, -1, -1):
            if self.__cells[line][column].value == self.__empty_value:
                return line
        return -1

    def __str__(self):
        """
        :return: returns the board in printable form
        """
        res = ""
        for line in self.__cells:
            s = " ".join(['◌' if cell.value == 0 else '🞩' if cell.value == 1 else '○' for cell in line]) + "│\n"
            res += '│' + s
        return res

    def copy(self):
        return copy.deepcopy(self)

    def cells(self):
        return self.__cells
