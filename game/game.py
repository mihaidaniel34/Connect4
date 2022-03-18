from player.human import Human


class Game:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.latest_move = None
        self.verdict = None

    def move(self, player, value, line, column):
        """
        :param player: the player that makes the move
        :param value: the value that will be put on the board
        :param line: line of the move
        :param column: column of the move
        :return: the latest move as a cell object and the verdict of the move
        """
        self.latest_move = player.move(line, column, value)
        self.board.latest_move = self.latest_move
        if self.is_over():
            self.verdict = 'draw'
            self.board.verdict = self.verdict
        elif self.is_winner():
            if type(player) is Human:
                self.verdict = 'win'
                self.board.verdict = self.verdict
            else:
                self.verdict = 'lose'
                self.board.verdict = self.verdict

        return self.latest_move, self.verdict

    def is_winner(self):
        """
        Checks if we have a 4-sequence of the same value on the line/column/diagonal
        :return: True if winner move
        """

        # check line
        line_values = self.board.get_line_values(self.latest_move.line)
        if self.__check_list_values(line_values, self.latest_move.value):
            return True

        # check col
        column_values = self.board.get_column_values(self.latest_move.column)
        if self.__check_list_values(column_values, self.latest_move.value):
            return True

        # check diag
        diag_values = self.board.get_diagonal(self.latest_move.line, self.latest_move.column, 1)
        if self.__check_list_values(diag_values, self.latest_move.value):
            return True

        diag_values = self.board.get_diagonal(self.latest_move.line, self.latest_move.column, -1)
        if self.__check_list_values(diag_values, self.latest_move.value):
            return True

        pass

    def is_over(self):
        """
        Checks if the board is full
        :return: True if board is full else False
        """
        if self.latest_move is None:
            return True
        if len(self.board.get_empty_cells()) == 0:
            return True
        return False

    def __check_list_values(self, list_values, value):
        """
        Check if we have a sequence of 4 cells of the same value
        :param list_values: values to check
        :param value: value to search
        :return: True if sequence found else False
        """
        if len(list_values) < 4:
            return False
        for index in range(len(list_values) - 3):
            if all(v == value for v in list_values[index:index + 4]):
                return True
        return False
