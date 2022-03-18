from board.cell import Cell


class Beginner:
    @staticmethod
    def move(board, value):
        """
        Makes the computer deny the last human player move / play random
        :param board: the game board
        :param value: the value of the move
        :return: The cell where the move was made
        """
        if board.latest_move is not None:
            line = board.latest_move.line
            column = board.latest_move.column
            opponent_value = board.latest_move.value
            line_values = board.get_line_values(line)
            column_values = board.get_column_values(column)
            if line_values.count(opponent_value) > column_values.count(opponent_value):
                if (column + 1 < 7) and board.get_bottom_of_column(column + 1) == line:
                    if board.cells()[line][column + 1].value == 0:
                        board.set_value(line, column + 1, value)
                        return Cell(line, column + 1, value)
                elif board.get_bottom_of_column(column - 1) == line:
                    if board.cells()[line][column - 1].value == 0:
                        board.set_value(line, column - 1, value)
                        return Cell(line, column - 1, value)
            else:
                if line - 1 > -1:
                    if board.cells()[line - 1][column].value == 0:
                        board.set_value(line - 1, column, value)
                        return Cell(line - 1, column, value)

        empty = board.get_empty_cells()
        if len(empty) == 0:
            return None
        line = (board.get_bottom_of_column(empty[0].column))
        board.set_value(line, empty[0].column, value)
        return Cell(line, empty[0].column, value)
