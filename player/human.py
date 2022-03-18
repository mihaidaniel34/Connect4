from board.cell import Cell
from player.player import Player


class Human(Player):
    def move(self, line, column, value):
        """
        Sets the value of the cell to given value
        :param line: line of move
        :param column: column of move
        :param value: value of move
        :return: The cell where the value was set
        """
        self._board.set_value(line, column, value)
        return Cell(line, column, value)