import unittest

from board.board import Board
from game.game import Game
from player.computer import Computer
from player.human import Human
from strategy.beginner import Beginner
from strategy.nostrategy import NoStrategy


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(6, 7, 0)

    def test_set_value(self):
        self.assertEqual(self.board.cells()[1][1].value, 0)
        self.board.set_value(1, 1, 7)
        self.assertEqual(self.board.cells()[1][1].value, 7)

    def test_get_line_values(self):
        line_values = self.board.get_line_values(1)
        self.assertListEqual(line_values, [0, 0, 0, 0, 0, 0, 0])

    def test_get_column_values(self):
        column_values = self.board.get_column_values(1)
        self.assertListEqual(column_values, [0, 0, 0, 0, 0, 0])

    def test_get_diagonal_lr(self):
        for i in range(6):
            self.board.set_value(i, i, 1)
        diagonal_values = self.board.get_diagonal_lr(0, 0)
        self.assertListEqual(diagonal_values, [1, 1, 1, 1, 1, 1])

    def test_get_diagonal_rl(self):
        for i in range(5, -1, -1):
            self.board.set_value(i, 6 - i - 1, 1)
        diagonal_values = self.board.get_diagonal_rl(5, 0)
        self.assertListEqual(diagonal_values, [1, 1, 1, 1, 1, 1])

    def test_get_diagonal(self):
        self.assertListEqual(self.board.get_diagonal_lr(0, 0), self.board.get_diagonal(3, 3, 1))
        self.assertListEqual(self.board.get_diagonal_lr(0, 1), self.board.get_diagonal(3, 4, 1))
        self.assertListEqual(self.board.get_diagonal_lr(1, 0), self.board.get_diagonal(4, 3, 1))
        self.assertListEqual(self.board.get_diagonal_rl(3, 3), self.board.get_diagonal(3, 3, -1))

    def test_get_empty_cells(self):
        self.assertEqual(len(self.board.get_empty_cells()), 42)

    def test_get_valid_columns(self):
        self.assertEqual(len(self.board.get_valid_columns()), 7)

    def test_get_bottom_of_column(self):
        self.assertEqual(self.board.get_bottom_of_column(0), 5)
        self.board.set_value(5, 0, 1)
        self.assertEqual(self.board.get_bottom_of_column(0), 4)
        for i in range(0, 6):
            self.board.set_value(i, 0, 1)
        self.assertEqual(self.board.get_bottom_of_column(0), -1)

    def test_str(self):
        self.assertEqual(str(self.board), "│◌ ◌ ◌ ◌ ◌ ◌ ◌│\n"
                                          "│◌ ◌ ◌ ◌ ◌ ◌ ◌│\n"
                                          "│◌ ◌ ◌ ◌ ◌ ◌ ◌│\n"
                                          "│◌ ◌ ◌ ◌ ◌ ◌ ◌│\n"
                                          "│◌ ◌ ◌ ◌ ◌ ◌ ◌│\n"
                                          "│◌ ◌ ◌ ◌ ◌ ◌ ◌│\n")

    def test_copy(self):
        copy = self.board.copy()
        for i in range(6):
            for j in range(7):
                self.assertEqual(self.board.cells()[i][j].value, copy.cells()[i][j].value)


class TestGame(unittest.TestCase):
    def setUp(self):
        self.board = Board(6, 7, 0)
        strategy = NoStrategy()
        self.player1 = Computer(self.board, strategy)
        self.player2 = Human(self.board)
        self.game = Game(self.board, self.player1, self.player2)

    def test_move(self):
        self.assertEqual(self.board.cells()[0][0].value, 0)
        self.game.move(self.player2, 2, 0, 0)
        self.assertEqual(self.board.cells()[0][0].value, 2)
        for i in range(3):
            self.board.set_value(0, i, 2)
        latest_move, verdict = self.game.move(self.player2, 2, 0, 3)
        self.assertEqual(verdict, "win")
        for i in range(6):
            for j in range(7):
                self.board.set_value(i, j, 2)
        self.board.set_value(5, 5, 0)
        latest_move, verdict = self.game.move(self.player2, 2, 5, 5)
        self.assertEqual(verdict, "draw")
        latest_move, verdict = self.game.move(self.player1, 1, -1, -1)
        self.assertIsNone(latest_move)

    def test_move_lose(self):
        for i in range(5, 2, -1):
            self.board.set_value(i, 0, 1)
        latest_move, verdict = self.game.move(self.player1, 1, -1, -1)
        self.assertEqual(verdict, 'lose')

    def test_is_over(self):
        for i in range(6):
            for j in range(7):
                self.board.set_value(i, j, 2)
        self.assertTrue(self.game.is_over())

    def test_is_winner(self):
        for i in range(3):
            self.board.set_value(0, i, 2)
        self.game.move(self.player2, 2, 0, 3)
        self.assertTrue(self.game.is_winner())

    def test_is_winner_diag_lr(self):
        for i in range(3):
            self.board.set_value(i, i, 2)
        self.game.move(self.player2, 2, 3, 3)
        self.assertTrue(self.game.is_winner())

    def test_is_winner_diag_rl(self):
        for i in range(3):
            self.board.set_value(i, 5 - i, 2)
        self.game.move(self.player2, 2, 3, 2)
        self.assertTrue(self.game.is_winner())


class TestBeginner(unittest.TestCase):
    def setUp(self):
        self.board = Board(6, 7, 0)
        strategy = Beginner()
        self.player1 = Computer(self.board, strategy)
        self.player2 = Human(self.board)
        self.game = Game(self.board, self.player1, self.player2)

    def test_deny_on_line_right(self):
        self.game.move(self.player2, 2, 5, 0)
        self.game.move(self.player2, 2, 5, 1)
        self.game.move(self.player1, 1, -1, -1)
        latest_move = self.board.latest_move
        self.assertEqual(latest_move.line, 5)
        self.assertEqual(latest_move.column, 2)

    def test_deny_on_line_left(self):
        self.game.move(self.player2, 2, 5, 2)
        self.game.move(self.player2, 2, 5, 1)
        self.game.move(self.player1, 1, -1, -1)
        latest_move = self.board.latest_move
        self.assertEqual(latest_move.line, 5)
        self.assertEqual(latest_move.column, 0)

    def test_deny_on_column(self):
        self.game.move(self.player2, 2, 5, 0)
        self.game.move(self.player2, 2, 4, 0)
        self.game.move(self.player1, 1, -1, -1)
        latest_move = self.board.latest_move
        self.assertEqual(latest_move.line, 3)
        self.assertEqual(latest_move.column, 0)

    def test_random_move(self):
        self.game.move(self.player1, 1, -1, -1)
        latest_move = self.board.latest_move
        self.assertEqual(latest_move.line, 5)
        self.assertEqual(latest_move.column, 0)
    
    def test_full_board(self):
        for i in range(6):
            for j in range(7):
                self.board.set_value(i, j, 2)
        self.game.move(self.player1, 1, -1, -1)
        self.assertIsNone(self.board.latest_move)