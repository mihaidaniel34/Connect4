from player.player import Player


class Computer(Player):
    def __init__(self, board, strategy):
        super().__init__(board)
        self.__strategy = strategy

    def move(self, line, column, value):
        """
        Calls the strategy to make a move
        :param line: not used - decided by strategy
        :param column: not used - decided by strategy
        :param value: value of the move
        :return: the move made
        """
        return self.__strategy.move(self._board, value)
