from board.cell import Cell


class NoStrategy:
    @staticmethod
    def move(board, value):
        """
        Makes the computer move to the first empty cell
        :param board: the game board
        :param value: the value of the move
        :return: The cell where the move was made
        """

        empty = board.get_empty_cells()
        if len(empty) == 0:
            return None
        line = (board.get_bottom_of_column(empty[0].column))
        board.set_value(line, empty[0].column, value)
        return Cell(line, empty[0].column, value)
