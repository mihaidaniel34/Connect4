from board.board import Board
from console.console import Console
from game.game import Game
from gui.gui import GUI
from player.computer import Computer
from player.human import Human
from strategy.beginner import Beginner
from strategy.minmax import Strategy
from strategy.nostrategy import NoStrategy


def main():
    board = Board(6, 7)
    strategy = Strategy(board)
    player1 = Computer(board, strategy)
    player2 = Human(board)
    game = Game(board, player1, player2)
    display_mode = 'gui'
    if display_mode == 'console':
        display = Console(game)
    else:
        display = GUI(game)


if __name__ == '__main__':
    while True:
        main()
